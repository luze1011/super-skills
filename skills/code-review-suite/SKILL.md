---
name: code-review-suite
description: 完整的代码审查工作流套件，支持请求审查、接收反馈、重构改进的端到端流程。适用于任务完成后验证、合并前检查、代码质量提升等场景。
license: MIT
version: 1.0.0
keywords:
  - code-review
  - refactoring
  - quality-assurance
  - best-practices
---

# Code Review Suite

完整的代码审查工作流套件，覆盖从请求审查到实施改进的全流程。

## 核心原则

1. **审查前置** - 问题越早发现，修复成本越低
2. **技术严谨** - 验证优先，避免盲目实施
3. **行为保持** - 重构不改变外部行为
4. **小步快跑** - 每次只做一件事，测试验证

---

## 完整工作流

```
┌─────────────────┐
│  1. 准备阶段     │  确保有测试覆盖
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  2. 请求审查     │  提交代码，获取反馈
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  3. 接收反馈     │  理解、验证、评估
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  4. 实施改进     │  重构、修复、测试
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  5. 验证闭环     │  测试通过，提交变更
└─────────────────┘
```

---

## 第一阶段：请求代码审查

### 何时必须审查

| 场景 | 优先级 | 说明 |
|------|--------|------|
| 子代理开发中每个任务后 | 🔴 强制 | 防止问题累积 |
| 完成主要功能后 | 🔴 强制 | 确保功能正确 |
| 合并到主分支前 | 🔴 强制 | 最后一道防线 |
| 遇到困难时 | 🟡 推荐 | 获取新视角 |
| 重构前 | 🟡 推荐 | 建立基线 |
| 修复复杂 bug 后 | 🟡 推荐 | 确认修复正确 |

### 审查请求流程

**步骤 1：准备 Git SHA**
```bash
BASE_SHA=$(git rev-parse HEAD~1)  # 或 origin/main
HEAD_SHA=$(git rev-parse HEAD)
```

**步骤 2：构造审查上下文**
```
WHAT_WAS_IMPLEMENTED: 实现了什么
PLAN_OR_REQUIREMENTS: 应该做什么
BASE_SHA: 起始提交
HEAD_SHA: 结束提交
DESCRIPTION: 简要描述
```

**步骤 3：处理反馈**
- 🔴 Critical → 立即修复
- 🟠 Important → 继续前修复
- 🟢 Minor → 记录后续处理
- ⚠️ 反馈错误 → 技术推理反驳

### 示例

```
完成：任务 2 - 添加验证函数

BASE_SHA=$(git log --oneline | grep "Task 1" | head -1 | awk '{print $1}')
HEAD_SHA=$(git rev-parse HEAD)

审查上下文：
- WHAT: 会话索引的验证和修复函数
- PLAN: docs/superpowers/plans/deployment-plan.md 的 Task 2
- BASE: a7981ec
- HEAD: 3df7661

审查结果：
  优点: 架构清晰，真实测试
  问题:
    🟠 缺少进度指示器
    🟢 魔法数字 100（报告间隔）
  评估: 可以继续

行动: 修复进度指示器 → 继续任务 3
```

---

## 第二阶段：接收审查反馈

### 核心原则

> **验证优先，技术严谨，避免表演性同意**

### 响应模式

```
收到反馈 →
  1. READ: 完整阅读，不急于反应
  2. UNDERSTAND: 用自己的话重述（或提问）
  3. VERIFY: 对照代码库验证
  4. EVALUATE: 对本代码库技术上合理吗？
  5. RESPOND: 技术确认或理由反驳
  6. IMPLEMENT: 逐项实施，逐项测试
```

### 禁止的响应

| ❌ 禁止 | ✅ 正确做法 |
|---------|------------|
| "你完全正确！" | 重述技术要求 |
| "好观点！" | 验证后行动 |
| "让我立即实施" | 先验证建议 |
| 过度感谢 | 直接修复即可 |

### 处理不清楚的反馈

