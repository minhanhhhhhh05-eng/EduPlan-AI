
import json
import urllib.request
import urllib.error

def tao_giao_an_ai(api_key, thong_tin):
    url = (
        "https://generativelanguage.googleapis.com/v1beta/"
        "models/gemini-3.1-flash-lite:generateContent"
    )

    prompt = f"""
Bạn là giáo viên phổ thông tại Việt Nam.
Hãy đề xuất kế hoạch bài dạy tham khảo theo CT GDPT 2018,
với cấu trúc hoạt động tham chiếu Công văn 5512.

Thông tin bài dạy:
{json.dumps(thong_tin, ensure_ascii=False)}

Yêu cầu:
- Bám sát yêu cầu cần đạt do giáo viên cung cấp.
- Không tự nhận đã kiểm chứng nội dung SGK.
- Thiết kế hoạt động phù hợp trình độ và số tiết.
- Mỗi hoạt động có mục tiêu, nội dung, sản phẩm
  và bốn bước tổ chức thực hiện.
- Viết cụ thể, dễ chỉnh sửa và áp dụng trên lớp.
- Chỉ trả về JSON, không kèm Markdown.

JSON phải có chính xác các khóa sau:
kien_thuc, nang_luc, pham_chat, thiet_bi,
hd1_muc_tieu, hd1_noi_dung, hd1_san_pham, hd1_to_chuc,
hd2_muc_tieu, hd2_noi_dung, hd2_san_pham, hd2_to_chuc,
hd3_muc_tieu, hd3_noi_dung, hd3_san_pham, hd3_to_chuc,
hd4_muc_tieu, hd4_noi_dung, hd4_san_pham, hd4_to_chuc.

Mỗi giá trị là một chuỗi văn bản.
"""

    data = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "responseMimeType": "application/json"
        }
    }

    request = urllib.request.Request(
        url,
        data=json.dumps(data).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "x-goog-api-key": api_key
        },
        method="POST"
    )

    with urllib.request.urlopen(request, timeout=90) as response:
        result = json.load(response)

    van_ban = "".join(
        part.get("text", "")
        for part in result["candidates"][0]["content"]["parts"]
    )
    noi_dung = json.loads(van_ban)

    cac_truong = [
        "kien_thuc", "nang_luc", "pham_chat", "thiet_bi"
    ]

    for i in range(1, 5):
        cac_truong.extend([
            f"hd{i}_muc_tieu",
            f"hd{i}_noi_dung",
            f"hd{i}_san_pham",
            f"hd{i}_to_chuc"
        ])

    if not isinstance(noi_dung, dict):
        raise ValueError("AI chưa trả về đúng cấu trúc giáo án.")

    if any(
        not isinstance(noi_dung.get(k), str)
        for k in cac_truong
    ):
        raise ValueError("AI trả về thiếu nội dung hoặc sai cấu trúc.")

    return {k: noi_dung[k] for k in cac_truong}
