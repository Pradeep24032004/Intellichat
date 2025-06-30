
import os
from dotenv import load_dotenv
from openai import OpenAI
import asyncio

# Load .env file
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key="write-your-openai-apikey")

# Async-compatible AI response function
async def get_ai_response(user_message: str) -> str:
    try:
        # Run blocking OpenAI call in async executor
        loop = asyncio.get_running_loop()
        response = await loop.run_in_executor(
            None,
            lambda: client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant in a chat room. Keep responses concise and friendly."},
                    {"role": "user", "content": user_message}
                ],
                max_tokens=150,
                temperature=0.7
            )
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"I'm sorry, I'm having trouble responding right now. Error: {str(e)}"
