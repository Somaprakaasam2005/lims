PDF generation tooling

This project can generate PDF reports in multiple ways:

1. Preferred: WeasyPrint (HTML -> PDF)
   - Python package: `WeasyPrint` (already listed optionally in `requirements.txt`)
   - Pros: Good CSS support, pure-Python API for rendering Jinja2 HTML.
   - Cons: Requires system libraries (C libraries) to be installed: Cairo, Pango, GDK-PixBuf and their dev headers.

   Install on Ubuntu / Debian (example):

   ```bash
   sudo apt update
   sudo apt install -y python3-dev build-essential libpango1.0-0 libpango1.0-dev libcairo2 libcairo2-dev libgdk-pixbuf2.0-0 libgdk-pixbuf2.0-dev libffi-dev libxml2-dev libxslt1-dev
   python3 -m pip install --upgrade pip
   pip install WeasyPrint
   ```

   On macOS (with Homebrew):

   ```bash
   brew install cairo pango gdk-pixbuf libffi
   python3 -m pip install WeasyPrint
   ```

   On Windows:
   - WeasyPrint on Windows is possible but often fragile; use the official docs: https://weasyprint.org/docs/
   - Install GTK/Cairo runtime packages, or prefer `pdfkit`/`wkhtmltopdf` on Windows.

2. Lightweight fallback: wkhtmltopdf (via `pdfkit` Python wrapper)
   - Pros: Binary-based, simpler system requirements (standalone binary), easy to install on many platforms.
   - Cons: Uses an older WebKit engine, CSS support is more limited than WeasyPrint.

   Install wkhtmltopdf on Ubuntu/Debian (example):

   ```bash
   sudo apt update
   sudo apt install -y wkhtmltopdf
   python3 -m pip install pdfkit
   ```

   On macOS (Homebrew):

   ```bash
   brew install wkhtmltopdf
   pip install pdfkit
   ```

   On Windows:
   - Download the MSI from https://wkhtmltopdf.org/downloads.html and install.
   - Add the wkhtmltopdf installation directory (containing `wkhtmltopdf.exe`) to your PATH.
   - Then install the Python wrapper:

   ```powershell
   pip install pdfkit
   ```

   Notes for `pdfkit` in code:
   - If `wkhtmltopdf` binary is not on the PATH, you can configure pdfkit with its full path:

   ```python
   import pdfkit
   config = pdfkit.configuration(wkhtmltopdf=r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe")
   pdfkit.from_string(html, output_path, configuration=config)
   ```

3. Fallback: ReportLab programmatic PDF generation
   - Pros: Already present and reliable for simple reports.
   - Cons: Not HTML-based; designing complex layouts in code is more work.

Recommendations
- For production Linux deployments: install system deps and use WeasyPrint for best HTML/CSS fidelity.
- For Windows or environments where installing C libs is painful: install `wkhtmltopdf` binary and use `pdfkit` as fallback.

Quick verification commands (Ubuntu):

```bash
# Install wkhtmltopdf and run tests
sudo apt update
sudo apt install -y wkhtmltopdf
python3 -m pip install -r requirements.txt
pytest -q
```

If you want, I can add a small script to detect available PDF engines at runtime and print instructions when none are available. Or I can add Windows-specific guidance to this file — tell me which you prefer.