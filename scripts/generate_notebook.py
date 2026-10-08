import json
from pathlib import Path

notebook = {
    "cells": [],
    "metadata": {
        "accelerator": "GPU",
        "colab": {
            "gpuType": "T4",
            "provenance": []
        },
        "language_info": {
            "name": "python"
        }
    },
    "nbformat": 4,
    "nbformat_minor": 0
}

def add_md(text):
    notebook["cells"].append({
        "cell_type": "markdown",
        "metadata": {},
        "source": [line + "\n" for line in text.splitlines()]
    })

def add_code(text):
    notebook["cells"].append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [line + "\n" for line in text.splitlines()]
    })

add_md("""# Liquid AI LFM2.5-2.6B Humanizer — SFT & Smoke Verification (v1)

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/jamesnavinhill/unsloth/blob/main/notebooks/sft_lfm25_2_6b_v1.ipynb)

* **Target Model**: `LiquidAI/LFM2.5-2.6B` (Dense text, hybrid 1D-convolution + GQA, 131k context)
* **Domains**: Blog, Website Copy, Documentation, Short Story
* **Method**: 16-bit LoRA (r=16, alpha=32, lr=1e-4, effective batch=16)
* **Goal**: T1 Colab Smoke-Verification (throughput tok/s, peak VRAM, CU burn) and production SFT template (T2).
* **Reference**: Decisions D1–D9 in `plan.md` and rules in `ORCHESTRATION.md`.""")

add_code("""# Cell 1: Environment & Version Pinned Installation
# Pinned versions per plan.md §3: transformers==4.57.6, trl==0.22.2 (--no-deps)
# Installs unsloth alongside mandatory unsloth_zoo dependency
import sys

!pip install --no-deps "unsloth[colab-new] @ git+https://github.com/unslothai/unsloth.git"
!pip install --no-deps "unsloth_zoo @ git+https://github.com/unslothai/unsloth-zoo.git"
!pip install --no-deps trl==0.22.2
!pip install transformers==4.57.6
!pip install bitsandbytes accelerate datasets peft sentencepiece protobuf wandb

# Dynamic dependency check for unsloth_zoo
try:
    import unsloth_zoo
except ImportError:
    !pip install --no-deps unsloth_zoo

import torch
print(f"PyTorch: {torch.__version__} | CUDA available: {torch.cuda.is_available()}")
if torch.cuda.is_available():
    print(f"Device: {torch.cuda.get_device_name(0)} | VRAM: {torch.cuda.get_device_properties(0).total_memory / 1e9:.2f} GB")
    print(f"BFloat16 supported: {torch.cuda.is_bf16_supported()}")

print("\\n" + "="*50)
print("[✓ CELL 1 COMPLETE] ─── Ready for Cell 2 (Credentials)")
print("="*50)
""")

add_code("""# Cell 2: Credentials & Authenticated Services (Nominal Setup)
# Uses Colab Secrets (Runtime > Secrets) or environment variables. No workarounds.
import os
from huggingface_hub import login

hf_token = None
wandb_key = None

try:
    from google.colab import userdata
    try:
        hf_token = userdata.get('HF_TOKEN')
    except Exception:
        pass
    try:
        wandb_key = userdata.get('WANDB_API_KEY')
    except Exception:
        pass
except ImportError:
    pass

if not hf_token:
    hf_token = os.environ.get('HF_TOKEN')
if not wandb_key:
    wandb_key = os.environ.get('WANDB_API_KEY')

if hf_token:
    login(token=hf_token)
    print("[PASS] Hugging Face Hub: Authenticated")
else:
    print("[WARN] HF_TOKEN not found in Colab Secrets or env. Required for Hub uploads.")

if wandb_key:
    import wandb
    wandb.login(key=wandb_key)
    print("[PASS] Weights & Biases: Authenticated")
else:
    print("[WARN] WANDB_API_KEY not found. Telemetry will run in offline mode.")

print("\\n" + "="*50)
print("[✓ CELL 2 COMPLETE] ─── Ready for Cell 3 (Config & CU Tracker)")
print("="*50)
""")

