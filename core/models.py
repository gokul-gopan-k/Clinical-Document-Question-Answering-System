import torch
from langchain_huggingface import HuggingFaceEmbeddings, HuggingFacePipeline
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline, BitsAndBytesConfig
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Optimal for your RTX 3060
DEVICE = "cuda"
COMPUTE_DTYPE = torch.bfloat16 
EMBEDDING_MODEL_NAME = "NeuML/pubmedbert-base-embeddings" # Clinical standard
LLM_MODEL_NAME = "BioMistral/BioMistral-7B-DARE"

# shared globals 
embedding_model = None
llm_chain = None
auditor_chain = None
tokenizer = None
# Model Loading (Optimized for 6GB VRAM)
def load_models():
    global embedding_model, llm_chain, auditor_chain, tokenizer
    
    if embedding_model is None:
        logger.info("Loading Medical Embeddings...")
        embedding_model = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME)

    if llm_chain is None:
        logger.info("Loading BioMistral 7B in 4-bit...... This may take 2-3 minutes.")
        
        # 4-bit config to fit into ~5.5GB VRAM
        bnb_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_use_double_quant=True,
            bnb_4bit_compute_dtype=COMPUTE_DTYPE,
            llm_int8_enable_fp32_cpu_offload=False 
        )
        
        try:
            tokenizer = AutoTokenizer.from_pretrained(LLM_MODEL_NAME)
            # Add these fixes:
            tokenizer.pad_token = tokenizer.eos_token
            tokenizer.padding_side = "right" # Standard for Mistral/Llama
            CACHE_DIR = "E:/huggingface_cache"
            # Cap the model at 4.8GB to leave room for Embeddings + Windows OS
            max_mem = {0: "4.8GiB", "cpu": "16GiB"}
            # Adding a strict memory map to prevent any crash during loading
            model = AutoModelForCausalLM.from_pretrained(
                LLM_MODEL_NAME,
                quantization_config=bnb_config,
                device_map="auto",
                max_memory=max_mem,
                cache_dir=CACHE_DIR  # Forces download to E: drive
            )
            logger.info("Model object created successfully")
        except Exception as e:
            logger.error(f"FATAL ERROR DURING LOADING: {e}")
        logger.info("Creating pipeline...")
        pipe = pipeline(
            "text-generation",
            model=model,
            tokenizer=tokenizer,
            max_new_tokens=250,
            temperature=0.01, # Low temperature for medical precision
            repetition_penalty=1.15,
            return_full_text=False
        )
        
        llm = HuggingFacePipeline(pipeline=pipe)
        
        # Proper LCEL Chain
        prompt = ChatPromptTemplate.from_template(
            "<s>[INST] <<SYS>>\nYou are a clinical assistant. Use ONLY the context provided to answer. "
            "If the answer is not in context, say 'Information not found in protocol.' "
            "Example: Q: When is metformin stopped? A: Permanently discontinued if eGFR < 30 mL/min/1.73 m2.\n<</SYS>>\n\n"
            "Context: {context}\n\nQuestion: {question} [/INST]"
        )
        
        llm_chain = prompt | llm | StrOutputParser()

   
        auditor_prompt = ChatPromptTemplate.from_template(
            "<s>[INST] You are a Medical Auditor. Verify the following:\n{query} [/INST]"
        )
        auditor_chain = auditor_prompt | llm | StrOutputParser()
        logger.info("--- MODEL FULLY LOADED AND READY ---")
# Explicit public API
__all__ = ["load_models", "embedding_model", "llm_chain", "auditor_chain", "tokenizer"]
