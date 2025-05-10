import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
import os

MODEL_NAME = "mistralai/Mistral-7B-Instruct-v0.1"
SYSTEM_PROMPT = (
    "You are a helpful reinsurance treaty assistant. Your job is to read treaty wording and explain key coverage terms, exclusions, "
    "retention levels, limits, and any special conditions clearly and concisely for underwriters."
)

# ✅ Device auto-detection: prioritize CUDA, fall back to MPS or CPU
def get_best_device():
    if torch.cuda.is_available():
        return "cuda"
    elif torch.backends.mps.is_available():
        return "mps"
    else:
        return "cpu"

# ✅ Load model + tokenizer


def load_mistral_pipeline():
    # Set up device correctly
    device_str = "mps" if torch.backends.mps.is_available() else "cpu"
    device = torch.device(device_str)
    print(f"Device set to use: {device_str}")

    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_NAME,
        device_map=None,
        torch_dtype=torch.float16 if device.type == "cuda" else torch.float32,
    ).to(device)

    pipe = pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
        device=0 if device_str == "cuda" else -1,
        max_new_tokens=512,
        do_sample=True,
        temperature=0.7,
        top_k=50,
        top_p=0.95,
    )

    return pipe


# ✅ Reusable treaty summarization function
def summarize_treaty(treaty_text, pipe=None):
    if not pipe:
        pipe = load_mistral_pipeline()

    prompt = f"<s>[INST] {SYSTEM_PROMPT}\n\nTreaty Text:\n{treaty_text.strip()} [/INST]"

    output = pipe(prompt)[0]["generated_text"]
    return output.strip()

# 🔧 CLI test
if __name__ == "__main__":
    pipe = load_mistral_pipeline()
    treaty_text = (
        "This Excess of Loss Treaty attaches at $5,000,000 and covers 95% of losses up to $20,000,000 in excess of the attachment point. "
        "Subject to an annual aggregate deductible of $2,000,000 and limited to $30,000,000 per annum."
    )

    print("\n🤖 Summary Output:\n")
    summary = summarize_treaty(treaty_text, pipe=pipe)
    print(summary)
