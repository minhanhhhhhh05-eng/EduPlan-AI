
# EDUPLAN AI
## Ứng dụng hỗ trợ xây dựng kế hoạch bài dạy bằng trí tuệ nhân tạo

### 1. Giới thiệu
EduPlan AI là ứng dụng được xây dựng bằng Python và Streamlit, tích hợp Google Gemini AI để hỗ trợ giáo viên xây dựng bản nháp kế hoạch bài dạy theo định hướng Chương trình GDPT 2018.

Ứng dụng cho phép giáo viên xem xét, chỉnh sửa nội dung AI đề xuất và xuất kế hoạch bài dạy thành file Word (.docx).

### 2. Chức năng chính
- Nhập thông tin bài dạy: môn học, lớp, tên bài, số tiết, bộ sách và yêu cầu cần đạt.
- Sử dụng Gemini AI để đề xuất nội dung giáo án.
- Tạo mục tiêu, thiết bị dạy học và 4 hoạt động:
  1. Mở đầu.
  2. Hình thành kiến thức mới.
  3. Luyện tập.
  4. Vận dụng.
- Cho phép giáo viên chỉnh sửa nội dung.
- Xuất kế hoạch bài dạy thành file Word.
- Hỗ trợ lưu bản nháp dưới dạng JSON.

### 3. Cài đặt
Yêu cầu: Python 3.11 trở lên và kết nối Internet.

Mở Terminal trong thư mục chứa ứng dụng và chạy:

python -m pip install -r requirements.txt

### 4. Cấu hình Gemini API
- Tạo API key tại https://aistudio.google.com/apikey
- Mở thư mục .streamlit.
- Sao chép file secrets.toml.example và đổi tên bản sao thành secrets.toml.
- Thay giá trị mẫu của GEMINI_API_KEY bằng API key của người sử dụng.
- Không chia sẻ API key hoặc đưa khóa thật lên Internet.

### 5. Khởi động ứng dụng
Chạy lệnh:

python -m streamlit run app.py

Mở địa chỉ được Streamlit hiển thị, thường là:
http://localhost:8501

### 6. Hướng dẫn sử dụng
Bước 1: Nhập thông tin bài dạy và yêu cầu cần đạt.

Bước 2: Nhấn "AI GỢI Ý NỘI DUNG GIÁO ÁN".

Bước 3: Kiểm tra nội dung được AI đề xuất.

Bước 4: Chỉnh sửa, bổ sung các thông tin cần thiết.

Bước 5: Nhấn "TẢI KẾ HOẠCH BÀI DẠY WORD (.DOCX)".

### 7. Lưu ý
- Nội dung AI tạo ra chỉ là bản nháp tham khảo.
- Giáo viên chịu trách nhiệm kiểm tra tính chính xác và sự phù hợp với chương trình, sách giáo khoa.
- Chức năng AI cần Internet và Gemini API key hợp lệ.
- Hạn mức miễn phí phụ thuộc vào chính sách của Google.
- Không nhập thông tin cá nhân hoặc dữ liệu nhạy cảm của học sinh vào AI.

### 8. Công nghệ sử dụng
- Python
- Streamlit
- Google Gemini API
- python-docx
