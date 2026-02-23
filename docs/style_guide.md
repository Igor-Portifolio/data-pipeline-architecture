# Style Guide

This document defines the coding standards and architectural conventions for this project. Its purpose is to ensure
consistency, clarity, and long-term maintainability across all modules. It establishes rules for naming, documentation,
layering, contracts, and structural organization. These guidelines are normative: they reduce ambiguity in design
decisions, enforce clear separation of responsibilities, and make the codebase predictable for current and future
contributors.

## 1 Architectural Principles

The architecture of this project is built on strict separation of responsibilities and explicit contracts. The following principles are non-negotiable and apply to all layers of the system.

### 1.1 Single Responsibility

Each class must have one clearly defined responsibility.
If a class performs validation, transformation, orchestration, and persistence simultaneously, it is incorrectly designed. Responsibilities must be decomposed into smaller, composable units.

A class should answer a single question: *What fundamental problem does this component solve?*

---

### 1.2 Layered Separation

The system is organized into distinct layers. Each layer has a specific role and must not leak responsibilities across boundaries.

* **`domain/`**
  Contains pure business rules and transformations.
  No I/O, no logging, no database access, and no external integrations.
  Deterministic and fully testable in isolation.

* **`services/`**
  Implements composed use cases built from domain components.
  Coordinates multiple domain operations but does not perform low-level I/O.

* **`pipelines/`**
  Responsible for orchestration.
  Manages execution flow, state transitions, and error propagation across services.

* **`infra/`**
  Handles all external interactions (database access, file systems, APIs, logging backends).
  Infrastructure concerns must never leak into domain logic.

Cross-layer dependencies must follow this direction:
`domain → services → pipelines → infra`
Lower layers must not depend on higher ones.

---

### 1.3 Fail-Fast by Design

All components must validate inputs early and raise explicit exceptions when constraints are violated.

Silent failures, implicit corrections, or hidden fallbacks are prohibited.

Invalid input must result in:

* A clear exception type
* A deterministic failure
* A descriptive error message

The system favors explicit failure over implicit recovery.

---

## 2 Naming Conventions

Naming is a structural decision. It defines intent, abstraction level, and responsibility. All identifiers must be precise, consistent, and aligned with the architectural layer they belong to.

---

### 2.1 Language

All code must be written in English.

Domain-specific terms (e.g., CPF, CNPJ, IBGE) may be preserved when they represent stable business concepts. However, class names, function names, and variables must follow English grammatical structure.

Mixing languages within the same layer or module is not allowed.

---

### 2.2 File Names

* Must use `snake_case.py`.
* The file name must reflect a single, specific responsibility.
* The name should describe *what the module provides*, not how it is implemented.

Examples:

* `cpf_cleaner.py`
* `address_normalizer.py`
* `geography_validator.py`

The following generic names should be avoided:

* `utils.py`
* `helpers.py`
* `basic.py`
* `support.py`

Generic names introduce ambiguity and encourage responsibility accumulation.

---

### 2.3 Class Names

* Must use `PascalCase`.
* A class name must represent a stable concept within the system.
* A class must communicate *what it is*, not what it does internally.

Permitted suffixes when semantically appropriate:

* `Cleaner`
* `Validator`
* `Normalizer`
* `Service`
* `Pipeline`

Examples:

* `CPFCleaner`
* `AddressNormalizer`
* `GeographyValidator`
* `IBGEIngestionService`
* `TextBatchPipeline`

Avoid vague or procedural class names.

---

### 2.4 Function Names

* Must use `snake_case`.
* Must follow the structure: **verb + specific object**.
* The name must clearly express intent without requiring code inspection.

Acceptable examples:

* `normalize_phone`
* `validate_cpf`
* `standardize_state_code`
* `build_pipeline`
* `execute_pipeline`

The following generic verbs are prohibited:

* `process`
* `handle`
* `fix`
* `run`
* `do`

Ambiguous verbs reduce clarity and obscure responsibility.

---

### 2.5 Boolean Variables

Boolean names must read as logical assertions or questions.

Use prefixes such as:

* `is_`
* `has_`
* `should_`
* `can_`

Examples:

* `is_valid`
* `has_mask`
* `should_raise`
* `can_execute`

Boolean variables must not be named with neutral or ambiguous nouns.

----

## 3 Docstrings (Google Style – Mandatory)

All public classes and functions must include docstrings written in Google style. Docstrings define the **contract** of a component: what it guarantees, what it expects, and how it fails. They are not implementation notes.

The following structure must be used:

```python
"""
Short one-line summary.

Args:
    param: Description.

Returns:
    Description.

Raises:
    ExceptionType: Condition.
"""
```

---

### 3.1 General Rules

* Docstrings are **mandatory** for all public classes, methods, and functions.
* The first line must be a concise, single-sentence summary.
* The description must focus on behavior and guarantees, not internal mechanics.
* Implementation details (algorithms, regex patterns, internal steps) must not appear in docstrings.
* Type information must not be repeated; it is already defined in type hints.
* Examples should be included only when they add clarity or prevent ambiguity.

---

### 3.2 Purpose

Docstrings must allow a developer to understand:

* What the component does
* What inputs it expects
* What it returns
* Under what conditions it fails

A reader should be able to rely on the docstring without inspecting the implementation.

---

### 3.3 Class-Level Docstrings

For classes, the docstring must describe:

* The responsibility of the class
* Its role in the architecture (if relevant)
* Any guarantees or invariants it maintains

Example:

```python
class CPFCleaner:
    """
    Cleaner responsible for CPF normalization and validation.

    Ensures canonical 11-digit formatting and raises validation errors
    for invalid documents.
    """
```

---

### 3.4 Method and Function Docstrings

Function docstrings must describe:

* Expected input behavior (not internal parsing logic)
* Deterministic output behavior
* Explicit failure modes

Avoid vague descriptions. Every public function must define a clear behavioral contract.

---

Docstrings are part of the system’s interface. They are not optional commentary; they are executable documentation of the system’s design.

---




