```
如果任何项目不清楚：
  停止 - 不要实施任何内容
  对不清楚的项目请求澄清

原因：项目可能相关联。部分理解 = 错误实施。
```

**示例：**
```
反馈: "修复 1-6"
理解 1,2,3,6。不清楚 4,5。

❌ 错误: 实施 1,2,3,6，稍后问 4,5
✅ 正确: "我理解项目 1,2,3,6。需要在实施前澄清 4 和 5。"
```

### 按来源处理

#### 来自用户/主管
- **可信** - 理解后实施
- **范围不清楚时仍需询问**
- **无需表演性同意**
- **直接行动或技术确认**

#### 来自外部审查者
```
实施前检查：
  1. 对本代码库技术正确吗？
  2. 破坏现有功能吗？
  3. 当前实现有原因吗？
  4. 所有平台/版本都能工作吗？
  5. 审查者理解完整上下文吗？

如果建议似乎错误：
  用技术推理反驳

如果无法轻松验证：
  说明："没有 [X] 我无法验证。我应该 [调查/询问/继续]？"

如果与用户/主管的先前决定冲突：
  先停止并与用户/主管讨论
```

### YAGNI 检查

```
如果审查者建议"正确实现"：
  grep 代码库查找实际使用

  如果未使用: "此端点未被调用。移除它（YAGNI）？"
  如果已使用: 然后正确实现
```

### 何时反驳

| 情况 | 说明 |
|------|------|
| 破坏现有功能 | 技术上不正确 |
| 审查者缺乏完整上下文 | 信息不对称 |
| 违反 YAGNI | 未使用的功能 |
| 技术上不适合此技术栈 | 平台限制 |
| 存在遗留/兼容性原因 | 历史约束 |
| 与架构决定冲突 | 需要升级讨论 |

**如何反驳：**
- 使用技术推理，而非防御性
- 提出具体问题
- 引用工作的测试/代码
- 如果是架构问题，涉及用户/主管

### 正确反馈的确认方式

```
✅ "已修复。[简要描述变更]"
✅ "好发现 - [具体问题]。已在 [位置] 修复。"
✅ [直接修复并在代码中展示]

❌ "你完全正确！"
❌ "好观点！"
❌ "感谢发现那个！"
❌ 任何感谢表达
```

**为何不感谢：** 行动胜于言。直接修复即可。代码本身表明你听到了反馈。

---

## 第三阶段：重构改进

### 重构原则

| 原则 | 说明 |
|------|------|
| 行为保持 | 重构不改变代码做什么，只改变怎么做 |
| 小步骤 | 微小变更，每步测试 |
| 版本控制友好 | 每个安全状态前后提交 |
| 测试必不可少 | 没有测试不是重构，是编辑 |
| 一次一件事 | 不要混合重构和功能变更 |

### 何时不重构

- 工作正常且不再修改的代码（如果不坏...）
- 没有测试的关键生产代码（先添加测试）
- 紧迫的截止期限下
- "仅仅因为" - 需要明确目的

---

## 常见代码异味与修复

### 1. 过长函数/方法

```diff
# 坏：200 行的函数
- async function processOrder(orderId) {
-   // 50 行：获取订单
-   // 30 行：验证订单
-   // 40 行：计算价格
-   // 30 行：更新库存
-   // 20 行：创建装运
-   // 30 行：发送通知
- }

# 好：分解为专注的函数
+ async function processOrder(orderId) {
+   const order = await fetchOrder(orderId);
+   validateOrder(order);
+   const pricing = calculatePricing(order);
+   await updateInventory(order);
+   const shipment = await createShipment(order);
+   await sendNotifications(order, pricing, shipment);
+   return { order, pricing, shipment };
+ }
```

### 2. 重复代码

