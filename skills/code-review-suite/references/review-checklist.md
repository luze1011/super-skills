# Code Review Checklist

A comprehensive checklist for reviewing code changes. Use this during code reviews to ensure thorough coverage.

---

## 📋 Pre-Review Preparation

Before starting the review:

- [ ] Understand the context and purpose of the change
- [ ] Read the related issue/ticket
- [ ] Check if there are design docs or RFCs
- [ ] Understand the acceptance criteria

---

## 🎯 Functional Correctness

### Core Functionality
- [ ] Does the code do what it's supposed to do?
- [ ] Are all requirements met?
- [ ] Are edge cases handled?
- [ ] Does it work with existing features?

### Error Handling
- [ ] Are errors properly caught and handled?
- [ ] Are error messages clear and helpful?
- [ ] Is there appropriate logging?
- [ ] Are failures graceful?

### Data Integrity
- [ ] Is input validation present?
- [ ] Are data transformations correct?
- [ ] Is data sanitization applied?
- [ ] Are there potential data corruption risks?

---

## 🧪 Testing

### Test Coverage
- [ ] Are there unit tests for new code?
- [ ] Do tests cover happy path?
- [ ] Do tests cover error cases?
- [ ] Are edge cases tested?

### Test Quality
- [ ] Are tests meaningful and not just for coverage?
- [ ] Are test names descriptive?
- [ ] Are tests maintainable?
- [ ] Do tests use appropriate mocking?

### Integration
- [ ] Are integration tests needed?
- [ ] Do existing tests still pass?
- [ ] Is test data appropriate?

---

## 🏗️ Code Quality

### Readability
- [ ] Is the code easy to understand?
- [ ] Are variable names clear and meaningful?
- [ ] Are functions/methods focused and small?
- [ ] Is there unnecessary complexity?

### Structure
- [ ] Is the code well-organized?
- [ ] Are responsibilities clearly separated?
- [ ] Is there code duplication?
- [ ] Is the abstraction level appropriate?

### Consistency
- [ ] Does the code follow project conventions?
- [ ] Is naming consistent?
- [ ] Is formatting consistent?
- [ ] Are patterns used consistently?

### Documentation
- [ ] Are complex parts explained?
- [ ] Is the API documentation updated?
- [ ] Are there inline comments where needed?
- [ ] Is the README updated if needed?

---

## 🔒 Security

### Input Handling
- [ ] Is user input validated?
- [ ] Is input sanitized before use?
- [ ] Are there injection vulnerabilities?
- [ ] Is sensitive data protected?

### Authentication & Authorization
- [ ] Are auth checks present?
- [ ] Are permissions verified?
- [ ] Is there proper access control?
- [ ] Are there privilege escalation risks?

### Data Protection
- [ ] Is sensitive data encrypted?
- [ ] Are secrets properly managed?
- [ ] Is PII handled correctly?
- [ ] Are logs free of sensitive data?

### Common Vulnerabilities
- [ ] No SQL injection
- [ ] No XSS vulnerabilities
- [ ] No CSRF vulnerabilities
- [ ] No insecure dependencies

---

## ⚡ Performance

### Efficiency
- [ ] Are there obvious performance issues?
- [ ] Is there unnecessary work?
- [ ] Are loops and iterations efficient?
- [ ] Is caching used appropriately?

### Resources
- [ ] Are resources properly managed?
- [ ] Are connections closed?
- [ ] Is memory properly released?
- [ ] Are there potential leaks?

### Scalability
- [ ] Will this scale?
- [ ] Are there N+1 queries?
- [ ] Is pagination needed?
- [ ] Are there bottleneck risks?

---

## 🔄 Maintainability

### Future-Proofing
- [ ] Is the code easy to modify?
- [ ] Are there hardcoded values?
- [ ] Is configuration externalized?
- [ ] Is the code testable?

### Technical Debt
- [ ] Is there debt being introduced?
- [ ] Is existing debt being addressed?
- [ ] Are workarounds documented?
- [ ] Are there TODOs with follow-up plans?

### Dependencies
- [ ] Are new dependencies needed?
- [ ] Are dependencies up-to-date?
- [ ] Are dependencies trustworthy?
- [ ] Can dependencies be removed?

---

## 📦 Deployment

### Compatibility
- [ ] Is this a breaking change?
- [ ] Is backward compatibility maintained?
- [ ] Are migrations needed?
- [ ] Is versioning correct?

### Configuration
- [ ] Are config changes needed?
- [ ] Are feature flags used?
- [ ] Is rollback possible?
- [ ] Are there environment-specific changes?

### Monitoring
- [ ] Is logging sufficient?
- [ ] Are metrics needed?
- [ ] Are alerts needed?
- [ ] Is debugging possible?

---

## ✅ Final Checks

- [ ] All CI checks pass
- [ ] No new warnings introduced
- [ ] Documentation is complete
- [ ] Reviewer comments addressed
- [ ] Ready for merge

---

## 📝 Review Feedback Format

When providing feedback, use this format:

```
**Priority:** [Critical/Important/Suggestion]
**File:** [filename:line]
**Issue:** [description]
**Suggestion:** [how to fix]
```

### Example:
```
**Priority:** Critical
**File:** auth.js:45
**Issue:** SQL injection vulnerability in user input
**Suggestion:** Use parameterized queries instead of string concatenation
```

---

## 🎓 Review Etiquette

### For Reviewers:
- Be constructive and specific
- Explain the "why"
- Distinguish must-fix from nice-to-have
- Acknowledge good code
- Ask questions, don't demand

### For Authors:
- Be open to feedback
- Respond to all comments
- Explain your reasoning
- Don't take it personally
- Thank your reviewers

---

*Use this checklist to ensure thorough and consistent code reviews.*