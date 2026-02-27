# Solve Clean Engine

An architecture-first data quality engine for deterministic rule execution and
controlled pipeline orchestration.

Organizations spend significant time and resources manually cleaning, validating,
and enriching customer and registration data. Inconsistent formats, incomplete fields, and 
rule-based validations often require repetitive work that slows down analytics and operational processes.

This project automates the cleaning, standardization, and enrichment of structured registration data, 
reducing manual effort and improving data reliability. Its layered and well-defined architecture ensures that business rules remain deterministic and testable, enabling the system to scale safely as complexity and data volume grow.

---

## 1.0 Project Motivation

While working as a freelance consultant cleaning spreadsheets, I noticed that I was repeatedly writing the same lines of code and utility functions to normalize text columns. Name fields, email addresses, and other registration data required similar validation and transformation patterns across different projects. This repetition led to the idea of building a reusable and structured solution.

The project started with a simple name-cleaning class and gradually evolved in complexity as new requirements emerged. What began as a small utility grew into a more organized system with clear boundaries between business rules, orchestration, and infrastructure concerns.

The specific gap this project fills is the absence of a lightweight, reusable, and architecturally disciplined framework for cleaning and enriching structured registration data. Instead of isolated scripts tailored to individua  spreadsheets, this project provides a consistent and scalable foundation for applying deterministic rules, standardizing data, and enabling controlled review workflows.

---


## 2.0 Architecture Overview

This project follows a layered architecture designed to enforce separation of concerns, deterministic rule execution, and long-term maintainability.

The core principle is simple: **business rules must remain pure, and orchestration must be explicit.**

### Layered Structure

- **domain**

Contains pure business rules and deterministic transformations.
No I/O, no logging, no database access. Fully testable in isolation.

---

- **services**

Coordinates domain logic over structured data (e.g., DataFrames).
Applies rules but does not create new business logic.

---

- **pipelines**

Orchestrates execution flow.
Manages state transitions, error propagation, and composition of services.

---

- **infra**

Handles external interactions such as file systems, databases, and logging backends.
Infrastructure concerns never leak into domain logic.

---

- **review**

Captures rule violations and anomalies for structured human inspection.
Observes and reports without mutating core business logic.

---

- **future**

Contains experimental modules and architectural ideas under validation before promotion to stable layers.

---

### Design Principles

- Deterministic domain logic

- Strict dependency direction

- Fail-fast behavior

- Explicit orchestration

- Testability by design

- Type safety and clear contracts

For detailed architectural rules and coding standards, see the [Style Guide](docs/style_guide.md)

---

## 3.0 Getting Started

Within the **projeto_geral** directory, there are two pipeline modules: pipeline1.py and pipeline2.py. The pipelines must be executed sequentially — first pipeline1.py, followed by pipeline2.py — for the full process to function correctly.

The images below illustrate examples from the spreadsheet "projeto_teste", highlighting common registration data issues such as inconsistent name formatting and structural inconsistencies. They also demonstrate the final result after applying both pipelines.

Additionally, the file "projeto_teste_logs_names" is generated during execution. This file contains flagged records that require manual review and adjustment before running the final cleaning stage.
















---

# 5️⃣ Quickstart (Minimal Working Example)

This is critical.

Show:

* Small code snippet
* Real input
* Real output

It must be executable in under 60 seconds.

If someone cannot see value quickly, they leave.

---

    
Show:

* Practical scenarios
* Before → After
* Logging example
* Review output example

If your project involves data quality, show logs and flags.

---

# 7️⃣ Design Principles

This is where excellence shows.

State clearly:

* Deterministic domain logic
* No I/O in business rules
* Fail-fast philosophy
* Test-driven design
* Strict typing

This shows engineering intent.

---

# 8️⃣ Testing & Quality Standards

Include:

* How to run tests
* Coverage target
* MyPy strict mode (if applicable)
* Linting tools

Professionals show quality metrics openly.

---

# 9️⃣ Project Structure

Show the tree.

This reduces cognitive load.

Example:

```
src/
  domain/
  services/
  pipelines/
  infra/
tests/
```

This gives immediate orientation.

---

# 🔟 Roadmap (Controlled Ambition)

This shows forward thinking.

Example:

* [ ] CLI interface
* [ ] Metrics export
* [ ] Packaging for pip

Avoid unrealistic promises.

---

# 1️⃣1️⃣ License

Always explicit.

No license = legally unusable.

---

# 1️⃣2️⃣ Contribution Guidelines (Even if Solo)

Even if you’re the only developer, include:

* Branch strategy
* Testing requirements
* Code standards

This signals production mindset.

# 4️⃣ Installation (Reproducibility First)

Must include:

* Python version requirement
* Virtual environment instructions
* How to install
* How to run tests

If installation fails, your credibility drops immediately.

---

# What Makes a README Excellent (Not Just Good)

An excellent README:

* Is structured, not verbose
* Explains architecture decisions
* Shows real outputs
* Demonstrates testability
* Communicates constraints
* Makes dependency flow explicit
* Shows maturity in trade-offs

---

# What Makes It Amateur

* Only installation instructions
* No problem context
* No architecture explanation
* No examples
* No tests mentioned
* No license
* No explanation of design intent

---

# The Real Goal

Your README should make a senior engineer think:

> “This person understands software architecture, not just Python.”

If you want, next we can:

* Design your README structure specifically for your project
* Or write the first professional draft together.
