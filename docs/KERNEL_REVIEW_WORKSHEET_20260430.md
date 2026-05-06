# Kernel Review Worksheet

## Before Looking At Code

Ask:
- what operation is this?
- where is it on the model path?
- is it dominant FLOPs or a latency-sensitive side op?

## While Looking At Code

Ask:
- is this the real kernel or a wrapper?
- what shapes and dtypes does it support?
- what are the fallback conditions?
- what route conditions select it?

## Before Proposing A Speedup

Ask:
- is the problem math speed, memory movement, or wrong route?
- does a tuned version already exist?
- does a fused version already exist?
- is the kernel actually hot in traces?

## Valid Speedup Classes

- fewer launches
- less fallback
- less emulation
- better tuned-shape coverage
- lower memory movement
- better path selection

## Invalid First Move

- rewrite math before proving the current path is actually the bottleneck
