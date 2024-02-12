import torch
from llama_cpp import Llama
import sqlparse
from prompts import sql_prompt

llm = Llama(
    model_path="sqlcoder-7b-q5_k_m.gguf",
    n_gpu_layers=-1,
    seed=42,
    n_ctx=2048,
)

prompt = sql_prompt[0]


def generate_query(question):
    updated_prompt = prompt.format(question=question)
    
    output = llm.create_completion(
        prompt=updated_prompt,
        max_tokens=400,
        stop=["[SQL]"],
        echo=False
    )

    # Extract the generated text from the output dictionary
    generated_text = output['choices'][0]['text'] if 'choices' in output and len(output['choices']) > 0 else ''

    # Process and format the generated output
    generated_sql = generated_text.split("[SQL]")[-1].strip()
    formatted_sql = sqlparse.format(generated_sql, reindent=True)

    return formatted_sql

def generate_query(question):
    updated_prompt = prompt.format(question=question)
    
    output = llm.create_completion(
        prompt=updated_prompt,
        max_tokens=400,
        stop=["[SQL]"],
        echo=False
    )

    # Extract the generated text from the output dictionary
    generated_text = output['choices'][0]['text'] if 'choices' in output and len(output['choices']) > 0 else ''

    # Process and format the generated output
    generated_sql = generated_text.split("[SQL]")[-1].strip()
    formatted_sql = sqlparse.format(generated_sql, reindent=True)
    
    return formatted_sql