```diff
# 坏：多处相同逻辑
- function calculateUserDiscount(user) {
-   if (user.membership === 'gold') return user.total * 0.2;
-   if (user.membership === 'silver') return user.total * 0.1;
-   return 0;
- }
-
- function calculateOrderDiscount(order) {
-   if (order.user.membership === 'gold') return order.total * 0.2;
-   if (order.user.membership === 'silver') return order.total * 0.1;
-   return 0;
- }

# 好：提取公共逻辑
+ function getMembershipDiscountRate(membership) {
+   const rates = { gold: 0.2, silver: 0.1 };
+   return rates[membership] || 0;
+ }
+
+ function calculateUserDiscount(user) {
+   return user.total * getMembershipDiscountRate(user.membership);
+ }
+
+ function calculateOrderDiscount(order) {
+   return order.total * getMembershipDiscountRate(order.user.membership);
+ }
```

### 3. 过大的类/模块

```diff
# 坏：上帝对象
- class UserManager {
-   createUser() { /* ... */ }
-   updateUser() { /* ... */ }
-   deleteUser() { /* ... */ }
-   sendEmail() { /* ... */ }
-   generateReport() { /* ... */ }
-   handlePayment() { /* ... */ }
-   validateAddress() { /* ... */ }
-   // 50 多个方法...
- }

# 好：单一职责
+ class UserService {
+   create(data) { /* ... */ }
+   update(id, data) { /* ... */ }
+   delete(id) { /* ... */ }
+ }
+
+ class EmailService {
+   send(to, subject, body) { /* ... */ }
+ }
+
+ class ReportService {
+   generate(type, params) { /* ... */ }
+ }
+
+ class PaymentService {
+   process(amount, method) { /* ... */ }
+ }
```

### 4. 过长参数列表

```diff
# 坏：参数过多
- function createUser(email, password, name, age, address, city, country, phone) {
-   /* ... */
- }

# 好：分组相关参数
+ interface UserData {
+   email: string;
+   password: string;
+   name: string;
+   age?: number;
+   address?: Address;
+   phone?: string;
+ }
+
+ function createUser(data: UserData) {
+   /* ... */
+ }
```

### 5. 魔法数字/字符串

```diff
# 坏：未解释的值
- if (user.status === 2) { /* ... */ }
- const discount = total * 0.15;
- setTimeout(callback, 86400000);

# 好：命名常量
+ const UserStatus = {
+   ACTIVE: 1,
+   INACTIVE: 2,
+   SUSPENDED: 3
+ } as const;
+
+ const DISCOUNT_RATES = {
+   STANDARD: 0.1,
+   PREMIUM: 0.15,
+   VIP: 0.2
+ } as const;
+
+ const ONE_DAY_MS = 24 * 60 * 60 * 1000;
+
+ if (user.status === UserStatus.INACTIVE) { /* ... */ }
+ const discount = total * DISCOUNT_RATES.PREMIUM;
+ setTimeout(callback, ONE_DAY_MS);
```

### 6. 嵌套条件

```diff
# 坏：箭头代码
- function process(order) {
-   if (order) {
-     if (order.user) {
-       if (order.user.isActive) {
-         if (order.total > 0) {
-           return processOrder(order);
-         } else {
-           return { error: 'Invalid total' };
-         }
-       } else {
-         return { error: 'User inactive' };
-       }
-     } else {
-       return { error: 'No user' };
-     }
-   } else {
-     return { error: 'No order' };
-   }
- }

# 好：保护子句 / 早期返回
+ function process(order) {
+   if (!order) return { error: 'No order' };
+   if (!order.user) return { error: 'No user' };
+   if (!order.user.isActive) return { error: 'User inactive' };
+   if (order.total <= 0) return { error: 'Invalid total' };
+   return processOrder(order);
+ }
```

### 7. 死代码

```diff
# 坏：未使用的代码
- function oldImplementation() { /* ... */ }
- const DEPRECATED_VALUE = 5;
- import { unusedThing } from './somewhere';
- // 注释掉的代码
- // function oldCode() { /* ... */ }

# 好：删除它
+ // 删除未使用的函数、导入和注释代码
+ // 如果需要，git 历史中有记录
```

---

## 安全重构流程

