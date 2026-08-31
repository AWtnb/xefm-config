import datetime
import os
import shlex
from collections.abc import Iterator
from pathlib import Path


def is_skippable(dir_name: str) -> bool:
    return dir_name == "node_modules" or dir_name.startswith((".", "__"))


def traverse_file(root: str) -> Iterator[str]:
    for dir_path, dir_names, file_names in os.walk(root):
        dir_names[:] = [d for d in dir_names if not is_skippable(d)]
        for f in file_names:
            yield os.path.join(dir_path, f)


def summarize(
    root: Path, targets: list[str], chunk_limit: int = 12000
) -> tuple[list[str], int]:
    """
    プロジェクト構成サマリーをチャンク分割して返す。

    Args:
        root: プロジェクトルートパス
        targets: 対象ファイル・ディレクトリのパスリスト
        chunk_limit: 1チャンクあたりの最大文字数

    Returns:
        (チャンク文字列のリスト, 読み込んだファイル数)
    """
    paths: list[str] = []
    tree_flag = False
    for path in targets:
        if Path(path).is_dir():
            tree_flag = True
            paths.extend(traverse_file(path))
        else:
            paths.append(path)

    border = "```"

    header_lines: list[str] = ["# SUMMARY\n"]
    if tree_flag:
        header_lines.append("## DIRECTORIES\n")
        header_lines.append(border)
        header_lines.extend(str(Path(p).relative_to(root)) for p in paths)
        header_lines.append(f"{border}\n")
    header_lines.append("## FILE CONTENTS\n")

    chunks: list[str] = []
    current_lines: list[str] = header_lines
    counter = 0

    for path in paths:
        p = Path(path)
        try:
            content = p.read_text(encoding="utf-8")
            counter += 1
        except Exception:  # noqa: BLE001, S112
            continue

        file_block_lines = [
            f"### Content of `{p.relative_to(root)}`\n",
            border,
            content,
            f"{border}\n",
        ]
        file_block = "\n".join(file_block_lines)
        current_text = "\n".join(current_lines)

        if 0 < len(chunks) and chunk_limit < len(current_text) + len(file_block):
            chunks.append(current_text)
            current_lines = [
                f"# SUMMARY (continued, part {len(chunks) + 1})\n",
                "## FILE CONTENTS (continued)\n",
            ]

        current_lines.extend(file_block_lines)

    chunks.append("\n".join(current_lines))
    return chunks, counter


def get_timestamp() -> str:
    tz_jst = datetime.timezone(datetime.timedelta(hours=9))
    return datetime.datetime.now(tz=tz_jst).strftime("%Y%m%d-%H%M%S")


def main():
    root = Path(os.environ.get("XEFM_THIS_DIR", os.getcwd()))
    selected_names = shlex.split(os.environ.get("XEFM_THIS_SELECTED", ""))
    if len(selected_names) < 1:
        print("Nothing selected.")
        return

    targets = [
        (name if os.path.isabs(name) else os.path.join(root, name))
        for name in selected_names
    ]

    timestamp = get_timestamp()
    out_dir = Path(os.environ.get("XEFM_OTHER_DIR", os.getcwd()))
    chunks, count = summarize(root, targets)

    for i, chunk in enumerate(chunks, 1):
        suffix = f"_part{i}" if 1 < len(chunks) else ""
        out_name = f"{root.name}_summary_{timestamp}{suffix}.txt"
        out_path = out_dir / out_name
        out_path.write_text(chunk, encoding="utf-8")

    print(f"[FINISHED] Summarized {count} files into {len(chunks)} file(s).")


if __name__ == "__main__":
    main()
