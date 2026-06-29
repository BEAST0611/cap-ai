from pathlib import Path
ROOT = Path(r"c:\Users\Admin\CAP_AI")
req = "streamlit>=1.32.0\npandas>=2.0.0\nnumpy>=1.24.0\nplotly>=5.18.0\nopenpyxl>=3.1.0\nnetworkx>=3.1\nstreamlit-aggrid>=0.3.4\nfpdf2>=2.7.0\nreportlab>=4.0.0\nxlsxwriter>=3.1.0\nstreamlit-lottie>=0.0.5\nstreamlit-extras>=0.4.0\nstreamlit-option-menu>=0.3.6\nhydralit-components>=1.0.10\npython-docx>=1.1.0\nPillow>=10.0.0\n"
(ROOT / "requirements.txt").write_text(req, encoding="utf-8")
print("req ok", (ROOT / "requirements.txt").read_bytes()[:20])