```
1. 准备
   - 确保存在测试（缺失则编写）
   - 提交当前状态
   - 创建功能分支

2. 识别
   - 找到要解决的代码异味
   - 理解代码做什么
   - 计划重构

3. 重构（小步骤）
   - 做一个小变更
   - 运行测试
   - 测试通过则提交
   - 重复

4. 验证
   - 所有测试通过
   - 如需手动测试
   - 性能不变或改进

5. 清理
   - 更新注释
   - 更新文档
   - 最终提交
```

---

## 重构检查清单

### 代码质量
- [ ] 函数小（< 50 行）
- [ ] 函数只做一件事
- [ ] 无重复代码
- [ ] 描述性名称（变量、函数、类）
- [ ] 无魔法数字/字符串
- [ ] 移除死代码

### 结构
- [ ] 相关代码在一起
- [ ] 清晰的模块边界
- [ ] 依赖单向流动
- [ ] 无循环依赖

### 类型安全
- [ ] 所有公共 API 定义类型
- [ ] 无 `any` 类型（除非有理由）
- [ ] 可空类型显式标记

### 测试
- [ ] 重构代码有测试
- [ ] 测试覆盖边缘情况
- [ ] 所有测试通过

---

## 常见重构操作

| 操作 | 说明 |
|------|------|
| 提取方法 | 将代码片段转为方法 |
| 提取类 | 移动行为到新类 |
| 提取接口 | 从实现创建接口 |
| 内联方法 | 将方法体移回调用者 |
| 内联类 | 将类行为移到调用者 |
| 上拉方法 | 移动方法到超类 |
| 下推方法 | 移动方法到子类 |
| 重命名方法/变量 | 改善清晰度 |
| 引入参数对象 | 分组相关参数 |
| 用多态替换条件 | 使用多态代替 switch/if |
| 用常量替换魔法数字 | 命名常量 |
| 分解条件 | 打破复杂条件 |
| 合并条件 | 合并重复条件 |
| 用保护子句替换嵌套条件 | 早期返回 |
| 引入空对象 | 消除 null 检查 |
| 用类/枚举替换类型代码 | 强类型 |
| 用委托替换继承 | 组合优于继承 |

---

## 设计模式应用

### 策略模式

```diff
# 重构前：条件逻辑
- function calculateShipping(order, method) {
-   if (method === 'standard') {
-     return order.total > 50 ? 0 : 5.99;
-   } else if (method === 'express') {
-     return order.total > 100 ? 9.99 : 14.99;
-   } else if (method === 'overnight') {
-     return 29.99;
-   }
- }

# 重构后：策略模式
+ interface ShippingStrategy {
+   calculate(order: Order): number;
+ }
+
+ class StandardShipping implements ShippingStrategy {
+   calculate(order: Order) {
+     return order.total > 50 ? 0 : 5.99;
+   }
+ }
+
+ class ExpressShipping implements ShippingStrategy {
+   calculate(order: Order) {
+     return order.total > 100 ? 9.99 : 14.99;
+   }
+ }
+
+ class OvernightShipping implements ShippingStrategy {
+   calculate(order: Order) {
+     return 29.99;
+   }
+ }
+
+ function calculateShipping(order: Order, strategy: ShippingStrategy) {
+   return strategy.calculate(order);
+ }
```

---

## 总结

本套件覆盖完整的代码审查工作流：

| 阶段 | 核心动作 | 关键原则 |
|------|---------|---------|
| 请求审查 | 提交代码，获取反馈 | 审查前置，频繁审查 |
| 接收反馈 | 理解、验证、评估 | 技术严谨，避免盲目 |
| 重构改进 | 修复、重构、测试 | 行为保持，小步快跑 |

**记住：**
- 审查不是批评，是质量保障
- 反馈是建议，不是命令
- 重构不改变行为，只改善结构
- 测试是重构的安全网

---

## 来源说明

本套件融合以下技能：
- `requesting-code-review` - 请求代码审查流程
- `receiving-code-review` - 接收审查反馈处理
- `refactor` - 代码重构技术

完整保留各技能的核心价值，形成端到端的代码审查工作流支持。