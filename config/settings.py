import torch
DEVICE = "cuda"
COMPUTE_DTYPE = torch.bfloat16
EMBEDDING_MODEL_NAME = "NeuML/pubmedbert-base-embeddings"
LLM_MODEL_NAME = "BioMistral/BioMistral-7B-DARE"

token_stats = {
    "input_tokens": 0,
    "output_tokens": 0,
    "num_queries": 0
}
