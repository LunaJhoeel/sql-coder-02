import sqlparse

def format_sql(generated_sql):
    formatted_sql = sqlparse.format(generated_sql, reindent=True)
    return formatted_sql

