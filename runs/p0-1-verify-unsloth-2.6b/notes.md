# Run Notes — p0-1-verify-unsloth-2.6b

**Task**: T1 · Verify Unsloth trains LFM2.5-2.6B (Pairs with T2 template `notebooks/sft_lfm25_2_6b_v1.ipynb`)  
**Surface**: Google Colab (Tesla T4 GPU, 15.64 GB VRAM)  
**Notebook**: [`notebooks/sft_lfm25_2_6b_v1.ipynb`](../../notebooks/sft_lfm25_2_6b_v1.ipynb)  
**W&B Run**: [https://wandb.ai/navin_hill/huggingface/runs/huxz5tt6](https://wandb.ai/navin_hill/huggingface/runs/huxz5tt6)  
**Status**: `DONE (2026-10-07)` — VERDICT: PASS

---

## 1. Objectives & Definition of Done (DoD)

- [x] Execute 10-sample smoke training pass end-to-end on Colab GPU.
- [x] Measure and record token throughput (`62.86s` for 10 effective steps with batch 16).
- [x] Measure and record peak VRAM consumption (`5.35 GB` peak on T4 — only 34% of available VRAM).
- [x] Measure and record Colab CU meter reading delta (`0.20 CU` spent, burn rate `0.67 CU/h`).
- [x] Execute post-smoke 4-domain completion check (`blog`, `website copy`, `documentation`, `short story`).
- [x] Document final Go / No-Go verdict: **GO — Decision D1 primary track is verified.**

---

## 2. Key Findings & Diagnostic Audit

### 2.1 Model Architecture & Unsloth Native Support
* **Base Model**: `LiquidAI/LFM2.5-2.6B` loaded cleanly via `FastLanguageModel.from_pretrained(load_in_16bit=True)`.
* **LoRA Attachment**: All 8 target linear modules (`q_proj, k_proj, v_proj, out_proj, in_proj, w1, w2, w3`) attached successfully.
* **Trainable Parameters**: `20,135,936` out of `2,717,334,528` (0.7410% trainable).
* **Fallback Ladder**: Neither fallback (a) nor fallback (b) was required. The pure 2.6B dense text model is fully trainable natively.

### 2.2 Measured Hardware Telemetry
* **GPU**: Tesla T4 (Linux, CUDA 7.5 / Toolkit 13.0, PyTorch 2.11.0+cu130).
* **Peak VRAM**: **5.35 GB** at sequence length 4096! This leaves massive headroom (~10 GB free) on T4, and even more on an L4 (24 GB).
* **Training Speed**: 10 steps took 62.86 seconds (~6.2 s per effective batch 16 step).
* **Compute Cost**: 0.20 CU total consumption (0.67 CU/hour).

### 2.3 Optimization Insights for Full SFT Run
1. **LoRA Dropout Optimization**:
   Unsloth reported: `Dropout = 0 is supported for fast patching. You are using dropout = 0.05. Unsloth will patch all other layers, except LoRA matrices, causing a performance hit.`
   * *Resolution*: Set `lora_dropout = 0` in production SFT to re-enable Unsloth's fused Triton kernels for an additional ~15–25% throughput boost.
2. **Attention Mask in Generation**:
   Cell 10 reported: `The attention mask is not set and cannot be inferred from input because pad token is same as eos token.`
   * *Resolution*: Pass `attention_mask=inputs['attention_mask']` explicitly during inference/generation.
3. **Model Chain-of-Thought Trait**:
   During post-smoke generation, the model began exhibiting internal editorial reasoning (*"The user wants me to rewrite... I should avoid: Overly formal language... Let me write something that feels like..."*).
   * *Resolution*: For SFT training pairs, response formatting must clearly anchor on emitting the final human prose directly, or cleanly encapsulate reasoning traces.
4. **W&B Project Parameter**:
   The run logged to `navin_hill/huggingface` instead of `copyright` because HF Trainer defaults to `huggingface` unless `os.environ["WANDB_PROJECT"] = "copyright"` is explicitly exported before trainer instantiation. We will set this in the environment block.
