# NEW
import json
import logging
import gradio as gr

from evaluation.evaluator import evaluate_single_query
from core.retriever import ensemble_retriever, vectorstore
from evaluation.metrics import token_stats
from data.gold_dataset import GOLD_DATASET

logger = logging.getLogger(__name__)
# -----------------------------
#  Metrics Evaluation
# -----------------------------
def run_rag_benchmark(progress=gr.Progress()):
    # Ensemble Retriever
    global ensemble_retriever
    total_stats = {
        "Recall@k": 0, "Precision@k": 0, "ROUGE": 0, 
        "Ret_Lat": 0, "Ans_Lat": 0, "Triad": 0, "Faithfulness": 0,
    "Answer Relevancy": 0,"Context Precision": 0}
    all_individual_logs = [] 
    file_log_content = [] # List to store data for the .txt file
    num_queries = len(GOLD_DATASET)



    for i, item in enumerate(progress.tqdm(GOLD_DATASET, desc="Evaluating Protocol Queries")):
        metrics = evaluate_single_query(
            query=item["question"],
            retriever=ensemble_retriever,
            # llm=llm_chain,
            expected_ans=item["expected"],
            expected_page=item.get("source_page", 0), qn_no =i+1
        )

        # Accumulate Statistics
        total_stats["Recall@k"] += metrics["Recall@k"]
        total_stats["Precision@k"] += metrics["Precision@k"]
        total_stats["ROUGE"] += metrics["ROUGE-L"]
        total_stats["Ret_Lat"] += metrics["Retrieval_Latency"]
        total_stats["Ans_Lat"] += metrics["Answer_Latency"]
        total_stats["Triad"] += metrics["Triad_Score"]
        total_stats["Faithfulness"] += metrics["Faithfulness"]
        total_stats["Answer Relevancy"] += metrics["Answer Relevancy"]
        total_stats["Context Precision"] += metrics["Context Precision"]

        # Format UI Display Log
        status_icon = '✅' if metrics['Faithfulness'] and metrics['Answer Relevancy'] else '❌'
        log = f"Q{i+1}: {item['question']}\nVerdict: {status_icon}\n"
        log += f"F: {metrics['Faithfulness']} | R: {metrics['Answer Relevancy']} | P: {metrics['Context Precision']}\n"
        log += "-"*30
        all_individual_logs.append(log)

        #  Format .txt File Content 
        file_entry = f"q{i+1}) {item['question']}\n"
        file_entry += f"answer: {metrics.get('Generated_Answer', 'N/A')}\n"
        file_entry += f"context: {metrics.get('Context_Used', 'N/A')}\n"
        file_entry += "="*50 + "\n"
        file_log_content.append(file_entry)

    avg_input_tokens = token_stats["input_tokens"] / token_stats["num_queries"]
    avg_output_tokens = token_stats["output_tokens"] / token_stats["num_queries"]
    total_time = total_stats["Ret_Lat"] + total_stats["Ans_Lat"]
    throughput_qps = num_queries / total_time if total_time > 0 else 0
    #  Save the .txt file to  project directory
    with open("evaluation_logs.txt", "w", encoding="utf-8") as f:
        f.write("--- CLINICAL RAG EVALUATION LOG ---\n")
        f.write("\n".join(file_log_content))

    # Final Average Formatting
    report = "--- Average Performance Metrics ---\n"
    for k, v in total_stats.items():
        avg = v / num_queries
        report += f"{k}: {avg:.3f}\n"
    
    # -----------------------------
# Final Aggregated Metrics
# -----------------------------
    summary_metrics = {
    "num_queries": num_queries,
    "ContextRecall@6": round(total_stats["Recall@k"] / num_queries, 4),
    "ContextPrecision@6": round(total_stats["Precision@k"] / num_queries, 4),
    "Answer_Similarity_ROUGE-L": round(total_stats["ROUGE"] / num_queries, 4),

    "RAG_Triad": {
        "Faithfulness": round(total_stats["Faithfulness"] / num_queries, 4),
        "Answer Relevancy": round(total_stats["Answer Relevancy"] / num_queries, 4),
        "Precision": round(total_stats["Context Precision"] / num_queries, 4)
    },

    "Performance": {
        "avg_retrieval_latency_sec": round(total_stats["Ret_Lat"] / num_queries, 4),
        "avg_generation_latency_sec": round(total_stats["Ans_Lat"] / num_queries, 4),
        "throughput_qps": round(throughput_qps, 3)},
    "Efficiency": {
        "avg_input_tokens": int(avg_input_tokens),
        "avg_output_tokens": int(avg_output_tokens)}
    }

    logger.info(f"Completed evaluation for {num_queries} queries")
    logger.info(f"RAG Triad Score: {summary_metrics['RAG_Triad']}")
    # Save structured summary 
    with open("evaluation_summary.json", "w", encoding="utf-8") as f:
        json.dump(summary_metrics, f, indent=2)

    # Human-readable summary (for UI)
    summary_text = "--- Average Performance Metrics ---\n"
    for k, v in summary_metrics.items():
        summary_text += f"{k}: {v}\n"

    return {
        "per_query_logs": all_individual_logs,
        "summary": summary_metrics,
        "summary_text": summary_text
    }

def run_full_benchmark(progress=gr.Progress()):
    results = run_rag_benchmark(progress)
    return (
    "\n".join(results["per_query_logs"]),
    format_metrics_for_ui(results["summary"]))

def format_metrics_for_ui(summary):
    rag = summary["RAG_Triad"]
    perf = summary["Performance"]
    eff = summary["Efficiency"]

    return f"""
## 📊 Executive RAG Evaluation Summary

### 📁 Dataset
- **Evaluation Queries**: **{summary['num_queries']}**

### 🔎 Retrieval Quality (Hybrid BM25 + Dense)
- **Context Recall@6**: **{summary['ContextRecall@6']*100:.1f}%**
- **Context Precision@6**: **{summary['ContextPrecision@6']*100:.1f}%**
- **Answer Similarity (ROUGE-L)**: **{summary['Answer_Similarity_ROUGE-L']:.3f}**

### 🧪 RAG Triad (LLM-as-Judge)
- **Faithfulness**: ✅ **{rag['Faithfulness']*100:.1f}%**
- **Answer Relevancy**: ✅ **{rag['Answer Relevancy']*100:.1f}%**
- **Context Precision**: ✅ **{rag['Precision']*100:.1f}%**

### ⏱ Performance
- **Avg Retrieval Latency**: `{perf['avg_retrieval_latency_sec']} sec`
- **Avg Generation Latency**: `{perf['avg_generation_latency_sec']} sec`
- **Throughput**: `{perf['throughput_qps']} QPS`

### ⚡ Efficiency
- **Avg Input Tokens**: `{eff['avg_input_tokens']}`
- **Avg Output Tokens**: `{eff['avg_output_tokens']}`
"""

__all__ = ["run_rag_benchmark", "run_full_benchmark", "format_metrics_for_ui"]
