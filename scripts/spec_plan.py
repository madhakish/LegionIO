#!/usr/bin/env python3
"""Print review-oriented RSpec candidates; never load Ruby or execute tests.

Python 3.9+, standard library only. This is a conservative path map, not coverage
analysis or a sandbox. A candidate suite may still have application side effects.
"""
import argparse
import json
from pathlib import Path

CONFIG = {'entry': 'lib/legion.rb',
 'groups': [('lib/legion/service',
             ['spec/legion/service*spec.rb'],
             'Boot/reload order crosses subsystem boundaries; never start a daemon as a unit '
             'test.'),
            ('lib/legion/cli',
             ['spec/cli/**/*_spec.rb', 'spec/legion/cli/**/*_spec.rb'],
             'Check both executable dispatch paths, Thor reserved names, JSON output and mutation '
             'boundaries.'),
            ('lib/legion/extensions',
             ['spec/legion/extensions/**/*_spec.rb'],
             'Check definition metadata, runner discovery and actor lifecycle without loading live '
             'extensions.'),
            ('lib/legion/api',
             ['spec/api/**/*_spec.rb', 'spec/legion/api/**/*_spec.rb'],
             'Use Rack test helpers; test auth/error envelopes without binding a server port.'),
            ('lib/legion/tools',
             ['spec/legion/tools/**/*_spec.rb'],
             'Check registry/discovery contracts and avoid embedding or model calls.')],
 'example': 'lib/legion/service.rb'}


def within(root, path):
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False


def plan(root, paths):
    root = Path(root).resolve()
    if not (root / CONFIG["entry"]).is_file():
        raise ValueError("not the expected repository root")
    specs, risks, unmatched, missing = set(), set(), [], set()
    for raw in paths:
        path = Path(raw)
        if path.is_absolute() or ".." in path.parts or not within(root, root / path):
            raise ValueError("changed paths must remain inside the repository")
        name = path.as_posix()
        candidates = set()
        if name.startswith("spec/") and name.endswith("_spec.rb"):
            candidates.add(name)
        if name.startswith("lib/") and name.endswith(".rb"):
            stem = path.stem
            candidates.update(p.relative_to(root).as_posix()
                              for p in (root / "spec").rglob(stem + "_spec.rb"))
        for prefix, patterns, risk in CONFIG["groups"]:
            if name.startswith(prefix):
                risks.add(risk)
                for pattern in patterns:
                    matched = list(root.glob(pattern))
                    if not matched:
                        missing.add(pattern)
                    candidates.update(p.relative_to(root).as_posix() for p in matched)
        valid = {p for p in candidates if (root / p).is_file()
                 and within(root, root / p) and not (root / p).is_symlink()}
        specs.update(valid)
        if not valid:
            unmatched.append(name)
    return {"spec_candidates": sorted(specs), "review_notes": sorted(risks),
            "unmapped_paths": sorted(set(unmatched)), "stale_patterns": sorted(missing),
            "full_suite_still_required": True, "executed": False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="+", help="repository-relative changed paths")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    try:
        result = plan(root, args.paths)
    except ValueError as error:
        parser.error(str(error))
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
