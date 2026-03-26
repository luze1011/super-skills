---
name: marketing-suite
description: "社交营销全流程套件：融合 TikTok 营销、营销策略心理学、社交媒体内容运营三大能力。覆盖内容创作→多平台发布→数据优化→自动化工作流的完整链路。"
version: "1.0.0"
author: OpenClaw
license: MIT

category: marketing
tags:
  - social-media
  - tiktok
  - content-strategy
  - marketing-psychology
  - automation
  - multi-platform
  - conversion-optimization

models:
  recommended:
    - claude-sonnet-4
    - claude-opus-4
  compatible:
    - gpt-4
    - gpt-4o

capabilities:
  - content_strategy
  - video_scripting
  - multi_platform_publishing
  - psychology_driven_copy
  - hashtag_optimization
  - analytics_tracking
  - automation_workflows
  - content_repurposing

languages:
  - en
  - zh

related_skills:
  - copywriting
  - seo-audit
  - email-sequence
  - ab-test-setup
---

# Marketing Suite - 社交营销全流程套件

融合 TikTok 营销、营销策略心理学、社交媒体内容运营三大能力，提供从内容创作到转化的完整解决方案。

---

## 🎯 套件概览

| 模块 | 能力来源 | 核心功能 |
|------|---------|---------|
| **内容引擎** | tiktok-marketing + social-content | 短视频脚本、多平台内容复用 |
| **策略大脑** | marketing-mode | 营销策略、心理学模型、转化优化 |
| **运营系统** | social-content + tiktok-marketing | 内容日历、发布优化、数据追踪 |
| **自动化** | tiktok-marketing | n8n 工作流、批量发布 |

---

# PART 1: 营销策略与心理学基础

## 营销策略框架（23 个领域精华）

### 核心思维模型

| 模型 | 应用场景 | 营销实践 |
|------|---------|---------|
| **第一性原理** | 破解行业惯例 | 不复制竞品，追问"为什么"找到根本解 |
| **Jobs to Be Done** | 产品定位 | 客户"雇佣"产品是为了完成什么任务？ |
| **帕累托法则** | 资源分配 | 找到带来 80% 结果的 20% 渠道 |
| **希克定律** | 转化优化 | 减少选择，一个 CTA 优于三个 |
| **损失厌恶** | 定价策略 | "别错过" 比"你能得到" 更有力 |
| **锚定效应** | 价格呈现 | 先展示高价，建立价格锚点 |
| **社会认同** | 信任建立 | 展示客户数量、评价、趋势指标 |

### 心理学钩子公式

```
🧠 认知型钩子：
"我发现了一个 [行业] 秘密..."
"大多数人都在 [错误做法]，但实际上..."

⚡️ 情感型钩子：
"我差点 [失败/错过]，直到..."
"3 年前我 [过去状态]，今天 [现在状态]"

🎯 价值型钩子：
"如何 [实现目标]（无需 [常见痛点]）"
"[数字] 个 [方法] 帮你 [结果]"

🔥 爆发型钩子：
"不讨好但不得不说：[大胆观点]"
"我停止 [常见做法] 后，[积极结果]"
```

---

## 内容支柱框架

### 内容支柱配置模板

```yaml
content_pillars:
  - pillar: "教育/价值"
    ratio: 30-40%
    formats: [教程, 技巧, 方法论, 框架]
    platforms: [LinkedIn, YouTube, TikTok]
    goal: 建立权威
    
  - pillar: "娱乐/互动"
    ratio: 25-30%
    formats: [趋势, 挑战, 幕后, 故事]
    platforms: [TikTok, Instagram, Twitter/X]
    goal: 扩大触达
    
  - pillar: "社交/社区"
    ratio: 20-25%
    formats: [UGC, 问答, 投票, 合创]
    platforms: [Instagram, TikTok, Facebook]
    goal: 提升互动
    
  - pillar: "推广/转化"
    ratio: 10-15%
    formats: [产品演示, 案例, 优惠]
    platforms: [LinkedIn, Instagram, TikTok]
    goal: 驱动转化
```

---

# PART 2: 内容创作引擎

## TikTok 短视频脚本框架

### Hook-Content-CTA 结构

