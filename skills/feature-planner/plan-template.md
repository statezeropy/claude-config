# Implementation Plan: [Feature Name]

**Status**: 🔄 In Progress
**Started**: YYYY-MM-DD
**Last Updated**: YYYY-MM-DD
**Estimated Completion**: YYYY-MM-DD

---

**⚠️ CRITICAL INSTRUCTIONS**: After completing each phase:
1. ✅ Check off completed task checkboxes
2. 🧪 Run all quality gate validation commands
3. ⚠️ Verify ALL quality gate items pass
4. 📅 Update "Last Updated" date above
5. 📝 Document learnings in Notes section
6. ➡️ Only then proceed to next phase

⛔ **DO NOT skip quality gates or proceed with failing checks**

---

## 📋 Overview

### Feature Description
[What this feature does and why it's needed]

### Success Criteria
- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

### User Impact
[How this benefits users or improves the product]

---

## 🏗️ Architecture Decisions

| Decision | Rationale | Trade-offs |
|----------|-----------|------------|
| [Decision 1] | [Why this approach] | [What we're giving up] |
| [Decision 2] | [Why this approach] | [What we're giving up] |

---

## 📦 Dependencies

### Required Before Starting
- [ ] Dependency 1: [Description]
- [ ] Dependency 2: [Description]

### External Dependencies
- Package/Library 1: version X.Y.Z
- Package/Library 2: version X.Y.Z

---

## 🧪 Test Strategy

### Testing Approach
**TDD Principle**: Write tests FIRST, then implement to make them pass

### Test Pyramid for This Feature
| Test Type | Coverage Target | Purpose |
|-----------|-----------------|---------|
| **Unit Tests** | ≥80% | Business logic, models, core algorithms |
| **Integration Tests** | Critical paths | Component interactions, data flow |
| **E2E Tests** | Key user flows | Full system behavior validation |

### Test File Organization
```
tests/
├── unit/
│   ├── test_[domain].py
│   └── test_[models].py
├── integration/
│   └── test_[feature_name].py
├── conftest.py
└── fixtures/
    └── [test_data].json
```

### Coverage Requirements by Phase
- **Phase 1 (Foundation)**: Unit tests for core models/entities (≥80%)
- **Phase 2 (Business Logic)**: Logic + repository tests (≥80%)
- **Phase 3 (Integration)**: Component integration tests (≥70%)
- **Phase 4 (E2E)**: End-to-end user flow test (1+ critical path)

### Test Naming Convention
Follow pytest conventions:
```python
# tests/unit/test_llm_chain.py

class TestLLMChain:
    def test_invoke_returns_valid_response(self):
        # Arrange → Act → Assert pattern
        ...

    def test_handles_api_error_gracefully(self):
        ...
```

---

## 🚀 Implementation Phases

### Phase 1: [Foundation Phase Name]
**Goal**: [Specific working functionality this phase delivers]
**Estimated Time**: X hours
**Status**: ⏳ Pending | 🔄 In Progress | ✅ Complete

#### Tasks

**🔴 RED: Write Failing Tests First**
- [ ] **Test 1.1**: Write unit tests for [specific functionality]
  - File(s): `tests/unit/test_[component].py`
  - Expected: Tests FAIL (red) because feature doesn't exist yet
  - Details: Test cases covering:
    - Happy path scenarios
    - Edge cases
    - Error conditions

- [ ] **Test 1.2**: Write integration tests for [component interaction]
  - File(s): `tests/integration/test_[feature].py`
  - Expected: Tests FAIL (red) because integration doesn't exist yet
  - Details: Test interaction between [list components]

**🟢 GREEN: Implement to Make Tests Pass**
- [ ] **Task 1.3**: Implement [component/module]
  - File(s): `src/[layer]/[component].py`
  - Goal: Make Test 1.1 pass with minimal code
  - Details: [Implementation notes]

- [ ] **Task 1.4**: Implement [integration/glue code]
  - File(s): `src/[layer]/[integration].py`
  - Goal: Make Test 1.2 pass
  - Details: [Implementation notes]

**🔵 REFACTOR: Clean Up Code**
- [ ] **Task 1.5**: Refactor for code quality
  - Files: Review all new code in this phase
  - Goal: Improve design without breaking tests
  - Checklist:
    - [ ] Remove duplication (DRY principle)
    - [ ] Improve naming clarity
    - [ ] Extract reusable components
    - [ ] Add inline documentation
    - [ ] Optimize performance if needed

#### Quality Gate ✋

**⚠️ STOP: Do NOT proceed to Phase 2 until ALL checks pass**

**TDD Compliance** (CRITICAL):
- [ ] **Red Phase**: Tests were written FIRST and initially failed
- [ ] **Green Phase**: Production code written to make tests pass
- [ ] **Refactor Phase**: Code improved while tests still pass
- [ ] **Coverage Check**: Test coverage meets requirements
  ```bash
  uv run pytest --cov=src --cov-report=html --cov-report=term
  ```

**Build & Tests**:
- [ ] **Build**: Project builds/compiles without errors
- [ ] **All Tests Pass**: 100% of tests passing (no skipped tests)
- [ ] **Test Performance**: Test suite completes in acceptable time
- [ ] **No Flaky Tests**: Tests pass consistently (run 3+ times)

**Code Quality**:
- [ ] **Linting**: No linting errors or warnings
- [ ] **Formatting**: Code formatted per project standards
- [ ] **Type Safety**: Type checker passes (if applicable)
- [ ] **Static Analysis**: No critical issues from static analysis tools

**Security & Performance**:
- [ ] **Dependencies**: No known security vulnerabilities
- [ ] **Performance**: No performance regressions
- [ ] **Memory**: No memory leaks or resource issues
- [ ] **Error Handling**: Proper error handling implemented

**Documentation**:
- [ ] **Code Comments**: Complex logic documented
- [ ] **API Docs**: Public interfaces documented
- [ ] **README**: Usage instructions updated if needed

**Manual Testing**:
- [ ] **Functionality**: Feature works as expected
- [ ] **Edge Cases**: Boundary conditions tested
- [ ] **Error States**: Error handling verified

**Validation Commands**:
```bash
# Test & Coverage
uv run pytest --cov=src --cov-report=term

# Code Quality
uv run ruff check .
uv run ruff format --check .

# Type Check
uv run mypy src/

# Dependency Sync
uv sync
```

**Manual Test Checklist**:
- [ ] Test case 1: [Specific scenario to verify]
- [ ] Test case 2: [Edge case to verify]
- [ ] Test case 3: [Error handling to verify]

---

### Phase 2: [Core Feature Phase Name]
**Goal**: [Specific deliverable]
**Estimated Time**: X hours
**Status**: ⏳ Pending | 🔄 In Progress | ✅ Complete

#### Tasks

**🔴 RED: Write Failing Tests First**
- [ ] **Test 2.1**: Write unit tests for [specific functionality]
  - File(s): `tests/unit/test_[component].py`
  - Expected: Tests FAIL (red) because feature doesn't exist yet
  - Details: Test cases covering:
    - Happy path scenarios
    - Edge cases
    - Error conditions

- [ ] **Test 2.2**: Write integration tests for [component interaction]
  - File(s): `tests/integration/test_[feature].py`
  - Expected: Tests FAIL (red) because integration doesn't exist yet
  - Details: Test interaction between [list components]

**🟢 GREEN: Implement to Make Tests Pass**
- [ ] **Task 2.3**: Implement [component/module]
  - File(s): `src/[layer]/[component].py`
  - Goal: Make Test 2.1 pass with minimal code
  - Details: [Implementation notes]

- [ ] **Task 2.4**: Implement [integration/glue code]
  - File(s): `src/[layer]/[integration].py`
  - Goal: Make Test 2.2 pass
  - Details: [Implementation notes]

**🔵 REFACTOR: Clean Up Code**
- [ ] **Task 2.5**: Refactor for code quality
  - Files: Review all new code in this phase
  - Goal: Improve design without breaking tests
  - Checklist:
    - [ ] Remove duplication (DRY principle)
    - [ ] Improve naming clarity
    - [ ] Extract reusable components
    - [ ] Add inline documentation
    - [ ] Optimize performance if needed

#### Quality Gate ✋

**⚠️ STOP: Do NOT proceed to Phase 3 until ALL checks pass**

**TDD Compliance** (CRITICAL):
- [ ] **Red Phase**: Tests were written FIRST and initially failed
- [ ] **Green Phase**: Production code written to make tests pass
- [ ] **Refactor Phase**: Code improved while tests still pass
- [ ] **Coverage Check**: Test coverage meets requirements

**Build & Tests**:
- [ ] **Build**: Project builds/compiles without errors
- [ ] **All Tests Pass**: 100% of tests passing (no skipped tests)
- [ ] **Test Performance**: Test suite completes in acceptable time
- [ ] **No Flaky Tests**: Tests pass consistently (run 3+ times)

**Code Quality**:
- [ ] **Linting**: No linting errors or warnings
- [ ] **Formatting**: Code formatted per project standards
- [ ] **Type Safety**: Type checker passes (if applicable)
- [ ] **Static Analysis**: No critical issues from static analysis tools

**Security & Performance**:
- [ ] **Dependencies**: No known security vulnerabilities
- [ ] **Performance**: No performance regressions
- [ ] **Memory**: No memory leaks or resource issues
- [ ] **Error Handling**: Proper error handling implemented

**Documentation**:
- [ ] **Code Comments**: Complex logic documented
- [ ] **API Docs**: Public interfaces documented
- [ ] **README**: Usage instructions updated if needed

**Manual Testing**:
- [ ] **Functionality**: Feature works as expected
- [ ] **Edge Cases**: Boundary conditions tested
- [ ] **Error States**: Error handling verified

**Validation Commands**:
```bash
[Same as Phase 1 - customize for your project]
```

**Manual Test Checklist**:
- [ ] Test case 1: [Specific scenario to verify]
- [ ] Test case 2: [Edge case to verify]
- [ ] Test case 3: [Error handling to verify]

---

### Phase 3: [Enhancement Phase Name]
**Goal**: [Specific deliverable]
**Estimated Time**: X hours
**Status**: ⏳ Pending | 🔄 In Progress | ✅ Complete

#### Tasks

**🔴 RED: Write Failing Tests First**
- [ ] **Test 3.1**: Write unit tests for [specific functionality]
  - File(s): `tests/unit/test_[component].py`
  - Expected: Tests FAIL (red) because feature doesn't exist yet
  - Details: Test cases covering:
    - Happy path scenarios
    - Edge cases
    - Error conditions

- [ ] **Test 3.2**: Write integration tests for [component interaction]
  - File(s): `tests/integration/test_[feature].py`
  - Expected: Tests FAIL (red) because integration doesn't exist yet
  - Details: Test interaction between [list components]

**🟢 GREEN: Implement to Make Tests Pass**
- [ ] **Task 3.3**: Implement [component/module]
  - File(s): `src/[layer]/[component].py`
  - Goal: Make Test 3.1 pass with minimal code
  - Details: [Implementation notes]

- [ ] **Task 3.4**: Implement [integration/glue code]
  - File(s): `src/[layer]/[integration].py`
  - Goal: Make Test 3.2 pass
  - Details: [Implementation notes]

**🔵 REFACTOR: Clean Up Code**
- [ ] **Task 3.5**: Refactor for code quality
  - Files: Review all new code in this phase
  - Goal: Improve design without breaking tests
  - Checklist:
    - [ ] Remove duplication (DRY principle)
    - [ ] Improve naming clarity
    - [ ] Extract reusable components
    - [ ] Add inline documentation
    - [ ] Optimize performance if needed

#### Quality Gate ✋

**⚠️ STOP: Do NOT proceed until ALL checks pass**

**TDD Compliance** (CRITICAL):
- [ ] **Red Phase**: Tests were written FIRST and initially failed
- [ ] **Green Phase**: Production code written to make tests pass
- [ ] **Refactor Phase**: Code improved while tests still pass
- [ ] **Coverage Check**: Test coverage meets requirements

**Build & Tests**:
- [ ] **Build**: Project builds/compiles without errors
- [ ] **All Tests Pass**: 100% of tests passing (no skipped tests)
- [ ] **Test Performance**: Test suite completes in acceptable time
- [ ] **No Flaky Tests**: Tests pass consistently (run 3+ times)

**Code Quality**:
- [ ] **Linting**: No linting errors or warnings
- [ ] **Formatting**: Code formatted per project standards
- [ ] **Type Safety**: Type checker passes (if applicable)
- [ ] **Static Analysis**: No critical issues from static analysis tools

**Security & Performance**:
- [ ] **Dependencies**: No known security vulnerabilities
- [ ] **Performance**: No performance regressions
- [ ] **Memory**: No memory leaks or resource issues
- [ ] **Error Handling**: Proper error handling implemented

**Documentation**:
- [ ] **Code Comments**: Complex logic documented
- [ ] **API Docs**: Public interfaces documented
- [ ] **README**: Usage instructions updated if needed

**Manual Testing**:
- [ ] **Functionality**: Feature works as expected
- [ ] **Edge Cases**: Boundary conditions tested
- [ ] **Error States**: Error handling verified

**Validation Commands**:
```bash
[Same as previous phases - customize for your project]
```

**Manual Test Checklist**:
- [ ] Test case 1: [Specific scenario to verify]
- [ ] Test case 2: [Edge case to verify]
- [ ] Test case 3: [Error handling to verify]

---

## ⚠️ Risk Assessment

| Risk | Probability | Impact | Mitigation Strategy |
|------|-------------|--------|---------------------|
| [Risk 1: e.g., LLM API rate limits] | Low/Med/High | Low/Med/High | [Specific mitigation steps] |
| [Risk 2: e.g., Model output variability] | Low/Med/High | Low/Med/High | [Specific mitigation steps] |
| [Risk 3: e.g., External API changes] | Low/Med/High | Low/Med/High | [Specific mitigation steps] |

---

## 🔄 Rollback Strategy

### If Phase 1 Fails
**Steps to revert**:
- Undo code changes in: [list files]
- Restore configuration: [specific settings]
- Remove dependencies: [if any were added]

### If Phase 2 Fails
**Steps to revert**:
- Restore to Phase 1 complete state
- Undo changes in: [list files]
- Database rollback: [if applicable]

### If Phase 3 Fails
**Steps to revert**:
- Restore to Phase 2 complete state
- [Additional cleanup steps]

---

## 📊 Progress Tracking

### Completion Status
- **Phase 1**: ⏳ 0% | 🔄 50% | ✅ 100%
- **Phase 2**: ⏳ 0% | 🔄 50% | ✅ 100%
- **Phase 3**: ⏳ 0% | 🔄 50% | ✅ 100%

**Overall Progress**: X% complete

### Time Tracking
| Phase | Estimated | Actual | Variance |
|-------|-----------|--------|----------|
| Phase 1 | X hours | Y hours | +/- Z hours |
| Phase 2 | X hours | - | - |
| Phase 3 | X hours | - | - |
| **Total** | X hours | Y hours | +/- Z hours |

---

## 📝 Notes & Learnings

### Implementation Notes
- [Add insights discovered during implementation]
- [Document decisions that deviate from original plan]
- [Record helpful debugging discoveries]

### Blockers Encountered
- **Blocker 1**: [Description] → [Resolution]
- **Blocker 2**: [Description] → [Resolution]

### Improvements for Future Plans
- [What would you do differently next time?]
- [What worked particularly well?]

---

## 📚 References

### Documentation
- [Link to relevant docs]
- [Link to API references]
- [Link to design mockups]

### Related Issues
- Issue #X: [Description]
- PR #Y: [Description]

---

## ✅ Final Checklist

**Before marking plan as COMPLETE**:
- [ ] All phases completed with quality gates passed
- [ ] Full integration testing performed
- [ ] Documentation updated
- [ ] Performance benchmarks meet targets
- [ ] Security review completed (no hardcoded secrets)
- [ ] API error handling verified
- [ ] All stakeholders notified
- [ ] Plan document archived for future reference

---

## 📖 TDD Example Workflow

### Example: Adding LLM Summarization Chain

**Phase 1: RED (Write Failing Tests)**

```python
# tests/unit/test_summarizer.py

import pytest
from unittest.mock import MagicMock, patch

def test_summarize_returns_valid_response():
    # Arrange
    summarizer = Summarizer(model="gpt-4")
    input_text = "Long article text here..."

    # Act
    result = summarizer.summarize(input_text)

    # Assert
    assert result is not None
    assert len(result) < len(input_text)
    # TEST FAILS - Summarizer class doesn't exist yet
```

**Phase 2: GREEN (Minimal Implementation)**

```python
# src/chains/summarizer.py

from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate

class Summarizer:
    def __init__(self, model: str = "gpt-4"):
        self.llm = ChatOpenAI(model=model)
        self.prompt = PromptTemplate.from_template(
            "Summarize the following text:\n\n{text}"
        )

    def summarize(self, text: str) -> str:
        chain = self.prompt | self.llm
        response = chain.invoke({"text": text})
        return response.content
        # TEST PASSES - minimal functionality works
```

**Phase 3: REFACTOR (Improve Design)**

```python
# src/chains/summarizer.py

import logging
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from tenacity import retry, stop_after_attempt, wait_exponential

logger = logging.getLogger(__name__)

class Summarizer:
    def __init__(self, model: str = "gpt-4", max_length: int = 500):
        self.llm = ChatOpenAI(model=model)
        self.max_length = max_length
        self.prompt = PromptTemplate.from_template(
            "Summarize in {max_length} chars:\n\n{text}"
        )

    @retry(stop=stop_after_attempt(3), wait=wait_exponential())
    def summarize(self, text: str) -> str:
        if not text or not text.strip():
            raise ValueError("Input text cannot be empty")

        try:
            chain = self.prompt | self.llm
            response = chain.invoke({
                "text": text,
                "max_length": self.max_length
            })
            return response.content
        except Exception as e:
            logger.exception("Summarization failed")
            raise
        # TESTS STILL PASS - improved code quality
```

### TDD Red-Green-Refactor Cycle Visualization

```
Phase 1: 🔴 RED
├── Write test for feature X
├── Run test → FAILS ❌
└── Commit: "Add failing test for X"

Phase 2: 🟢 GREEN
├── Write minimal code
├── Run test → PASSES ✅
└── Commit: "Implement X to pass tests"

Phase 3: 🔵 REFACTOR
├── Improve code quality
├── Run test → STILL PASSES ✅
├── Extract helper methods
├── Run test → STILL PASSES ✅
├── Improve naming
├── Run test → STILL PASSES ✅
└── Commit: "Refactor X for better design"

Repeat for next feature →
```

### Benefits of This Approach

**Safety**: Tests catch regressions immediately
**Design**: Tests force you to think about API design first
**Documentation**: Tests document expected behavior
**Confidence**: Refactor without fear of breaking things
**Quality**: Higher code coverage from day one
**Debugging**: Failures point to exact problem area

---

**Plan Status**: 🔄 In Progress
**Next Action**: [What needs to happen next]
**Blocked By**: [Any current blockers] or None

