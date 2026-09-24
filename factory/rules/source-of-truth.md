# Source of Truth

## Purpose

This repository contains an existing airline mobile app prototype.

The existing application UI is the primary source of truth for the
customer experience.

The Software Factory must preserve the existing UI, interaction patterns,
navigation and visual behaviour unless a requirement explicitly asks for
a change.

## Rules

1. Do not redesign existing screens unless explicitly requested.

2. Do not replace existing UI components merely because another
   implementation is technically preferable.

3. Do not change navigation or user flows without identifying the
   product requirement that requires the change.

4. Historical scripts, patch scripts, debug scripts and experimental
   files are not automatically considered part of the production
   application.

5. Before changing code, identify the actual files and components
   responsible for the current behaviour.

6. Before implementing a feature, perform a blast-radius analysis.

7. The blast-radius analysis must identify:
   - Directly affected files
   - Dependent components
   - Screens/routes affected
   - User journeys affected
   - Data requirements
   - API/service requirements
   - Analytics impact
   - Tests affected
   - Potential regression areas

8. No implementation should begin until the blast-radius analysis
   is complete.

## Architecture Principle

The existing UI represents the desired customer experience.

The Software Factory is responsible for progressively building the
product, backend, APIs, data model, services and tests required to make
that experience functional.

The factory must build around the existing experience rather than
rebuilding the experience from scratch.

## Change Philosophy

Prefer:

    Existing UI
        ↓
    Understand
        ↓
    Specify
        ↓
    Assess impact
        ↓
    Implement
        ↓
    Test
        ↓
    Validate against existing UI

Avoid:

    New requirement
        ↓
    Rewrite existing application
