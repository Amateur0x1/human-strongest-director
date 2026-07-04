---
name: human-strongest-director
description: 把小红书博主「人类最强编导」的编导方法论持续蒸馏为可复用的 playbook。每当他发一期新视频，就提取视频素材（ffmpeg 截帧 + whisper 转录），分析其编导手法、内容策略和底层逻辑，更新 playbook 并归档一期 episode 分析。当用户提到"蒸馏编导""更新编导 skill""人类最强编导又更新了""分析他的新视频"时使用。
---

# 人类最强编导 — 编导方法论蒸馏 Skill

## 定位

这个 Skill 做一件事：把「人类最强编导」每一期视频里的编导脑、内容策略、底层逻辑提取出来，累积成一套可复用的 playbook。

它不是看视频写总结，而是**逆向工程一个顶级编导的决策树**——他为什么这样开头、为什么用白板、为什么选这个选题、为什么在这个节奏切镜头。每一期都会往 playbook 里增加新的方法论条目或修正既有条目。

## 博主画像

- **账号名**：人类最强编导
- **平台**：小红书
- **人设**：戴蜘蛛侠头套的匿名编导，自称"全国收入高的编导不超过三个"
- **内容形式**：2-5 分钟深度口播干货，白板+手机拍摄，快速剪辑无气口
- **核心主张**：把同行付费内容免费做出来，"我不要卖课割韭菜，我要桃李满天下"
- **起号成绩**：5 条视频 5 万粉，一周百万播放
- **视觉标记**：蜘蛛侠头套、白板手书、极简字幕

## 目录结构

```
human-strongest-director/
├── SKILL.md                  ← 你正在读的文件（工作流定义）
├── playbook.md               ← 编导方法论累积库（持续更新）
├── episodes/                 ← 每期视频的深度分析
│   ├── ep01-全国比我收入高的编导不超过三个.md
│   ├── ep02-人类最强编导一条视频起号1.4w.md
│   ├── ...
│   └── epNN-<标题>.md
├── raw/
│   └── videos/               ← 原始素材（视频、截帧、转录）
│       └── <note_id>/
│           ├── video.mp4
│           ├── frames/
│           ├── audio.wav
│           ├── transcript.txt
│           └── metadata.json
└── scripts/
    └── batch_extract.py      ← 批量提取脚本
```

## 前置依赖

- `ffmpeg` — 视频截帧和音频提取
- `whisper` (openai-whisper CLI) — 语音转文字
- `Python 3.8+` — 脚本运行

提取脚本复用 social-media-sniffer 项目的 `content-extractor/scripts/extract_video.py`。

## 工作流程

### 触发条件

用户说以下任何一种时激活：
- "人类最强编导又更新了" + 提供 XHS JSON 文件
- "蒸馏编导" / "更新编导 skill"
- "分析他的新视频"
- 直接提供一个包含该博主视频数据的 JSON 文件

### Step 1：素材提取

用户提供 XHS 导出的 JSON 文件后：

1. 解析 JSON，筛选出视频类笔记
2. 对每条新视频（playbook.md 中未记录的 note_id）执行：
   - 下载视频 → `ffmpeg -vf fps=1` 每秒截帧
   - 提取音频 → `ffmpeg -vn -acodec pcm_s16le -ar 16000 -ac 1`
   - whisper 转录 → `whisper audio.wav --model base --language zh`
3. 保存到 `raw/videos/<note_id>/`
4. 同时保存 `metadata.json`（标题、点赞、收藏、评论、分享、标签、时长）

```bash
python scripts/batch_extract.py <json_file> <output_dir> [whisper_model]
```

### Step 2：单期深度分析

对每条新视频，创建一个 episode 文件 `episodes/ep<NN>-<标题简称>.md`。

分析维度（详见 episode 模板）：

1. **内容策略** — 选题逻辑、目标受众、核心论点
2. **编导手法** — 开头钩子、节奏控制、信息密度、视觉设计
3. **底层逻辑** — 提炼可复用的方法论原则
4. **金句提取** — 可截图传播的句子
5. **评论洞察** — 评论区反映的受众真实需求
6. **playbook 增量** — 本期新增或修正了哪些方法论条目

### Step 3：更新 playbook

每分析完一期，将新发现的方法论条目合并到 `playbook.md` 中：

- 新条目：追加到对应章节
- 修正：更新已有条目，标注来源 episode
- 矛盾：如果新内容与旧条目矛盾，保留两者并标注演变

### Step 4：归档

将 episode 文件保存到 `episodes/` 目录，文件名格式：`ep<两位序号>-<标题关键词>.md`

## Episode 分析模板

```markdown
# EP<NN> — <标题>

## 元数据
- note_id: <id>
- 发布时间: <date>
- 时长: <duration>s
- 数据: 赞<like> 收藏<collect> 评论<comment> 分享<share>
- 标签: <tags>

## 逐段拆解
（按视频段落，逐段分析内容和编导手法）

## 编导手法分析
### 开头钩子
### 节奏控制
### 信息密度
### 视觉设计
### 结尾设计

## 底层逻辑提炼
（本期可复用的方法论原则）

## 金句
> "..."
> "..."

## 评论洞察
（评论区高赞反馈反映的受众需求）

## Playbook 增量
- 新增: ...
- 修正: ...
```

## 注意事项

- whisper 转录可能有错别字，分析时结合截帧画面交叉验证
- 视频 URL 有时效签名，过期需用户重新用扩展抓取
- playbook.md 是累积式的，只增不减（矛盾时标注演变，不删除旧条目）
- 每期分析聚焦"可复用的编导决策"，不是写内容摘要
