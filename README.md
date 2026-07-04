# human-strongest-director

把小红书博主「人类最强编导」的编导脑蒸馏为 AI 可执行的知识体。

## 核心文件

`SKILL.md` — 读取这个文件，AI 就化身为人类最强编导。包含从 11 期视频中蒸馏的全部编导方法论：内容哲学、爆款逻辑、起号 SOP、IP 打造、平台策略、剪辑节奏、商业化全链路。结尾是 episodes + playbook 的索引。

`playbook.md` — 12 章方法论累积库，持续更新。

`episodes/` — 11 期视频的逐期深度分析，每期包含逐段拆解、编导手法、底层逻辑、金句、评论洞察。

`raw/` — 原始 XHS JSON 数据 + 每条视频的 whisper 转录文本和元数据。

## 当前状态

- 已蒸馏 episode 数：11（EP01-EP11，全部覆盖）
- playbook 章节：12 章
- 原始视频数：11 条（全部转录完成）
- 数据来源：2026-07-04 导出

## 更新方式

当「人类最强编导」发布新视频时：
1. 用 social-media-sniffer 浏览器扩展抓取 XHS JSON
2. 用 ffmpeg 截帧 + whisper 转录提取素材
3. 创建 episode 分析文件
4. 更新 playbook.md 和 SKILL.md

## 依赖

- ffmpeg（视频截帧 + 音频提取）
- whisper / openai-whisper（语音转文字）
