#  OptiGrid-Agent: Autonomous Microgrid Optimization & Agentic Reporting

[![Python 3.10](https://img.shields.io/badge/python-3.10-blue.svg)](https://www.python.org/downloads/release/python-3100/)
[![Optimization](https://img.shields.io/badge/Math_Solver-PuLP-success.svg)](https://coin-or.github.io/pulp/)
[![AI Framework](https://img.shields.io/badge/Agentic_Framework-crewAI-orange.svg)](https://crewai.com/)
[![LLM](https://img.shields.io/badge/LLM-Gemini_2.5_Flash-blueviolet.svg)](https://deepmind.google/technologies/gemini/)

##  Executive Summary
OptiGrid-Agent is a dual-engine AI pipeline designed to solve two distinct challenges in modern energy management: mathematically optimizing battery dispatch schedules, and autonomously translating those complex financial metrics into pedagogical, client-facing communications.

By combining deterministic **Mathematical Programming** (Linear Optimization via PuLP) with non-deterministic **Agentic Frameworks** (crewAI + Gemini), this project acts as an autonomous "Energy Manager," ensuring commercial microgrids maximize their ROI while keeping human stakeholders fully informed with zero manual reporting overhead.

##  Business Value
* **Financial Optimization:** Minimizes daily electricity costs by mathematically solving load forecasts against dynamic peak/off-peak pricing curves.
* **Automated Internal Functions:** Eliminates the bottleneck of manual data storytelling. The AI automatically generates highly polished, client-ready emails explaining the strategy and exact dollar savings.
* **Pedagogical Data Translation:** Bridges the gap between raw vector-based matrices and plain-English business value, ensuring facility managers trust the AI's decisions.

##  Technical Architecture
### 1. The Mathematical Engine (Operations Research)
* Built using `PuLP` and `COIN_CMD`.
* Formulates a Linear Programming (LP) matrix to minimize total cost: `Σ(Load + Charge - Discharge) * Price`.
* Applies strict physical constraints: Maximum charge/discharge rates, battery capacity limits, and round-trip efficiency ($\eta$).
* Utilizes vectorized `NumPy`/`Pandas` operations for efficient financial calculations.

### 2. The Agentic Framework (crewAI)
* **Lead Energy Analyst Agent:** Orchestrates the workflow by utilizing the Python optimization engine as a callable Tool to extract the daily financial metrics.
* **Client Communications Agent:** Enforces a specific persona to translate the mathematical output into a jargon-free, encouraging summary for customer support operations.

##  Quick Start

### 1. Installation
Clone the repository and spin up the isolated environment:
```bash
git clone [https://github.com/shashayanyan/optigrid-agent.git](https://github.com/shashayanyan/optigrid-agent.git)
cd optigrid-agent
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Environment Configuration
Create a .env file in the root directory and add your Google Gemini API key:

```txt
GEMINI_API_KEY="your_api_key_here"
```

### 3. Run the Agentic Workflow
Watch the ReAct (Reason + Act) loop dynamically trigger the math solver and generate the final client communication:

```bash
python3 src/agents.py
```


### 4. Run the Pytest Suite
The mathematical constraints are heavily validated to prevent LLM hallucinations from impacting financial recommendations:

```bash
pytest tests/ -v
```
## 📁 Repository Structure
```txt
├── src/
│   ├── optimizer.py     # Linear Programming battery solver (PuLP)
│   ├── tools.py         # Agentic tool wrappers for the mathematical engine
│   └── agents.py        # crewAI multi-agent orchestration and personas
├── tests/               # Pytest suite validating optimization constraints
├── requirements.txt     # Python dependencies
└── README.md            # Project documentation
```
