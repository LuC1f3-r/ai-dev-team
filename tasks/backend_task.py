from crewai import Task
import yaml
from pathlib import Path

with open(Path(__file__).parent.parent / "config" / "prompts.yaml") as f:
    prompts = yaml.safe_load(f)

backend_prompt = prompts["task_prompts"]["backend"]

def get_backend_task(agent, description: str) -> Task:
    return Task(
        description=f"{backend_prompt['description']}: {description}",
        agent=agent,
        expected_output=backend_prompt["expected_output"],
    )