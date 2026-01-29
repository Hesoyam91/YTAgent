import os
from fastapi import FastAPI
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_classic.agents import AgentExecutor
from langchain_classic.agents import create_react_agent
from langchain_classic import hub
from .rag_engine import get_song_context
from fastapi.middleware.cors import CORSMiddleware
from .yt_service import yt_provider
from .agent import agent_executor 

load_dotenv() # Carga tu GROQ_API_KEY desde un archivo .env

app = FastAPI()

# Definimos el Agente y sus herramientas
# ... (Aquí incluyes la lógica del Agente ReAct que perfeccionamos) ...
def tool_consultar_tendencia(query: str):
    """Consulta al modelo TFT para saber qué 'mood' musical viene a continuación."""
    # Aquí llamarías a model_tft.predict()
    return "La tendencia predicha para las próximas 2 horas es: Música de alta energía (Techno/Rock)."

def tool_buscar_cancion_especifica(query: str):
    """Busca en el RAG canciones que coincidan con la tendencia o el pedido del usuario."""
    # Usa el motor de búsqueda semántica en ChromaDB
    return get_song_context(query)

#Peticiones HTTP
@app.get("/api/v1/recommend")
async def get_ai_recommendation(user_query: str):
    # Paso 1: Obtener contexto real de tu cuenta
    musica_actual = yt_provider.get_user_vibe()
    
    # Paso 2: (Lo que haremos a continuación) 
    # Enviar user_query + musica_actual a Llama 3 mediante Groq
    
    return {
        "contexto_detectado": musica_actual,
        "mensaje": "Contexto cargado correctamente. ¿Listo para configurar el Agente de LangChain?"
    }

@app.get("/api/v1/chat")
async def chat_con_agente(pregunta: str):
    try:
       inputs = {"input": pregunta}
       response = agent_executor.invoke(inputs)
       return {"respuesta": response.get("output", "Sin respuesta")}
    except Exception as e:
        return {"error": str(e)}


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # En producción pon la URL de tu frontend
    allow_methods=["*"],
    allow_headers=["*"],
)