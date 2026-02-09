import os
# Force offline mode to prevent HuggingFace connection errors
os.environ["HF_HUB_OFFLINE"] = "1"

from langchain_community.vectorstores import FAISS
import os
# Force offline mode to prevent HuggingFace connection errors
os.environ["HF_HUB_OFFLINE"] = "1"

from langchain_huggingface import HuggingFaceEmbeddings

VECTOR_PATH = "vector_store/faiss_index"

def load_index():
    print("⏳ Loading index and embeddings...")
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    vector_db = FAISS.load_local(
        VECTOR_PATH,
        embeddings,
        allow_dangerous_deserialization=True
    )
    return vector_db

def search_sirl(question, vector_db=None, k=3):
    if vector_db is None:
        vector_db = load_index()

    results = vector_db.similarity_search(question, k=k)
    return results

if __name__ == "__main__":
    from rich.console import Console
    from rich.panel import Panel
    from rich.prompt import Prompt

    console = Console()
    db = load_index()

    console.print(Panel("🤖 [bold green]Welcome to the SIRL Search Assistant![/bold green]\nType 'exit' or 'quit' to stop.", title="System Ready"))

    while True:
        try:
            q = Prompt.ask("\n[bold cyan]Ask a question about the SIRL paper[/bold cyan]")
            if q.lower() in ['exit', 'quit']:
                break
            
            docs = search_sirl(q, vector_db=db)

            console.print(f"\n[bold yellow]🔍 Found {len(docs)} Relevant Sections:[/bold yellow]\n")
            for i, doc in enumerate(docs, 1):
                page_num = doc.metadata.get('page', 'Unknown')
                content = doc.page_content.strip()
                console.print(Panel(content, title=f"Result {i} (Page {page_num})", border_style="blue"))
                console.print()

        except KeyboardInterrupt:
            console.print("\n[bold red]Exiting...[/bold red]")
            break
