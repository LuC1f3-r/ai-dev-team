from crewai import Agent
from langchain_anthropic import ChatAnthropic
import yaml
from pathlib import Path

with open(Path(__file__).parent.parent / "config" / "prompts.yaml") as f:
    prompts = yaml.safe_load(f)

senior_prompt = prompts["prompts"]["senior_dev"]

class SeniorDevAgent:
    @staticmethod
    def get_agent() -> Agent:
        return Agent(
            role=senior_prompt["role"],
            goal=senior_prompt["goal"],
            backstory=senior_prompt["backstory"],
            verbose=True,
            allow_delegation=False,
            llm=ChatAnthropic(model="claude-3-opus-20240229", temperature=0.7),
        )

def get_senior_dev_agent() -> Agent:
    return SeniorDevAgent.get_agent()