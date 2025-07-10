import os
from dotenv import load_dotenv

load_dotenv()
FIGMA_API_TOKEN = os.getenv("FIGMA_API_TOKEN")

HEADERS = {
    "X-Figma-Token": FIGMA_API_TOKEN
}
