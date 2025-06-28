
try:
    import sentence_transformers
    print("sentence_transformers imported successfully")
    print(f"Version: {sentence_transformers.__version__}")
except ImportError as e:
    print(f"Import error: {e}")

try:
    from langchain_huggingface import HuggingFaceEmbeddings
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    print("HuggingFaceEmbeddings created successfully")
except Exception as e:
    print(f"HuggingFaceEmbeddings error: {e}")