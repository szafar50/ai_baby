# backend/src/local_functions.py
import httpx
import logging

# Configure logging without emojis
logging.basicConfig(
    level=logging.INFO,
    format='[%(levelname)s] %(name)s: %(message)s'
)
logger = logging.getLogger(__name__)

WARMUP_MODELS = ["llama3", "mistral", "phi3:mini", "qwen:1.8b"]
OLLAMA_BASE_URL = "http://localhost:11434/api/generate"

async def warm_up_models():
    """
    Warm up Ollama models asynchronously.
    """
    logger.info("[INFO] Starting model warm-up...")

    async with httpx.AsyncClient(timeout=15.0, limits=httpx.Limits(max_connections=3)) as client:
        for model in WARMUP_MODELS:
            try:
                logger.info(f"[INFO] Warming up {model}...")
                response = await client.post(
                    OLLAMA_BASE_URL,
                    json={
                        "model": model,
                        "prompt": "hi",
                        "stream": False
                    }
                )

                if response.status_code == 200:
                    logger.info(f"[OK] {model} is warm and ready!")
                else:
                    logger.warning(f"[WARN] {model} responded with status {response.status_code}")
            except httpx.ConnectError:
                logger.error(f"[ERROR] Failed to connect to Ollama for {model}. Is 'ollama serve' running?")
            except httpx.ReadTimeout:
                logger.error(f"[ERROR] {model} warm-up timed out after 15s")
            except Exception as e:
                logger.error(f"[ERROR] Unexpected error for {model}: {e}")

    logger.info("[INFO] Model warm-up complete!")