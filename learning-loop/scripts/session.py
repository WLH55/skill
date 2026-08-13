#!/usr/bin/env python3
"""learning-loop 会话状态机。

用法:
  session.py init "<主题>" [--mode quick|standard] [--dir <基础目录>]
  session.py status [--topic <主题>] [--dir <基础目录>]
  session.py advance <stage> [--topic <主题>] [--dir <基础目录>]
  session.py upgrade [--topic <主题>] [--dir <基础目录>]
  session.py list
"""

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
def _setup_utf8():
    for stream in (sys.stdout, sys.stderr):
        if stream is not None and hasattr(stream, "reconfigure"):
            try:
                stream.reconfigure(encoding="utf-8")
            except Exception:
                pass


_setup_utf8()

PIPELINES = {
    "quick": ["storm", "brief", "core20", "quiz", "feynman", "cheatsheet"],
    "standard": [
        "storm", "conflict", "brief", "review", "resources",
        "ladder", "core20", "quiz", "feynman", "cheatsheet",
    ],
}

STAGE_FILES = {
    "storm": "01-storm.md",
    "conflict": "02-conflict.md",
    "brief": "03-brief.md",
    "review": "04-review.md",
    "resources": "05-resources.md",
    "ladder": "06-ladder.md",
    "core20": "07-core20.md",
    "quiz": "08-quiz-log.md",
    "feynman": "09-feynman-log.md",
    "cheatsheet": "10-cheatsheet.md",
}

DEFAULT_MODE = "standard"


def now_iso():
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def slugify(text):
    slug = re.sub(r"[^\w-]+", "-", text.lower()).strip("-")
    slug = re.sub(r"-{2,}", "-", slug)
    return slug or "session"


def die(message):
    print(f"错误: {message}", file=sys.stderr)
    sys.exit(1)


def session_dir(base, topic):
    return Path(base) / "learning-sessions" / slugify(topic)


def find_sessions(base):
    return sorted(Path(base).glob("learning-sessions/*/session.json"))


def load_state(path):
    if not path.exists():
        die(f"会话不存在: {path}（先用 init 创建）")
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def save_state(path, state):
    state["updated_at"] = now_iso()
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(state, fh, ensure_ascii=False, indent=2)
        fh.write("\n")


def print_state(state):
    print(f"主题: {state['topic']}  (模式: {state['mode']})")
    parts = []
    for stage in state["pipeline"]:
        if stage in state["completed"]:
            parts.append(f"[✔] {stage}")
        elif stage == state["current"]:
            parts.append(f"[▶] {stage}")
        else:
            parts.append(f"[ ] {stage}")
    print("进度: " + " → ".join(parts))
    if state["current"]:
        print(f"当前阶段: {state['current']}  产物: {STAGE_FILES[state['current']]}")
    else:
        print("状态: 全部完成 🎉")


def cmd_init(args):
    base = Path(args.dir)
    sdir = session_dir(base, args.topic)
    sdir.mkdir(parents=True, exist_ok=True)
    path = sdir / "session.json"
    if path.exists():
        die(f"会话已存在: {path}（如需恢复请用 status/advance，不要重建）")
    state = {
        "schema": 1,
        "topic": args.topic,
        "mode": args.mode,
        "pipeline": PIPELINES[args.mode],
        "completed": [],
        "current": PIPELINES[args.mode][0],
        "created_at": now_iso(),
        "updated_at": now_iso(),
    }
    save_state(path, state)
    print(f"已创建会话: {path}")
    print(f"模式: {args.mode}  路径: {' → '.join(state['pipeline'])}")
    print(f"当前阶段: {state['current']}  产物: {STAGE_FILES[state['current']]}")


def resolve_session(args):
    if getattr(args, "topic", None):
        return session_dir(args.dir, args.topic) / "session.json"
    sessions = find_sessions(args.dir)
    if not sessions:
        die("没有找到任何会话（先用 init 创建，或指定 --topic）")
    return max(sessions, key=lambda p: p.stat().st_mtime)


def cmd_status(args):
    if getattr(args, "topic", None):
        print_state(load_state(session_dir(args.dir, args.topic) / "session.json"))
        return
    sessions = find_sessions(args.dir)
    if not sessions:
        print("没有找到会话。创建: python scripts/session.py init \"<主题>\" --mode quick|standard")
        return
    for path in sessions:
        print_state(load_state(path))
        print()


def cmd_advance(args):
    path = resolve_session(args)
    state = load_state(path)
    stage = args.stage
    if stage not in state["pipeline"]:
        die(f"未知阶段 {stage}，本模式的路径为: {' → '.join(state['pipeline'])}")
    if state["current"] is None:
        die("会话已全部完成，无需推进")
    if stage != state["current"]:
        die(f"当前阶段是 {state['current']}，不能直接推进 {stage}（按顺序推进）")
    state["completed"].append(stage)
    remaining = [s for s in state["pipeline"] if s not in state["completed"]]
    state["current"] = remaining[0] if remaining else None
    save_state(path, state)
    print(f"✔ {stage} 已完成")
    if state["current"]:
        print(f"下一阶段: {state['current']}  产物: {STAGE_FILES[state['current']]}")
    else:
        print("全部阶段完成 🎉  最终交付物: " + STAGE_FILES["cheatsheet"])


def cmd_upgrade(args):
    path = resolve_session(args)
    state = load_state(path)
    if state["mode"] == "standard":
        die("已经是标准模式，无需升级")
    state["mode"] = "standard"
    state["pipeline"] = PIPELINES["standard"]
    state["current"] = next((s for s in state["pipeline"] if s not in state["completed"]), None)
    save_state(path, state)
    print("已升级为标准模式")
    print_state(state)


def cmd_list(_args):
    for mode, pipeline in PIPELINES.items():
        print(f"{mode}: {' → '.join(pipeline)}")


def main():
    parser = argparse.ArgumentParser(description="learning-loop 会话状态机")
    sub = parser.add_subparsers(dest="command", required=True)

    p_init = sub.add_parser("init", help="创建会话")
    p_init.add_argument("topic", help="学习主题")
    p_init.add_argument("--mode", choices=PIPELINES.keys(), default=DEFAULT_MODE, help="quick 或 standard")
    p_init.add_argument("--dir", default=".", help="会话基础目录（默认当前目录）")
    p_init.set_defaults(func=cmd_init)

    p_status = sub.add_parser("status", help="查看进度")
    p_status.add_argument("--topic", default=None)
    p_status.add_argument("--dir", default=".")
    p_status.set_defaults(func=cmd_status)

    p_advance = sub.add_parser("advance", help="推进当前阶段")
    p_advance.add_argument("stage", help="阶段 id（如 storm）")
    p_advance.add_argument("--topic", default=None)
    p_advance.add_argument("--dir", default=".")
    p_advance.set_defaults(func=cmd_advance)

    p_upgrade = sub.add_parser("upgrade", help="quick 升级为 standard")
    p_upgrade.add_argument("--topic", default=None)
    p_upgrade.add_argument("--dir", default=".")
    p_upgrade.set_defaults(func=cmd_upgrade)

    p_list = sub.add_parser("list", help="列出模式与流水线")
    p_list.set_defaults(func=cmd_list)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()


