# Code Review Request Template

Use this template to create structured review requests.

---

## 📋 Pull Request Information

**PR Title:** [Brief description of changes]

**Branch:** `feature/branch-name` → `main`

**Author:** @username

**Reviewers:** @reviewer1, @reviewer2

**Related Issues:** #123, #456

---

## 📝 Description

### What does this PR do?

[Provide a clear description of the changes]

### Why is this change needed?

[Explain the motivation and context]

### How was this tested?

- [ ] Unit tests added/updated
- [ ] Integration tests added/updated
- [ ] Manual testing performed
- [ ] E2E tests added/updated

---

## 📂 Files Changed

| File | Changes | Reason |
|------|---------|--------|
| `src/auth.js` | +45 -12 | Add JWT authentication |
| `src/user.js` | +23 -5 | Update user model |
| `tests/auth.test.js` | +67 -0 | Add auth tests |

**Total:** +135 lines, -17 lines

---

## 🎯 Key Changes

### 1. [Change Category]

**Files:** `file1.js`, `file2.js`

**Description:**
- What changed
- Why it changed
- Any considerations

### 2. [Another Change Category]

**Files:** `file3.js`

**Description:**
- What changed
- Why it changed
- Any considerations

---

## ✅ Review Checklist

Please check the following when reviewing:

### Functionality
- [ ] Code does what it's supposed to do
- [ ] Edge cases are handled
- [ ] Error handling is appropriate

### Quality
- [ ] Code is readable and well-organized
- [ ] Naming is clear and consistent
- [ ] No unnecessary complexity

### Testing
- [ ] Tests are meaningful
- [ ] Coverage is adequate
- [ ] Tests pass locally

### Security
- [ ] No security vulnerabilities
- [ ] Input is validated
- [ ] Sensitive data is protected

### Performance
- [ ] No obvious performance issues
- [ ] Resources are managed properly
- [ ] Appropriate data structures used

---

## 🔍 Areas to Focus On

Please pay special attention to:

1. **[Specific Area]**
   - Why: [Reason]
   - Question: [Specific question if any]

2. **[Another Area]**
   - Why: [Reason]
   - Question: [Specific question if any]

---

## ⚠️ Known Issues

| Issue | Status | Notes |
|-------|--------|-------|
| Test coverage low for X | Will address in follow-up | Tracked in #789 |
| Performance optimization needed | TODO | Need benchmark data |

---

## 📸 Screenshots (if applicable)

[Add screenshots for UI changes]

**Before:**
![Before](before.png)

**After:**
![After](after.png)

---

## 🧪 Testing Instructions

### Setup
```bash
# Commands to set up the test environment
npm install
npm run migrate
```

### Run Tests
```bash
# Commands to run tests
npm test
npm run test:integration
```

### Manual Testing
1. Step 1
2. Step 2
3. Step 3

---

## 📚 Documentation

- [ ] README updated
- [ ] API documentation updated
- [ ] Inline comments added for complex logic
- [ ] Migration guide provided (if breaking change)

---

## 🔄 Deployment Notes

### Breaking Changes
- [ ] No breaking changes
- [ ] Breaking changes (describe below)

**Breaking Change Description:**
[If applicable, describe the breaking changes and migration path]

### Configuration Changes
- [ ] No config changes
- [ ] Config changes required (describe below)

**Config Changes:**
[Describe any required configuration changes]

### Database Changes
- [ ] No database changes
- [ ] Migration required (describe below)

**Migration:**
[Describe any database migrations]

---

## 💬 Questions for Reviewers

1. [Question 1]
2. [Question 2]
3. [Question 3]

---

## 📅 Timeline

- **Created:** YYYY-MM-DD
- **Ready for Review:** YYYY-MM-DD
- **Target Merge Date:** YYYY-MM-DD

---

## 🔗 Related Resources

- Design Doc: [Link]
- Issue: [Link]
- Documentation: [Link]
- Discussion: [Link]

---

## 📝 Notes

[Any additional notes or context]

---

*Thank you for reviewing! Please provide feedback using the review checklist.*

---

## Quick Reference: Feedback Format

When providing feedback, please use:

```
**Priority:** [Critical/Important/Suggestion]
**Location:** file:line
**Comment:** [Your feedback]
**Suggestion:** [How to fix (optional)]
```

### Examples:

```
**Priority:** Critical
**Location:** auth.js:45
**Comment:** SQL injection vulnerability in user input
**Suggestion:** Use parameterized query
```

```
**Priority:** Suggestion
**Location:** utils.js:23
**Comment:** Consider extracting this to a helper function
**Suggestion:** Create a formatCurrency helper
```

---

*Template version: 1.0*