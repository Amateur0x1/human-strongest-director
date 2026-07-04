#!/usr/bin/env python3
"""
批量视频提取脚本 — 从 XHS JSON 导出文件中批量下载视频、截帧、whisper 转录
复用 social-media-sniffer 的 extract_video.py 逻辑
"""

import json
import os
import subprocess
import sys
import time
from pathlib import Path

# 配置
JSON_FILE = sys.argv[1] if len(sys.argv) > 1 else "/Users/zhourongchang/Downloads/xhs-users-2026-07-04.json"
OUTPUT_ROOT = Path(sys.argv[2]) if len(sys.argv) > 2 else Path.home() / "self/human-strongest-director/raw/videos"
EXTRACT_SCRIPT = Path("/Users/zhourongchang/self/social-media-sniffer/skills/content-extractor/scripts/extract_video.py")
WHISPER_MODEL = sys.argv[3] if len(sys.argv) > 3 else "base"

def main():
    with open(JSON_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    users = data.get("users", [])
    all_notes = []
    for user in users:
        notes = user.get("notes", [])
        for note in notes:
            if note.get("type") == "video" and note.get("video", {}).get("video_url"):
                all_notes.append(note)

    print(f"共找到 {len(all_notes)} 条视频笔记")
    print(f"输出目录: {OUTPUT_ROOT}")
    print(f"Whisper 模型: {WHISPER_MODEL}")
    print()

    results = []
    for i, note in enumerate(all_notes, 1):
        note_id = note["note_id"]
        title = note.get("title", "untitled")
        video_url = note["video"]["video_url"]
        output_dir = OUTPUT_ROOT / note_id

        # 跳过已完成的
        transcript_path = output_dir / "transcript.txt"
        if transcript_path.exists():
            print(f"[{i}/{len(all_notes)}] 跳过（已存在）: {title}")
            results.append({"note_id": note_id, "title": title, "status": "skipped"})
            continue

        print(f"[{i}/{len(all_notes)}] 处理: {title}")
        print(f"  note_id: {note_id}")
        print(f"  url: {video_url[:80]}...")

        output_dir.mkdir(parents=True, exist_ok=True)

        # 调用 extract_video.py
        cmd = [
            sys.executable, str(EXTRACT_SCRIPT),
            video_url, str(output_dir),
            "--note-id", note_id,
            "--whisper-model", WHISPER_MODEL
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)

        if result.returncode == 0:
            print(f"  ✓ 完成")
            # 保存元数据
            meta = {
                "note_id": note_id,
                "title": title,
                "desc": note.get("desc", ""),
                "like_count": note.get("like_count", 0),
                "collect_count": note.get("collect_count", 0),
                "comment_count": note.get("comment_count", 0),
                "share_count": note.get("share_count", 0),
                "tags": note.get("tags", []),
                "duration": note.get("video", {}).get("duration", 0),
                "time": note.get("time", 0),
                "ip_location": note.get("ip_location", ""),
            }
            with open(output_dir / "metadata.json", "w", encoding="utf-8") as f:
                json.dump(meta, f, ensure_ascii=False, indent=2)
            results.append({"note_id": note_id, "title": title, "status": "success"})
        else:
            print(f"  ✗ 失败: {result.stderr[:200]}")
            results.append({"note_id": note_id, "title": title, "status": "failed", "error": result.stderr[:200]})

        print()

    # 汇总
    print("=== 批量提取完成 ===")
    success = sum(1 for r in results if r["status"] == "success")
    skipped = sum(1 for r in results if r["status"] == "skipped")
    failed = sum(1 for r in results if r["status"] == "failed")
    print(f"成功: {success} / 跳过: {skipped} / 失败: {failed}")

    with open(OUTPUT_ROOT / "batch_result.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()
