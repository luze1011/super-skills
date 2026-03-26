---
name: super-writing-assistant
description: Use when writing any content that requires planning, drafting, and polishing - including marketing copy, technical docs, tutorials, skills, or implementation plans. Covers the full workflow from structure to final polish. Make sure to use this skill whenever the user mentions writing, drafting, content creation, documentation, or needs help with any text-based output.
---

# Super Writing Assistant

一站式写作助手，融合规划→撰写→润色全流程。

## 核心理念

```
规划阶段 → 结构清晰，目标明确
撰写阶段 → 内容充实，风格匹配
润色阶段 → 精炼打磨，闭环验证
```

---

## 三阶段工作流

### 阶段一：规划 (Planning)

**触发条件**：内容超过500字，或需要结构化输出。

使用 `scripts/plan-outline.py` 生成大纲：

```bash
python scripts/plan-outline.py --type <营销|技术|技能|计划> --topic "<主题>"
```

**需求收集清单**：

| 内容类型 | 必问问题 |
|---------|---------|
| 营销文案 | 页面类型？目标行动？受众画像？痛点是什么？ |
| 技术文档 | 读者水平？技术栈？要解决什么问题？ |
| 教程指南 | 前置知识？预期产出？代码示例需求？ |
| 技能文档 | 触发场景？核心原则？测试验证？ |
| 实施计划 | 技术栈？文件结构？任务粒度？ |

**结构模板参考**：见 `assets/article-template.md` 和 `assets/report-template.md`

---

### 阶段二：撰写 (Drafting)

根据内容类型选择撰写策略，详见 `references/writing-styles.md`。

**快速参考**：

| 类型 | 核心原则 | 风格要点 |
|------|---------|---------|
| 营销文案 | 收益导向 | 清晰、具体、用户语言 |
| 技术文档 | 实现导向 | 深度、同行语气、完整示例 |
| 技能文档 | 触发导向 | 症状描述、原则、速查表 |
| 实施计划 | 验证导向 | 小任务、TDD、文件路径 |

**撰写工具**：

```bash
# 生成初稿
python scripts/write-draft.py --outline <大纲文件> --style <风格>
```

**模板参考**：见 `references/content-templates.md`

---

### 阶段三：润色 (Polishing)

**质量检查清单**：

- [ ] 每句话有独特价值（无重复信息）
- [ ] 无冗余形容词/副词
- [ ] 句式有变化（不单调）
- [ ] 术语使用准确

**润色工具**：

```bash
# 润色文本
python scripts/polish-text.py --input <文件> --check-all
```

**润色技巧**：

```markdown
❌ "这是一个非常重要的关键功能"
✅ "该功能..."

❌ "在当今快速发展的技术领域中"
✅ （删除）

❌ "可以帮助用户实现"
✅ "帮助用户实现" / "实现"
```

---

## 快速决策树

```
需要写什么？
├─ 营销页面/转化文案 → 收益导向、用户语言、强CTA
├─ 技术文档/教程 → 直接切入、深度解释、完整示例
├─ 技能/SKILL.md → 触发条件、核心原则、测试验证
└─ 实施计划 → 任务分解、TDD、验证步骤
```

---

## 常见错误

| 错误 | 修复 |
|------|------|
| 标题模糊 | 用具体数字/结果替代 |
| 功能堆砌 | 转化为用户收益 |
| 代码片段不完整 | 补全可运行示例 |
| description 写流程 | 只写触发条件 |
| 任务太大 | 拆分为2-5分钟小步 |
| 滥用形容词 | 删除或具体化 |
| 营销废话 | 删除"革命性"、"创新"等词 |

---

## 输出格式

完成写作后提供：

1. **内容本体**（按结构组织）
2. **关键选择说明**（为什么这样写）
3. **备选方案**（标题/CTA等提供2-3个选项）
4. **质量自检**（清单勾选结果）

---

## 参考资源

- **写作风格指南**：`references/writing-styles.md`
- **内容模板库**：`references/content-templates.md`
- **文章模板**：`assets/article-template.md`
- **报告模板**：`assets/report-template.md`