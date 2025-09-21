# CRF_QC_MVP

Kho lưu trữ này cung cấp một quy trình gọn nhẹ để kiểm soát chất lượng (QC) việc số hóa phiếu ghi nhận ca bệnh (Case Report Form - CRF, biểu mẫu thu thập dữ liệu trong thử nghiệm lâm sàng). Cấu trúc được giữ nguyên như nguyên mẫu nội bộ để các nhóm có thể tái tạo đường ống xử lý ngay trên máy của mình.

## Repository layout

```
.
├── data/
│   ├── scans/          # Ảnh quét CRF ở cấp trang (định dạng PDF đã tách trang hoặc ảnh PNG/JPG)
│   ├── drafts/         # Bản nháp HTML do đường ống trích xuất tạo ra
│   └── qc_output/      # Tệp JSON/CSV trung gian sinh ra trong bước QC
├── label_studio/
│   ├── template_crf.xml        # Cấu hình giao diện cho Label Studio (nền tảng gán nhãn dữ liệu mã nguồn mở)
│   └── sample_import.jsonl     # Tác vụ mẫu giúp khởi tạo dự án nhanh chóng
├── output/
│   └── crf_final.xlsx          # Tệp Excel tổng hợp kết quả QC cuối cùng (placeholder)
├── scripts/
│   ├── run_labelstudio.sh      # Script hỗ trợ khởi chạy Label Studio cùng dự án CRF
│   ├── make_labelstudio_tasks.py   # Tạo tệp JSONL nhiệm vụ từ scans + drafts
│   ├── json_to_excel.py            # Chuyển đổi dữ liệu xuất từ Label Studio sang Excel
│   ├── ocr_pdf_to_images.py        # Trợ thủ tùy chọn để tách PDF thành ảnh (OCR = Optical Character Recognition, nhận dạng ký tự quang học)
│   └── ocr_image_to_text.py        # Trợ thủ tùy chọn chạy OCR hàng loạt trên ảnh
├── requirements.txt
└── README.md
```

## Getting started

1. **Cài đặt phụ thuộc**
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Chuẩn bị dữ liệu đầu vào**
   * Đặt các ảnh quét CRF theo từng trang (PNG hoặc JPG) trong `data/scans/`. Nếu nguồn ban đầu là PDF, hãy dùng `scripts/ocr_pdf_to_images.py` để kết xuất thành ảnh.
   * Thả các bản nháp HTML do đường ống trích xuất tạo ra vào `data/drafts/`. Mỗi tệp cần được đặt tên trùng với ảnh tương ứng (ví dụ: `subject001_page_01.html`).

3. **Sinh nhiệm vụ cho Label Studio**
   ```bash
   python scripts/make_labelstudio_tasks.py label_studio/import.jsonl
   ```
   Lệnh trên ghép cặp ảnh với bản nháp và tạo tệp JSONL sẵn sàng để nhập vào Label Studio. Dùng thêm `--checklist path/to/items.txt` nếu muốn thay thế danh sách kiểm QC mặc định.

4. **Khởi chạy Label Studio**
   ```bash
   ./scripts/run_labelstudio.sh
   ```
   Script bật chế độ phục vụ tệp cục bộ, trỏ Label Studio tới giao diện CRF được định nghĩa trong `label_studio/template_crf.xml`, và nạp sẵn dự án bằng `label_studio/sample_import.jsonl` (hoặc tệp JSONL bạn vừa tạo ở bước trước). Đăng nhập tại http://localhost:8080 để bắt đầu rà soát.

5. **Tiến hành rà soát QC**
   * So sánh ảnh quét với bản nháp hiển thị ở bảng điều khiển bên phải.
   * Điền lần lượt các hạng mục trong checklist và ghi chép sai lệch tại trường ghi chú.
   * Đặt trạng thái QC tổng thể bằng các lựa chọn đã cung cấp.

6. **Xuất kết quả**
   * Từ Label Studio, xuất các nhiệm vụ đã hoàn thành dưới dạng JSON hoặc JSONL.
   * Chuyển đổi tệp xuất sang Excel với lệnh:
     ```bash
     python scripts/json_to_excel.py path/to/export.json output/crf_final.xlsx
     ```
   * Tệp Excel thu được sẽ tổng hợp quyết định, nhận xét và siêu dữ liệu của người rà soát. Chia sẻ cho nhóm hòa giải ở bước tiếp theo.

## Optional OCR helpers

* `ocr_pdf_to_images.py` chuyển đổi các tệp PDF thành ảnh PNG phù hợp cho bước rà soát và các tác vụ OCR tiếp theo.
* `ocr_image_to_text.py` chạy công cụ Tesseract OCR trên một loạt ảnh và lưu văn bản thô vào `data/qc_output/` để tiện kiểm tra nhanh hoặc so sánh với nội dung bản nháp.

Các tiện ích này không bắt buộc cho quy trình QC nhưng tái hiện những script hỗ trợ từ nguyên mẫu ban đầu.
