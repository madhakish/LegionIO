---
name: review-legion-runtime
description: Plan and validate changes to LegionIO boot, CLI, extension definitions and API contracts without starting a daemon.
---

Read [the fork development guide](../../../docs/DEVELOPMENT.md) for the concrete source/spec map and validation boundaries. Keep the architecture reference in `CLAUDE.md`; do not duplicate it here.

1. Identify changed behavior and read the implementation plus the relevant spec helper before proposing execution.
2. Run `python3 scripts/spec_plan.py lib/legion/service.rb` from the repository root and substitute the actual changed paths. Review every warning; this is planning/static validation only.
3. Add focused positive and negative behavioral tests for the change. Use the guide's component-specific contracts and synthetic fixtures.
4. Execute only in the isolated environment described by the guide. Report the exact tests run, commands blocked, remaining integration gaps and any documentation drift supported by source.

Stop before live service access, credentials, publication or host configuration changes; a review task does not authorize those actions.
