# Data Contract Runner

A Python standard-library CLI for checking CSV data against declarative JSON field contracts. Supports required fields, `string`, `integer`, `number`, and `boolean` types, plus allowed-value constraints. Reports row numbers and field-specific validation failures.

## Usage

```bash
python contracts.py examples/data.csv examples/contract.json
```

The example includes an intentionally invalid status and exits with status code 1. A valid file exits with code 0. Contracts have a `fields` array with objects containing `name`, `type`, optional `required`, and optional `allowed`.

## Tests

```bash
python -m unittest discover -s tests -v
```

Eight tests run on Python 3.10, 3.12, and 3.13 via GitHub Actions.

## Limitations

The tool validates individual field values but does not enforce uniqueness, foreign keys, cross-field business rules, or a formal JSON Schema specification. It is intended as a lightweight data quality gate.
