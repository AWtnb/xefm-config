import os
import shlex
import shutil
import subprocess
from pathlib import Path

from lib.util import get_timestamp


def summarize(root: Path, rel_paths: list[str]) -> str | None:

    target = []
    for rel in rel_paths:
        p = root / rel
        if p.exists():
            target.append(p)

    if len(target) < 1:
        return None

    border = "```"
    lines: list[str] = ["# SUMMARY\n"]
    lines.append("## DIRECTORIES (excerpt)\n")
    lines.append(border)
    lines.extend(rel_paths)
    lines.append(f"{border}\n")

    lines.append("## FILE CONTENTS\n")

    for path in target:
        try:
            content = path.read_text(encoding="utf-8")
        except Exception:  # noqa: BLE001, S112
            continue
        lines.append(f"### Content of `{p.relative_to(root)}`\n")
        lines.append(border)
        lines.append(content)
        lines.append(f"{border}\n")

    return "\n".join(lines)


def md2docx(md_path: Path) -> None:
    if not shutil.which("pandoc"):
        print("pandoc not found in PATH")
        return

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

    selected_names = shlex.split(os.environ.get("XEFM_THIS_SELECTED", ""))
    if len(selected_names) != 1:
        print("Select just 1 source file.")
        return

    source_file = selected_names[0]
    source_path = Path(os.environ.get("XEFM_THIS_DIR", os.getcwd())) / source_file

    other_path = os.environ.get("XEFM_OTHER_DIR", None)
    if other_path is None:
        return

    rel_paths = source_path.read_text(encoding="utf-8").splitlines()

    root = Path(other_path)
    md = summarize(root=root, rel_paths=rel_paths)
    if md is None:
        print("[ERROR] Nothing to summarize...")
        return

    out_name = f"{root.name}_summary_{get_timestamp()}.md"
    out_path = Path(os.environ.get("XEFM_THIS_DIR", os.getcwd())) / out_name
    out_path.write_text(md, encoding="utf-8")

    md2docx(out_path)


if __name__ == "__main__":
    main()