```
┌─────────────────────────────────────────┐
│ 🪝 HOOK（0-3 秒）                        │
│ • 问题："你知道...？"                   │
│ • 惊叹："这改变了一切"                   │
│ • 清单："3 个你必须知道的..."            │
│ 必须让用户停止滑动                       │
└─────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────┐
│ 📺 CONTENT（3-50 秒）                    │
│ • 兑现 Hook 承诺                        │
│ • 一个视频一个核心信息                   │
│ • 每 3-5 秒视觉变化                      │
│ • 关键点文字叠加                         │
└─────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────┐
│ 📢 CTA（最后 2-3 秒）                    │
│ • 关注："关注获取更多..."               │
│ • 互动："评论区告诉我..."               │
│ • 分享："转发给需要的人"                 │
│ • 转化："主页链接/私信领取"              │
└─────────────────────────────────────────┘
```

### 脚本模板库

**教育类视频**：
```
[HOOK - 3s]
"这是一个大多数人不知道的 [主题] 技巧..."

[SETUP - 5s]
"我一直在 [问题] 中挣扎，直到发现了这个方法。"

[CONTENT - 20s]
"第一步：[动作 + 视觉]
第二步：[动作 + 视觉]
第三步：[动作 + 视觉]"

[PROOF - 5s]
"看看结果：[展示前后对比]"

[CTA - 3s]
"关注获取更多 [领域] 技巧！"
```

**趋势参与类**：
```
[趋势音频同步]
- 转场配合节奏点
- 48 小时内使用热门音频
- 加入独特转折

[视觉结构]
- 开场：匹配第一个节拍
- 中段：关键信息在 Hook 段
- 结尾：惊喜或反转
```

---

## 内容复用矩阵

### 一鱼多吃策略

| 源内容 | LinkedIn | Twitter/X | Instagram | TikTok |
|--------|----------|-----------|-----------|--------|
| 博客文章 | 关键洞察 + 评论链接 | 主题推文串 | 图文轮播 | 视频总结 |
| TikTok 视频 | 转载 + 专业解读 | 精彩片段 | Reels | 原发 |
| 播客访谈 | 金句卡片 | 金句推文 | Story 剪辑 | 短视频切片 |
| 客户案例 | 详细案例研究 | 成果数据 | Before/After | 见证视频 |

### 复用工作流

```
1. 创建支柱内容（博客/视频/播客）
2. 提取 3-5 个关键洞察
3. 适配各平台格式和语调
4. 一周内分批发布
5. 更新并重复使用（常青内容）
```

---

# PART 3: 多平台运营系统

## 平台策略对比

| 平台 | 最佳用途 | 发布频率 | 关键格式 | 算法偏好 |
|------|---------|---------|---------|---------|
| **LinkedIn** | B2B、思想领导 | 3-5x/周 | 轮播、故事 | 专业内容、互动评论 |
| **Twitter/X** | 实时、技术、社区 | 3-10x/天 | 推文串、热点 | 高频、热点参与 |
| **Instagram** | 视觉品牌、生活方式 | 1-2 帖 + Story/天 | Reels、轮播 | Reels 优先、Story 互动 |
| **TikTok** | 品牌认知、年轻群体 | 1-4x/天 | 短视频 | 原生内容、趋势音频 |
| **Facebook** | 社群、本地商家 | 1-2x/天 | 群组、原生视频 | 社群互动、视频 |

## 内容日历模板

### 周计划示例

| 日 | LinkedIn | Twitter/X | Instagram | TikTok |
|----|----------|-----------|-----------|--------|
| 周一 | 行业洞察 | 主题推文串 | 图文轮播 | 教程视频 |
| 周二 | 幕后故事 | 互动回复 | Story | 趋势参与 |
| 周三 | 教育内容 | 技巧推文 | Reels | 生活日常 |
| 周四 | 故事分享 | 推文串 | 教育图文 | 产品展示 |
| 周五 | 热点观点 | 互动时间 | Story | 挑战参与 |

### 批量创作流程（每周 2-3 小时）

```
1. 回顾内容支柱主题
2. 撰写 5 条 LinkedIn 帖子
3. 撰写 3 条推文串 + 日常推文
4. 创作 Instagram 轮播 + Reel 创意
5. 规划 TikTok 脚本
6. 全部排期发布
7. 预留实时互动时间
```

