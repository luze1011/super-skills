# 重构模式大全

## 📋 目录

1. [代码坏味道](#代码坏味道)
2. [基础重构手法](#基础重构手法)
3. [常见重构模式](#常见重构模式)
4. [重构步骤](#重构步骤)
5. [重构工具](#重构工具)

---

## 代码坏味道

### 1. 重复代码 (Duplicated Code)

**症状**: 同样的代码出现在多个地方

**解决方案**:
- 提取方法 (Extract Method)
- 提取父类 (Extract Superclass)
- 使用模板方法模式 (Form Template Method)

**示例**:
```javascript
// ❌ 坏味道
function calculateTotal(items) {
  let total = 0;
  for (let item of items) {
    total += item.price * item.quantity;
  }
  return total;
}

function calculateTax(items) {
  let total = 0;
  for (let item of items) {
    total += item.price * item.quantity;
  }
  return total * 0.1;
}

// ✅ 重构后
function calculateSubtotal(items) {
  return items.reduce((sum, item) => sum + item.price * item.quantity, 0);
}

function calculateTotal(items) {
  return calculateSubtotal(items);
}

function calculateTax(items) {
  return calculateSubtotal(items) * 0.1;
}
```

---

### 2. 过长函数 (Long Method)

**症状**: 函数太长，难以理解

**解决方案**:
- 提取方法 (Extract Method)
- 以查询取代临时变量 (Replace Temp with Query)
- 引入参数对象 (Introduce Parameter Object)
- 分解条件表达式 (Decompose Conditional)

**示例**:
```javascript
// ❌ 坏味道
function processOrder(order) {
  // 验证订单 (10 行)
  if (!order.items || order.items.length === 0) {
    throw new Error('Empty order');
  }
  if (!order.customer) {
    throw new Error('No customer');
  }
  // ...更多验证

  // 计算价格 (20 行)
  let subtotal = 0;
  for (let item of order.items) {
    subtotal += item.price * item.quantity;
  }
  let tax = subtotal * 0.1;
  let total = subtotal + tax;
  // ...更多计算

  // 更新库存 (15 行)
  for (let item of order.items) {
    // ...
  }

  // 发送通知 (10 行)
  // ...
}

// ✅ 重构后
function processOrder(order) {
  validateOrder(order);
  const pricing = calculatePricing(order);
  updateInventory(order);
  sendNotification(order, pricing);
}

function validateOrder(order) {
  if (!order.items?.length) throw new Error('Empty order');
  if (!order.customer) throw new Error('No customer');
  // ...更多验证
}

function calculatePricing(order) {
  const subtotal = order.items.reduce((sum, item) => 
    sum + item.price * item.quantity, 0
  );
  const tax = subtotal * 0.1;
  return { subtotal, tax, total: subtotal + tax };
}
```

---

### 3. 过大类 (Large Class)

**症状**: 类承担太多责任

**解决方案**:
- 提取类 (Extract Class)
- 提取子类 (Extract Subclass)
- 提取接口 (Extract Interface)

**示例**:
```javascript
// ❌ 坏味道
class User {
  constructor(name, email) {
    this.name = name;
    this.email = email;
  }
  
  // 用户相关
  getName() { return this.name; }
  getEmail() { return this.email; }
  
  // 订单相关 (不应该在这里)
  getOrders() { /* ... */ }
  createOrder() { /* ... */ }
  
  // 支付相关 (不应该在这里)
  processPayment() { /* ... */ }
  refundPayment() { /* ... */ }
}

// ✅ 重构后
class User {
  constructor(name, email) {
    this.name = name;
    this.email = email;
    this.orders = [];
  }
  
  getName() { return this.name; }
  getEmail() { return this.email; }
  
  addOrder(order) { this.orders.push(order); }
  getOrders() { return this.orders; }
}

class OrderService {
  createOrder(user, items) { /* ... */ }
  cancelOrder(orderId) { /* ... */ }
}

class PaymentService {
  processPayment(order, paymentMethod) { /* ... */ }
  refundPayment(paymentId) { /* ... */ }
}
```

---

### 4. 过长参数列表 (Long Parameter List)

**症状**: 参数太多，难以理解和使用

**解决方案**:
- 引入参数对象 (Introduce Parameter Object)
- 保持对象完整 (Preserve Whole Object)
- 以函数取代参数 (Replace Parameter with Method)

**示例**:
```javascript
// ❌ 坏味道
function createUser(name, email, age, address, phone, department, role) {
  // ...
}

// ✅ 重构后 - 参数对象
function createUser(userInfo) {
  const { name, email, age, address, phone, department, role } = userInfo;
  // ...
}

// 调用
createUser({
  name: 'John',
  email: 'john@example.com',
  age: 30,
  address: '123 Main St',
  phone: '555-1234',
  department: 'Engineering',
  role: 'Developer'
});
```

---

### 5. 发散式变化 (Divergent Change)

**症状**: 一个类因不同原因在不同方向上变化

**解决方案**:
- 提取类 (Extract Class)

**示例**:
```javascript
// ❌ 坏味道 - 一个类处理多种不同关注点
class Report {
  generateReport() { /* 报告逻辑 */ }
  saveToFile() { /* 文件操作 */ }
  sendEmail() { /* 邮件操作 */ }
}

// ✅ 重构后 - 分离关注点
class Report {
  generate() { /* 报告逻辑 */ }
}

class ReportFileHandler {
  save(report, filePath) { /* 文件操作 */ }
}

class ReportEmailSender {
  send(report, recipient) { /* 邮件操作 */ }
}
```

---

### 6. 散弹式修改 (Shotgun Surgery)

**症状**: 一个变化导致多个类的修改

**解决方案**:
- 移动方法 (Move Method)
- 移动字段 (Move Field)
- 内联类 (Inline Class)

**示例**:
```javascript
// ❌ 坏味道 - 价格计算分散在多处
class Product {
  getPrice() { return this.basePrice; }
}

class Order {
  calculateTotal() {
    let total = 0;
    for (let item of this.items) {
      total += item.product.getPrice() * item.quantity;
    }
    return total;
  }
}

class Invoice {
  calculateAmount() {
    let amount = 0;
    for (let item of this.order.items) {
      amount += item.product.getPrice() * item.quantity;
    }
    return amount;
  }
}

// ✅ 重构后 - 集中价格计算
class PricingCalculator {
  calculateTotal(items) {
    return items.reduce((sum, item) => 
      sum + item.product.price * item.quantity, 0
    );
  }
  
  applyDiscount(total, discount) {
    return total * (1 - discount);
  }
  
  applyTax(total, taxRate) {
    return total * (1 + taxRate);
  }
}
```

---

### 7. 依恋情结 (Feature Envy)

**症状**: 一个方法对另一个类的数据感兴趣

**解决方案**:
- 移动方法 (Move Method)
- 提取方法 (Extract Method)

**示例**:
```javascript
// ❌ 坏味道
class Order {
  // ...
}

class ReportGenerator {
  generateOrderReport(order) {
    // 对 Order 的数据很感兴趣
    const items = order.getItems();
    const customer = order.getCustomer();
    const total = order.getTotal();
    // 大量使用 order 的数据
  }
}

// ✅ 重构后
class Order {
  generateReport() {
    // 订单自己生成报告
    return {
      items: this.items,
      customer: this.customer,
      total: this.calculateTotal()
    };
  }
}

class ReportGenerator {
  generateOrderReport(order) {
    const data = order.generateReport();
    // 格式化报告
  }
}
```

---

### 8. 数据泥团 (Data Clumps)

**症状**: 几个数据总是一起出现

**解决方案**:
- 提取类 (Extract Class)
- 引入参数对象 (Introduce Parameter Object)

**示例**:
```javascript
// ❌ 坏味道
function findCustomer(firstName, lastName, email) { /* ... */ }
function updateCustomer(id, firstName, lastName, email) { /* ... */ }
function createOrder(customerId, firstName, lastName, email) { /* ... */ }

// ✅ 重构后
class CustomerInfo {
  constructor(firstName, lastName, email) {
    this.firstName = firstName;
    this.lastName = lastName;
    this.email = email;
  }
}

function findCustomer(customerInfo) { /* ... */ }
function updateCustomer(id, customerInfo) { /* ... */ }
function createOrder(customerId, customerInfo) { /* ... */ }
```

---

## 基础重构手法

### 提取方法 (Extract Method)

**何时使用**: 有一段代码可以独立出来

**步骤**:
1. 创建新方法
2. 将代码复制到新方法
3. 替换原代码为方法调用
4. 测试

```javascript
// 重构前
function printOwing(invoice) {
  let outstanding = 0;
  
  console.log('***********************');
  console.log('*** Customer Owes ***');
  console.log('***********************');
  
  for (const o of invoice.orders) {
    outstanding += o.amount;
  }
  
  console.log(`name: ${invoice.customer}`);
  console.log(`amount: ${outstanding}`);
}

// 重构后
function printOwing(invoice) {
  printBanner();
  const outstanding = calculateOutstanding(invoice);
  printDetails(invoice, outstanding);
}

function printBanner() {
  console.log('***********************');
  console.log('*** Customer Owes ***');
  console.log('***********************');
}

function calculateOutstanding(invoice) {
  return invoice.orders.reduce((sum, o) => sum + o.amount, 0);
}

function printDetails(invoice, outstanding) {
  console.log(`name: ${invoice.customer}`);
  console.log(`amount: ${outstanding}`);
}
```

---

### 内联方法 (Inline Method)

**何时使用**: 方法体比方法名还清晰

**步骤**:
1. 找到所有调用
2. 替换为方法体
3. 删除方法
4. 测试

```javascript
// 重构前
function getRating(driver) {
  return moreThanFiveLateDeliveries(driver) ? 2 : 1;
}

function moreThanFiveLateDeliveries(driver) {
  return driver.numberOfLateDeliveries > 5;
}

// 重构后
function getRating(driver) {
  return driver.numberOfLateDeliveries > 5 ? 2 : 1;
}
```

---

### 提取变量 (Extract Variable)

**何时使用**: 表达式复杂难懂

```javascript
// 重构前
if (platform.toUpperCase().indexOf('MAC') > -1 &&
    browser.toUpperCase().indexOf('IE') > -1 &&
    wasInitialized() && resize > 0) {
  // ...
}

// 重构后
const isMacOS = platform.toUpperCase().indexOf('MAC') > -1;
const isIE = browser.toUpperCase().indexOf('IE') > -1;
const wasResized = resize > 0;

if (isMacOS && isIE && wasInitialized() && wasResized) {
  // ...
}
```

---

### 以查询取代临时变量 (Replace Temp with Query)

**何时使用**: 临时变量阻止了提取方法

```javascript
// 重构前
function calculateTotal() {
  let basePrice = quantity * itemPrice;
  if (basePrice > 1000) {
    return basePrice * 0.95;
  }
  return basePrice * 0.98;
}

// 重构后
function calculateTotal() {
  if (basePrice() > 1000) {
    return basePrice() * 0.95;
  }
  return basePrice() * 0.98;
}

function basePrice() {
  return quantity * itemPrice;
}
```

---

## 常见重构模式

### 策略模式重构

将条件逻辑转换为策略对象

```javascript
// 重构前
function calculateShipping(order) {
  if (order.type === 'standard') {
    return order.weight * 1.0;
  } else if (order.type === 'express') {
    return order.weight * 2.0 + 10;
  } else if (order.type === 'overnight') {
    return order.weight * 3.0 + 20;
  }
}

// 重构后
const shippingStrategies = {
  standard: (order) => order.weight * 1.0,
  express: (order) => order.weight * 2.0 + 10,
  overnight: (order) => order.weight * 3.0 + 20
};

function calculateShipping(order) {
  const strategy = shippingStrategies[order.type];
  if (!strategy) throw new Error('Unknown shipping type');
  return strategy(order);
}
```

---

### 状态模式重构

将状态相关的条件逻辑转换为状态对象

```javascript
// 重构前
class Employee {
  pay() {
    switch (this.state) {
      case 'active':
        return this.calculatePay();
      case 'terminated':
        return 0;
      case 'suspended':
        return this.calculatePay() * 0.5;
    }
  }
}

// 重构后
class Employee {
  constructor() {
    this.states = {
      active: new ActiveState(this),
      terminated: new TerminatedState(this),
      suspended: new SuspendedState(this)
    };
    this.state = this.states.active;
  }
  
  setState(stateName) {
    this.state = this.states[stateName];
  }
  
  pay() {
    return this.state.pay();
  }
}

class ActiveState {
  pay() { return this.employee.calculatePay(); }
}

class TerminatedState {
  pay() { return 0; }
}

class SuspendedState {
  pay() { return this.employee.calculatePay() * 0.5; }
}
```

---

## 重构步骤

### 标准重构流程

1. **识别问题**
   - 使用代码审查
   - 运行静态分析工具
   - 团队讨论

2. **编写测试**
   - 确保现有功能有测试覆盖
   - 测试应该通过

3. **小步重构**
   - 每次只做一个小改动
   - 保持代码可编译/可运行

4. **运行测试**
   - 每步后都运行测试
   - 确保测试通过

5. **提交代码**
   - 每个重构步骤独立提交
   - 写清晰的提交信息

### 重构检查清单

- [ ] 理解现有代码
- [ ] 编写/确认测试
- [ ] 重构前运行测试（通过）
- [ ] 小步修改
- [ ] 每步运行测试
- [ ] 重构后测试通过
- [ ] 代码审查
- [ ] 更新文档
- [ ] 提交变更

---

## 重构工具

### IDE 支持

**VS Code**:
- 内置重构功能
- 扩展：JavaScript Booster, TypeScript Hero

**WebStorm / IntelliJ**:
- 强大的重构工具
- 安全重构（Safe Refactor）

**Visual Studio**:
- 内置重构菜单
- ReSharper 扩展

### 常用重构命令

| 操作 | VS Code | WebStorm |
|------|---------|----------|
| 提取方法 | Ctrl+Shift+R | Ctrl+Alt+M |
| 提取变量 | Ctrl+Shift+R | Ctrl+Alt+V |
| 重命名 | F2 | Shift+F6 |
| 移动文件 | - | F6 |
| 内联变量 | - | Ctrl+Alt+N |

### 静态分析工具

**JavaScript/TypeScript**:
- ESLint
- TypeScript compiler
- SonarQube

**Python**:
- Pylint
- Flake8
- Black (格式化)

**通用**:
- SonarQube
- CodeClimate
- LGTM

---

**推荐书籍**:
- 《重构：改善既有代码的设计》 - Martin Fowler
- 《代码整洁之道》 - Robert C. Martin
- 《修改代码的艺术》 - Michael Feathers