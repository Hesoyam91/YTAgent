import React, { useState } from 'react';
import { Sparkles, Music, Play, Search } from 'lucide-react';
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';
import axios from 'axios';

// Datos de ejemplo para la gráfica del TFT (Tendencia de energía)
const mockTFTData = [
  { time: '10am', energy: 0.2 }, { time: '12pm', energy: 0.4 },
  { time: '2pm', energy: 0.8 }, { time: '4pm', energy: 0.6 },
  { time: '6pm', energy: 0.9 },
];

export default function MusicAgent() {
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [response, setResponse] = useState(null);

  const askDJ = async () => {
    setLoading(true);
    try {
      const res = await axios.get(`http://localhost:8000/recommend?user_mood=${input}`);
      setResponse(res.data.recommendation);
    } catch (err) {
      setResponse("Error al conectar con el cerebro de IA.");
    }
    setLoading(false);
  };

  return (
    <div className="min-h-screen bg-zinc-950 text-white p-8 font-sans">
      {/* Header */}
      <div className="max-w-4xl mx-auto flex items-center gap-3 mb-12">
        <div className="bg-red-600 p-2 rounded-full"><Music size={32} /></div>
        <h1 className="text-4xl font-black tracking-tighter">YT AGENT</h1>
      </div>

      <div className="max-w-4xl mx-auto grid grid-cols-1 md:grid-cols-2 gap-8">
        
        {/* Columna Izquierda: Input y TFT */}
        <div className="space-y-6">
          <div className="bg-zinc-900 p-6 rounded-2xl border border-zinc-800">
            <h2 className="text-zinc-400 text-sm font-bold uppercase mb-4">Predicción de Energía (TFT)</h2>
            <div className="h-40 w-full">
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={mockTFTData}>
                  <Line type="monotone" dataKey="energy" stroke="#dc2626" strokeWidth={3} dot={false} />
                  <XAxis dataKey="time" hide />
                  <YAxis hide domain={[0, 1]} />
                  <Tooltip contentStyle={{backgroundColor: '#18181b', border: 'none'}} />
                </LineChart>
              </ResponsiveContainer>
            </div>
            <p className="text-xs text-zinc-500 mt-2 italic">Basado en tu historial reciente de YouTube Music</p>
          </div>

          <div className="relative">
            <input 
              className="w-full bg-zinc-900 border border-zinc-800 p-4 rounded-xl focus:outline-none focus:ring-2 focus:ring-red-600 pl-12"
              placeholder="¿Cómo quieres sentirte ahora?"
              value={input}
              onChange={(e) => setInput(e.target.value)}
            />
            <Search className="absolute left-4 top-4 text-zinc-500" />
            <button 
              onClick={askDJ}
              disabled={loading}
              className="w-full mt-4 bg-white text-black font-bold py-3 rounded-xl hover:bg-zinc-200 transition flex items-center justify-center gap-2"
            >
              {loading ? "Pensando..." : <><Sparkles size={20}/> Generar Recomendación</>}
            </button>
          </div>
        </div>

        {/* Columna Derecha: Respuesta del Agente */}
        <div className="bg-zinc-900 p-8 rounded-2xl border border-zinc-800 flex flex-col">
          <h2 className="text-red-500 font-bold mb-4 flex items-center gap-2">
            <Play size={18} fill="currentColor"/> RECOMENDACIÓN DE LLAMA 3
          </h2>
          {response ? (
            <div className="text-zinc-300 leading-relaxed animate-in fade-in duration-700">
              {response}
            </div>
          ) : (
            <div className="text-zinc-600 italic">
              El agente está esperando que describas tu estado de ánimo o actividad...
            </div>
          )}
        </div>

      </div>
    </div>
  );
}