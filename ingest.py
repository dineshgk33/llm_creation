from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

PDF_PATH = "data/sirl.pdf"
VECTOR_PATH = "vector_store/faiss_index"

def ingest_pdf():
    print("📄 Loading SIRL PDF...")
    loader = PyPDFLoader(PDF_PATH)
    documents = loader.load()

    print("✂️ Splitting into chunks...")
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=150
    )
    chunks = splitter.split_documents(documents)

    print("🔢 Creating embeddings...")
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    print("💾 Storing vectors in FAISS...")
    vector_db = FAISS.from_documents(chunks, embeddings)
    vector_db.save_local(VECTOR_PATH)

    print("✅ SIRL PDF successfully indexed")

if __name__ == "__main__":
    ingest_pdf()
