# SDD Index - Hotel Booking

## 1. Purpose

- This folder contains the Software Development Documentation for AI-assisted maintenance.
- Read files in the order below before changing requirements, business rules, APIs, schema, or diagrams.
- Folder prefixes are intentional and should stay stable for AI indexing.

## 2. Recommended Reading Order

| Order | File | Purpose |
| --- | --- | --- |
| 1 | `01-product/PRD.md` | Product scope, personas, functional requirements, NFR, screen inventory |
| 2 | `01-product/USE_CASE_CATALOG.md` | Complete use case inventory by role |
| 3 | `02-business/BUSINESS_PROCESS.md` | Business process index, journeys, state machines |
| 4 | `02-business/business-processes/07-business-rules-and-edge-cases.md` | Global business rules and edge cases |
| 5 | `02-business/business-processes/*.md` | Detailed business processes by module |
| 6 | `03-technical/TECH_SPEC.md` | Architecture, modules, flows, transactions, concurrency notes |
| 7 | `03-technical/API_CONTRACT.md` | API endpoints, request/response, access rules, errors |
| 8 | `03-technical/ENTITY_SCHEMA.md` | Entity schema, relationships, constraints, indexes |
| 9 | `04-diagrams/CORE_FLOW_DIAGRAMS.md` | Mermaid diagrams for core flows and ERD |
| 10 | `05-guides/AI_MAINTENANCE_GUIDE.md` | AI workflow, traceability checklist, guardrails |

## 3. Folder Structure

| Folder | Contents |
| --- | --- |
| `01-product/` | Product-facing requirements and use case catalog |
| `02-business/` | Business process index and module-level process specs |
| `03-technical/` | Technical specification, API contract, entity schema |
| `04-diagrams/` | Mermaid diagrams for AI and developer navigation |
| `05-guides/` | Maintenance guide for future AI agents |

## 4. Traceability Path

Use this chain for any feature:

```text
PRD requirement -> Use case -> Business process -> API contract -> Entity schema -> Diagram -> Implementation
```

## 5. Maintenance Rules

- Keep file names and folder prefixes stable unless reorganizing the entire SDD index.
- When adding a new feature, update all affected docs in the traceability path.
- When changing booking, availability, permissions, or delete behavior, update business rules and diagrams.
- After modifying docs/code, run `graphify update .` when permitted.

