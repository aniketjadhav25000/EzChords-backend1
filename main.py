from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Get OpenAI API key
openai_api_key = os.getenv("OPENAI_API_KEY")

# Validate API key
if not openai_api_key:
    raise ValueError("OPENAI_API_KEY is not set in the environment")

# Initialize OpenAI client
client = OpenAI(api_key=openai_api_key)

# Initialize FastAPI app
app = FastAPI()

# CORS Middleware for frontend integration (adjust origins in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with ["https://your-frontend-domain.com"]
    allow_methods=["*"],
    allow_headers=["*"],
)

# Route to handle user questions
@app.post("/ask")
async def ask(request: Request):
    try:
        data = await request.json()
        question = data.get("question", "").strip()

        if not question:
            return {"answer": "Please enter a valid question."}

        # OpenAI chat completion
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful guitar tutor."},
                {"role": "user", "content": question}
            ]
        )

        return {"answer": response.choices[0].message.content.strip()}

    except Exception as e:
        return {"answer": f"An error occurred: {str(e)}"}
