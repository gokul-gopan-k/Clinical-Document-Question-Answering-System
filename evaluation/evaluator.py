import torch
import time, gc, re
from rouge_score import rouge_scorer
import logging

from core.models import llm_chain, tokenizer
from evaluation.metrics import get_binary_score, token_stats

logger = logging.getLogger(__name__)

def count_tokens(text, tokenizer):
    return len(tokenizer.encode(text))
def evaluate_single_query(query, retriever, expected_ans, expected_page, qn_no,top_k=3):
    """
    Complete evaluation for a single query:
    1. Retrieval Performance (Metadata-based)
    2. Generation Quality (Linguistic-based)
    3. RAG Triad (LLM-as-a-Judge based)
    """
    # Log the query for debugging
    logger.info(f"Evaluating query: {query}")
    # Clear memory before starting a new question
    torch.cuda.empty_cache()
    gc.collect()
    if tokenizer is None:
      raise RuntimeError("Tokenizer not initialized. Call load_models() first.")
    #  Retrieval 
    start_retrieval = time.time()
    # retrieve top 3 docs
    retrieved_docs = retriever.invoke(query)
    retrieval_latency = time.time() - start_retrieval

    # Calculate Retrieval Metrics 
    pages_found = [d.metadata.get('page') for d in retrieved_docs]

    # Check if the retrieved pages hit any of the expected pages 
    expected_list = expected_page if isinstance(expected_page, list) else [expected_page]
    recall_at_k = 1 if any(p in pages_found for p in expected_list) else 0
    # Count how many of the retrieved chunks match any page in gold list
    hits = sum(1 for p in pages_found if p in expected_list)

    precision_at_k = hits / len(pages_found) if pages_found else 0

    # ----- Generation -----
    start_gen = time.time()
    context_text = "\n\n".join([d.page_content for d in retrieved_docs])
    generated_answer = llm_chain.invoke({"context": context_text, "question": query})
    gen_latency = time.time() - start_gen

    # -----------------------------
    # Token Usage Tracking
    # -----------------------------

    input_text = context_text + query
    input_tokens = count_tokens(input_text, tokenizer)
    output_tokens = count_tokens(generated_answer, tokenizer)

    token_stats["input_tokens"] += input_tokens
    token_stats["output_tokens"] += output_tokens
    token_stats["num_queries"] += 1

    # Clean citations out of expected answer for fair ROUGE comparison
    clean_expected = re.sub(r"\\", "", expected_ans).strip()

    # ROUGE-L (Fast & CPU based)
    scorer = rouge_scorer.RougeScorer(['rougeL'], use_stemmer=True)
    rouge_scores = scorer.score(clean_expected, generated_answer)
    rouge_l = rouge_scores['rougeL'].fmeasure
    
    #  Triad Metrics 
    # Faithfulness: is generated answer supported by the retrieved context?
    faith = get_binary_score("faithfulness", generated_answer, context_text)

    # Relevance: does generated answer address the question?
    rel = get_binary_score("relevance", generated_answer, query)

    # Precision: does the retrieved context contain exact info from Gold answer?
    prec = get_binary_score("precision", context_text, clean_expected)
  

    triad_score = (faith + rel + prec) /3
    verdict = "PASS" if triad_score == 1 else "FAIL"

    # ----- Output -----
    metrics = {
        "Recall@k": recall_at_k,
        "Precision@k": precision_at_k,
        "ROUGE-L": rouge_l,
        "Faithfulness": faith, 
        "Answer Relevancy": rel,
        "Context Precision": prec,
        # "BERTScore F1": bert_f1,
        "Retrieval_Latency": retrieval_latency,
        "Answer_Latency": gen_latency,
        "Triad_Score": triad_score,
        "Generated_Answer": generated_answer, 
        "Context_Used": context_text,         
    }

    return metrics
__all__ = ["evaluate_single_query"]