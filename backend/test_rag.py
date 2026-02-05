import asyncio
from dotenv import load_dotenv
from app.services.rag_service import RagService

load_dotenv()

async def main():
    rag = RagService()
    
    print("Testing HuggingFace Embedding Generation...")
    # HF Inference API might be slow on cold start
    try:
        text = "주인공의 성격은 냉철하다."
        vector = await rag.generate_embedding(text)
        
        if vector:
            print(f"Success! Embedding length: {len(vector)}")
            print(f"First 5 dims: {vector[:5]}")
        else:
            print("Failed to generate embedding (Empty result). Check API Token or quota.")
            
    except Exception as e:
        print(f"Error during embedding: {e}")

    print("\nTesting Context Search...")
    try:
        context = await rag.search_relevant_context("주인공의 성격")
        print(f"Search Result:\n{context}")
    except Exception as e:
        print(f"Error during search: {e}")

if __name__ == "__main__":
    asyncio.run(main())
