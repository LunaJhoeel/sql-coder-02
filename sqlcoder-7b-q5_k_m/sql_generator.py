import sqlparse
from model_loader import initialize_model
from prompts import sql_prompt

# Initialize the model
llm = initialize_model("sqlcoder-7b-q5_k_m.gguf")

prompt = sql_prompt[0]

def generate_query(question, model):
    updated_prompt = prompt.format(question=question)
    
    output = model.create_completion(
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

