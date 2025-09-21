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
│   ├── template_crf.xml        # Cấu hình giao diện cho Label Studio
│   └── sample_import.json      # Tác vụ mẫu giúp khởi tạo dự án nhanh chóng
├── output/
│   └── crf_final.xlsx          # Tệp Excel tổng hợp kết quả QC cuối cùng (placeholder)
├── scripts/
│   ├── make_labelstudio_tasks.py   # Tạo tệp JSON nhiệm vụ từ scans + drafts
│   ├── json_to_excel.py            # Chuyển đổi dữ liệu xuất từ Label Studio sang Excel
│   ├── ocr_pdf_to_images.py        # Trợ thủ tùy chọn để tách PDF thành ảnh
│   └── ocr_image_to_text.py        # Trợ thủ tùy chọn chạy OCR hàng loạt trên ảnh
├── requirements.txt
└── README.md
```

## Getting started

### 1) Cài đặt phụ thuộc (Windows PowerShell)
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 2) Chuẩn bị dữ liệu đầu vào
- Đặt ảnh quét từng trang vào `data/scans/` (PNG/JPG hoặc PDF đã tách trang).
- Đặt bản nháp HTML vào `data/drafts/`, tên trùng với ảnh tương ứng (ví dụ: `subject001_page_01.html`).

### 3) Sinh nhiệm vụ cho Label Studio (JSON)
```powershell
python scripts/make_labelstudio_tasks.py label_studio/import.json
```
> ⚠️ **Lưu ý:** Giao diện import của Label Studio hiện không chấp nhận JSONL. Hãy giữ phần mở rộng `.json` khi tạo tệp nhiệm vụ.

### 4) Khởi tạo và chạy Label Studio (Windows)
```powershell
# Cho phép Label Studio truy cập file cục bộ
$env:LABEL_STUDIO_LOCAL_FILES_SERVING_ENABLED = "true"
$env:LABEL_STUDIO_LOCAL_FILES_DOCUMENT_ROOT = "C:\Users\BeTin\Documents\GitHub\CRF_QC_MVP"

# Khởi tạo project "CRF QC" với label config
label-studio init "CRF QC" `
  -l "C:\Users\BeTin\Documents\GitHub\CRF_QC_MVP\label_studio\template_crf.xml" `
  --username admin@example.com `
  --password admin123
```

**Bước trong UI (bắt buộc 1 lần):** vào *Label Studio → Projects → CRF QC → Settings → Labeling Interface*, xóa nội dung mặc định và dán template trong `label_studio/template_crf.xml` → **Save**.

```powershell
# Khởi động server (Windows cần thêm fix SQLite)
label-studio start --agree-fix-sqlite
```
Mở trình duyệt tới: http://localhost:8080 và đăng nhập bằng tài khoản đã đặt ở bước `init`.

### 5) Import dữ liệu
Trong giao diện web, chọn **Import** và tải file `label_studio\sample_import.json` để nạp dữ liệu.

### 6) Tiến hành rà soát QC
- So sánh ảnh quét với bản nháp hiển thị bên phải.
- Điền checklist và ghi chú.
- Đặt trạng thái QC tổng thể.

### 7) Xuất kết quả
- Trong Label Studio, export nhiệm vụ đã hoàn thành (JSON/JSONL).
- Chuyển đổi sang Excel:
```powershell
python scripts/json_to_excel.py path\to\export.json output\crf_final.xlsx
```

## Optional OCR helpers
- `ocr_pdf_to_images.py` chuyển đổi PDF thành ảnh PNG.
- `ocr_image_to_text.py` chạy Tesseract OCR hàng loạt, lưu văn bản thô vào `data/qc_output/`.
