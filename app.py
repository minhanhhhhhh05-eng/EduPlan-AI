
import streamlit as st
import json
from giao_an import tao_khung_giao_an
from xuat_word import tao_file_word
from gemini_giao_an import tao_giao_an_ai
# Cấu hình trang ứng dụng
st.set_page_config(
    page_title="EduPlan AI",
    page_icon="📚",
    layout="wide"
)

# Ghi nhớ trạng thái tạo kế hoạch bài dạy
if "da_tao_giao_an" not in st.session_state:
    st.session_state["da_tao_giao_an"] = False

# Tiêu đề ứng dụng
st.title("📚 EDUPLAN AI")

st.subheader(
    "Ứng dụng hỗ trợ xây dựng Kế hoạch bài dạy"
)

st.write(
    "Thiết kế Kế hoạch bài dạy theo Công văn "
    "5512/BGDĐT-GDTrH và Chương trình GDPT 2018."
)

st.divider()

# Mo lai ban nhap giao an
st.subheader("📂 MỞ LẠI BẢN NHÁP GIÁO ÁN")

file_ban_nhap = st.file_uploader(
    "Chọn file bản nháp đã lưu (.json)",
    type=["json"],
    key="file_ban_nhap"
)

if file_ban_nhap is not None:
    try:
        du_lieu_doc = json.load(file_ban_nhap)

        if (
            isinstance(du_lieu_doc, dict)
            and isinstance(du_lieu_doc.get("thong_tin"), dict)
            and isinstance(du_lieu_doc.get("giao_an"), dict)
        ):
            st.success("Đã đọc file bản nháp JSON thành công!")
            if st.button("📂 KHÔI PHỤC BẢN NHÁP"):
                
                thong_tin_cu = du_lieu_doc["thong_tin"]

                cac_truong = {
                    "Trường": "ten_truong",
                    "Tổ chuyên môn": "to_chuyen_mon",
                    "Giáo viên": "ten_giao_vien",
                    "Môn học": "mon_hoc",
                    "Lớp": "lop",
                    "Tên bài": "ten_bai",
                    "Số tiết": "so_tiet",
                    "Bộ sách": "bo_sach",
                    "Trình độ học sinh": "trinh_do"
                }

                for ten_json, ten_key in cac_truong.items():
                    if ten_json in thong_tin_cu:
                        st.session_state[ten_key] = thong_tin_cu[ten_json]
                        
                # Khoi phuc muc tieu bai day
                muc_tieu_cu = du_lieu_doc["giao_an"].get("I. MỤC TIÊU", {})

                st.session_state["kien_thuc"] = muc_tieu_cu.get("Kiến thức", "")
                st.session_state["nang_luc"] = muc_tieu_cu.get("Năng lực", "")
                st.session_state["pham_chat"] = muc_tieu_cu.get("Phẩm chất", "")
                
                # Khoi phuc thiet bi day hoc va hoc lieu
                st.session_state["thiet_bi"] = du_lieu_doc["giao_an"].get(
                    "II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU", ""
                )

                # Khoi phuc Hoat dong 1
                hd1_cu = du_lieu_doc["giao_an"].get(
                    "III. TIẾN TRÌNH DẠY HỌC", {}
                ).get("Hoạt động 1: Mở đầu", {})

                st.session_state["hd1_muc_tieu"] = hd1_cu.get("Mục tiêu", "")
                st.session_state["hd1_noi_dung"] = hd1_cu.get("Nội dung", "")
                st.session_state["hd1_san_pham"] = hd1_cu.get("Sản phẩm", "")
                st.session_state["hd1_to_chuc"] = hd1_cu.get(
                    "Tổ chức thực hiện", {}
                ).get("Các bước tổ chức", "")

                # Khoi phuc Hoat dong 2
                hd2_cu = du_lieu_doc["giao_an"].get(
                    "III. TIẾN TRÌNH DẠY HỌC", {}
                ).get("Hoạt động 2: Hình thành kiến thức mới", {})

                st.session_state["hd2_muc_tieu"] = hd2_cu.get("Mục tiêu", "")
                st.session_state["hd2_noi_dung"] = hd2_cu.get("Nội dung", "")
                st.session_state["hd2_san_pham"] = hd2_cu.get("Sản phẩm", "")
                st.session_state["hd2_to_chuc"] = hd2_cu.get(
                    "Tổ chức thực hiện", {}
                ).get("Các bước tổ chức", "")

                st.session_state["da_tao_giao_an"] = True
                st.success("Đã khôi phục thông tin chung!")
                st.rerun()

        else:
            st.error("File JSON không đúng cấu trúc bản nháp EduPlan AI.")

    except (json.JSONDecodeError, UnicodeDecodeError):
        st.error("File JSON không hợp lệ hoặc không đọc được.")

