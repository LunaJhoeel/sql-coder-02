import runpod
from llama_cpp import Llama
from prompts import sql_prompt
from utils import format_sql
from pydantic import BaseModel, ValidationError
from typing import List

class SQLRequest(BaseModel):
    question: str
    sql_schema: List[str]

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

def generate_query(sql_request: SQLRequest, model):
    combined_schema = ' '.join(sql_request.sql_schema)
    updated_prompt = sql_prompt[0].format(question=sql_request.question, sql_schema=combined_schema)
    
    output = model.create_completion(
        prompt=updated_prompt,
        max_tokens=400,
        stop=["[SQL]"],
        echo=False
    )

    generated_text = output['choices'][0]['text'] if 'choices' in output and len(output['choices']) > 0 else ''
    generated_sql = generated_text.split("[SQL]")[-1].strip()
    
    return format_sql(generated_sql)

def handler(job):
    job_input = job.get("input", {})
    try:
        sql_request = SQLRequest(**job_input)
    except ValidationError as e:
        return {"error": str(e)}

    generated_sql = generate_query(sql_request, llm)
    return generated_sql

runpod.serverless.start({"handler": handler})
