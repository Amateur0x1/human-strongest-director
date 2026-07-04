# human-strongest-director

把小红书博主「人类最强编导」的编导方法论持续蒸馏为可复用的 playbook。

## 怎么用

1. 用 social-media-sniffer 浏览器扩展抓取博主的 XHS 数据 JSON
2. 运行批量提取脚本下载视频、截帧、转录
3. 每条视频生成一个 episode 分析文件
4. 将新发现的方法论合并到 playbook.md

## 快速开始

```bash
# 批量提取视频素材（下载 + 截帧 + whisper 转录）
python scripts/batch_extract.py <xhs-json-file> <output-dir> [whisper-model]

# 然后让 AI 按照 SKILL.md 中的工作流进行分析和 playbook 更新
```

## 目录结构

```
├── SKILL.md          # 工作流定义和 episode 分析模板
├── playbook.md       # 编导方法论累积库（核心产出）
├── episodes/         # 每期视频的深度分析
├── raw/videos/       # 原始素材（视频、截帧、转录）
└── scripts/          # 批量提取脚本
```

## 当前状态

- 已蒸馏 episode 数：11（EP01-EP11，全部覆盖）
- playbook 章节：12 章
- 原始视频数：11 条（全部转录完成）
- 数据来源：2026-07-04 导出

## 依赖

- ffmpeg（视频截帧 + 音频提取）
- whisper / openai-whisper（语音转文字）
- Python 3.8+
