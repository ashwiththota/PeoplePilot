
 HR Assistant

A production-style Retrieval-Augmented Generation (RAG) agent that answers employee questions about company HR policy — leave, work-from-home, probation, notice period, reimbursement, code of conduct, IT security, and exit process — grounded in the actual policy documents, with input/output guardrails, an LLM gateway, and automated evaluation.

Features
Answers HR policy questions using RAG, retrieving relevant chunks from the actual policy documents rather than relying on the model's general knowledge
Input and output guardrails — every question and every answer is checked by a safety model before being processed/shown, blocking prompt injection attempts, other-employee data requests, PII leaks, and unauthorized promises
LLM gateway (Portkey) in front of all model calls, routing through provider slugs rather than exposing raw API keys in application code
Cloud vector store (Qdrant Cloud) — no local vector DB to manage; embeddings persist across restarts
Automated evaluation (LangSmith) — a fixed set of HR policy test questions scored by an LLM judge for both correctness and RAG groundedness, so answer quality can be tracked across changes
Chat interface (Streamlit) with message history
Fully containerized with Docker
Tech Stack
Component	Technology
LLM	Groq (openai/gpt-oss-120b), via Portkey gateway
Guard model	Groq (openai/gpt-oss-safeguard-20b)
Embeddings	Jina (jina-embeddings-v2-base-en)
Vector Database	Qdrant Cloud
LLM Gateway	Portkey
Agent Framework	LangChain + LangGraph
Evaluation & Tracing	LangSmith
Web UI	Streamlit
Containerization	Docker
Project Structure
basic_rag/
├── hr_assistant/
│   ├── config.py           # Centralized settings, env vars, prompts, model names
│   ├── document_loader.py  # Stage 1: load the HR policy document
│   ├── splitter.py         # Stage 2: split into chunks
│   ├── embeedings.py       # Stage 3: embedding model setup (Jina)
│   ├── vector_store.py     # Stage 4: build/load/check the Qdrant Cloud collection
│   ├── tools.py            # Retriever tool the agent can call, with retry logic
│   ├── guadrails.py        # Input/output safety checks via a Groq guard model
│   ├── gateway.py          # Portkey-routed LLM clients (main + judge)
│   ├── agent.py            # Builds the LangGraph tool-calling agent
│   ├── pipeline.py         # Wires everything together (used by main.py and app.py)
│   ├── tracing.py          # LangSmith tracing setup
│   ├── logger.py           # Shared logger
│   └── evaluation.py       # Evaluation dataset, target function, and evaluators
├── data/
│   └── hr_policy.txt       # Source HR policy document(s)
├── logs/                   # Application logs
├── main.py                 # CLI demo entrypoint
├── app.py                  # Streamlit chat app entrypoint
├── evaluate.py              # Runs the LangSmith evaluation
├── delete_dataset.py       # One-off script to delete the LangSmith dataset
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env                    # Secrets (not committed)
├── .env.docker             # Secrets for Docker (not committed)
└── .gitignore
Setup
1. Clone and create a virtual environment
bash
git clone <https://github.com/ashwiththota/PeoplePilot>
cd basic_rag
python -m venv PeoplePilot
PeoplePilot\Scripts\Activate.ps1   # Windows PowerShell
2. Install dependencies
bash
pip install -r requirements.txt
3. Configure environment variables

Create a .env file with:

GROQ_API_KEY=your_groq_api_key
JINA_API_KEY=your_jina_api_key
PORTKEY_KEY_API=your_portkey_api_key
QDRANT_URL=your_qdrant_cloud_url
QDRANT_API_KEY=your_qdrant_api_key
QDRANT_COLLECTION_NAME=hr_policy

LANGSMITH_TRACING=true
LANGSMITH_ENDPOINT=https://api.smith.langchain.com
LANGSMITH_API_KEY=your_langsmith_api_key
LANGSMITH_PROJECT=hr_policy_assistant

Note: environment variable values should not be wrapped in quotes — some tooling (Docker's --env-file) does not strip them the way python-dotenv does locally.

4. Set up your Portkey provider slugs

In the Portkey dashboard, create provider slugs pointing at your Groq credentials:

@hrpolicy — the main application model
@hrpolicyjudge — used by the evaluation judge, so it isn't grading its own output
Usage
Run the CLI demo
bash
python main.py
Run the Streamlit app
bash
streamlit run app.py

Opens a chat interface at http://localhost:8501.

Run the evaluation suite
bash
python evaluate.py

Runs the fixed set of HR policy test questions through the live agent, scores each answer for correctness and groundedness using an LLM judge, and uploads the results to LangSmith as an experiment.

Evaluation makes many LLM calls in quick succession and can hit Groq's tokens-per-minute rate limit on the free tier — this is expected. The client automatically retries with backoff, so the run completes, just more slowly.

How It Works
Ingestion — the HR policy document is loaded, split into chunks, embedded with Jina, and stored in a Qdrant Cloud collection. If the collection already exists, ingestion is skipped and it connects directly.
Input guard — every user question is checked against an input safety policy (prompt injection, requests for another employee's data) before the agent sees it.
Retrieval — a LangGraph agent, routed through the Portkey gateway, calls a search tool that retrieves the most relevant policy chunks for the question.
Output guard — the agent's answer is checked against an output safety policy (PII leaks, unauthorized promises, suspicious links) before being shown to the user.
Evaluation — a separate LangSmith-tracked pipeline runs a fixed question set through the live agent and scores each answer for correctness (against a reference answer) and groundedness (against what was actually retrieved).
Guardrails

The assistant runs two safety checks around every interaction, each using a dedicated Groq guard model that classifies text as safe or a violation and returns a reason:

Input policy — blocks prompt injection / jailbreak attempts (including fake SYSTEM/ASSISTANT role labels embedded in user text) and requests for another named employee's personal data.
Output policy — blocks PII leaks, unauthorized promises (e.g. approving a leave request on the company's behalf), discriminatory or toxic language, and suspicious links or credentials.

A blocked question or answer returns a fixed refusal message instead of proceeding.

Notes
If the embedding model changes, the Qdrant Cloud collection must be rebuilt — mixing embedding models produces a dimension-mismatch error.
ChatGroq/ChatOpenAI clients must be given an explicit api_key argument rather than relying on the GROQ_API_KEY OS environment variable being set — required for compatibility with environments (like Streamlit Cloud) where secrets aren't automatically injected as OS env vars.
Only one virtual environment (basicragenv) is the source of truth for this project's dependencies.
  
