# ReAnalytics: The Reinsurance Co-Pilot

🚀 Transforming reinsurance analytics with AI — powered by LangChain, Retrieval-Augmented Generation (RAG), and Proximal Policy Optimization (PPO).

---

## 🧠 Core Capabilities

- **Treaty AI Assistant**  
  Upload a reinsurance treaty (text or PDF) and ask precise, intelligent questions.  
  - Retrieval-Augmented Generation (RAG) powered by local Mistral-7B or any LLM
  - Instant extraction of limits, terms, and conditions

- **Reserve Optimization Simulator**  
  Upload synthetic claims data and run simulations:
  - Traditional reserving (Chain Ladder / fixed factor method)
  - AI-driven reserve optimization using PPO reinforcement learning agent

- **Risk Insights Dashboard**  
  Instantly visualize:
  - Tail Risk metrics (Conditional Value at Risk - CVaR)
  - Solvency Ratios
  - Reserve distributions (Traditional vs AI-optimized)

---

## 📂 Project Structure

```plaintext
reanalytics_prototype/
├── app/
│   ├── components/
│   │   ├── dashboard.py
│   │   ├── uploaders.py
│   ├── streamlit_app.py
├── agents/
│   ├── treaty_rag_agent.py
├── models/
│   ├── mistral_model_loader.py
│   ├── ppo_reserving_agent.py
├── data/
│   ├── sample_treaty.txt
│   ├── synthetic_claims.csv
├── requirements.txt
```

---

## ⚡ Quickstart

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/reanalytics_prototype.git
   cd reanalytics_prototype
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Launch the app:**
   ```bash
   streamlit run app/streamlit_app.py
   ```

---

## 🛠️ System Requirements

- Python 3.10+
- Key libraries:
  - `streamlit`
  - `langchain`
  - `langchain-community`
  - `sentence-transformers`
  - `faiss-cpu`
  - `transformers`
  - `torch`
  - `plotly`

---

## ✨ Demo Links

- [3-minute product walkthrough](#) (link)
- [Live app deployment](#) (Hugging Face Space link)

---

## 📩 Contact

Created by **Stella Dong** | 📧 stellacydong@gmail.com

**Let's reimagine reinsurance together.**