---

# PART 4: TikTok 专项优化

## 标签策略

### 标签混合公式

```yaml
hashtag_strategy:
  total: 5-7 标签（TikTok 最优）
  
  mix:
    - 细分领域标签: 2-3 个
      examples: ["#创业技巧", "#营销方法"]
      触达: 10万-100万观看
      
    - 热门趋势标签: 1-2 个
      examples: ["#fyp", "#viral", "#trending"]
      触达: 10亿+观看
      
    - 品牌标签: 1 个
      examples: ["#你的品牌名", "#你的活动"]
      触达: 自定义
      
    - 社区标签: 1 个
      examples: ["#tiktokmademedoit", "#learnontiktok"]
      触达: 1000万-1亿观看
```

## 发布优化

### 最佳发布时间

| 受众地区 | 最佳时间 | 最佳日期 |
|---------|---------|---------|
| 中国 | 7:00, 12:00, 21:00 | 周一、周三、周六 |
| 美国 | 7:00, 12:00, 19:00 EST | 周二、周四、周五 |
| 英国 | 7:00, 12:00, 22:00 GMT | 周三、周四、周五 |
| 全球 | 7:00, 22:00 UTC | 周四、周五、周六 |

### 发布频率建议

```yaml
recommended_frequency:
  minimum: 1 视频/天
  optimal: 2-3 视频/天
  maximum: 5 视频/天
  
consistency_rules:
  - 每天相同时间段发布，培养受众习惯
  - 不要超过 24 小时不发布
  - 3 个/天后，质量 > 数量
  - 测试不同时间 2 周后再决定
```

---

# PART 5: 数据分析与优化

## 关键指标追踪

| 指标 | 目标值 | 低于目标时的行动 |
|------|--------|-----------------|
| **完播率** | >50% | 优化 Hook |
| **互动率** | >5% | 加强 CTA |
| **分享率** | >1% | 创造分享价值 |
| **关注率** | >2% | 强化价值主张 |
| **主页访问** | >10%观看量 | 清晰的 CTA |

## 周度分析模板

```markdown
# 营销周报

## 概览
- 发布数量：21 个
- 总观看：150,000
- 新增粉丝：500
- 互动率：6.2%

## 表现最佳内容
| 内容 | 观看 | 点赞 | 评论 | 分享 |
|------|------|------|------|------|
| "3 个效率技巧" | 45K | 3.2K | 234 | 567 |
| "周一早晨 POV" | 38K | 2.8K | 189 | 423 |

## 内容分析
- 最佳支柱：教育类（平均 25K 观看）
- 最佳发布时间：19:00（2倍互动）
- 最佳 Hook 类型：问题格式

## 优化建议
1. 增加教程内容（40% → 50%）
2. 调整发布时间到 19:00
3. 更多使用问题型 Hook
4. 参与趋势音频 X
```

---

# PART 6: 自动化工作流

## n8n 自动化配置

### 工作流 1：AI 内容生成管道

```
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│ Google Sheet │───▶│ OpenAI       │───▶│ ElevenLabs   │
│ (创意库)     │    │ (脚本生成)   │    │ (配音)       │
└──────────────┘    └──────────────┘    └──────────────┘
                                               │
┌──────────────┐    ┌──────────────┐    ┌──────┴───────┐
│ TikTok       │◀───│ 视频编辑     │◀───│ 图像生成     │
│ (发布)       │    │ (合成)       │    │ (视觉素材)   │
└──────────────┘    └──────────────┘    └──────────────┘
```

**n8n 配置**：
```yaml
workflow: "AI TikTok 内容生成器"

nodes:
  1. trigger:
      type: schedule
      cron: "0 9 * * *"  # 每天 9:00
  
  2. get_idea:
      type: google_sheets
      action: get_next_unused_row
      sheet: "内容创意"
  
  3. generate_script:
      type: openai
      model: gpt-4
      prompt: |
        为以下创意创建 TikTok 脚本：{idea}
        格式：Hook (3s) + Content (20s) + CTA (3s)
        风格：轻松、吸引人、带文字叠加
  
  4. generate_voiceover:
      type: elevenlabs
      voice: "young_professional"
      script: "{script}"
  
  5. generate_visuals:
      type: dalle
      prompts: "{visual_descriptions}"
  
  6. create_video:
      type: video_editor
      template: "tiktok_vertical"
      assets: [voiceover, visuals, captions]
  
  7. publish:
      type: tiktok
      caption: "{generated_caption}"
      hashtags: "{hashtags}"
      schedule: "{optimal_time}"
  
  8. update_tracker:
      type: google_sheets
      action: mark_as_published
```

