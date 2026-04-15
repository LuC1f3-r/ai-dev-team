Ai-dev-team
============

A multi-agent AI development team powered by [crewAI](https://github.com/joaomdmoura/crewAI).

Architecture
------------

```
Manager Agent
    │
    ├── Senior Dev Agent (Architecture/Review)
    │
    ├── Frontend Dev Agent (UI Implementation)
    │
    ├── Backend Dev Agent (API/Database)
    │
    └── Tester Agent (QA/Testing)
```

Features
--------

- **5 Specialized AI Agents**: Manager, Senior Dev, Frontend, Backend, Tester
- **Model Flexibility**: Local (Ollama) + Cloud (OpenAI, Anthropic)
- **Real-time Web GUI**: Streamlit-based monitoring dashboard
- **Memory System**: Session context + ChromaDB vector store
- **Mind Map Export**: Per-project context retention

Quick Start
-----------

1. **Install dependencies**:
   ```bash
   cd ~/Documents/personal-work/ai-dev-team
   python3.10 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Setup environment**:
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

3. **Install Ollama models** (optional, for local models):
   ```bash
   ollama pull codellama
   ollama pull mistral
   ```

4. **Run the web GUI**:
   ```bash
   streamlit run gui/app.py
   # Open http://localhost:8501
   ```

5. **Or use the CLI**:
   ```bash
   python cli.py
   # Type 'task Build a tic tac toe game with React'
   ```

Usage
-----

### Web GUI

1. Submit a task in the Task Input box
2. Watch agents work in real-time
3. View output in the Code View panel
4. Manage memory in the sidebar

### CLI

```
> task Build a user authentication system
> status
> memory
> projects
> exit
```

### Python API

```python
from crews.dev_crew import get_dev_crew

crew = get_dev_crew("Build a blog with React")
result = crew.kickoff()
print(result)
```

Configuration
-------------

Edit `config/models.yaml` to change model routing:

- Simple tasks → Local Ollama models
- Complex tasks → Cloud APIs (GPT-4, Claude)

Memory
------

- **Short-term**: Session context (cleared on new session)
- **Long-term**: Per-project ChromaDB storage with mind map export

Project Structure
-----------------

```
ai-dev-team/
├── agents/          # Agent definitions
├── tasks/           # Task definitions
├── crews/           # Crew orchestration
├── memory/          # Memory system
├── gui/             # Streamlit web interface
├── config/          # Configuration files
├── tests/           # Test suite
├── main.py          # CLI entry point
└── cli.py           # Interactive CLI
```

License
-------

MIT