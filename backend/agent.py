# backend/agent.py
from langchain_groq import ChatGroq
from langchain_classic.agents import AgentExecutor, create_react_agent
from langchain_classic import hub
from langchain_classic.prompts import PromptTemplate
from .tools import (
    obtener_historial_reciente,
    listar_mis_playlists,
    buscar_playlist_por_nombre,
    ver_canciones_de_playlist,
    buscar_canciones,
    obtener_canciones_mas_escuchadas,
    recomendar_canciones_similares
)
from dotenv import load_dotenv

load_dotenv()

# Template personalizado con TODAS las variables requeridas
REACT_PROMPT_TEMPLATE = """Responde la siguiente pregunta lo mejor que puedas. Tienes acceso a las siguientes herramientas:

{tools}

Usa el siguiente formato:

Question: la pregunta de entrada que debes responder
Thought: siempre debes pensar qué hacer
Action: la acción a tomar, debe ser una de [{tool_names}]
Action Input: la entrada para la acción (SOLO el valor, sin formato adicional)
Observation: el resultado de la acción
... (este Thought/Action/Action Input/Observation puede repetirse N veces)
Thought: Ahora sé la respuesta final
Final Answer: la respuesta final a la pregunta original de entrada

REGLAS IMPORTANTES para Action Input:
- Si la herramienta requiere un número: usa SOLO el número (ejemplo: 10)
- Si la herramienta requiere texto: usa SOLO el texto (ejemplo: wenardo)
- NO uses formato "variable = valor" ni explicaciones
- Para listar_mis_playlists: usa None

Comienza!

Question: {input}
Thought:{agent_scratchpad}"""

def inicializar_agente():
    llm = ChatGroq(
        model_name="llama-3.3-70b-versatile",
        temperature=0
    )
    
    tools = [
        obtener_historial_reciente,
        listar_mis_playlists,
        buscar_playlist_por_nombre,
        ver_canciones_de_playlist,
        buscar_canciones,
        obtener_canciones_mas_escuchadas,
        recomendar_canciones_similares
    ]
    
    # Crear prompt con partial_variables
    prompt = PromptTemplate(
        template=REACT_PROMPT_TEMPLATE,
        input_variables=["input", "agent_scratchpad"],
        partial_variables={
            "tools": "\n".join([f"{tool.name}: {tool.description}" for tool in tools]),
            "tool_names": ", ".join([tool.name for tool in tools])
        }
    )
    
    agent = create_react_agent(llm, tools, prompt)
    
    return AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        handle_parsing_errors=True,
        max_iterations=8,
        early_stopping_method="generate"
    )

agent_executor = inicializar_agente()