# Khu vực nhập thông tin
st.header("THÔNG TIN BÀI DẠY")

# Thông tin đơn vị và giáo viên
ten_truong = st.text_input(
    "Tên trường",
    placeholder="Ví dụ: THPT Nguyễn Văn Hai",
    key="ten_truong"
)

to_chuyen_mon = st.text_input(
    "Tổ chuyên môn",
    placeholder="Ví dụ: Tổ Tiếng Anh",
    key="to_chuyen_mon"
)

ten_giao_vien = st.text_input(
    "Họ và tên giáo viên",
    placeholder="Nhập họ tên giáo viên",
    key="ten_giao_vien"
)
mon_hoc = st.selectbox(
    "Chọn môn học",
    ["Tiếng Anh", "Toán", "Ngữ văn",
     "Lịch sử", "Hoạt động trải nghiệm"],
     key="mon_hoc"
)

lop = st.selectbox(
    "Chọn lớp",
    [6, 7, 8, 9, 10, 11, 12],
    key="lop"
)

ten_bai = st.text_input(
    "Nhập tên bài dạy",
    key="ten_bai"
)

so_tiet = st.number_input(
    "Số tiết",
    min_value=1,
    max_value=10,
    value=1,
    key="so_tiet"
)

bo_sach = st.selectbox(
    "Chọn bộ sách giáo khoa",
    [
        "Kết nối tri thức với cuộc sống",
        "Chân trời sáng tạo",
        "Cánh diều",
        "Global Success",
        "Khác"
    ],
    key="bo_sach"
)

trinh_do = st.selectbox(
    "Chọn trình độ học sinh",
    [
        "Trung bình",
        "Khá",
        "Giỏi",
        "Không đồng đều (phân hóa)"
    ],
    key="trinh_do"
)
yeu_cau = st.text_area(
    "Yêu cầu cần đạt của bài học",
    placeholder="Nhập yêu cầu cần đạt theo chương trình hoặc SGK...",
    height=150,
    key="yeu_cau"
)



if st.button("✨ AI GỢI Ý NỘI DUNG GIÁO ÁN"):
    if not ten_bai.strip() or not yeu_cau.strip():
        st.warning("Vui lòng nhập tên bài và yêu cầu cần đạt trước.")
    else:
        thong_tin_ai = {
            "Môn học": mon_hoc,
            "Lớp": lop,
            "Tên bài": ten_bai,
            "Số tiết": so_tiet,
            "Bộ sách": bo_sach,
            "Trình độ học sinh": trinh_do,
            "Yêu cầu cần đạt": yeu_cau
        }

        try:
            with st.spinner("Gemini AI đang xây dựng giáo án..."):
                noi_dung_ai = tao_giao_an_ai(
                    st.secrets["GEMINI_API_KEY"],
                    thong_tin_ai
                )

            for ten_truong, noi_dung in noi_dung_ai.items():
                st.session_state[ten_truong] = noi_dung

            st.session_state["da_tao_giao_an"] = True
            st.success("AI đã gợi ý nội dung giáo án thành công!")
            st.rerun()

        
        except Exception as e:
            import urllib.error

            if isinstance(e, urllib.error.HTTPError):
                st.error(
                    f"Gemini API báo lỗi HTTP {e.code}. "
                    "Vui lòng kiểm tra kết nối, hạn mức hoặc quyền truy cập mô hình."
                )
            else:
                st.error(
                    f"Không thể tạo giáo án bằng AI. "
                    f"Loại lỗi: {type(e).__name__}"
                )


if st.button("TẠO KẾ HOẠCH BÀI DẠY"):

    if not ten_bai.strip():
        st.warning("Vui lòng nhập tên bài dạy!")
        st.session_state["da_tao_giao_an"] = False

    elif not yeu_cau.strip():
        st.warning("Vui lòng nhập yêu cầu cần đạt!")
        st.session_state["da_tao_giao_an"] = False

    else:
        st.session_state["da_tao_giao_an"] = True

