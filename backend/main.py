# backend/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from .agent import agent_executor

load_dotenv()
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/v1/chat")
async def chat_con_agente(pregunta: str):
    try:
        inputs = {"input": pregunta}
        response = agent_executor.invoke(inputs)
        return {"respuesta": response.get("output", "Sin respuesta")}
    except Exception as e:
        import traceback
        traceback.print_exc()
        return {"error": str(e)}