"""Export agent transcript JSONL to Prompt markdown."""

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
TRANSCRIPTS_DIR = Path(
    r"C:\Users\usejen_id\.cursor\projects"
    r"\c-Users-usejen-id-Desktop-ai-dev-MagicSquare-xx"
    r"\agent-transcripts"
)
DEFAULT_TRANSCRIPT_ID = "48f402dd-31cc-4a31-8528-65bb630a635d"
DEFAULT_OUTPUT = PROJECT_ROOT / "Prompt" / (
    "04.cursor_project_rules_mdc_migration_transcript.md"
)
DEFAULT_TITLE = (
    "# Cursor Project Rules (.mdc) 마이그레이션 — 대화 Transcript"
)


def extract_user(text: str) -> str:
    """Pull user query from tagged message."""
    match = re.search(r"<user_query>\s*(.*?)\s*</user_query>", text, re.S)
    return match.group(1).strip() if match else text.strip()


def extract_assistant(parts: list[dict[str, str]]) -> str:
    """Collect non-redacted assistant text blocks."""
    texts: list[str] = []
    for part in parts:
        if part.get("type") != "text":
            continue
        block = part.get("text", "")
        if block and block != "[REDACTED]":
            texts.append(block)
    return "\n\n".join(texts)


def resolve_transcript(path: Path | None, transcript_id: str | None) -> Path:
    """Resolve JSONL path from explicit path, id, or newest transcript."""
    if path is not None:
        return path
    if transcript_id:
        candidate = TRANSCRIPTS_DIR / transcript_id / f"{transcript_id}.jsonl"
        if candidate.is_file():
            return candidate
        raise FileNotFoundError(f"Transcript not found: {candidate}")
    jsonl_files = sorted(
        TRANSCRIPTS_DIR.glob("*/*.jsonl"),
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )
    if not jsonl_files:
        raise FileNotFoundError(f"No transcripts under {TRANSCRIPTS_DIR}")
    return jsonl_files[0]


def export_transcript(
    transcript: Path,
    output: Path,
    title: str,
    append: str | None = None,
) -> int:
    """Write markdown transcript; return user turn count."""
    exported_at = datetime.now().strftime("%m/%d/%Y at %H:%M:%S GMT+9")
    lines: list[str] = [
        title,
        f"_Exported on {exported_at} from Cursor Agent transcript "
        f"(`{transcript.parent.name}`)_",
        "",
        "---",
        "",
    ]
    user_turns = 0
    for raw in transcript.read_text(encoding="utf-8").splitlines():
        if not raw.strip():
            continue
        obj = json.loads(raw)
        role = obj.get("role")
        content = obj["message"]["content"]
        if role == "user":
            user_turns += 1
            text = extract_user(content[0]["text"])
            lines.extend(["**User**", "", text, "", "---", ""])
        elif role == "assistant":
            text = extract_assistant(content)
            if text.strip():
                lines.extend(["**Cursor**", "", text, "", "---", ""])

    if append:
        lines.extend(["**Cursor**", "", append.strip(), "", "---", ""])

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines), encoding="utf-8")
    return user_turns


def main() -> None:
    """CLI entry."""
    parser = argparse.ArgumentParser(description="Export Cursor agent transcript")
    parser.add_argument(
        "--transcript",
        type=Path,
        help="Path to .jsonl transcript file",
    )
    parser.add_argument(
        "--id",
        default=DEFAULT_TRANSCRIPT_ID,
        help="Transcript UUID folder name",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help="Output markdown path",
    )
    parser.add_argument("--title", default=DEFAULT_TITLE, help="Markdown H1 title")
    parser.add_argument(
        "--append",
        type=str,
        default=None,
        help="Optional final Cursor block (e.g. closing summary)",
    )
    args = parser.parse_args()
    transcript = resolve_transcript(args.transcript, args.id)
    user_turns = export_transcript(
        transcript, args.output, args.title, append=args.append
    )
    out = args.output
    print(f"Wrote {out} ({out.stat().st_size} bytes, user turns={user_turns})")


if __name__ == "__main__":
    main()
