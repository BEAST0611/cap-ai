from pathlib import Path
ROOT = Path(r"c:\Users\Admin\CAP_AI")
fixed = 0
for f in list(ROOT.rglob("*.py")) + [ROOT / "requirements.txt"]:
    if not f.exists():
        continue
    data = f.read_bytes()
    if b"\x00" not in data:
        continue
    try:
        text = data.decode("utf-16-le")
    except Exception:
        try:
            text = data.decode("utf-16")
        except Exception:
            print("skip", f)
            continue
    f.write_text(text, encoding="utf-8")
    fixed += 1
    print("fixed", f)
print("total fixed", fixed)
