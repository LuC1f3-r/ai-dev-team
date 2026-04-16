from crewai import Task
import yaml
from pathlib import Path

with open(Path(__file__).parent.parent / "config" / "prompts.yaml") as f:
    prompts = yaml.safe_load(f)

planning_prompt = prompts["task_prompts"]["planning"]

def get_planning_task(agent, description: str) -> Task:
    return Task(
        description=f"{planning_prompt['description']}: {description}",
        agent=agent,
        expected_output=planning_prompt["expected_output"],
    )