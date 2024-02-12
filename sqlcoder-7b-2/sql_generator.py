import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
import sqlparse
import time
from prompts import sql_prompt

# Initialize model and tokenizer
model_name = "defog/sqlcoder-7b-2"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    trust_remote_code=True,
    load_in_8bit=True,
    device_map="auto",
    use_cache=True,
)

def generate_query(question):
    prompt = sql_prompt[0]
    updated_prompt = prompt.format(question=question)
    inputs = tokenizer(updated_prompt, return_tensors="pt").to("cuda")
    
    start_time = time.time()  # Start timing

    generated_ids = model.generate(
        **inputs,
        num_return_sequences=1,
        eos_token_id=tokenizer.eos_token_id,
        pad_token_id=tokenizer.eos_token_id,
        max_new_tokens=400,
        do_sample=False,
        num_beams=1,
    )
    outputs = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)

    end_time = time.time()  

    # Calculate tokens per second
    num_tokens = len(tokenizer.encode(outputs[0]))
    elapsed_time = end_time - start_time
    tokens_per_second = num_tokens / elapsed_time

    torch.cuda.empty_cache()
    torch.cuda.synchronize()
    
    return sqlparse.format(outputs[0].split("[SQL]")[-1], reindent=True), tokens_per_second

