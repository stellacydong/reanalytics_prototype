from typing import List
from langchain_core.language_models.llms import LLM
from pydantic import PrivateAttr

import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline

MODEL_NAME = "mistralai/Mistral-7B-Instruct-v0.1"

class MistralLLM(LLM):
    llm_device: str = None  # allowed public field

    # ✅ Private internal attributes (Pydantic-safe)
    _tokenizer: any = PrivateAttr()
    _model: any = PrivateAttr()
    _generator: any = PrivateAttr()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        print("\n🚀 Initializing Mistral LLM...")

        self.llm_device = (
            "mps" if torch.backends.mps.is_available()
            else "cuda" if torch.cuda.is_available()
            else "cpu"
        )
        print(f"Device set to use: {self.llm_device}")

        self._tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

        if self.llm_device == "mps":
            self._model = AutoModelForCausalLM.from_pretrained(
                MODEL_NAME,
                torch_dtype=torch.float16
            ).to("mps")
        else:
            from transformers import BitsAndBytesConfig
            quant_config = BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_use_double_quant=True,
                bnb_4bit_quant_type="nf4",
                bnb_4bit_compute_dtype=torch.float16,
            )
            self._model = AutoModelForCausalLM.from_pretrained(
                MODEL_NAME,
                quantization_config=quant_config,
                device_map="auto",
                trust_remote_code=True
            )

        self._generator = pipeline(
            "text-generation",
            model=self._model,
            tokenizer=self._tokenizer,
            max_new_tokens=512,
            temperature=0.7,
            do_sample=True
        )

    def _call(self, prompt: str, stop: List[str] = None) -> str:
        output = self._generator(prompt)[0]["generated_text"]
        return output[len(prompt):].strip()

    @property
    def _llm_type(self) -> str:
        return "mistral-custom"

# Local test
if __name__ == "__main__":
    llm = MistralLLM()
    prompt = "Summarize: The reinsurer shall pay the excess of loss above $10M up to $50M."
    print("\n🤖 Summary Output:\n")
    print(llm._call(prompt))

