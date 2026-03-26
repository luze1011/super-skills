# 写作风格指南

本文档详细说明不同内容类型的写作风格和技巧。

---

## 目录

1. [营销文案风格](#营销文案风格)
2. [技术文档风格](#技术文档风格)
3. [技能文档风格](#技能文档风格)
4. [实施计划风格](#实施计划风格)
5. [通用润色技巧](#通用润色技巧)

---

## 营销文案风格

### 核心原则

| 原则 | 示例 |
|------|------|
| **清晰胜于聪明** | "快速生成报告" > "革命性的数据处理范式" |
| **收益胜于功能** | "节省每周4小时" > "支持自动化" |
| **具体胜于模糊** | "从4小时减到15分钟" > "大幅提升效率" |
| **用户语言** | 用客户的原话，不用公司术语 |

### 标题公式

```
✅ {达成结果} 无需 {痛点}
✅ 为{受众}打造的{品类}
✅ 再也不用{不愉快经历}
✅ {直击痛点的问题}
```

**示例**：
- ✅ "无需写代码，快速构建数据看板"
- ✅ "为产品经理打造的需求管理工具"
- ✅ "再也不用手动复制粘贴数据"
- ✅ "如何让团队协作不再混乱？"

### CTA 公式

```
✅ [动词] + [得到什么] + [限定词]
```

**示例**：
- ✅ "开始免费试用" / "获取完整指南" / "立即加入 10000+ 用户"
- ❌ "提交" / "了解更多" / "点击这里"

### 营销文案结构

```
标题（价值主张）
    ↓
副标题（具体化）
    ↓
CTA（主要行动号召）
    ↓
社会证明（用户评价/数据）
    ↓
痛点描述
    ↓
解决方案/收益
    ↓
工作原理（可选）
    ↓
异议处理（可选）
    ↓
最终CTA
```

### 常见错误

| 错误 | 修复 |
|------|------|
| 标题模糊 | 用具体数字/结果替代 |
| 功能堆砌 | 转化为用户收益 |
| 使用公司术语 | 用用户的原话替代 |
| CTA不明确 | 明确行动和收益 |
| 空洞形容词 | 删除"革命性"、"创新"等词 |

---

## 技术文档风格

### 核心原则

1. **直接切入技术内容**：避免泛泛介绍
2. **用同行对话语气**：不要教科书式
3. **解释"为什么"**：不只是"怎么做"
4. **一个优秀示例胜过多个平庸示例**

### 代码示例要求

```markdown
✅ 完整可运行，不是片段
✅ 注释解释"为什么"而非"是什么"
✅ 标注文件位置
✅ 读者可直接改编使用
```

**示例**：

```python
# ❌ 不好的示例
def process_data(data):
    return data.transform()  # 转换数据

# ✅ 好的示例
def process_user_actions(actions: list[dict]) -> pd.DataFrame:
    """
    将用户行为日志转换为时序特征
    
    Args:
        actions: 原始行为日志，每条包含 user_id, action, timestamp
    
    Returns:
        按用户聚合的特征 DataFrame，包含 session_count, avg_actions_per_session
    
    Why: 下游模型需要时序特征，而非原始日志
    File: src/features/user_actions.py
    """
    df = pd.DataFrame(actions)
    # 按用户分组计算 session 数量（30分钟间隔为一次 session）
    df['session'] = (df['timestamp'].diff() > pd.Timedelta('30min')).cumsum()
    return df.groupby('user_id').agg(
        session_count=('session', 'nunique'),
        avg_actions_per_session=('action', 'count')
    )
```

### 技术文档结构

```
概述（1-2句说明要解决什么问题）
    ↓
前置条件（需要什么环境/知识）
    ↓
核心概念（关键术语和原理）
    ↓
实现步骤（带完整代码示例）
    ↓
常见问题（FAQ）
    ↓
进阶话题（可选）
```

### 避免

```markdown
❌ 滥用形容词："关键"、"重要"、"强大"
❌ 陈词滥调："在当今的技术领域..."
❌ 无实质的列表：pros/cons/通用场景
❌ 代码片段不完整
❌ 只说"怎么做"，不说"为什么"
```

---

## 技能文档风格

### SKILL.md 结构

```markdown
---
name: skill-name-with-hyphens
description: Use when [具体触发条件和症状]
---

# Skill Name

## Overview
核心原则（1-2句）

## When to Use
触发场景（症状、情境）

## Core Pattern
Before/After 对比

## Quick Reference
速查表/决策树

## Implementation
代码或链接

## Common Mistakes
常见错误 + 修复
```

### 描述字段铁律

```markdown
✅ 只写触发条件，不写工作流程
✅ 以 "Use when..." 开头
✅ 第三人称
✅ 包含症状、错误信息、具体场景

❌ 描述工作流程
❌ 使用第一人称
❌ 缺少具体触发场景
```

**示例**：

```yaml
# ❌ 错误
description: A tool that helps you write better marketing copy by following a step-by-step process.

# ✅ 正确
description: Use when writing marketing copy, landing pages, or conversion-focused content. Triggers for product descriptions, ad copy, email campaigns, and any text aimed at driving user action.
```

---

## 实施计划风格

### 任务模板

```markdown
### Task N: [组件名]

**Files:**
- Create: `path/to/new.py`
- Modify: `path/to/existing.py:123-145`
- Test: `tests/path/test.py`

- [ ] **Step 1: Write the failing test**
- [ ] **Step 2: Run test to verify it fails**
- [ ] **Step 3: Write minimal implementation**
- [ ] **Step 4: Run test to verify it passes**
- [ ] **Step 5: Commit**
```

### 核心原则

1. **小任务**：每步 2-5 分钟可完成
2. **独立验证**：每步有明确的验证方式
3. **TDD 流程**：先写测试，再写实现
4. **文件路径明确**：标注涉及的文件和行号

### 实施计划结构

```
目标陈述（一句话）
    ↓
架构概述（系统设计）
    ↓
技术栈（使用的工具）
    ↓
文件清单（涉及的所有文件）
    ↓
任务分解（每步 2-5 分钟）
    ↓
验证步骤（如何验证完成）
    ↓
提交节点（何时提交代码）
```

---

## 通用润色技巧

### 删减冗余

```markdown
❌ "这是一个非常重要的关键功能"
✅ "该功能..."

❌ "在当今快速发展的技术领域中"
✅ （删除）

❌ "对...进行了优化"
✅ "优化了..."
```

### 强化动词

```markdown
❌ "可以帮助用户实现"
✅ "帮助用户实现" / "实现"

❌ "对...进行分析"
✅ "分析..."
```

### 具体化

```markdown
❌ "提升用户体验"
✅ "将加载时间从5秒降至1秒"

❌ "大幅提升效率"
✅ "从每周4小时减到15分钟"
```

### 句式变化

```markdown
❌ 我们提供了... 我们实现了... 我们支持...
✅ 提供了... 实现了... 支持...（省略主语，避免重复）

❌ 该功能可以帮助... 该工具可以简化... 该平台可以优化...
✅ 该功能帮助... 该工具简化... 该平台优化...（删除"可以"）
```

---

## 验证闭环

### 营销文案验证

- [ ] 读者能否一句话说出价值主张？
- [ ] CTA 是否明确行动和收益？
- [ ] 是否使用了用户语言？
- [ ] 是否避免了空洞形容词？

### 技术文档验证

- [ ] 读者能否按教程实现功能？
- [ ] 代码示例能否直接运行？
- [ ] 是否解释了技术决策的原因？
- [ ] 文件位置是否标注清晰？

### 技能文档验证

- [ ] 新 agent 能否找到并正确使用？
- [ ] description 是否只含触发条件？
- [ ] 是否包含常见错误案例？
- [ ] 是否有速查表或决策树？

### 实施计划验证

- [ ] 每步是否独立可验证？
- [ ] 新工程师能否理解并执行？
- [ ] 是否遵循 TDD 流程？
- [ ] 文件路径是否明确？