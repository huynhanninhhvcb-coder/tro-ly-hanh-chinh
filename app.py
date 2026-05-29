import streamlit as st
import time
import os
import base64

# Nhúng thư viện thu âm trình duyệt
from streamlit_mic_recorder import speech_to_text
from bo_nao import xu_ly_cau_hoi, text_to_speech_base64

# --- HÀM HỖ TRỢ TẢI FRONTEND VÀ ẢNH ---
def load_frontend(filename):
    duong_dan = os.path.join(os.path.dirname(__file__), "frontend", filename)
    try:
        with open(duong_dan, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return ""

def get_image_base64(file_path):
    try:
        with open(file_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode("utf-8")
    except FileNotFoundError:
        return ""

# --- CẤU HÌNH TRANG VÀ NHÚNG FRONTEND ---
st.set_page_config(page_title="Tra cứu Hành chính công", page_icon="🏛️", layout="centered")

logo_path = "TTHCC.png"
logo_b64 = get_image_base64(logo_path)

header_html = load_frontend('header.html')
if logo_b64:
    header_html = header_html.replace('{{LOGO_SRC}}', f"data:image/png;base64,{logo_b64}")

st.markdown(f"<style>{load_frontend('styles.css')}</style>", unsafe_allow_html=True)
st.markdown(header_html, unsafe_allow_html=True)
st.markdown(f"<script>{load_frontend('script.js')}</script>", unsafe_allow_html=True)

# --- THANH BÊN (SIDEBAR) ---
with st.sidebar:
    st.markdown("### 🔍 TIỆN ÍCH TRA CỨU")
    st.markdown("Các liên kết ngoài hỗ trợ công dân tra cứu thông tin nhanh chóng.")
    st.link_button("🏥 Tra cứu thẻ Bảo hiểm Y tế", "https://baohiemxahoi.gov.vn/tracuu/Pages/tra-cuu-thoi-han-su-dung-the-bhyt.aspx", use_container_width=True)
    
    st.markdown("<br>", unsafe_allow_html=True) 
    
    st.markdown("### 📚 TÀI LIỆU ĐỊA PHƯƠNG")
    st.markdown("Kho lưu trữ văn bản và tài liệu văn hóa - xã hội do AI hỗ trợ.")
    st.link_button("📖 Tra cứu tài liệu Văn hóa - Xã hội", "https://notebooklm.google.com/notebook/a41316ce-b623-4e76-b7ae-b3235f157f49", use_container_width=True)
    st.markdown("---")
    st.info("💡 Hướng dẫn: Nhấn vào các nút bên trên để mở trang tra cứu hoặc kho tài liệu trong một thẻ (tab) mới.")

# --- QUẢN LÝ BỘ NHỚ TRÒ CHUYỆN ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Kính chào công dân! Đây là Hệ thống Trợ lý ảo tra cứu thủ tục hành chính của Trung tâm phục vụ hành chính công phường Minh Phụng. Tôi có thể giúp gì cho bạn?"}
    ]

# --- HIỂN THỊ LỊCH SỬ CHAT ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

audio_player_container = st.empty()


# ==================================================
# --- THANH CÔNG CỤ ĐÁY (CHỈ CÒN ĐÚNG 1 NÚT NÓI) ---
# ==================================================
# Dùng 3 cột: Cột trái (1 phần), Cột giữa (2 phần chứa nút), Cột phải (1 phần)
col_left, col_mic, col_right = st.columns([1, 2, 1])

with col_mic:
    spoken_text = speech_to_text(
        language='vi-VN',
        start_prompt="🎤 Chạm để Nói",
        stop_prompt="⏹️ Đang thu âm... (Dừng)",
        just_once=True,
        use_container_width=True, # Lệnh ép nút co giãn
        key='STT'
    )

# --- XỬ LÝ LÔ-GÍC KHI NGƯỜI DÂN VỪA NÓI XONG ---
if spoken_text:
    # In câu người dân vừa nói
    st.session_state.messages.append({"role": "user", "content": spoken_text})
    with st.chat_message("user"):
        st.markdown(spoken_text)

    # Não bộ xử lý
    response = xu_ly_cau_hoi(spoken_text)
    
    # Tạo luồng giọng nói
    audio_b64 = text_to_speech_base64(response)
    
    # In câu trả lời của Trợ lý
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        for chunk in response.split("\n"):
            for word in chunk.split():
                full_response += word + " "
                time.sleep(0.02)
                message_placeholder.markdown(full_response + "▌")
            full_response += "\n\n"
        message_placeholder.markdown(full_response)
        
        # Phát âm thanh
        if audio_b64:
            audio_html = f'''
                <audio autoplay="true" class="hidden">
                    <source src="data:audio/mp3;base64,{audio_b64}" type="audio/mp3">
                </audio>
            '''
            audio_player_container.markdown(audio_html, unsafe_allow_html=True)
    
    st.session_state.messages.append({"role": "assistant", "content": full_response})
