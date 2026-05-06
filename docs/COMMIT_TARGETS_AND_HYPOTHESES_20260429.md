# Commit Targets And Hypotheses

## Target A

Commit:
- `944e138bcf39e9236bbfd49d98f00fb45e6cea54`

Public claim:
- W4A4 MoE was using emulation instead of AITER on supported hardware.

Initial hypothesis:
- performance loss may have been caused less by raw math quality and more by wrong backend-path selection.

Questions:
- where is the routing decision made?
- what hardware/support predicate was wrong?
- is the fix in vLLM, AITER integration, or both?

## Target B

Commit:
- `6841f5dc77e9200a2fa45a4bf935b23bd843bf30`

Public claim:
- env flags added to disable dynamic MXFP4 quant and enable AITER tuned GEMMs for attention projection layers.

Initial hypothesis:
- some DeepSeek-family performance issues are controlled by path selection and override policy, not only by fundamental kernel limitations.

Questions:
- what exact layers are affected?
- what default path was underperforming?
- what benchmark evidence should prove improvement?

## Target C

Commit:
- `fb5635d3f90635ce9d1acbc975baab6e911a262b`

Public claim:
- MLA dual RMS norm fusion for DeepSeek/Kimi-K2.

Initial hypothesis:
- fusion opportunities on newer architectures are a meaningful performance frontier independent of quant pathing.

Questions:
- is this a true GPU-kernel-path improvement or a graph/fusion preparation change?
- where would traces show the gain?

## Target D

Commit:
- `ec8ab9d254d3b2e6b919a55277da599a7b9ab146`

Public claim:
- dynamic MXFP4 quantization for DeepSeek V2 projection layers.

Initial hypothesis:
- later bugs and tuning work may have cascaded from this earlier quant-path introduction.

Questions:
- which later fixes are cleanup versus real advance?
- does this create a benchmark split between correctness and speed?

## Cross-Target Working Thesis

The likely frontier is not "invent a new kernel from scratch first."

The likely frontier is:
- detect wrong path selection
- distinguish emulation from tuned kernel execution
- map quant format to actual backend route
- benchmark the exact token-throughput and latency deltas
- only then decide whether true kernel invention is warranted
