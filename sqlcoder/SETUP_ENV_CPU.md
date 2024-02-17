# Creating a venv Environment for Scripts
python3.10 -m venv venv

## Activating the Environment
source venv/bin/activate

## Installing the Requirements
pip install -r requirements.txt

## Download the model
curl -L "https://huggingface.co/defog/sqlcoder-7b-2/resolve/main/sqlcoder-7b-q5_k_m.gguf?download=true" -o sqlcoder-7b-q5_k_m.gguf

## Test
python handler.py --test_input '{"input": {"question": "What was our revenue by product in the New York region last month?", "sql_schema": ["CREATE TABLE products (product_id INTEGER PRIMARY KEY, name VARCHAR(50), price DECIMAL(10,2), quantity INTEGER);", "CREATE TABLE customers (customer_id INTEGER PRIMARY KEY, name VARCHAR(50), address VARCHAR(100));", "CREATE TABLE salespeople (salesperson_id INTEGER PRIMARY KEY, name VARCHAR(50), region VARCHAR(50));", "CREATE TABLE sales (sale_id INTEGER PRIMARY KEY, product_id INTEGER, customer_id INTEGER, salesperson_id INTEGER, sale_date DATE, quantity INTEGER);", "CREATE TABLE product_suppliers (supplier_id INTEGER PRIMARY KEY, product_id INTEGER, supply_price DECIMAL(10,2));"]}}'
