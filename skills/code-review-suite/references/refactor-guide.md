# Refactor Guide

A practical guide for refactoring code based on review feedback. Follow these principles and patterns when implementing changes.

---

## 🎯 Refactoring Principles

### Core Principles

1. **Small Steps** - Make one change at a time, test after each step
2. **Preserve Behavior** - Don't change functionality while refactoring
3. **Test Coverage** - Have tests before you refactor
4. **Frequent Commits** - Commit after each successful refactoring

### The Refactoring Cycle

```
1. Identify the problem
2. Write a test (if needed)
3. Make the smallest possible change
4. Run tests
5. Commit if successful
6. Repeat
```

---

## 📋 Common Refactoring Scenarios

### 1. Extract Method

**When:** A method is too long or has multiple responsibilities

**Before:**
```javascript
function processOrder(order) {
    // Validate order
    if (!order.items || order.items.length === 0) {
        throw new Error('Empty order');
    }
    if (!order.customer) {
        throw new Error('No customer');
    }
    
    // Calculate total
    let total = 0;
    for (const item of order.items) {
        total += item.price * item.quantity;
    }
    
    // Apply discount
    if (order.discount) {
        total = total * (1 - order.discount);
    }
    
    // Create order record
    const record = {
        id: generateId(),
        customer: order.customer,
        items: order.items,
        total: total,
        status: 'pending'
    };
    
    return record;
}
```

**After:**
```javascript
function processOrder(order) {
    validateOrder(order);
    const total = calculateTotal(order);
    return createOrderRecord(order, total);
}

function validateOrder(order) {
    if (!order.items || order.items.length === 0) {
        throw new Error('Empty order');
    }
    if (!order.customer) {
        throw new Error('No customer');
    }
}

function calculateTotal(order) {
    let total = order.items.reduce((sum, item) => {
        return sum + (item.price * item.quantity);
    }, 0);
    
    if (order.discount) {
        total = total * (1 - order.discount);
    }
    
    return total;
}

function createOrderRecord(order, total) {
    return {
        id: generateId(),
        customer: order.customer,
        items: order.items,
        total: total,
        status: 'pending'
    };
}
```

**Benefits:**
- Each function has a single responsibility
- Easier to test individual parts
- Better readability

---

### 2. Rename Variable/Method

**When:** Names are unclear or misleading

**Before:**
```javascript
function calc(d) {
    const x = d * 0.1;
    return x;
}
```

**After:**
```javascript
function calculateTax(price) {
    const taxRate = 0.1;
    return price * taxRate;
}
```

**Guidelines:**
- Use intention-revealing names
- Avoid abbreviations
- Use consistent naming conventions
- Name should answer "what" not "how"

---

### 3. Remove Duplication

**When:** Same code appears in multiple places

**Before:**
```javascript
function validateEmail(email) {
    const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!regex.test(email)) {
        throw new Error('Invalid email');
    }
}

function validateUserEmail(user) {
    const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!regex.test(user.email)) {
        throw new Error('Invalid email');
    }
}
```

**After:**
```javascript
const EMAIL_REGEX = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

function isValidEmail(email) {
    return EMAIL_REGEX.test(email);
}

function validateEmail(email) {
    if (!isValidEmail(email)) {
        throw new Error('Invalid email');
    }
}

function validateUserEmail(user) {
    validateEmail(user.email);
}
```

**Benefits:**
- Single source of truth
- Easier to maintain
- Consistent behavior

---

### 4. Simplify Conditionals

**When:** Complex boolean logic or nested conditionals

**Before:**
```javascript
function canUserAccess(user, resource) {
    if (user) {
        if (user.isActive) {
            if (resource) {
                if (resource.isPublic) {
                    return true;
                } else {
                    if (user.role === 'admin') {
                        return true;
                    } else if (user.role === 'member') {
                        return resource.ownerId === user.id;
                    }
                }
            }
        }
    }
    return false;
}
```

