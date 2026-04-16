from crewai import Task
import yaml
from pathlib import Path

with open(Path(__file__).parent.parent / "config" / "prompts.yaml") as f:
    prompts = yaml.safe_load(f)

frontend_prompt = prompts["task_prompts"]["frontend"]

def get_frontend_task(agent, description: str) -> Task:
    return Task(
        description=f"{frontend_prompt['description']}: {description}",
        agent=agent,
        expected_output=frontend_prompt["expected_output"],
    )