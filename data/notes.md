# General Notes

## Raw – Mirror of Reality

Stores the data exactly as it was received.
This layer acts as a reliable backup and a faithful snapshot of the original source.

No transformations, corrections, or structural changes should occur here.
The purpose of this layer is traceability and reproducibility.

---

## Staging – Technical Organization

Transforms raw data into a structurally consistent format.

This layer handles technical normalization and structural corrections, including:

* Inconsistent column names
* Incorrect data types
* Duplicate records
* Basic normalization and standardization

Staging ensures that data is technically coherent and ready for business-level processing.

---

## Curated – Business Logic Layer

Applies domain-specific business rules to structurally consistent data.

This layer is responsible for:

* Business validations
* Rule enforcement
* Domain-specific transformations
* Canonical formatting according to company standards

Curated data represents trusted, business-ready information.
