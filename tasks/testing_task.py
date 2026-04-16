from crewai import Task
import yaml
from pathlib import Path

with open(Path(__file__).parent.parent / "config" / "prompts.yaml") as f:
    prompts = yaml.safe_load(f)

testing_prompt = prompts["task_prompts"]["testing"]

def get_testing_task(agent, description: str) -> Task:
    return Task(
        description=f"{testing_prompt['description']}: {description}",
        agent=agent,
        expected_output=testing_prompt["expected_output"],
    )