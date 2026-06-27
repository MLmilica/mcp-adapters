import asyncio
import os
from dotenv import load_dotenv  

load_dotenv()

async def main():
    print("Hello from mcp-adapters!")
    print(os.getenv("OPENAI_API_KEY"))


if __name__ == "__main__":
    asyncio.run(main())
