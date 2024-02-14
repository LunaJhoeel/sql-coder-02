import runpod
from llama_cpp import Llama
from prompts import sql_prompt
from utils import format_sql


def initialize_model(model_path, seed=42, n_ctx=2048, n_batch=126):
    llm = Llama(
        model_path=model_path,
        n_gpu_layers=-1,  # GPU only
        seed=seed,
        n_ctx=n_ctx,
        n_batch=n_batch
    )
    return llm

model_path = "sqlcoder-7b-q5_k_m.gguf"
llm = initialize_model(model_path)

def generate_query(question, model):
    updated_prompt = sql_prompt[0].format(question=question)
    
    output = model.create_completion(
        prompt=updated_prompt,
        max_tokens=400,
        stop=["[SQL]"],
        echo=False
    )

    # Extract the generated text from the output dictionary
    generated_text = output['choices'][0]['text'] if 'choices' in output and len(output['choices']) > 0 else ''
    generated_sql = generated_text.split("[SQL]")[-1].strip()
    #formatted_sql = sqlparse.format(generated_sql, reindent=True)
    
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

