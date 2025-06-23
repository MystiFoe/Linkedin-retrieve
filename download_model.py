import os
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel, PeftConfig

import os
HF_TOKEN = os.getenv("HF_TOKEN")

def download_model():
    print("Starting model download...")

    os.makedirs("models", exist_ok=True)

    # 1️⃣ Base model
    base_model_name = "microsoft/phi-2"
    base_model_path = os.path.join("models", "phi-2")

    print(f"Downloading base model {base_model_name}...")
    tokenizer = AutoTokenizer.from_pretrained(base_model_name, token=HF_TOKEN)
    base_model = AutoModelForCausalLM.from_pretrained(base_model_name, token=HF_TOKEN)

    print(f"Saving base model to {base_model_path}...")
    tokenizer.save_pretrained(base_model_path)
    base_model.save_pretrained(base_model_path)

    # 2️⃣ PEFT adapter
    adapter_repo = "mystifoe/Comment-Generator"
    adapter_local_path = os.path.join("models", "comment-generator")

    print(f"Downloading PEFT adapter {adapter_repo}...")
    peft_config = PeftConfig.from_pretrained(adapter_repo, token=HF_TOKEN)
    peft_model = PeftModel.from_pretrained(base_model, adapter_repo, token=HF_TOKEN)

    print(f"Saving PEFT adapter to {adapter_local_path}...")
    peft_model.save_pretrained(adapter_local_path)

    print("✅ Model and adapter successfully downloaded and saved.")
    return True

if __name__ == "__main__":
    download_model()