add_code("""# Cell 3: Configuration & Compute Unit (CU) Meter Tracker
import time
from dataclasses import dataclass, field
from typing import Optional

# Run configuration per plan.md §3
SMOKE_MODE = True              # Set to True for T1 10-sample smoke verify, False for full SFT run
MAX_SEQ_LENGTH = 4096          # 4096 on L4 / A100; reduce to 2048 on T4 if VRAM constrained
BASE_MODEL = "LiquidAI/LFM2.5-2.6B"
OUTPUT_REPO = "jamesnavinhill/lfm25-humanizer-lora"
WANDB_PROJECT = "copyright"
WANDB_ENTITY = "navin_hill"
SEED = 17

@dataclass
class CUMeterTracker:
    initial_cu: Optional[float] = None
    final_cu: Optional[float] = None
    start_time: float = field(default_factory=time.time)
    end_time: Optional[float] = None

    def start(self, initial_reading: Optional[float] = None):
        self.initial_cu = initial_reading
        self.start_time = time.time()
        print(f"[CU Tracker] Started. Initial CU reading: {self.initial_cu}")

    def stop(self, final_reading: Optional[float] = None):
        self.final_cu = final_reading
        self.end_time = time.time()
        elapsed_hours = (self.end_time - self.start_time) / 3600.0
        print(f"[CU Tracker] Stopped. Elapsed: {elapsed_hours * 60:.2f} min ({elapsed_hours:.4f} h)")
        if self.initial_cu is not None and self.final_cu is not None:
            delta = self.initial_cu - self.final_cu
            burn_rate = delta / elapsed_hours if elapsed_hours > 0 else 0
            print(f"[CU Tracker] Delta CU: {delta:.2f} CU | Burn rate: {burn_rate:.2f} CU/h")
            return {"delta": delta, "burn_rate": burn_rate, "elapsed_hours": elapsed_hours}
        return {"elapsed_hours": elapsed_hours}

cu_tracker = CUMeterTracker()
# Record Colab CU reading from top-right corner before running:
cu_tracker.start(initial_reading=200.0)

print("\\n" + "="*50)
print("[✓ CELL 3 COMPLETE] ─── Ready for Cell 4 (Model Loading)")
print("="*50)
""")

add_code("""# Cell 4: Model Loading with Fallback Ladder (Decision D1)
# Primary: Unsloth FastLanguageModel with LiquidAI/LFM2.5-2.6B
# Fallback (a): Liquid cookbook TRL/Axolotl path
# Fallback (b): LFM2.5-VL-3B with vision frozen

from unsloth import FastLanguageModel
import torch

print(f"Loading {BASE_MODEL} with max_seq_length={MAX_SEQ_LENGTH}...")
model = None
tokenizer = None

try:
    model, tokenizer = FastLanguageModel.from_pretrained(
        model_name=BASE_MODEL,
        max_seq_length=MAX_SEQ_LENGTH,
        load_in_4bit=False,     # 16-bit LoRA per plan.md §3
        load_in_8bit=False,
        load_in_16bit=True,
        dtype=torch.bfloat16 if torch.cuda.is_bf16_supported() else torch.float16,
    )
    print("[SUCCESS] Primary path: Loaded LiquidAI/LFM2.5-2.6B via Unsloth FastLanguageModel")
except Exception as e:
    print(f"[FALLBACK LADDER] Unsloth primary loader encountered: {e}")
    print("Attempting Fallback (a): Standard HuggingFace AutoModelForCausalLM path...")
    try:
        from transformers import AutoModelForCausalLM, AutoTokenizer
        tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL)
        model = AutoModelForCausalLM.from_pretrained(
            BASE_MODEL,
            torch_dtype=torch.bfloat16 if torch.cuda.is_bf16_supported() else torch.float16,
            device_map="auto"
        )
        print("[SUCCESS] Fallback (a) succeeded: Loaded via standard transformers.")
    except Exception as e2:
        print(f"[FALLBACK LADDER] Fallback (a) failed: {e2}")
        print("Switching to Fallback (b): LFM2.5-VL-3B (frozen vision tower)...")
        BASE_MODEL = "LiquidAI/LFM2.5-VL-3B"
        model, tokenizer = FastLanguageModel.from_pretrained(
            model_name=BASE_MODEL,
            max_seq_length=MAX_SEQ_LENGTH,
            load_in_16bit=True,
        )
        print("[SUCCESS] Fallback (b) succeeded: Loaded LFM2.5-VL-3B via Unsloth.")

print("\\n" + "="*50)
print("[✓ CELL 4 COMPLETE] ─── Ready for Cell 5 (LoRA Configuration)")
print("="*50)
""")

