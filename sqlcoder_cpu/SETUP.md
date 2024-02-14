# Creating a venv Environment for Scripts and Jupyter Notebooks
python3.9 -m venv venv

## Activating the Environment
source venv/bin/activate

## Installing the Requirements
pip install -r requirements.txt

## Download the model
curl -L "https://huggingface.co/defog/sqlcoder-7b-2/resolve/main/sqlcoder-7b-q5_k_m.gguf?download=true" -o /app/sqlcoder-7b-q5_k_m.gguf

## Test
python handler.py --test_input '{"input": {"question": "What was our revenue by product in the New York region last month?"}}'