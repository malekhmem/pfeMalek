import os
from transformers import AutoTokenizer, AutoModelForCausalLM, GenerationConfig
import torch
from config import Config

# Set your Hugging Face API token
HUGGINGFACE_TOKEN = Config.HUGGINGFACE_TOKEN
BASE_MODEL=Config.BASE_MODEL
MODEL_NAME = Config.MODEL_NAME
GENERATION_CONFIG = Config.GENERATION_CONFIG

tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL, token=HUGGINGFACE_TOKEN)
model = AutoModelForCausalLM.from_pretrained(MODEL_NAME, token=HUGGINGFACE_TOKEN,device_map="auto")

GENERATION_CONFIG['pad_token_id'] = tokenizer.eos_token_id

generation_config = GenerationConfig(**GENERATION_CONFIG)

