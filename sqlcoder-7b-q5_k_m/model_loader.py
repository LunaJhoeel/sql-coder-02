from llama_cpp import Llama

def initialize_model(model_path, n_gpu_layers=-1, seed=42, n_ctx=2048):
    llm = Llama(
        model_path=model_path,
        n_gpu_layers=n_gpu_layers,
        seed=seed,
        n_ctx=n_ctx,
    )
    return llm

# Initialize the model
model_path = "sqlcoder-7b-q5_k_m.gguf"
llm = initialize_model(model_path)