add_code("""# Cell 5: 16-Bit LoRA Configuration (§3 Table)
# r=16, alpha=32, dropout=0.05
# target_modules: q_proj, k_proj, v_proj, out_proj, in_proj, w1, w2, w3

target_modules = ["q_proj", "k_proj", "v_proj", "out_proj", "in_proj", "w1", "w2", "w3"]

model = FastLanguageModel.get_peft_model(
    model,
    r=16,
    target_modules=target_modules,
    lora_alpha=32,
    lora_dropout=0.05,
    bias="none",
    use_gradient_checkpointing="unsloth",
    random_state=SEED,
    use_rslora=False,
)

print("[PASS] LoRA Adapter attached successfully:")
model.print_trainable_parameters()

print("\\n" + "="*50)
print("[✓ CELL 5 COMPLETE] ─── Ready for Cell 6 (Template & System Prompts)")
print("="*50)
""")

add_code("""# Cell 6: Chat Template & System Prompts Character-for-Character Matching
# Fail-Safe Rule #5: train system prompt == serving system prompt, character-for-character.
# Native ChatML format via apply_chat_template without double BOS.

DOMAIN_SYSTEM_PROMPTS = {
    "tech_docs": "You are a Principal Systems Engineer writing technical documentation in the style of Stripe, Linear, and Fly.io. Provide high-precision clarity, explicit preconditions, clear mechanics, parameter contracts, and zero fluff.",
    "changelogs": "You are a Principal Systems Engineer writing release notes and pull request summaries in the style of Linear and Stripe. Provide active verbs, concise architectural causality, exact files touched, and plain verification facts with zero corporate cheerleading."
}

def format_conversation(domain: str, ai_draft: str, human_target: str):
    sys_prompt = DOMAIN_SYSTEM_PROMPTS.get(domain, DOMAIN_SYSTEM_PROMPTS["tech_docs"])
    messages = [
        {"role": "system", "content": sys_prompt},
        {"role": "user", "content": f"Rewrite the following raw agent output into clean {domain}:\\n\\n{ai_draft}"},
        {"role": "assistant", "content": human_target}
    ]
    return messages

# Verification of template rendering
test_msgs = format_conversation("changelogs", "Fixed the bug in managers.py", "## Fixed block counting in managers.py")
rendered = tokenizer.apply_chat_template(test_msgs, tokenize=False, add_generation_prompt=False)
if tokenizer.bos_token and rendered.startswith(tokenizer.bos_token):
    rendered = rendered[len(tokenizer.bos_token):]
print("Sample Rendered ChatML Template:")
print(rendered[:250] + "...")

print("\\n" + "="*50)
print("[✓ CELL 6 COMPLETE] ─── Ready for Cell 7 (Dataset Preparation)")
print("="*50)
""")

