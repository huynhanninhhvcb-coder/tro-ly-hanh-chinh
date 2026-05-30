import streamlit as st
from streamlit_mic_recorder import speech_to_text
from bo_nao import xu_ly_cau_hoi, text_to_speech_base64

# ==========================================
# 1. CẤU HÌNH GIAO DIỆN TRANG WEB
# ==========================================
st.set_page_config(page_title="Trợ lý Hành chính công", page_icon="🇻🇳", layout="centered")

# Nhúng file CSS để tùy chỉnh giao diện (khung chữ, nút bấm vàng...)
try:
    with open("frontend/styles.css", "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except:
    pass

# Hiển thị Logo của Trung tâm (đảm bảo file TTHCC.png có sẵn)
try:
    st.image("TTHCC.png", width=300)
except:
    pass

# ==========================================
# 2. KHỞI TẠO BỘ NHỚ LỊCH SỬ CHAT
# ==========================================
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Kính chào công dân! Đây là Hệ thống Trợ lý ảo tra cứu thủ tục hành chính của Trung tâm phục vụ hành chính công phường Minh Phụng. Tôi có thể giúp gì cho bạn?"}
    ]

# ==========================================
# 3. HIỂN THỊ LỊCH SỬ TRÒ CHUYỆN 
# ==========================================
for message in st.session_state.messages:
    # Gắn ảnh robot.png cho Trợ lý, của người dân thì để mặc định
    hinh_dai_dien = "robot.png" if message["role"] == "assistant" else None
    
    with st.chat_message(message["role"], avatar=hinh_dai_dien):
        st.markdown(message["content"])

# ==========================================
# 4. THANH NHẬP LIỆU (THU ÂM & GÕ PHÍM)
# ==========================================
# Giao diện nút bấm "Chạm để Nói" thu giọng nói và dịch thành chữ
giong_noi = speech_to_text(
    language='vi-VN',
    start_prompt="Chạm để Nói",
    stop_prompt="Đang thu âm (Chạm để Dừng)...",
    just_once=True,
    key='STT'
)

# Thanh gõ phím dự phòng
van_ban = st.chat_input("Hoặc nhập câu hỏi vào đây...")

# Gom chung dữ liệu: Ưu tiên nhận giọng nói, nếu không có thì nhận văn bản gõ phím
cau_hoi = giong_noi if giong_noi else van_ban

# ==========================================
# 5. XỬ LÝ LÔ-GÍC KHI CÔNG DÂN ĐẶT CÂU HỎI
# ==========================================
if cau_hoi:
    # A. Hiển thị câu hỏi của người dân lên màn hình
    with st.chat_message("user"):
        st.markdown(cau_hoi)
    # Lưu câu hỏi vào lịch sử
    st.session_state.messages.append({"role": "user", "content": cau_hoi})

    # B. Dò từ khóa tìm câu trả lời từ file txt (gọi từ bo_nao.py)
    cau_tra_loi = xu_ly_cau_hoi(cau_hoi)
    
    # C. Tạo file âm thanh (chuyển chữ thành giọng nói Google)
    audio_b64 = text_to_speech_base64(cau_tra_loi)

    # D. Hiển thị câu trả lời và phát âm thanh
    with st.chat_message("assistant", avatar="robot.png"):
        st.markdown(cau_tra_loi)
        
        # --- ĐOẠN CODE ĐÃ ĐƯỢC SỬA LỖI MÀN HÌNH HỒNG ---
        if audio_b64:
            audio_html = f'''
                <audio autoplay="true" controls style="width: 100%; outline: none; border-radius: 8px; margin-top: 15px; box-shadow: 0px 2px 5px rgba(0,0,0,0.1);">
                    <source src="data:audio/mp3;base64,{audio_b64}" type="audio/mp3">
                </audio>
            '''
            # Lệnh st.markdown in trực tiếp thanh phát âm thanh ra màn hình
            st.markdown(audio_html, unsafe_allow_html=True)
            
    # Lưu câu trả lời vào lịch sử
    st.session_state.messages.append({"role": "assistant", "content": cau_tra_loi})
