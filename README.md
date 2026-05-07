## 🧩 Multi-LLM Ensemble Reasoning System with LLM-as-a-Judge Evaluation and Fault-Tolerant Inference Pipeline

### *The Semantic Grand Prix of AI Orchestration*

This project is a high-performance **orchestration framework** designed to pit multiple Large Language Models (LLMs) against each other in a "Semantic Grand Prix." By utilizing an **API pipeline** and an **LLM-as-a-Judge** architecture, the system evaluates model outputs across dimensions like accuracy, hallucination, and bias to determine a definitive winner for any complex query.

---

## 🚀 Key Features

* **Multi-Model Reasoning**: Simultaneously triggers multiple state-of-the-art models (GPT-4o, Llama 3.1, Mistral Large) to provide diverse perspectives on a single prompt.
* **Intelligent Orchestration**: A central controller manages the **API pipeline**, handling inference requests and aggregating responses in real-time.
* **LLM-as-a-Judge Framework**: Uses a dedicated evaluator model to score competitors based on 5 key metrics: Accuracy, Completeness, Relevance, Efficiency, and Cost.
* **Gamified Scoreboard**: A custom-built Streamlit UI featuring a **Grand Prix Scoreboard** with sports cars that race toward a finish line based on their confidence scores.
* **Stress Test Suite**: Built-in suggestion box for testing **Conflict, Hallucination, and Bias** to push the boundaries of model logic.

---

## 🛠️ Technical Architecture

The system is built on a modular **framework** designed for scalability:

1.  **Frontend**: Streamlit-based UI with dynamic theme switching (High-Contrast Light/Dark modes).
2.  **Inference Engine**: A robust pipeline connecting to model providers (OpenAI, Meta, Mistral) via unified API calls.
3.  **Evaluation Layer**: A semantic judge that analyzes cross-model conflicts and identifies hallucinations.
4.  **Visualization**: Custom CSS-in-JS animations for the "Championship" confetti and racing scoreboard.

---

## 🏁 Getting Started

### 1. Prerequisites
* Python 3.9+
* API Keys for OpenAI / Groq / Mistral (stored in a `.env` file)

### 2. Installation
```bash
# Clone the repository
git clone https://github.com/yourusername/multi-llm-ensemble.git

# Install dependencies
pip install -r requirements.txt
```

### 3. Execution
```bash
# Launch the Grand Prix
streamlit run app.py
```

---

## 🔬 Testing Logic Traps
Use the built-in **Suggestion Box** to evaluate how the framework handles:
* **Hallucinations**: Prompting for events that never happened (e.g., "The 1926 World Cup").
* **Conflict**: Forcing models to argue over hardware-specific coding logic.
* **Bias**: Testing for ageist, sexist, or professional stereotypes in technical responses.

---

## 👨‍💻 Author
**Zainab Jahan Umaima** *Technical Project Lead & Software Developer*

---
> *“In the race for intelligence, accuracy is the finish line.”*
