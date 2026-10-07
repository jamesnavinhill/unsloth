# Run Notes — p0-1-verify-unsloth-2.6b

**Task**: T1 · Verify Unsloth trains LFM2.5-2.6B (Pairs with T2 template `notebooks/sft_lfm25_2_6b_v1.ipynb`)  
**Surface**: Google Colab (T4 / L4 GPU)  
**Notebook**: [`notebooks/sft_lfm25_2_6b_v1.ipynb`](../../notebooks/sft_lfm25_2_6b_v1.ipynb)  
**Status**: Ready for execution on Colab GPU

---

## 1. Objectives & Definition of Done (DoD)

- [ ] Execute 10-sample smoke training pass end-to-end on Colab GPU.
- [ ] Measure and record token throughput (`tokens_per_second` and `steps_per_second`).
- [ ] Measure and record peak VRAM consumption (`torch.cuda.max_memory_allocated()`).
- [ ] Measure and record Colab CU meter reading delta (`at_start` vs `at_end`) and hourly burn rate.
- [ ] Execute post-smoke 4-domain completion check (`blog`, `website copy`, `documentation`, `short story`).
- [ ] Document final Go / No-Go verdict for Phase 2 SFT.

---

## 2. Fallback Ladder Protocol (Decision D1)

1. **Primary Track**:
   - `FastLanguageModel.from_pretrained("LiquidAI/LFM2.5-2.6B", max_seq_length=4096, load_in_16bit=True)`
   - Attach 16-bit LoRA with target modules `q_proj, k_proj, v_proj, out_proj, in_proj, w1, w2, w3`.
2. **Fallback Step (a)**:
   - If Unsloth throws architecture loading error for `Lfm2ForCausalLM` at 2.6B:
   - Execute Liquid cookbook TRL/Axolotl path via Hugging Face `AutoModelForCausalLM` + `PeftModel`.
3. **Fallback Step (b)**:
   - If fallback (a) fails:
   - Switch target to `LiquidAI/LFM2.5-VL-3B` (officially supported by Unsloth, freeze vision tower).
   - Document model switch in `plan.md` change log.

---

## 3. Results Ledger

| Metric | Target / Spec | Measured | Status |
|---|---|---|---|
| GPU Hardware | T4 (15 GB) or L4 (24 GB) | — | Pending |
| Training Throughput | > 200 tok/s | — | Pending |
| Peak VRAM | < 14 GB (fits T4/L4) | — | Pending |
| Colab CU Burn Rate | ~1.6–3.5 CU/h | — | Pending |
| Final Train Loss | > 0.2 (no memorization) | — | Pending |
| Generation Integrity | Natural prose across 4 domains | — | Pending |

---

## 4. Execution Log

- **2026-10-07**: Run directory initialized. Notebook `sft_lfm25_2_6b_v1.ipynb` created with pinned versions, Colab Secrets integration, 16-bit LoRA config, response-loss masking, and CU tracking helper.
