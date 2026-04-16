from crewai import Agent
from langchain_community.chat_models import ChatOllama
import yaml
from pathlib import Path

with open(Path(__file__).parent.parent / "config" / "prompts.yaml") as f:
    prompts = yaml.safe_load(f)

tester_prompt = prompts["prompts"]["tester"]

class TesterAgent:
    @staticmethod
    def get_agent() -> Agent:
        return Agent(
            role=tester_prompt["role"],
            goal=tester_prompt["goal"],
            backstory=tester_prompt["backstory"],
            verbose=True,
            allow_delegation=False,
            llm=ChatOllama(
                model="codellama",
                base_url="http://localhost:11434",
                temperature=0.5,
            ),
        )

def get_tester_agent() -> Agent:
    return TesterAgent.get_agent()