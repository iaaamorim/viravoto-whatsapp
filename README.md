# Viravoto Cognitivo - Agente de WhatsApp

> **Copiloto tático de inteligência artificial via WhatsApp para ativistas e voluntários dialogarem com eleitores indecisos, moderados e biconceituais no 2º turno.**

Construído com base na **Linguística Cognitiva de George Lakoff** (*Não pense num elefante!*), nas pesquisas do guia **"Como vencer o 2º turno"** e nas análises de campanha do **Calma Urgente**.

---

## O Que o Agente Faz?

1. **O voluntário recebe uma mensagem ou desabafo** de um familiar, vizinho ou colega (ex: *"Eu odeio o PT"*, *"Vou anular"*, *"Precisamos salvar o Brasil"*).
2. **O voluntário cola a mensagem no WhatsApp do robô.**
3. **O robô devolve em segundos:**
   - **Diagnóstico Rápido**: O que está na cabeça do eleitor e qual frame foi ativado.
   - **O que NÃO dizer**: Palavras-armadilha para nunca repetir (evitando fortalecer a narrativa adversária).
   - **Opção 1 (Pergunta Desarmadora)**: Abordagem socrática suave baseada em afeto e perguntas.
   - **Opção 2 (Resposta Direta & Firme)**: Mensagem assertiva focada nos 3 pontos fracos de Flávio Bolsonaro (mérito/nepo baby, Trump/soberania, falta de confiança/áudios).
   - **Roteiro de Áudio Curto**: Texto para falar em 15 segundos no WhatsApp.

---

## Stack Tecnológico

- **Backend**: Python 3.11 + FastAPI (assíncrono, leve e ultrarrápido)
- **IA Cognitiva**: Google Gemini 2.5 Flash / 3 Flash via SDK oficial `google-genai`
- **WhatsApp Gateway**: Evolution API v2 (Open-source, self-hosted via Docker)
- **Deploy**: Docker Compose pronto para rodar em 1 comando

---

## Como Rodar o Projeto (Guia para o Desenvolvedor)

### 1. Pré-requisitos
- [Docker](https://www.docker.com/) e Docker Compose instalados.
- Chave de API do Google Gemini (gratuita em [Google AI Studio](https://aistudio.google.com/)).

### 2. Clonar e Configurar Variáveis de Ambiente
```bash
cp .env.example .env
```
Edite o arquivo `.env` e insira sua `GEMINI_API_KEY`.

### 3. Subir os Containers
```bash
docker compose up -d --build
```
Isso iniciará:
- **Evolution API** em `http://localhost:8080`
- **Robô Viravoto (FastAPI)** em `http://localhost:8000`

### 4. Conectar o WhatsApp na Evolution API
1. Acesse o painel da Evolution API ou use a rota de criar instância:
   ```bash
   curl -X POST http://localhost:8080/instance/create \
     -H "apikey: viravoto_super_secreta_123" \
     -H "Content-Type: application/json" \
     -d '{"instanceName": "viravoto", "token": "viravoto_super_secreta_123", "qrcode": true}'
   ```
2. Escaneie o QR Code retornado com o WhatsApp do chip da campanha.
3. Aponte o Webhook da instância para a URL do bot:
   - URL: `http://reenquadra-bot:8000/webhook` (ou via IP/túnel se rodar em máquinas separadas)
   - Evento: `MESSAGES_UPSERT`

### 5. Testar Localmente sem WhatsApp
Você pode testar as respostas da IA diretamente pelo terminal ou navegador:
```bash
curl -X POST http://localhost:8000/test \
  -H "Content-Type: application/json" \
  -d '{"message": "Eu não voto no PT de jeito nenhum, precisamos salvar o Brasil"}'
```

---

## Estrutura de Pastas

```text
agente-viravoto-whatsapp/
├── README.md               # Este guia técnico
├── docker-compose.yml      # Sobe a Evolution API e o bot
├── Dockerfile              # Imagem do servidor FastAPI
├── requirements.txt        # Dependências Python
├── .env.example            # Template de variáveis de ambiente
├── app/
│   ├── __init__.py
│   ├── main.py             # Servidor e rotas de Webhook
│   ├── cognitive_engine.py # O Cérebro: Regras do Lakoff e Pesquisas
│   └── evolution_client.py # Conexão com o WhatsApp
└── docs/
    ├── GUIA_PASSO_A_PASSO_PARA_INICIANTES.md # Manual não-técnico
    └── METODOLOGIA_LAKOFF_E_PESQUISAS.md    # Fundamentação estratégica
```
