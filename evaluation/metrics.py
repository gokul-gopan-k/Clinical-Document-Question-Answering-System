import torch
from core.models import auditor_chain
token_stats = {
    "input_tokens": 0,
    "output_tokens": 0,
    "num_queries": 0
}
# -----------------------------
# Evaluation  6-Auditor Micro-Service Logic
def get_binary_score(metric_name, input_a, input_b):
    """Pass 1: High-speed Scorer (1 token output)"""
    prompts = {
        "faithfulness": "Is this ACTUAL ANSWER supported ONLY by the CONTEXT? Answer 1 for Yes, 0 for No.",
        "relevance": "Does this ACTUAL ANSWER directly address the QUESTION? Answer 1 for Yes, 0 for No.",
        "precision": "Does the CONTEXT contain the exact information in the GOLD STANDARD? Answer 1 for Yes, 0 for No."
    }
    query = f"<s>[INST] {prompts[metric_name]}\nA: {input_a}\nB: {input_b}\nOutput ONLY '1' or '0'. [/INST]"
    query = f"<s>[INST] {prompts[metric_name]}\nA: {input_a}\nB: {input_b}\nOutput ONLY '1' or '0'. [/INST]"
    response = auditor_chain.invoke({"query": query},config={"max_new_tokens": 1})  #1 as binary audit
    return 1 if "1" in response else 0


def get_micro_reason(metric_name, input_a, input_b):
    """Pass 2: Targeted Reasoner (Triggered only on failure)"""
    torch.cuda.empty_cache() # Clear VRAM for the long explanation pass
    prompts = {
        "faithfulness": "Point out the specific sentence in the answer that is NOT in the PDF context.",
        "relevance": "Explain why the answer fails to address the user's specific clinical question.",
        "precision": "Identify the specific clinical fact from the Gold Standard that is missing in the retrieved context."
    }
    query = f"<s>[INST] {prompts[metric_name]}\nInput A: {input_a}\nInput B: {input_b} [/INST]"
    return auditor_chain.invoke({"query": query})

__all__ = ["get_binary_score", "get_micro_reason", "token_stats"]