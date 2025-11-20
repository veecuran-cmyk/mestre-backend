// Arquivo: api/ia_master.js

// Importa a biblioteca 'node-fetch' para fazer requisições HTTP
// Nota: O Vercel e Node.js modernos suportam 'fetch' nativamente, mas 
// para maior compatibilidade, faremos a chamada direta como se estivéssemos
// dentro de uma função Serverless do Vercel.

// Pega a chave do ambiente (SEGURANÇA!)
const OPENROUTER_KEY = process.env.OPENROUTER_KEY; 
const MODEL_NAME = "meta-llama/llama-3-8b-instruct:free";
const API_URL = "https://openrouter.ai/api/v1/chat/completions";

// Função principal que o Vercel vai executar na rota /api/ia_master
module.exports = async (req, res) => {
    // 1. Verifica se a chave de segurança está configurada
    if (!OPENROUTER_KEY) {
        res.status(500).json({ error: "Chave API não configurada no servidor." });
        return;
    }

    // 2. Verifica se o método é POST (evita erro 405)
    if (req.method !== 'POST') {
        res.status(405).json({ error: "Método não permitido. Use POST." });
        return;
    }

    try {
        // 3. Lê o corpo da requisição (o histórico de mensagens)
        const { messages } = req.body;

        if (!messages || !Array.isArray(messages)) {
             res.status(400).json({ error: "Corpo da requisição inválido. Esperado {messages: [...]}" });
             return;
        }

        // 4. Monta o Payload para a OpenRouter
        const payload = {
            model: MODEL_NAME,
            messages: messages,
            // Outras configurações da OpenRouter aqui
        };

        // 5. Faz a chamada segura para o OpenRouter
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: {
                "Authorization": `Bearer ${OPENROUTER_KEY}`, // Usa a chave SECRETA AQUI
                "Content-Type": "application/json",
                // Headers de identificação exigidos pela OpenRouter
                "HTTP-Referer": "https://mestreos.app",
                "X-Title": "MestreOS-Nodejs-Backend"
            },
            body: JSON.stringify(payload)
        });

        if (!response.ok) {
            // Tenta obter o erro detalhado da OpenRouter
            const errorJson = await response.json().catch(() => ({}));
            throw new Error(errorJson.error || `Erro HTTP da OpenRouter: ${response.status}`);
        }

        const ai_response = await response.json();
        
        // 6. Devolve SÓ o texto para o seu Front-end (o HTML)
        const aiText = ai_response.choices[0].message.content;

        res.status(200).json({ text: aiText });

    } catch (e) {
        console.error("Erro no processamento da IA:", e.message);
        res.status(500).json({ error: e.message || "Erro interno do servidor Node.js." });
    }
};