**After:**
```javascript
function canUserAccess(user, resource) {
    if (!user || !user.isActive || !resource) {
        return false;
    }
    
    if (resource.isPublic) {
        return true;
    }
    
    return hasPermissionFor(user, resource);
}

function hasPermissionFor(user, resource) {
    if (user.role === 'admin') {
        return true;
    }
    
    return user.role === 'member' && resource.ownerId === user.id;
}
```

**Techniques:**
- Guard clauses (early return)
- Decompose conditional
- Replace nested conditional with guard clauses

---

### 5. Replace Magic Numbers

**When:** Unexplained constants in code

**Before:**
```javascript
function calculateDiscount(price, customerType) {
    if (customerType === 1) {
        return price * 0.9;
    } else if (customerType === 2) {
        return price * 0.85;
    } else if (customerType === 3) {
        return price * 0.8;
    }
    return price;
}
```

**After:**
```javascript
const CUSTOMER_TYPES = {
    REGULAR: 'regular',
    SILVER: 'silver',
    GOLD: 'gold'
};

const DISCOUNT_RATES = {
    [CUSTOMER_TYPES.REGULAR]: 0,
    [CUSTOMER_TYPES.SILVER]: 0.1,
    [CUSTOMER_TYPES.GOLD]: 0.15
};

function calculateDiscount(price, customerType) {
    const discountRate = DISCOUNT_RATES[customerType] || 0;
    return price * (1 - discountRate);
}
```

**Benefits:**
- Self-documenting code
- Easier to modify
- Reduces errors

---

## 🔧 Addressing Common Review Feedback

### Performance Issues

**Feedback:** "This loop is inefficient"

**Approach:**
1. Profile to identify bottlenecks
2. Look for algorithmic improvements
3. Consider caching
4. Use appropriate data structures

**Example:**
```javascript
// Before: O(n²)
function findDuplicates(items) {
    const duplicates = [];
    for (let i = 0; i < items.length; i++) {
        for (let j = i + 1; j < items.length; j++) {
            if (items[i] === items[j]) {
                duplicates.push(items[i]);
            }
        }
    }
    return duplicates;
}

// After: O(n)
function findDuplicates(items) {
    const seen = new Set();
    const duplicates = new Set();
    
    for (const item of items) {
        if (seen.has(item)) {
            duplicates.add(item);
        }
        seen.add(item);
    }
    
    return Array.from(duplicates);
}
```

---

### Security Issues

**Feedback:** "Potential SQL injection"

**Approach:**
1. Use parameterized queries
2. Validate and sanitize input
3. Use ORM methods
4. Apply principle of least privilege

**Example:**
```javascript
// Before: Vulnerable
function getUser(username) {
    const query = `SELECT * FROM users WHERE username = '${username}'`;
    return db.query(query);
}

// After: Secure
function getUser(username) {
    const query = 'SELECT * FROM users WHERE username = ?';
    return db.query(query, [username]);
}
```

---

### Code Duplication

**Feedback:** "This logic is duplicated"

**Approach:**
1. Identify common patterns
2. Extract to shared function
3. Parameterize differences
4. Consider inheritance or composition

---

## ✅ Refactoring Checklist

Before refactoring:
- [ ] Tests exist and pass
- [ ] You understand the code
- [ ] You have a clear goal
- [ ] You've committed your current work

After refactoring:
- [ ] All tests still pass
- [ ] No functionality changed
- [ ] Code is more readable
- [ ] Code is more maintainable
- [ ] Commit with clear message

---

## 📝 Commit Messages for Refactoring

Use clear commit messages that explain what and why:

```
refactor: extract validation logic into separate function

- Move validation from processOrder to validateOrder
- Improve testability and reusability
- No functional changes

Addresses review comment: #123
```

---

## 🎓 Best Practices

### Do:
- ✅ Refactor in small, incremental steps
- ✅ Run tests after each step
- ✅ Commit frequently
- ✅ Keep refactorings focused
- ✅ Document complex changes

### Don't:
- ❌ Refactor without tests
- ❌ Mix refactoring with feature changes
- ❌ Make large changes at once
- ❌ Skip running tests
- ❌ Leave broken code

---

*Follow this guide to implement review feedback effectively and maintain code quality.*