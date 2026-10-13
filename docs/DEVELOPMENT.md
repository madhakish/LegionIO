# Fork development guide

This guide is for `madhakish/LegionIO`. Upstream architecture remains in [CLAUDE.md](../CLAUDE.md); this file is the canonical fork-local validation and automation guidance. Use the checked-out source and [lib/legion/version.rb](../lib/legion/version.rb) for current behavior/version, rather than historical example counts.

Agent entrypoints: [AGENTS.md](../AGENTS.md) and the [review-legion-runtime skill](../.agents/skills/review-legion-runtime/SKILL.md).

## Change routing

- Start at `lib/legion.rb` and `lib/legion/service.rb` for lifecycle changes. Preserve startup dependency order and reverse shutdown; exercise failures with subsystem doubles.
- `lib/legion/extensions/definitions.rb` owns default metadata. `remote_invocable`, `mcp_exposed`, `idempotent` and risk fields affect execution boundaries; trace builders and consumers, not only the declaration.
- CLI specs live in both `spec/cli/` and `spec/legion/cli/`. For changed commands inspect `exe/legion`, `exe/legionio`, and Thor registration; do not assume the README's mixed binary examples are equivalent.
- API behavior belongs in `spec/api/` using Rack helpers. JSON wrapper responses have symbol keys. MCP implementation is in a separate gem; do not invent an in-tree MCP implementation.

## Safe validation

Starting Legion can load extensions, connect transports, run migrations and initialize providers. Lite mode removes some infrastructure dependencies; it is not an offline or permission sandbox.

Python 3.9+ is sufficient for the read-only helper; it uses only the standard library:

```sh
python3 scripts/spec_plan.py lib/legion/service.rb
python3 -m unittest discover -s scripts -p 'test_*.py'
```

Pass repository-relative changed paths to the planner. It returns existing spec candidates, cross-component review notes, unmapped files and stale curated patterns. It never loads Ruby or executes a test. Basename matching is conservative; inspect the result and add relevant integration coverage. It does not establish coverage or make the Ruby suite safe to run.

With Ruby >= 3.4 and dependencies provisioned in an approved disposable environment, inspect the spec helper, run the targeted specs, then `bundle exec rspec` and non-mutating `bundle exec rubocop`. Run `bundle check` before installing missing gems. Dependency installation may fetch packages and execute build hooks. If Ruby, dependencies or isolation are absent, report the blocked command; do not label static checks as passing RSpec. Autocorrection (`rubocop -A`) is an explicit code change, not a prerequisite to reading or reviewing this fork.

## GitHub Actions recommendations (not activated)

Separate fast CLI/definition/API contract tests from RabbitMQ integration. Run any required RabbitMQ in a disposable job environment, with no production broker routes. Keep gem release, Docker publication and Homebrew dispatch out of validation jobs.

The checked-in workflows do not verify an available self-hosted runner. Direct jobs in this family use `ubuntu-latest`; reusable jobs call `LegionIO/.github` workflows at mutable `@main`. The inspected upstream workflows use `${{ inputs.runner || 'ubuntu-latest' }}` and these callers do not supply `runner`, so they inherit GitHub-hosted defaults at the reviewed snapshot. Before implementing the requested self-hosted policy, inspect the reusable workflows and the registered runner inventory; choose only verified labels. Do not guess OS/architecture labels or silently fall back to GitHub-hosted runners.

Because this is a public repository, never run unreviewed pull-request code on a personal persistent runner. Prefer an isolated ephemeral runner with no host mounts, production network access or reusable credentials. If only the personal runner exists, keep proposed validation disabled until that isolation is established. A trusted manual dispatch must validate an exact maintainer-reviewed commit; do not use `pull_request_target` to check out and execute a PR head. Minimize token permissions, pin reviewed actions/reusable workflows to immutable SHAs, set timeouts/concurrency, and separate test artifacts from secrets. Release, publishing and infrastructure changes need their own approval. No workflow files are changed by this development overlay.
