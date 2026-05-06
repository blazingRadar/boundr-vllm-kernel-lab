# PR Review Packet Template

## Patch Class

- route fix
- config coverage
- benchmark tooling
- trace tooling
- fusion / kernel-adjacent

## Problem

- what is wrong today
- which gap class it belongs to

## Evidence

- commit lineage
- benchmark evidence
- trace evidence
- route evidence

## Proposed Change

- smallest code or config change that closes the issue

## Expected Runtime Effect

- native path reached
- fallback removed
- tuned coverage added
- instrumentation improved

## Risk

- correctness risk
- route risk
- unsupported-shape risk

## Reviewer Questions To Preempt

- does the native path already exist?
- is this a policy mistake or a missing kernel?
- what shape family benefits?
- what evidence proves the path changed?
