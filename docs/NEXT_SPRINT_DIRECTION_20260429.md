# Next Sprint Direction

## Updated Priority

1. one real ROCm trace
2. retroactive launch-gap packet
3. model-shape to tuned-config diffing
4. only then deeper tuning infrastructure

## Immediate Best Move

If compute arrives first:
- run one real DeepSeek-family ROCm trace

If compute does not arrive first:
- build the retroactive v1 packet for:
  - DeepSeek-V3
  - Kimi-K2
  - Qwen3-MoE

## What Not To Do

- do not expand into broad CUDA parity analysis
- do not promise upstream PR automation in v1
- do not treat tuning as the thesis when the public commit set says otherwise
