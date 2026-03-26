---
name: code-review-suite
description: A comprehensive code review workflow for requesting reviews, processing feedback, and implementing improvements. Use this skill when the user wants to request a code review, respond to review feedback, refactor code based on suggestions, or improve code quality. Also use when mentions "review", "code review", "审查代码", "代码审查", "反馈", "重构", or "refactor" in the context of code changes.
---

# Code Review Suite

A complete workflow for managing code reviews - from requesting reviews to processing feedback and implementing improvements.

## When to Use This Skill

Trigger this skill when:
- User wants to request a code review for their changes
- User receives review feedback and needs help processing it
- User wants to refactor code based on review suggestions
- User mentions "review", "代码审查", "反馈处理", or similar terms

## Workflow Overview

```
Request Review → Collect Feedback → Process Suggestions → Implement Changes → Follow-up
```

## Step 1: Request Code Review

Use the `scripts/request-review.sh` script to create a structured review request.

### What the script does:
1. Analyzes changed files in the current branch
2. Generates a review request with context
3. Creates a checklist for reviewers

### Usage:
```bash
./scripts/request-review.sh --branch <feature-branch> --reviewer <reviewer-name>
```

The script generates:
- Summary of changes
- Key areas to review
- Testing checklist
- Context for reviewers

Read `assets/review-template.md` for the standard review request format.

## Step 2: Process Review Feedback

When you receive feedback, use `scripts/process-feedback.sh` to organize and track responses.

### What the script does:
1. Parses review comments
2. Categorizes feedback (critical, important, suggestion)
3. Tracks resolution status

### Feedback Categories:

| Priority | Description | Action |
|----------|-------------|--------|
| 🔴 Critical | Bugs, security issues, breaking changes | Must fix before merge |
| 🟡 Important | Performance, best practices, maintainability | Should fix |
| 🟢 Suggestion | Style, minor improvements | Consider fixing |

## Step 3: Implement Changes

Based on the feedback, implement changes following the guidelines in `references/refactor-guide.md`.

### Implementation Principles:

1. **Address Critical First** - Handle blocking issues immediately
2. **One Change Per Commit** - Keep commits atomic and focused
3. **Explain Your Reasoning** - When you disagree with feedback, document why
4. **Test Thoroughly** - Ensure changes don't break existing functionality

## Step 4: Respond to Feedback

For each piece of feedback:
1. Acknowledge the comment
2. Explain what you changed (or why you didn't)
3. Link to the commit that addresses it

## Reference Files

- **Review Checklist**: Read `references/review-checklist.md` for what to check during reviews
- **Refactor Guide**: Read `references/refactor-guide.md` for best practices on implementing changes

## Tips for Effective Reviews

### For Authors:
- Keep changes small and focused
- Provide context in your review request
- Be open to feedback
- Respond to all comments

### For Reviewers:
- Be constructive and specific
- Explain the "why" behind suggestions
- Distinguish between must-fix and nice-to-have
- Acknowledge good code

## Example Workflow

```
User: "I need to request a review for my PR"

Agent:
1. Run `request-review.sh` to generate review request
2. Present the formatted request
3. Ask if user wants to customize it

User: "I got some feedback on my PR, can you help?"

Agent:
1. Ask user to share the feedback
2. Run `process-feedback.sh` to categorize it
3. Help implement changes following refactor-guide.md
4. Draft responses to each comment
```

## Integration with Git

This skill works well with git workflows:
- Analyzes branch differences
- Tracks file changes
- Integrates with PR/merge request workflows

---

Use this skill to make code reviews more efficient and ensure consistent quality improvements.