if st.session_state["da_tao_giao_an"]:
    st.success("Đã nhận đầy đủ thông tin bài dạy!")

    st.write("Trường:", ten_truong)
    st.write("Tổ chuyên môn:", to_chuyen_mon)
    st.write("Giáo viên:", ten_giao_vien)
    st.write("Môn học:", mon_hoc)
    st.write("Lớp:", lop)
    st.write("Tên bài:", ten_bai)
    st.write("Số tiết:", so_tiet)
    st.write("Bộ sách:", bo_sach)
    st.write("Trình độ học sinh:", trinh_do)
    st.write("Yêu cầu cần đạt:", yeu_cau)

        # Tạo và hiển thị khung giáo án
    khung = tao_khung_giao_an()

    st.divider()
    st.header("KẾ HOẠCH BÀI DẠY")

        
        # Phần I: Mục tiêu bài dạy
    st.subheader("I. MỤC TIÊU")

    kien_thuc = st.text_area(
            "1. Kiến thức",
            placeholder="Nhập mục tiêu về kiến thức...",
            height=120,
            key="kien_thuc"
        )

    nang_luc = st.text_area(
            "2. Năng lực",
            placeholder="Nhập năng lực học sinh cần phát triển...",
            height=120,
            key="nang_luc"
        )

    pham_chat = st.text_area(
            "3. Phẩm chất",
            placeholder="Nhập phẩm chất học sinh cần hình thành...",
            height=120,
            key="pham_chat"
        )

    st.subheader(
            "II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU"
        )

    thiet_bi = st.text_area(
            "Nhập thiết bị dạy học và học liệu",
            placeholder=(
                "Ví dụ: Máy tính, máy chiếu, "
                "SGK, tranh ảnh, phiếu học tập..."
            ),
            height=130,
            key="thiet_bi"
        )

    st.subheader("III. TIẾN TRÌNH DẠY HỌC")

    for ten_hoat_dong in khung[
            "III. TIẾN TRÌNH DẠY HỌC"
        ]:
            st.write("•", ten_hoat_dong)

        # Hoạt động 1: Mở đầu
    st.subheader("HOẠT ĐỘNG 1: MỞ ĐẦU (KHỞI ĐỘNG)")

    hd1_muc_tieu = st.text_area(
            "Hoạt động 1 - a) Mục tiêu",
            placeholder="Nhập mục tiêu của hoạt động mở đầu...",
            height=100,
            key="hd1_muc_tieu"
        )

    hd1_noi_dung = st.text_area(
            "Hoạt động 1 - b) Nội dung",
            placeholder="Nhập câu hỏi, trò chơi hoặc nhiệm vụ khởi động...",
            height=120,
            key="hd1_noi_dung"
        )

    hd1_san_pham = st.text_area(
            "Hoạt động 1 - c) Sản phẩm",
            placeholder="Nhập câu trả lời hoặc sản phẩm học tập dự kiến...",
            height=100,
            key="hd1_san_pham"
        )

    hd1_to_chuc = st.text_area(
            "Hoạt động 1 - d) Tổ chức thực hiện",
            placeholder=(
                "Bước 1: Chuyển giao nhiệm vụ\n"
                "Bước 2: Thực hiện nhiệm vụ\n"
                "Bước 3: Báo cáo, thảo luận\n"
                "Bước 4: Kết luận, nhận định"
            ),
            height=180,
            key="hd1_to_chuc"
        )

        # Hoạt động 2: Hình thành kiến thức mới
    st.subheader(
            "HOẠT ĐỘNG 2: HÌNH THÀNH KIẾN THỨC MỚI"
        )

    hd2_muc_tieu = st.text_area(
            "Hoạt động 2 - a) Mục tiêu",
            placeholder="Nhập mục tiêu hình thành kiến thức mới...",
            height=100,
            key="hd2_muc_tieu"
        )

    hd2_noi_dung = st.text_area(
            "Hoạt động 2 - b) Nội dung",
            placeholder=(
                "Nhập nhiệm vụ khám phá, câu hỏi, "
                "hoạt động nhóm hoặc nội dung kiến thức..."
            ),
            height=120,
            key="hd2_noi_dung"
        )

    hd2_san_pham = st.text_area(
            "Hoạt động 2 - c) Sản phẩm",
            placeholder=(
                "Nhập kiến thức, câu trả lời hoặc "
                "sản phẩm học tập học sinh cần hoàn thành..."
            ),
            height=100,
            key="hd2_san_pham"
        )

    hd2_to_chuc = st.text_area(
            "Hoạt động 2 - d) Tổ chức thực hiện",
            placeholder=(
                "Bước 1: Chuyển giao nhiệm vụ\n"
                "Bước 2: Thực hiện nhiệm vụ\n"
                "Bước 3: Báo cáo, thảo luận\n"
                "Bước 4: Kết luận, nhận định"
            ),
            height=180,
            key="hd2_to_chuc"
        )

        # Hoạt động 3: Luyện tập
    st.subheader("HOẠT ĐỘNG 3: LUYỆN TẬP")

    hd3_muc_tieu = st.text_area(
            "Hoạt động 3 - a) Mục tiêu",
            placeholder="Nhập mục tiêu củng cố kiến thức...",
            height=100,
            key="hd3_muc_tieu"
        )

    hd3_noi_dung = st.text_area(
            "Hoạt động 3 - b) Nội dung",
            placeholder="Nhập bài tập, câu hỏi hoặc nhiệm vụ luyện tập...",
            height=120,
            key="hd3_noi_dung"
        )

    hd3_san_pham = st.text_area(
            "Hoạt động 3 - c) Sản phẩm",
            placeholder="Nhập đáp án hoặc sản phẩm học tập dự kiến...",
            height=100,
            key="hd3_san_pham"
        )

    hd3_to_chuc = st.text_area(
            "Hoạt động 3 - d) Tổ chức thực hiện",
            placeholder=(
                "Bước 1: Chuyển giao nhiệm vụ\n"
                "Bước 2: Thực hiện nhiệm vụ\n"
                "Bước 3: Báo cáo, thảo luận\n"
                "Bước 4: Kết luận, nhận định"
            ),
            height=180,
            key="hd3_to_chuc"
        )

        # Hoạt động 4: Vận dụng
    st.subheader("HOẠT ĐỘNG 4: VẬN DỤNG")

    hd4_muc_tieu = st.text_area(
            "Hoạt động 4 - a) Mục tiêu",
            placeholder="Nhập mục tiêu vận dụng kiến thức vào thực tế...",
            height=100,
            key="hd4_muc_tieu"
        )

    hd4_noi_dung = st.text_area(
            "Hoạt động 4 - b) Nội dung",
            placeholder="Nhập tình huống thực tế hoặc nhiệm vụ vận dụng...",
            height=120,
            key="hd4_noi_dung"
        )

    hd4_san_pham = st.text_area(
            "Hoạt động 4 - c) Sản phẩm",
            placeholder="Nhập sản phẩm hoặc kết quả học sinh cần hoàn thành...",
            height=100,
            key="hd4_san_pham"
        )

    hd4_to_chuc = st.text_area(
            "Hoạt động 4 - d) Tổ chức thực hiện",
            placeholder=(
                "Bước 1: Chuyển giao nhiệm vụ\n"
                "Bước 2: Thực hiện nhiệm vụ\n"
                "Bước 3: Báo cáo, thảo luận\n"
                "Bước 4: Kết luận, nhận định"
            ),
            height=180,
            key="hd4_to_chuc"
        )
        
        # Chuẩn bị thông tin để xuất Word
    thong_tin_word = {
            "Trường": ten_truong,
            "Tổ chuyên môn": to_chuyen_mon,
            "Giáo viên": ten_giao_vien,
            "Môn học": mon_hoc,
            "Lớp": lop,
            "Tên bài": ten_bai,
            "Số tiết": so_tiet,
            "Bộ sách": bo_sach,
            "Trình độ học sinh": trinh_do
        }
        
        # Đưa mục tiêu bài dạy vào khung giáo án
    khung["I. MỤC TIÊU"]["Kiến thức"] = kien_thuc
    khung["I. MỤC TIÊU"]["Năng lực"] = nang_luc
    khung["I. MỤC TIÊU"]["Phẩm chất"] = pham_chat
        
        # Đưa thiết bị dạy học và học liệu vào giáo án
    khung["II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU"] = thiet_bi

        # Ket noi Hoat dong 1 voi du lieu xuat Word
    hd1 = khung["III. TIẾN TRÌNH DẠY HỌC"][
            "Hoạt động 1: Mở đầu"
        ]

    hd1["Mục tiêu"] = hd1_muc_tieu
    hd1["Nội dung"] = hd1_noi_dung
    hd1["Sản phẩm"] = hd1_san_pham

    hd1["Tổ chức thực hiện"] = {
            "Các bước tổ chức": hd1_to_chuc
        }

        # Ket noi Hoat dong 2 voi du lieu xuat Word
    hd2 = khung["III. TIẾN TRÌNH DẠY HỌC"][
            "Hoạt động 2: Hình thành kiến thức mới"
        ]

    hd2["Mục tiêu"] = hd2_muc_tieu
    hd2["Nội dung"] = hd2_noi_dung
    hd2["Sản phẩm"] = hd2_san_pham

    hd2["Tổ chức thực hiện"] = {
            "Các bước tổ chức": hd2_to_chuc
        }

        # Ket noi Hoat dong 3 voi du lieu xuat Word
    hd3 = khung["III. TIẾN TRÌNH DẠY HỌC"][
            "Hoạt động 3: Luyện tập"
        ]

    hd3["Mục tiêu"] = hd3_muc_tieu
    hd3["Nội dung"] = hd3_noi_dung
    hd3["Sản phẩm"] = hd3_san_pham

    hd3["Tổ chức thực hiện"] = {
            "Các bước tổ chức": hd3_to_chuc
        }

        # Ket noi Hoat dong 4 voi du lieu xuat Word
    hd4 = khung["III. TIẾN TRÌNH DẠY HỌC"][
            "Hoạt động 4: Vận dụng"
        ]

    hd4["Mục tiêu"] = hd4_muc_tieu
    hd4["Nội dung"] = hd4_noi_dung
    hd4["Sản phẩm"] = hd4_san_pham

    hd4["Tổ chức thực hiện"] = {
            "Các bước tổ chức": hd4_to_chuc
        }

    # Luu ban nhap giao an
    du_lieu_ban_nhap = {
        "thong_tin": thong_tin_word,
        "giao_an": khung
    }

    st.download_button(
        label="💾 LƯU BẢN NHÁP GIÁO ÁN (.JSON)",
        data=json.dumps(du_lieu_ban_nhap, ensure_ascii=False, indent=4),
        file_name="Ban_nhap_giao_an.json",
        mime="application/json"
    )

        # Tạo file Word từ dữ liệu giáo án
        
    
    file_word = tao_file_word(thong_tin_word, khung)
    
    
        # Kiểm tra nội dung trước khi xuất Word
    st.subheader("KIỂM TRA NỘI DUNG GIÁO ÁN")

    if not kien_thuc.strip():
            st.warning("Chưa nhập mục tiêu Kiến thức.")

    if not nang_luc.strip():
            st.warning("Chưa nhập mục tiêu Năng lực.")

    if not pham_chat.strip():
            st.warning("Chưa nhập mục tiêu Phẩm chất.")

    if not thiet_bi.strip():
            st.warning("Chưa nhập Thiết bị dạy học và học liệu.")

        # Kiểm tra Hoạt động 1 - Mở đầu
    if not hd1_muc_tieu.strip():
            st.warning("Hoạt động 1: Chưa nhập Mục tiêu.")

    if not hd1_noi_dung.strip():
            st.warning("Hoạt động 1: Chưa nhập Nội dung.")

    if not hd1_san_pham.strip():
            st.warning("Hoạt động 1: Chưa nhập Sản phẩm.")

    if not hd1_to_chuc.strip():
            st.warning("Hoạt động 1: Chưa nhập Tổ chức thực hiện.")

        # Kiem tra Hoat dong 2, 3 va 4
    cac_hoat_dong = {
            2: [hd2_muc_tieu, hd2_noi_dung,
                hd2_san_pham, hd2_to_chuc],
            3: [hd3_muc_tieu, hd3_noi_dung,
                hd3_san_pham, hd3_to_chuc],
            4: [hd4_muc_tieu, hd4_noi_dung,
                hd4_san_pham, hd4_to_chuc]
        }

    ten_muc = [
            "Mục tiêu",
            "Nội dung",
            "Sản phẩm",
            "Tổ chức thực hiện"
        ]

    for so_hd, cac_noi_dung in cac_hoat_dong.items():
            for ten, gia_tri in zip(ten_muc, cac_noi_dung):
                if not gia_tri.strip():
                    st.warning(
                        f"Hoạt động {so_hd}: Chưa nhập {ten}."
                    )

        # Kiểm tra giáo án đã nhập đủ nội dung hay chưa
    du_lieu_bat_buoc = [
            ten_truong, to_chuyen_mon, ten_giao_vien,
            ten_bai, yeu_cau,
            kien_thuc, nang_luc, pham_chat, thiet_bi,
            hd1_muc_tieu, hd1_noi_dung, hd1_san_pham, hd1_to_chuc,
            hd2_muc_tieu, hd2_noi_dung, hd2_san_pham, hd2_to_chuc,
            hd3_muc_tieu, hd3_noi_dung, hd3_san_pham, hd3_to_chuc,
            hd4_muc_tieu, hd4_noi_dung, hd4_san_pham, hd4_to_chuc
        ]

    giao_an_day_du = all(
            str(noi_dung).strip() for noi_dung in du_lieu_bat_buoc
        )

    st.divider()

    st.subheader("XUẤT KẾ HOẠCH BÀI DẠY")

    st.download_button(
            label="📥 TẢI KẾ HOẠCH BÀI DẠY WORD (.DOCX)",
            data=file_word.getvalue(),
            file_name="Ke_hoach_bai_day_EduPlan_AI.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    disabled=not giao_an_day_du    
        )









