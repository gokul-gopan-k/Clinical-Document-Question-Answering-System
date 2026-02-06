import fitz 
from langchain_classic.retrievers import EnsembleRetriever
from langchain_community.retrievers import BM25Retriever
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_chroma import Chroma


from core.models import embedding_model

vectorstore = None
ensemble_retriever = None
# -----------------------------
# PDF Processing 
# -----------------------------
def process_pdf(pdf_file):
    global vectorstore, ensemble_retriever
    doc = fitz.open(pdf_file)
    docs_with_metadata = []
    
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=512, chunk_overlap=100,separators=["\n\n", "\n", ". ", " "])
    page_offset = 1  
    for i, page in enumerate(doc):
        page_text = page.get_text("text")
        # Split text but keep the page number in metadata
        chunks = text_splitter.split_text(page_text)
        # Attach page number to each chunk
        for chunk in chunks:
            docs_with_metadata.append(Document(page_content=chunk, metadata={"page": i - page_offset + 1})) 
    
    doc.close()

    #  Create Vector Store (Dense Search)
    vectorstore = Chroma.from_documents(docs_with_metadata, embedding_model)
    chroma_retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
    
    #  Create BM25 (Sparse Keyword Search)
    bm25_retriever = BM25Retriever.from_documents(docs_with_metadata)
    bm25_retriever.k = 3
    
    # Ensemble both using weights
    ensemble_retriever = EnsembleRetriever(
        retrievers=[bm25_retriever, chroma_retriever], 
        weights=[0.4, 0.6] 
    )
    
    return "PDF Hybrid Indexing Successful!"

__all__ = ["process_pdf", "vectorstore", "ensemble_retriever"]

