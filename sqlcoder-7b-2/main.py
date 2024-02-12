from sql_generator import generate_query
from prompts import sql_prompt

def main():
    question = "What was our revenue by product in the New York region last month?"
    #prompt = sql_prompt[0]
    generated_sql, tokens_per_sec = generate_query(question)
    
    print(generated_sql)
    print("===========================================================")
    print(f"Tokens per second: {tokens_per_sec}")

if __name__ == "__main__":
    main()