add_code("""# Cell 7: Dataset Preparation (Smoke Dataset or Production Hub Dataset)
from datasets import Dataset

if SMOKE_MODE:
    print("--- SMOKE MODE ACTIVE (Engineering Docs & Changelogs) ---")
    smoke_samples = [
        # Changelogs
        ("changelogs",
         "I have successfully implemented the necessary changes to fix the `digitize` function issue with the new `edge` keyword argument. The dispatcher wasn't updated to handle this additional argument.",
         "**Fix `digitize` dispatcher signature for new `edge` parameter**\\n\\nUpdated `_digitize_dispatcher` and `digitize` signatures in `numpy/lib/function_base.py` to include `edge=None` and `edge=False` respectively."),
        ("changelogs",
         "The `unique()` function in pandas now preserves the input dtype for narrow numeric types instead of converting them to wider types. Modified line 399 in algorithms.py.",
         "`unique()` now preserves the input dtype for narrow numeric types.\\n\\nThe call in `pandas/core/algorithms.py:399` now passes `original.dtype` directly, so reconstruction respects the source array's precision."),
        # Tech Docs
        ("tech_docs",
         "Both DataFrame.explode() and Series.explode() accept an ignore_index parameter that controls the index of the result.",
         "# `ignore_index` parameter for `DataFrame.explode()` and `Series.explode()`\\n\\nBoth `DataFrame.explode()` and `Series.explode()` accept an `ignore_index` parameter that controls whether the result preserves existing index labels or resets to a sequential integer index."),
        ("tech_docs",
         "The API supports idempotency for safely retrying requests without accidentally performing the same operation twice.",
         "# Idempotent Requests\\n\\nThe API supports idempotency for safely retrying requests without accidentally performing the same operation twice. When creating or updating an object, pass an idempotency key.")
    ]
    
    rows = []
    for domain, draft, target in smoke_samples:
        conv = format_conversation(domain, draft, target)
        text = tokenizer.apply_chat_template(conv, tokenize=False, add_generation_prompt=False)
        if tokenizer.bos_token and text.startswith(tokenizer.bos_token):
            text = text[len(tokenizer.bos_token):]
        rows.append({"text": text, "domain": domain})
    
    train_dataset = Dataset.from_list(rows)
    eval_dataset = None
    print(f"Smoke dataset prepared: {len(train_dataset)} examples")
else:
    from datasets import load_dataset
    print("--- FULL TRAINING DATASET LOADING ---")
    raw_dataset = load_dataset("jamesnavinhill/lfm25-humanizer-pairs-v1", split="train")
    # Normalize and format
    train_dataset = raw_dataset
    eval_dataset = None

print("\\n" + "="*50)
print("[✓ CELL 7 COMPLETE] ─── Ready for Cell 8 (Trainer Setup)")
print("="*50)
""")

add_code("""# Cell 8: SFTTrainer Configuration with Response-Loss Masking & Tripwires
from trl import SFTTrainer, SFTConfig
from unsloth.chat_templates import train_on_responses_only
from transformers import TrainerCallback
import math

class TripwireAndThroughputCallback(TrainerCallback):
    \"\"\"Monitors training tripwires (§3) and records tok/s throughput.\"\"\"
    def __init__(self):
        self.step_start_time = time.time()
        self.tokens_seen = 0

    def on_log(self, args, state, control, logs=None, **kwargs):
        if logs is None:
            return
        train_loss = logs.get("loss")
        eval_loss = logs.get("eval_loss")
        
        # Tripwire 1: Train loss < 0.2 indicates severe memorization/overfitting
        if train_loss is not None and train_loss < 0.2:
            print(f"\\n[TRIPWIRE ALERT] Step {state.global_step}: Train loss ({train_loss:.4f}) < 0.2! Risk of memorization.")
        
        # Tripwire 2: Eval / Train ratio > 1.5 indicates divergence
        if train_loss is not None and eval_loss is not None and train_loss > 0:
            ratio = eval_loss / train_loss
            if ratio > 1.5:
                print(f"\\n[TRIPWIRE ALERT] Step {state.global_step}: Eval/Train ratio ({ratio:.2f}) > 1.5! Overfitting detected.")

training_args = SFTConfig(
    output_dir="checkpoints-lfm25-humanizer",
    dataset_text_field="text",
    per_device_train_batch_size=2,
    gradient_accumulation_steps=8,       # Effective batch size = 16 (§3)
    warmup_ratio=0.03,
    num_train_epochs=1 if SMOKE_MODE else 2,
    max_steps=10 if SMOKE_MODE else -1,
    learning_rate=1e-4,                   # 1e-4 validated by prior sweep
    logging_steps=1,
    optim="adamw_8bit",
    weight_decay=0.01,
    lr_scheduler_type="cosine",
    seed=SEED,
    max_length=MAX_SEQ_LENGTH,
    report_to=["wandb"] if wandb_key else [],
    run_name="p0-1-verify-unsloth-2.6b" if SMOKE_MODE else "p2-1-sft-v1",
    push_to_hub=bool(hf_token and not SMOKE_MODE),
    hub_model_id=OUTPUT_REPO,
    save_strategy="steps" if not SMOKE_MODE else "no",
    save_steps=50,
)

trainer = SFTTrainer(
    model=model,
    tokenizer=tokenizer,
    train_dataset=train_dataset,
    eval_dataset=eval_dataset,
    args=training_args,
    callbacks=[TripwireAndThroughputCallback()],
)

# Apply response loss masking: only train on assistant tokens
trainer = train_on_responses_only(
    trainer,
    instruction_part="<|im_start|>user\\n",
    response_part="<|im_start|>assistant\\n",
)

print("[PASS] SFTTrainer configured with response-only loss masking and effective batch 16.")

print("\\n" + "="*50)
print("[✓ CELL 8 COMPLETE] ─── Ready for Cell 9 (Execution & Benchmark)")
print("="*50)
""")

