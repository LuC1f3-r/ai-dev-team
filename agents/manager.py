from crewai import Agent, LLM
import yaml
from pathlib import Path

with open(Path(__file__).parent.parent / "config" / "prompts.yaml") as f:
    prompts = yaml.safe_load(f)

manager_prompt = prompts["prompts"]["manager"]

class ManagerAgent:
    @staticmethod
    def get_agent() -> Agent:
        return Agent(
            role=manager_prompt["role"],
            goal=manager_prompt["goal"],
            backstory=manager_prompt["backstory"],
            verbose=True,
            allow_delegation=True,
            llm=LLM(
                model="ollama/mistral",
                base_url="http://localhost:11434",
                temperature=0.7,
            ),
        )

def get_manager_agent() -> Agent:
    return ManagerAgent.get_agent()
