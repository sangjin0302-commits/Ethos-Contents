"""Run the repository CI preview inside this content folder, then package JPEGs.

From repository root with its dependencies installed:
  python content/COSMETICS-LABEL-07-CARD-DRAFT/render-preview.py
No approval metadata is changed. Shared renderer, fonts and gates are not edited.
"""
from pathlib import Path
import hashlib
import json
import sys
import zipfile

FOLDER = Path(__file__).resolve().parent
ROOT = FOLDER.parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from jsonschema import Draft7Validator
from PIL import Image
import ci_render


def main():
    data = json.loads((FOLDER / "card-data.ko.json").read_text(encoding="utf-8"))
    assert data["approvedBy"] == "비교용 초안 — 사용자 승인 전. 발행 금지"
    assert data["totalPages"] == len(data["cards"]) == 10
    source_hash = hashlib.sha256((FOLDER / "blog.md").read_bytes()).hexdigest()
    validator = Draft7Validator(json.loads((ROOT / "schema/card-data.schema.json").read_text(encoding="utf-8")))
    # Regenerate only this script's automatic preview files. ci_render otherwise
    # treats its own ethos-design=free + ethos-auto files as authored free HTML.
    for old in (FOLDER / "ko").glob("card_*.html"):
        assert old.resolve().parent == (FOLDER / "ko").resolve()
        html = old.read_text(encoding="utf-8")
        assert 'name="ethos-auto"' in html or not ci_render.copy_lint.is_free_design(html), 'Protect authored HTML'
        old.unlink()
    # Same CI path; using content as out_root preserves relative asset links and
    # limits all writes to this ID. Avoid ci_render.main's root-level compare.md.
    ok, summary = ci_render.run_id(FOLDER.name, ROOT / "content", validator)
    (FOLDER / "out/preview-summary.md").write_text(summary, encoding="utf-8")
    print(summary)
    assert source_hash == hashlib.sha256((FOLDER / "blog.md").read_bytes()).hexdigest()
    if not ok:
        return 1
    out = FOLDER / "out/ko"
    dest = out / "jpeg"
    dest.mkdir(exist_ok=True)
    files = []
    for number in range(1, 11):
        source = out / f"card_{number:02d}.png"
        if not source.exists():
            source = out / "png" / f"card_{number:02d}.png"
        with Image.open(source) as im:
            assert im.size == (1080, 1350)
            target = dest / f"card_{number:02d}.jpg"
            im.convert("RGB").save(target, "JPEG", quality=95, subsampling=0, optimize=True)
        with Image.open(target) as im:
            im.load()
            assert im.format == "JPEG" and im.mode == "RGB" and im.size == (1080, 1350)
        files.append(target)
    archive = dest / "cosmetics-label-07-ko-jpegs.zip"
    with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as z:
        for file in files:
            z.write(file, file.name)
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None and len(z.namelist()) == 10
        assert z.namelist() == [p.name for p in files]
    result = {"status": "preview-only", "approved": False, "count": len(files),
              "size": [1080, 1350], "mode": "RGB", "quality": 95, "subsampling": 0,
              "zipCrc": "pass", "sourceSha256": source_hash,
              "jpegSha256": {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in files}}
    (out / "jpeg-validation.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print("JPEG package verified: 10 RGB 1080x1350 images; ZIP CRC PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