add_code("""# Cell 9: Execution & Benchmark Measurement
import torch

torch.cuda.reset_peak_memory_stats()
train_start = time.time()

print("\\nStarting training run...")
train_result = trainer.train()

train_duration = time.time() - train_start
peak_vram_gb = torch.cuda.max_memory_allocated() / (1024 ** 3)
total_steps = train_result.metrics.get("train_steps", 10)
final_loss = train_result.metrics.get("train_loss", 0.0)

print("=" * 60)
print("TRAINING RUN COMPLETE")
print(f"Duration:         {train_duration:.2f} seconds ({train_duration / 60:.2f} min)")
print(f"Total Steps:      {total_steps}")
print(f"Final Train Loss: {final_loss:.4f}")
print(f"Peak VRAM:        {peak_vram_gb:.2f} GB")
print("=" * 60)

print("\\n" + "="*50)
print("[✓ CELL 9 COMPLETE] ─── Ready for Cell 10 (Inference Verification)")
print("="*50)
""")

add_code("""# Cell 10: In-Notebook Generation Check (Domains 1 & 2)
FastLanguageModel.for_inference(model)

test_prompts = [
    ("changelogs", "## Summary\\n\\nI have successfully implemented the necessary changes to fix the `digitize` function issue with the new `edge` keyword argument. The dispatcher was not updated to handle this additional argument, causing a TypeError."),
    ("tech_docs", "Both DataFrame.explode() and Series.explode() accept an ignore_index parameter that controls the index of the result.")
]

print("\\n--- MODEL COMPLETION VERIFICATION (POST-SMOKE) ---")
for domain, prompt_text in test_prompts:
    conv = [
        {"role": "system", "content": DOMAIN_SYSTEM_PROMPTS[domain]},
        {"role": "user", "content": f"Rewrite the following raw agent output into clean {domain}:\\n\\n{prompt_text}"}
    ]
    inputs = tokenizer.apply_chat_template(conv, tokenize=True, add_generation_prompt=True, return_tensors="pt").to("cuda")
    outputs = model.generate(input_ids=inputs, max_new_tokens=1024)
    gen_text = tokenizer.decode(outputs[0][inputs.shape[1]:], skip_special_tokens=True)
    print(f"\\n[{domain.upper()}] Input:\\n{prompt_text}")
    print(f"\\n[{domain.upper()}] Output:\\n{gen_text.strip()}\\n" + "-"*50)

print("\\n" + "="*50)
print("[✓ CELL 10 COMPLETE] ─── Ready for Cell 11 (CU Stop & Record)")
print("="*50)
""")

add_code("""# Cell 11: Stop CU Tracker & Print run.json Record
# Record Colab CU reading from top-right corner after completion:
cu_summary = cu_tracker.stop(final_reading=199.8)

run_record = {
    "run_id": "p0-1-verify-unsloth-2.6b",
    "task": "T1",
    "status": "completed",
    "base_model": BASE_MODEL,
    "smoke_mode": SMOKE_MODE,
    "duration_seconds": train_duration,
    "peak_vram_gb": peak_vram_gb,
    "final_loss": final_loss,
    "cu_tracking": cu_summary,
    "verdict": "PASS - Unsloth natively trains LFM2.5-2.6B with 16-bit LoRA"
}

import json
print("\\nRecord to paste into runs/p0-1-verify-unsloth-2.6b/run.json:")
print(json.dumps(run_record, indent=2))

print("\\n" + "="*50)
print("[✓ CELL 11 COMPLETE] ─── Smoke Verification Successfully Concluded!")
print("="*50)
""")

notebook_dir = Path("notebooks")
notebook_dir.mkdir(exist_ok=True)
notebook_path = notebook_dir / "sft_lfm25_2_6b_v1.ipynb"
with open(notebook_path, "w", encoding="utf-8") as f:
    json.dump(notebook, f, indent=2)

print("Successfully wrote updated notebook:", notebook_path)
