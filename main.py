
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from search import search_sirl

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Hello World - Backend is Running!"}

@app.get("/search")
async def search_endpoint(query: str):
    if not query:
        raise HTTPException(status_code=400, detail="Query is required")
    
    try:
        results = search_sirl(query)
        formatted_results = []
        for doc in results:
            formatted_results.append({
                "content": doc.page_content,
                "page": doc.metadata.get("page", "Unknown")
            })
            
        return {
            "results": formatted_results,
            "answer": None # Explicitly returning None to indicate no LLM answer
        }
    except Exception as e:
        print(f"Error during search: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
