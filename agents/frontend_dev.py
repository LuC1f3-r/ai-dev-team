from crewai import Agent
from langchain_community.chat_models import ChatOllama
import yaml
from pathlib import Path

with open(Path(__file__).parent.parent / "config" / "prompts.yaml") as f:
    prompts = yaml.safe_load(f)

frontend_prompt = prompts["prompts"]["frontend_dev"]

class FrontendDevAgent:
    @staticmethod
    def get_agent() -> Agent:
        return Agent(
            role=frontend_prompt["role"],
            goal=frontend_prompt["goal"],
            backstory=frontend_prompt["backstory"],
            verbose=True,
            allow_delegation=False,
            llm=ChatOllama(
                model="codellama",
                base_url="http://localhost:11434",
                temperature=0.5,
            ),
        )

def get_frontend_dev_agent() -> Agent:
    return FrontendDevAgent.get_agent()