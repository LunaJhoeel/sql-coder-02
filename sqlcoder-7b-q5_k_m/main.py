import runpod
from sql_generator import generate_query, llm
from prompts import sql_prompt

def handler(event):
    question = event.get("question", "")
    generated_sql = generate_query(question, llm)
    print(f"Generated SQL: {generated_sql}")
    return {"generated_sql": generated_sql}

runpod.serverless.start({"handler": handler})

