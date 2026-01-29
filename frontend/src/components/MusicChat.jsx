import React, { useState } from 'react';
import { Sparkles, Music, Play, Send, User, Bot } from 'lucide-react';
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';
import { sendMessageToAgent } from '../api';

const mockTFTData = [
  { time: '10am', energy: 0.2 }, { time: '12pm', energy: 0.4 },
  { time: '2pm', energy: 0.8 }, { time: '4pm', energy: 0.6 },
  { time: '6pm', energy: 0.9 },
];

export default function MusicChat() {
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [messages, setMessages] = useState([]);

  const handleSend = async () => {
    if (!input.trim() || loading) return;

    const userMessage = { role: 'user', text: input };
    setMessages(prev => [...prev, userMessage]);
    const currentInput = input;
    setInput("");
    setLoading(true);

    try {
      const data = await sendMessageToAgent(currentInput);
      setMessages(prev => [...prev, { role: 'assistant', text: data.respuesta }]);
    } catch (err) {
      setMessages(prev => [...prev, { role: 'error', text: "Error al conectar con el cerebro de IA." }]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-zinc-950 text-white p-4 md:p-8 font-sans">
      {/* Header Estilo YT Music */}
      <div className="max-w-6xl mx-auto flex items-center gap-3 mb-10">
        <div className="bg-red-600 p-2 rounded-full shadow-lg shadow-red-900/20">
          <Music size={28} />
        </div>
        <h1 className="text-3xl font-black tracking-tighter">YT AGENT <span className="text-zinc-500 text-lg ml-2">v1.0</span></h1>
      </div>

      <div className="max-w-6xl mx-auto grid grid-cols-1 lg:grid-cols-3 gap-8">
        
        {/* Lado Izquierdo: Stats y Status */}
        <div className="lg:col-span-1 space-y-6">
          <div className="bg-zinc-900/50 p-6 rounded-3xl border border-zinc-800 backdrop-blur-sm">
            <h2 className="text-zinc-400 text-xs font-bold uppercase mb-4 tracking-widest">Energía Reciente (TFT)</h2>
            <div className="h-32 w-full">
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={mockTFTData}>
                  <Line type="monotone" dataKey="energy" stroke="#dc2626" strokeWidth={3} dot={false} />
                  <XAxis dataKey="time" hide />
                  <YAxis hide domain={[0, 1]} />
                  <Tooltip contentStyle={{backgroundColor: '#18181b', border: 'none', borderRadius: '8px'}} />
                </LineChart>
              </ResponsiveContainer>
            </div>
            <p className="text-[10px] text-zinc-500 mt-4 uppercase tracking-tighter">Análisis de Llama 3 en tiempo real</p>
          </div>

          <div className="bg-gradient-to-br from-zinc-900 to-black p-6 rounded-3xl border border-zinc-800">
            <h3 className="text-red-500 font-bold text-sm mb-2 flex items-center gap-2">
              <Sparkles size={16}/> MODO OAUTH ACTIVO
            </h3>
            <p className="text-xs text-zinc-400 leading-relaxed">
              El agente tiene acceso a tu historial de YouTube Music para personalizar las respuestas.
            </p>
          </div>
        </div>

        {/* Lado Derecho: El Chat (La Columna de Recomendación) */}
        <div className="lg:col-span-2 flex flex-col bg-zinc-900/30 rounded-3xl border border-zinc-800 overflow-hidden h-[600px]">
          
          {/* Messages Area */}
          <div className="flex-1 overflow-y-auto p-6 space-y-6">
            {messages.length === 0 && (
              <div className="h-full flex flex-col items-center justify-center text-center space-y-4">
                <Play size={40} className="text-zinc-800" fill="currentColor"/>
                <p className="text-zinc-500 italic max-w-xs text-sm">
                  Dime qué humor tienes o pregunta por tu historial para empezar la magia.
                </p>
              </div>
            )}
            
            {messages.map((msg, i) => (
              <div key={i} className={`flex gap-4 ${msg.role === 'user' ? 'flex-row-reverse' : ''}`}>
                <div className={`p-2 rounded-full h-fit ${msg.role === 'user' ? 'bg-zinc-800' : 'bg-red-600'}`}>
                  {msg.role === 'user' ? <User size={18}/> : <Bot size={18}/>}
                </div>
                <div className={`max-w-[80%] p-4 rounded-2xl text-sm leading-relaxed ${
                  msg.role === 'user' ? 'bg-zinc-800 text-zinc-200' : 'bg-zinc-900 border border-zinc-800 text-zinc-300'
                }`}>
                  {msg.text}
                </div>
              </div>
            ))}
            {loading && (
              <div className="flex gap-4 animate-pulse">
                <div className="p-2 rounded-full h-fit bg-red-900/50 text-red-500">
                  <Bot size={18}/>
                </div>
                <div className="bg-zinc-900/50 h-10 w-32 rounded-2xl border border-zinc-800"></div>
              </div>
            )}
          </div>

          {/* Input Area */}
          <div className="p-6 bg-zinc-900/80 border-t border-zinc-800">
            <div className="relative flex items-center">
              <input 
                className="w-full bg-black border border-zinc-700 p-4 rounded-2xl focus:outline-none focus:ring-2 focus:ring-red-600 focus:border-transparent transition-all pr-14 text-sm"
                placeholder="Pregunta algo sobre tu música..."
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={(e) => e.key === 'Enter' && handleSend()}
              />
              <button 
                onClick={handleSend}
                disabled={loading}
                className="absolute right-3 p-2 bg-white text-black rounded-xl hover:bg-zinc-200 transition-colors disabled:opacity-50"
              >
                <Send size={20} />
              </button>
            </div>
          </div>

        </div>

      </div>
    </div>
  );
}