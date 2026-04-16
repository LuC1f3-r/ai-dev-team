import streamlit as st
import time
from typing import Dict, Any, Optional
from crews.dev_crew import get_dev_crew
from memory import ShortTermMemory, LongTermMemory

class CrewController:
    def __init__(self):
        if "short_term" not in st.session_state:
            st.session_state.short_term = ShortTermMemory()
        if "long_term" not in st.session_state:
            st.session_state.long_term = LongTermMemory()
        if "crew_result" not in st.session_state:
            st.session_state.crew_result = None
        if "task_status" not in st.session_state:
            st.session_state.task_status = "idle"
        if "agent_outputs" not in st.session_state:
            st.session_state.agent_outputs = {}

    def execute_task(self, task_description: str, project_name: str = "default") -> Dict[str, Any]:
        st.session_state.short_term.set_current_task(task_description)
        st.session_state.task_status = "running"

        for agent_name in ["manager", "senior", "frontend", "backend", "tester"]:
            st.session_state.short_term.update_agent_state(agent_name, "waiting")

        try:
            st.session_state.short_term.update_agent_state("manager", "active")

            crew = get_dev_crew(task_description)
            result = crew.kickoff()

            st.session_state.crew_result = result
            st.session_state.task_status = "completed"

            st.session_state.short_term.update_agent_state("manager", "completed")

            for agent_name in ["senior", "frontend", "backend", "tester"]:
                st.session_state.short_term.update_agent_state(agent_name, "completed")

            st.session_state.short_term.add_task({
                "task": task_description,
                "project": project_name,
                "status": "completed"
            })

            self._update_long_term_memory(project_name, task_description, result)

            return {"status": "success", "result": result}

        except Exception as e:
            st.session_state.task_status = "error"
            st.session_state.short_term.update_agent_state("manager", "error")
            return {"status": "error", "error": str(e)}

    def _update_long_term_memory(self, project_name: str, task: str, result: Any):
        project_data = st.session_state.long_term.projects.get(project_name, {})
        if not project_data:
            project_data = {
                "features": [],
                "tech_stack": [],
                "patterns": [],
                "decisions": []
            }

        project_data["features"] = project_data.get("features", [])
        project_data["features"].append(task)

        st.session_state.long_term.add_project(project_name, project_data)
        st.session_state.long_term.add_learning(project_name, str(result), "task_output")

    def get_agent_states(self) -> Dict[str, str]:
        return st.session_state.short_term.agent_states

    def get_task_status(self) -> str:
        return st.session_state.task_status

    def get_crew_result(self) -> Optional[Any]:
        return st.session_state.crew_result

    def get_memory_data(self) -> Dict[str, Any]:
        return {
            "short_term": st.session_state.short_term.to_mind_map(),
            "long_term_projects": st.session_state.long_term.get_all_projects()
        }

    def clear_session(self):
        st.session_state.short_term.clear()
        st.session_state.crew_result = None
        st.session_state.task_status = "idle"
        st.session_state.agent_outputs = {}

    def clear_project(self, project_name: str):
        st.session_state.long_term.clear_project(project_name)