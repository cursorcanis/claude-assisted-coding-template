---
paths:
  - "**/*.test.*"
  - "**/*.spec.*"
  - "**/test_*.py"
  - "**/*_test.go"
  - "**/tests/**"
  - "**/__tests__/**"
---

# Testing conventions

- A test asserts on behaviour the caller can observe. Asserting on internal
  call order locks in the implementation and makes refactors expensive.
- One reason to fail per test. If a test can fail two ways, the failure
  message stops telling you which.
- Name the test after the case, not the function: `returns_empty_when_no_rows`
  beats `test_query`.
- A bug fix ships with the test that would have caught it. Write the test
  first and watch it fail, so you know it can.
- Do not weaken an assertion to make a test pass. If the test is wrong, say
  it is wrong and why.
- Never mock the thing under test. Mock what it talks to.
