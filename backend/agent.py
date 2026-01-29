from langchain_groq import ChatGroq
from langchain_classic.agents import AgentExecutor
from langchain_classic.agents import create_react_agent
from langchain_classic import hub
from .tools import obtener_historial_usuario, buscar_musica
from dotenv import load_dotenv

# CARGA LAS VARIABLES DEL .ENV
load_dotenv()

def inicializar_agente():
    # 1. Configurar el modelo (Llama 3 vía Groq)
    llm = ChatGroq(model_name="llama-3.3-70b-versatile", temperature=0)

    # 2. Definir las herramientas disponibles
    tools = [obtener_historial_usuario, buscar_musica]

    # 3. Pull del prompt estándar de ReAct
    prompt = hub.pull("hwchase17/react")

    # 4. Crear el agente
    agent = create_react_agent(llm, tools, prompt)
    
    # 5. Ejecutor del agente (el que gestiona el bucle de pensamiento)
    return AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)

agent_executor = inicializar_agente()