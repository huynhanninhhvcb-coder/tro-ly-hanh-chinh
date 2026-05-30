import os

import io

import base64

from gtts import gTTS



# ==========================================

# 1. HÀM ĐỌC NỘI DUNG TỪ FILE TXT

# ==========================================

def doc_file_txt(ten_file: str) -> str:

    """Mở và đọc nội dung file .txt trong cùng thư mục"""

    thu_muc_hien_tai = os.path.dirname(__file__)

    duong_dan = os.path.join(thu_muc_hien_tai, ten_file)

    

    try:

        with open(duong_dan, "r", encoding="utf-8", errors="ignore") as f:

            # Đọc file và loại bỏ các khoảng trắng thừa

            return f.read().strip()

    except FileNotFoundError:

        return f"Xin lỗi, hệ thống không tìm thấy tài liệu {ten_file} trong cơ sở dữ liệu."

    except Exception as e:

        print(f"Lỗi đọc file {ten_file}: {e}")

        return "Xin lỗi, có lỗi xảy ra khi đọc tài liệu. Vui lòng thử lại sau."



# ==========================================

# 2. XỬ LÝ CÂU HỎI (TÌM TỪ KHÓA -> GỌI FILE TXT)

# ==========================================

def xu_ly_cau_hoi(user_input: str) -> str:

    """Kiểm tra từ khóa và móc nối với đúng file thủ tục"""

    if not user_input.strip():

        return "Xin lỗi, tôi chưa nghe rõ. Bạn có thể nói lại được không?"



    # Chuyển câu nói thành chữ thường để dễ so sánh

    cau_hoi = user_input.lower()



    # --- KỊCH BẢN TƯ VẤN BẰNG FILE TXT ---

    if "mai táng" in cau_hoi or "thủ tục hỗ trợ mai táng" in cau_hoi:

        return doc_file_txt("Ho_so_mai_tang.txt")

        

    elif "hỏa táng" in cau_hoi or "thủ tục hỗ trợ hỏa táng" in cau_hoi:

        return doc_file_txt("Ho_so_hoa_tang.txt")

        

    elif "khuyết tật" in cau_hoi or "thủ tục xác nhận mức độ khuyết tật" in cau_hoi:

        return doc_file_txt("Xac_dinh_muc_do_khuyet_tat.txt")

        

    elif "trợ cấp hưu trí" in cau_hoi or "trợ cấp hưu trí xã hội" in cau_hoi:

        return doc_file_txt("Thoi_huong_tro_cap.txt")

        

    elif "chào" in cau_hoi:

        return "Kính chào công dân. Tôi là trợ lý ảo của Trung tâm Hành chính công phường Minh Phụng. Tôi có thể giúp gì cho bạn?"

        

    # --- TRƯỜNG HỢP KHÔNG TÌM THẤY TỪ KHÓA ---

    else:

        return (

            "Xin lỗi, hiện tại hệ thống chưa được lập trình để trả lời về thủ tục này. "

            "Mong bạn liên hệ trực tiếp cán bộ tại quầy để được hướng dẫn cụ thể hơn."

        )



# ==========================================

# 3. TẠO GIỌNG NÓI (Dùng gTTS miễn phí)

# ==========================================

def text_to_speech_base64(text: str) -> str:

    """Sử dụng Google TTS để đọc văn bản, mã hóa thành Base64 để phát trên Web"""

    if not text:

        return ""

    try:

        # Lọc bớt văn bản quá dài (trên 800 ký tự) để tránh lỗi xử lý giọng nói

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
