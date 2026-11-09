# Public static release gate — reproducible DevOps example

This standalone **Python-standard-library** example demonstrates a secure
CI/CD publication pattern. It is independent of the private SaaS source, uses
no service accounts or tokens, and costs no external API calls.

## What you can inspect

- [stage.py](./stage.py) — accepts an explicit list of approved files, refuses
  directory traversal, unexpected extensions, symbolic links, missing assets,
  suspicious credentials, and files or bundles over a strict size budget.
- [test_stage.py](./test_stage.py) — 11 `unittest` scenarios, including
  normal delivery, negative cases and stale-artifact replacement.
- [GitHub Actions workflow](../../.github/workflows/engineering-proof.yml) —
  runs these tests on a hosted runner. Its status is real only when a run
  actually exists; see the
  [workflow history](https://github.com/Kvnbbg/kvnbbg/actions/workflows/engineering-proof.yml).

## Reproduce locally

Requires Python 3.10+.

```bash
python3 -m unittest discover -s examples/static-release-gate -p 'test_*.py' -v
python3 examples/static-release-gate/stage.py --help
```

To see a clean artifact with your own throwaway files:

```bash
mkdir -p /tmp/proof-source
printf '<h1>Public</h1>\n' > /tmp/proof-source/index.html
python3 examples/static-release-gate/stage.py /tmp/proof-source /tmp/proof-dist index.html
```

Do not put private content in a static artifact. **No scanner can guarantee
that every type of sensitive information is detected**: the positive allowlist
and review of each public asset remain the primary safety boundary.

## Evidence limits

Passing these public unit tests demonstrates the behavior of this **example
only**. It cannot establish that the private French Dev SaaS CI, Stripe payment
gates, live user experience, or security controls have passed. Those require
their own authorized checks and readable logs.

See the [dated incident report](../../docs/engineering-proof.md) for that
distinction. Updated: 9 November 2026.
