from sql_generator import generate_query
from prompts import sql_prompt

def main():
    question = "What was our revenue by product in the New York region last month?"
    generated_sql = generate_query(question)
    print(generated_sql)

if __name__ == "__main__":
    main()
