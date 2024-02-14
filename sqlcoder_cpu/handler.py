import runpod
from llama_cpp import Llama
from prompts import sql_prompt
from utils import format_sql

# CPU
def initialize_model(model_path, seed=42, n_ctx=2048, n_batch=126):
    llm = Llama(
        model_path=model_path,
        n_gpu_layers=0,
        seed=seed,
        n_ctx=n_ctx,
        n_batch=n_batch,
        device='cpu'
    )
    return llm

model_path = "sqlcoder-7b-q5_k_m.gguf"
llm = initialize_model(model_path)

def generate_query(question, model):
    prompt = sql_prompt[0].format(question=question)
    
    estimated_prompt_tokens = len(prompt.split())
    
    max_tokens = 512 - estimated_prompt_tokens

    output = model.create_completion(
        prompt=prompt,
        max_tokens=max(max_tokens, 0),
        stop=["[SQL]"],
        echo=False
    )

    generated_text = output['choices'][0]['text'] if 'choices' in output and len(output['choices']) > 0 else ''
    generated_sql = generated_text.split("[SQL]")[-1].strip()
    
    return format_sql(generated_sql)

def handler(event):
    question = event.get("question", "")
    generated_sql = generate_query(question, llm)
    print("==================================================")
    print("GENERATED SQL:")
    print("==================================================")
    print(f"{generated_sql}")
    print("==================================================")
    return {"generated_sql": generated_sql}

runpod.serverless.start({"handler": handler})