### 工作流 2：多平台发布

```yaml
workflow: "发布到 TikTok + Instagram Reels + YouTube Shorts"

trigger:
  type: google_drive
  event: new_video_uploaded
  folder: "/待发布"

actions:
  1. detect_video:
      get_metadata: [duration, aspect_ratio, filename]
  
  2. generate_captions:
      openai_prompt: |
        为此视频创建平台专属文案：{title}
        - TikTok：轻松、标签多
        - Instagram：稍长、表情丰富
        - YouTube：描述性、关键词优化
  
  3. parallel_publish:
      - tiktok:
          caption: "{tiktok_caption}"
          hashtags: ["#fyp", "#viral", "{niche_tags}"]
      
      - instagram:
          type: reel
          caption: "{instagram_caption}"
          hashtags: "{instagram_tags}"
      
      - youtube:
          type: short
          title: "{youtube_title}"
          description: "{youtube_description}"
  
  4. track_in_airtable:
      base: "内容追踪"
      fields: [video_url, platforms, publish_time, status]
  
  5. notify_slack:
      channel: "#content-published"
      message: "视频已发布到所有平台：{title}"
```

---

# PART 7: 实战模板库

## 互动策略

### 每日互动流程（30 分钟）

```
1. 回复自己帖子的所有评论（5 分钟）
2. 评论 5-10 个目标账号的帖子（15 分钟）
3. 分享/转发并添加见解（5 分钟）
4. 给新连接发 2-3 条私信（5 分钟）
```

### 高质量评论公式

```
❌ 低质量："好文章！"
✅ 高质量：
  - 添加新见解
  - 分享相关经验
  - 提出有深度的问题
  - 尊重地表达不同观点
```

## 内容创意生成器

### 创意触发问题

```
1. 客户最常问的 5 个问题是什么？
2. 你行业最大的误解是什么？
3. 有什么"反直觉"的真相？
4. 最近的一次失败教会了你什么？
5. 如果重来一次，你会怎么做？
6. 你的"秘密武器"是什么？
7. 新手最容易犯的错误有哪些？
8. 你最想打破的行业规则是什么？
9. 你的日常流程是什么样的？
10. 你是如何开始的？
```

---

# 快速参考

## 营销挑战 → 解决方案

| 挑战 | 起点 |
|------|------|
| 互动低 | 测试新 Hook、调整发布时间、增加互动 |
| 触达下降 | 避免帖子内放外链、提高频率、更多视频内容 |
| 转化差 | 优化 CTA、强化价值主张、简化路径 |
| 没灵感 | 复用高表现内容、分析竞品、客户问题 |
| 没时间 | 批量创作、自动化工作流、内容复用 |

## 平台选择指南

| 目标 | 首选平台 |
|------|---------|
| B2B 潜客 | LinkedIn |
| 品牌认知 | TikTok + Instagram |
| 实时互动 | Twitter/X |
| 社群建设 | Facebook Groups |
| 长期 SEO | YouTube + 博客 |

---

## 使用说明

**当你需要帮助时，请提供以下信息：**

### 关于目标
- 主要目标是什么？（品牌认知、潜客、流量、社区）
- 希望用户采取什么行动？
- 建立个人品牌还是公司品牌？

### 关于受众
- 目标受众是谁？
- 他们活跃在哪些平台？
- 他们喜欢什么内容？

### 关于现状
- 当前发布频率？
- 有哪些现有内容可复用？
- 过去什么内容表现好？
- 每周可投入多少时间？

---

## 相关技能

- **copywriting**: 长文案创作
- **seo-audit**: 技术和页面 SEO 诊断
- **email-sequence**: 邮件培育序列
- **ab-test-setup**: A/B 测试统计设计
- **analytics-tracking**: 数据追踪基建
- **page-cro**: 落地页优化

---

*Marketing Suite - 融合社交营销全流程*