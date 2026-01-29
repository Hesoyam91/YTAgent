const API_BASE_URL = "http://127.0.0.1:8000/api/v1";

export const sendMessageToAgent = async (message) => {
  const response = await fetch(`${API_BASE_URL}/chat?pregunta=${encodeURIComponent(message)}`);
  if (!response.ok) throw new Error("Error en la conexión con el servidor");
  return response.json();
};