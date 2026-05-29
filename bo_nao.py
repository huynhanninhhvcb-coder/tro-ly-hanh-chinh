import os
import io
import base64
from gtts import gTTS
import google.generativeai as genai

# ==========================================
# 1. CẤU HÌNH BỘ NÃO AI (GEMINI)
# ==========================================
# Đã tích hợp API Key của bạn:
import streamlit as st
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# Sử dụng mô hình Gemini 1.5 Flash (Tốc độ siêu nhanh, thông minh)
model = genai.GenerativeModel('gemini-1.5-flash')

def load_all_documents() -> str:
    """Tự động đọc TẤT CẢ các file .txt trong thư mục để làm kiến thức cho AI"""
    thu_muc_hien_tai = os.path.dirname(__file__)
    knowledge_base = ""
    
    # Quét tất cả các file có đuôi .txt
    for filename in os.listdir(thu_muc_hien_tai):
        if filename.endswith(".txt"):
            duong_dan = os.path.join(thu_muc_hien_tai, filename)
            try:
                with open(duong_dan, "r", encoding="utf-8", errors="ignore") as f:
                    knowledge_base += f"\n--- TÀI LIỆU THỦ TỤC: {filename} ---\n"
                    knowledge_base += f.read() + "\n"
            except Exception as e:
                print(f"Lỗi đọc file {filename}: {e}")
                
    return knowledge_base

# Nạp sẵn toàn bộ hồ sơ/tài liệu vào bộ nhớ khi khởi động ứng dụng
KNOWLEDGE_BASE = load_all_documents()


# ==========================================
# 2. XỬ LÝ CÂU HỎI VÀ TẠO GIỌNG NÓI
# ==========================================
def xu_ly_cau_hoi(user_input: str) -> str:
    """Đưa câu hỏi và tài liệu cho Gemini đọc, tóm tắt và trả lời"""
    if not user_input.strip():
        return "Xin lỗi, tôi chưa nghe rõ. Bạn có thể nói lại được không?"

    # Viết Prompt (Câu lệnh) để định hướng tính cách cho AI
    prompt = f"""
    Bạn là một chuyên viên tư vấn thủ tục hành chính chuyên nghiệp, nhiệt tình tại Trung tâm phục vụ hành chính công Phường Minh Phụng.
    Nhiệm vụ của bạn là dựa TƯYỆT ĐỐI vào các tài liệu được cung cấp dưới đây để trả lời câu hỏi của người dân.
    
    Quy tắc bắt buộc:
    1. Trả lời lịch sự (Luôn xưng 'tôi' và gọi 'bạn' hoặc 'công dân').
    2. Trả lời ngắn gọn, đúng trọng tâm, trình bày rõ ràng bằng các gạch đầu dòng.
    3. NẾU TÀI LIỆU KHÔNG CÓ THÔNG TIN, hãy nói: "Xin lỗi, hiện tại hệ thống chưa có tài liệu về vấn đề này. Mong bạn liên hệ trực tiếp cán bộ tại quầy để được hướng dẫn." (TUYỆT ĐỐI KHÔNG tự bịa ra thông tin không có trong tài liệu).

    TÀI LIỆU KIẾN THỨC CỦA BẠN:
    {KNOWLEDGE_BASE}

    CÂU HỎI CỦA NGƯỜI DÂN:
    {user_input}
    """

    try:
        # Gửi Prompt lên Google Gemini và lấy câu trả lời
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Lỗi gọi Gemini API: {e}")
        return "Xin lỗi, hệ thống AI đang bảo trì hoặc mất kết nối mạng. Vui lòng thử lại sau vài giây!"

def text_to_speech_base64(text: str) -> str:
    """Sử dụng Google TTS để đọc văn bản, mã hóa thành Base64 để phát trên Web"""
    if not text:
        return ""
    try:
        # Lọc bớt văn bản quá dài (trên 800 ký tự) để Google đọc không bị quá tải
        text_to_read = text[:800] + "..." if len(text) > 800 else text
        
        tts = gTTS(text=text_to_read, lang='vi')
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)
        b64 = base64.b64encode(fp.read()).decode()
        return b64
    except Exception as e:
        print(f"Lỗi TTS: {e}")
        return ""