from crewai import Crew
from agents import (
    get_manager_agent,
    get_senior_dev_agent,
    get_frontend_dev_agent,
    get_backend_dev_agent,
    get_tester_agent,
)
from tasks import (
    get_planning_task,
    get_frontend_task,
    get_backend_task,
    get_testing_task,
)

def get_dev_crew(task_description: str):
    manager = get_manager_agent()
    senior = get_senior_dev_agent()
    frontend = get_frontend_dev_agent()
    backend = get_backend_dev_agent()
    tester = get_tester_agent()

    planning = get_planning_task(manager, task_description)
    frontend_task = get_frontend_task(frontend, task_description)
    backend_task = get_backend_task(backend, task_description)
    testing = get_testing_task(tester, task_description)

    crew = Crew(
        agents=[manager, senior, frontend, backend, tester],
        tasks=[planning, frontend_task, backend_task, testing],
        verbose=True,
    )

    return crew