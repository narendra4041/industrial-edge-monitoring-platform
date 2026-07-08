# ADR-001: Use Modular Monorepo Structure

## Status

Accepted

## Date

2026-07-08

## Context

The Industrial Edge Monitoring Platform contains multiple related components:

* backend API service
* Linux edge agent
* infrastructure definitions
* CI/CD workflows
* SDLC documentation
* deployment manifests
* production runbooks

These components are part of the same platform and should evolve together.

A decision is required on whether to maintain these components in separate repositories or in one modular monorepo.

## Decision

We will use a modular monorepo structure.

The repository will contain clearly separated top-level folders:

```text
industrial-edge-monitoring-platform/
├── backend/
├── edge-agent/
├── infrastructure/
├── docs/
├── .github/
├── README.md
└── CHANGELOG.md
```

Each component will have its own internal structure, dependencies, tests, and documentation.

## Alternatives Considered

### Option 1: Separate repositories

Each component could have its own repository:

* backend repo
* edge-agent repo
* infrastructure repo
* documentation repo

Advantages:

* independent release lifecycle
* strict ownership boundaries
* smaller repositories

Disadvantages:

* more difficult for a portfolio project
* more coordination overhead
* harder to understand complete system architecture
* duplicated documentation and configuration
* more complex CI/CD setup at the beginning

### Option 2: Single unstructured repository

All files could be placed in one repository without clear modular boundaries.

Advantages:

* simple initial setup

Disadvantages:

* poor maintainability
* unclear ownership
* harder to scale
* difficult to test and deploy components independently

### Option 3: Modular monorepo

One repository with clear component boundaries.

Advantages:

* complete platform is visible in one place
* easier local development
* easier interview explanation
* shared documentation
* simpler initial CI/CD
* clear separation through folders
* supports future independent deployment

Disadvantages:

* repository can grow large over time
* CI/CD must be designed carefully to avoid unnecessary builds
* component boundaries must be respected

## Consequences

The project will use a modular monorepo.

Each major component must stay inside its own folder.

Backend code must not be mixed with edge-agent code.

Infrastructure code must stay under the infrastructure folder.

Documentation must stay under the docs folder.

This decision supports a production-style structure while keeping the project understandable and manageable.

## Related Requirements

* NFR-020: Layered Architecture
* NFR-021: Code Quality
* NFR-027: CI/CD
* NFR-032: Architecture Documentation
* NFR-033: Developer Documentation
