import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

print("🚀 Loading Mistral model pipeline...")

# Model setup
model_name = "mistralai/Mistral-7B-Instruct-v0.2"
device = "mps" if torch.backends.mps.is_available() else "cpu"

# Load tokenizer and model
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    device_map="auto",  # Let HF Accelerate handle it
    torch_dtype=torch.float16 if device == "mps" else torch.float32
)

# Load pipeline (no explicit device arg since we're using accelerate)
pipe = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer
)

print(f"✅ Mistral pipeline loaded via accelerate on {device}!")

# Sample prompt
prompt = "Explain retention and limit in reinsurance."

# Generate output
output = pipe(
    prompt,
    max_new_tokens=100,
    do_sample=False,
    temperature=0.7
)

print("\n🤖 Sample Output:")
print(output[0]["generated_text"])
