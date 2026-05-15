# Local Test Bootstrap Status

## Purpose

Track how far the lab got in making the cloned `vllm-upstream` test surfaces runnable inside the isolated AMD lab environment.

## What Was Added

Lab-local virtual environment:

- repository-local `.venv`

Lab-local requirement tracker:

- `benchmarks/local_test_env_requirements.txt`

Currently added:

- `tblib`
- `gguf`
- `pyzmq`
- `openai-harmony`

## What Was Verified

- modified test files compile cleanly with `python -m py_compile`
- the test bootstrap moved past the first `tblib` blocker
- the test bootstrap moved past the `gguf` blocker
- the test bootstrap moved past the `pyzmq` blocker

## Current Blocker

Shared upstream test infrastructure still pulls in:

- `pybase64`

through the `tests/conftest.py` import chain.

This means the lab can currently claim:

- syntax validation succeeded
- targeted upstream `pytest` execution is not yet fully available in the local clone

It cannot yet claim:

- full targeted pytest pass

## Why The Bootstrap Was Stopped Here

The lab's current priority is still:

- keep the first PR small
- avoid disappearing into full upstream environment recreation
- move the contribution lane forward

If needed later, the bootstrap can continue.
But at this stage the cost/benefit turned down sharply.

## Honest Read

The lab now has enough evidence to say:

- the first PR draft exists
- the edited files are syntax-valid
- the upstream test environment in this clone is broader than the narrow route/fusion lane needs

The lab does not yet have enough evidence to say:

- the touched pytest targets execute end-to-end locally
