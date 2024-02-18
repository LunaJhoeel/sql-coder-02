sql_prompt = [
"""### Instructions
- Consider some metrics will need aggregation functions, 
such as calculating force using mass and acceleration.

### Task
Generate a SQL query to answer [QUESTION]{question}[/QUESTION]

### Database Schema
This query will run on a database whose schema is represented in this string:
{sql_schema}

### Answer
Given the database schema, here is the SQL query that answers [QUESTION]{question}[/QUESTION]
[SQL]
"""
]