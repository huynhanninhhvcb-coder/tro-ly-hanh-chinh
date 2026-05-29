// In thông báo ra Console của trình duyệt để kiểm tra kết nối
console.log("Giao diện AI Hành chính công đã được tải thành công!");

// Hàm cuộn màn hình xuống cuối cùng (dự phòng nếu chat quá dài)
function scrollToBottom() {
    window.scrollTo({
        top: document.body.scrollHeight,
        behavior: 'smooth'
    });
}