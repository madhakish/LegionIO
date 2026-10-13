# AGENTS.md

Instructions for AI agents working in this repository.

## Pre-Commit Requirements

Before publication, run the full RSpec suite and non-mutating RuboCop in the isolated environment described in `docs/DEVELOPMENT.md`; report blockers explicitly.

## Repository Context

This is the primary gem (`legionio`) of the LegionIO framework. See `CLAUDE.md` for full architecture, file map, and conventions.

## Fork-local workflow

Read [docs/DEVELOPMENT.md](docs/DEVELOPMENT.md) for canonical validation boundaries and the repository-specific helper. Use the `review-legion-runtime` skill in `.agents/skills/` for this review workflow.
