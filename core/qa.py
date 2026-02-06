from core.models import llm_chain
from core.retriever import ensemble_retriever, vectorstore

# -----------------------------
# Query Logic 
# -----------------------------
def ask_question(question):
    if llm_chain is None:
        return "System is still loading the 7B model. Please wait 1 minute and try again."
    if vectorstore is None:
        return "Please upload and process a PDF first."
    
    # Retrieve top 3 medical context chunks
    context_docs = ensemble_retriever.invoke(question)
    context_text = "\n\n".join([d.page_content for d in context_docs])
    
    # Run the optimized LCEL chain
    response = llm_chain.invoke({"context": context_text, "question": question})
    # Clean up the context for the UI display
    display_context = context_text.replace("\n\n", " [PARAGRAPH] ").replace("\n", " ").replace(" [PARAGRAPH] ", "\n\n")
    # Return both so the evaluator can use the context
    return response, display_context