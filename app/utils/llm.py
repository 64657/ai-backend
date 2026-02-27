import httpx

# Ensure this matches your local Ollama port
OLLAMA_URL = "http://localhost:11434/api/generate"

async def generate_answer(prompt: str):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                OLLAMA_URL,
                json={
                    "model": "mistral",  # Changed from 'mistral' to match your setup
                    "prompt": prompt,
                    "stream": False
                },
                # Setting timeout to None is safest for slow local LLM generation
                timeout=None 
            )
            # Check for HTTP errors (like 404 if model not found)
            response.raise_for_status() 
            return response.json()["response"]
            
        except httpx.ConnectError:
            return "Error: Cannot connect to Ollama. Is the app running?"
        except httpx.ReadTimeout:
            return "Error: Ollama took too long. Check your system resources."