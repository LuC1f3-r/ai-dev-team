from crewai import Agent, LLM
import yaml
from pathlib import Path

with open(Path(__file__).parent.parent / "config" / "prompts.yaml") as f:
    prompts = yaml.safe_load(f)

backend_prompt = prompts["prompts"]["backend_dev"]

class BackendDevAgent:
    @staticmethod
    def get_agent() -> Agent:
        return Agent(
            role=backend_prompt["role"],
            goal=backend_prompt["goal"],
            backstory=backend_prompt["backstory"],
            verbose=True,
            allow_delegation=False,
            llm=LLM(
                model="ollama/mistral",
                base_url="http://localhost:11434",
                temperature=0.5,
            ),
        )

def get_backend_dev_agent() -> Agent:
    return BackendDevAgent.get_agent()
