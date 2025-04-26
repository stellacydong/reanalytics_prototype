# models/mistral_model_loader.py

from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import torch

def load_mistral_model(model_path="mistralai/Mistral-7B-Instruct-v0.2"):
    """
    Load a Mistral-7B model and prepare it for inference using HuggingFace pipeline.
    """
    device = "cuda" if torch.cuda.is_available() else "cpu"

    tokenizer = AutoTokenizer.from_pretrained(
        model_path,
        trust_remote_code=True
    )

    model = AutoModelForCausalLM.from_pretrained(
        model_path,
        torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
        device_map="auto",
        trust_remote_code=True
    )

    mistral_pipeline = pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
        device=0 if torch.cuda.is_available() else -1,
        max_new_tokens=300,
        temperature=0.3,
        top_p=0.9,
        do_sample=True,
        repetition_penalty=1.1
    )

    return mistral_pipeline

