# lex-reconciliation

A [LegionIO](https://github.com/LegionIO) extension for drift detection and reconciliation.

Detects drift between expected (desired) state and actual (observed) state for managed resources,
persists drift events to a log, and runs periodic reconciliation cycles that emit events for
downstream runners to act on.

## Components

### `Runners::DriftChecker`

Detects drift between expected and actual state for one or more resources.

ruby
result = drift_checker.check(
  resource: 'my-service',
  expected: { status: 'running', replicas: 3 },
  actual:   { status: 'stopped', replicas: 1 },
  severity: 'high'
)
# => { drifted: true, drift_id: '...', differences: [...], summary: { total: 2 } }


### `DriftLog`

Persistent drift event log backed by `legion-data`.

ruby
Legion::Extensions::Reconciliation::DriftLog.record(
  resource:   'my-service',
  expected:   { status: 'running' },
  actual:     { status: 'stopped' },
  severity:   'high'
)

Legion::Extensions::Reconciliation::DriftLog.open_entries(severity: 'high')
Legion::Extensions::Reconciliation::DriftLog.summary


### `Actors::ReconciliationCycle`

Interval actor (default: every 5 minutes) that checks all configured targets and emits
`reconciliation.drift_detected` and `reconciliation.reconcile_requested` events.

Configure targets in settings:


{
  "extensions": {
    "reconciliation": {
      "interval": 300,
      "targets": [
        {
          "resource": "my-service",
          "expected": { "status": "running", "replicas": 3 },
          "severity": "high"
        }
      ]
    }
  }
}


## Installation

ruby
gem 'lex-reconciliation'


## License

MIT

## Development in this fork

Read the [LegionIO fork development guide](../../docs/DEVELOPMENT.md) before testing this bundled extension. Use synthetic desired/observed state and stub the persistence and event-publishing boundaries; do not start the reconciliation actor against live targets. The root `spec/` planner does not select this extension's nested suite, so inspect `spec/spec_helper.rb` in this directory and plan its tests separately.
