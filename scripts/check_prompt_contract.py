"""Check a project's agreed prompt sections and current video-text references."""
import json
from pathlib import Path
import sys


def check(manifest_path):
    manifest_path = Path(manifest_path)
    data = json.loads(manifest_path.read_text(encoding="utf-8-sig"))
    headings = data.get("prompt_contract", {}).get("headings", [])
    if not headings or len(headings) != len(set(headings)):
        return ["Missing or duplicate agreed headings"]
    inputs = data.get("inputs", [])
    if not inputs:
        return ["No current video tasks"]
    errors, ids, paths = [], set(), set()
    for item in inputs:
        task_id = item.get("id")
        if not task_id or task_id in ids:
            errors.append(f"Duplicate or missing task id: {task_id}")
        ids.add(task_id)
        source = item.get("video_prompt_path")
        if not isinstance(source, str) or not source:
            errors.append(f"{task_id}: exactly one video_prompt_path is required")
            continue
        path = (manifest_path.parent / source).resolve()
        if path in paths:
            errors.append(f"{task_id}: shared current prompt path: {path}")
        paths.add(path)
        if not path.is_file():
            errors.append(f"{task_id}: missing prompt: {path}")
            continue
        lines = path.read_text(encoding="utf-8-sig").splitlines()
        found = [(i, line.strip()) for i, line in enumerate(lines) if line.strip() in headings]
        if [title for _, title in found] != headings:
            errors.append(f"{task_id}: missing, repeated or out-of-order sections")
        else:
            for pos, (start, title) in enumerate(found):
                end = found[pos + 1][0] if pos + 1 < len(found) else len(lines)
                if not any(line.strip() for line in lines[start + 1:end]):
                    errors.append(f"{task_id}: empty section: {title}")
        if data.get("execution_allowed") is True and item.get("status") not in {"APPROVED", "LOCKED"}:
            errors.append(f"{task_id}: execution enabled for unapproved input")
    return errors


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("Usage: check_prompt_contract.py manifest.json")
    try:
        findings = check(sys.argv[1])
    except (OSError, ValueError, TypeError) as exc:
        raise SystemExit(f"ERROR: {exc}")
    print("\n".join(findings) if findings else "PASS: prompt structure and current references only; media quality not assessed")
    raise SystemExit(1 if findings else 0)
