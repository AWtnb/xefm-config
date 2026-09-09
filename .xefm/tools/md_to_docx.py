import os
import shlex
import shutil
import subprocess
from pathlib import Path


def as_docx(md_path: Path) -> None:
    out_docx = md_path.with_suffix(".docx")
    try:
        subprocess.run(
            [
                "pandoc",
                "--from=markdown",
                "--to=docx",
                "--standalone",
                f"--out={out_docx}",
                str(md_path),
            ],
            check=True,
        )
        print(f"[FINISHED] Converted Markdown to docx: {out_docx}")
    except Exception as e:  # noqa: BLE001
        print(f"[ERROR] pandoc conversion failed: {e}")


def main():
    if not shutil.which("pandoc"):
        print("pandoc not found in PATH")
        return

    selected_names = shlex.split(os.environ.get("XEFM_THIS_SELECTED", ""))
    if len(selected_names) != 1:
        return

    paths = [
        Path(os.environ.get("XEFM_THIS_DIR", os.getcwd()), n) for n in selected_names
    ]

    for path in paths:
        if path.suffix == ".md":
            as_docx(path)


if __name__ == "__main__":
    main()
