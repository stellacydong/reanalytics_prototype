# TreatyStructuring-GPT

> **LLM + RAG + RL for Intelligent Reinsurance Treaty Design**  

## 🌍 Overview

**TreatyStructuring-GPT** is an AI-powered assistant for reinsurance underwriters. It leverages Retrieval-Augmented Generation (RAG), large language models (LLMs), and reinforcement learning (RL) to help analyze treaty documents, simulate outcomes, and suggest optimal treaty structures.

### 🔍 What It Does

- 📄 Summarizes treaty contracts using LLMs (Mistral, OpenRouter, etc.)
- 🧠 Uses LangChain + FAISS to enable retrieval from uploaded treaties
- 🤖 Optimizes treaty structures (retention, limit) using a PPO-based RL agent
- 📈 Visualizes outcomes, rewards, and capital efficiency metrics
- 💬 Allows natural language queries like:
  > "What if we raise the attachment point to $5M?"

## 🛠️ Architecture

- `Streamlit` for interactive UI
- `LangChain + FAISS` for document retrieval (RAG)
- `Transformers` for LLM summarization
- `Gymnasium + PPO` for strategy simulation
- `Matplotlib / Seaborn` for plotting

reinsurance_gpt/
│
├── app/                             # Frontend: Streamlit UI
│   ├── streamlit_app.py             # Entry point for the interactive assistant
│   ├── components/                  # Modular UI and logic handlers
│   │   ├── treaty_uploader.py
│   │   ├── treaty_parser.py
│   │   ├── rl_visualizer.py
│   │   └── summary_view.py
│   └── static/                      # CSS / JS for Streamlit customization
│       ├── css/
│       └── img/
│
├── models/                          # ML models
│   ├── ppo_structuring_agent.py     # PPO-based Gym RL environment
│   ├── ppo_trainer.py               # PPO training script
│   ├── ppo_inference.py             # PPO inference and strategy evaluation
│   ├── mistral_model_loader.py      # Loads LLM model (e.g., Mistral 7B via Transformers)
│   └── visualize_ppo_results.py     # Reward/strategy plots
│
├── agents/                          # LangChain RAG agents
│   ├── treaty_rag_agent.py          # LangChain retriever for treaty docs
│   └── retriever_utils.py           # FAISS, embedding, context chunking
│
├── data/                            # Input/Output datasets
│   ├── treaty_samples/              # Treaty .txt files
│   ├── synthetic_claims.csv         # Simulated claims
│   └── ppo_simulation.csv           # PPO rollout results
│
├── scripts/                         # Utilities
│   ├── generate_synthetic_claims.py
│   ├── generate_treaty_samples.py
│   └── plot_claims_distribution.py
│
├── outputs/                         # Reports, logs
│   └── training_logs/
│
├── requirements.txt
├── Dockerfile
├── .streamlit/config.toml
├── LICENSE
└── README.md                       


## 📦 Features

| Module              | Description                                                |
|---------------------|------------------------------------------------------------|
| 🧾 Treaty Parser     | Reads `.txt` treaties and chunked paragraphs for RAG       |
| 💡 LLM Summarizer    | Extracts key clauses, exclusions, attachment terms         |
| 🔁 RL Optimizer      | Trains PPO agent to optimize capital efficiency            |
| 📊 Visualizer        | Plots reward evolution and strategy comparison             |
| 🗣️ Natural Language  | Chat interface powered by LangChain for impact analysis    |

## 🚀 How to Run

```bash
# Install dependencies
pip install -r requirements.txt

# Launch the app
streamlit run app/streamlit_app.py
````

## 📁 Sample Data

* `data/treaty_samples/` – sample treaty text files
* `data/synthetic_claims.csv` – simulated loss experience
* `outputs/ppo_simulation.csv` – PPO evaluation logs

## 🧠 Example Use Case

Upload a treaty, ask:

> "What if we add a limit of \$10M and reduce retention to \$1M?"

See:

* 📘 Suggested clauses
* 🎯 PPO-optimized strategy
* 📊 Impact on risk metrics

## 📚 Research & Vision

This project underpins the paper:

**“TreatyStructuring-GPT: Retrieval-Augmented Language and Reinforcement Learning for Intelligent Reinsurance Treaty Design”**

Submitted to: *AAAI, IJCAI, NeurIPS, or Risk Management & Insurance Review*.

## 📜 License

MIT

