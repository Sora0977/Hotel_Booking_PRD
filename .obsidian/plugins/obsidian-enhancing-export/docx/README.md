# DOCX Export Pack

Folder này chứa toàn bộ phần cần thiết cho preset `Word (.docx)`:

- `reference.docx`: file reference template cho Pandoc.
- `build_reference_docx.py`: script tạo lại `reference.docx`.
- `report_docx_postprocess.py`: script hậu xử lý font, heading, spacing, caption, table borders.
- `export_config.json`: cấu hình nguồn của preset `Word (.docx)`.
- `install_docx_export.py`: script áp dụng cấu hình vào `main.js` và `data.json` của plugin.

Sau khi clone lại `obsidian-enhancing-export`, copy folder `docx` này vào:

```powershell
.obsidian\plugins\obsidian-enhancing-export\docx
```

Sau đó chạy một trong các lệnh sau.

Nếu terminal đang mở ở thư mục gốc vault/project:

```powershell
python .\.obsidian\plugins\obsidian-enhancing-export\docx\install_docx_export.py
```

Nếu dùng Git Bash:

```bash
python .obsidian/plugins/obsidian-enhancing-export/docx/install_docx_export.py
```

Nếu dùng macOS Terminal và đang mở ở thư mục gốc vault/project:

```bash
python3 .obsidian/plugins/obsidian-enhancing-export/docx/install_docx_export.py
```

Nếu terminal đang đứng sẵn trong thư mục `docx`:

```bash
python install_docx_export.py
```

Trên macOS, nếu đang đứng sẵn trong thư mục `docx`, dùng:

```bash
python3 install_docx_export.py
```

Không dùng dấu `\` trong Git Bash vì Git Bash sẽ xem `\` là ký tự escape và làm sai đường dẫn.

Reload Obsidian rồi export bằng preset `Word (.docx)`.
