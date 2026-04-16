from typing import Dict, List, Any
from datetime import datetime

class ShortTermMemory:
    def __init__(self):
        self.session_id: str = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.context: Dict[str, Any] = {}
        self.agent_states: Dict[str, str] = {}
        self.task_history: List[Dict[str, Any]] = []
        self.current_task: str = ""

    def update_context(self, key: str, value: Any):
        self.context[key] = value

    def update_agent_state(self, agent_name: str, state: str):
        self.agent_states[agent_name] = state

    def add_task(self, task: Dict[str, Any]):
        task["timestamp"] = datetime.now().isoformat()
        self.task_history.append(task)

    def set_current_task(self, task: str):
        self.current_task = task

    def get_context(self) -> Dict[str, Any]:
        return {
            "session_id": self.session_id,
            "context": self.context,
            "agent_states": self.agent_states,
            "current_task": self.current_task,
            "task_history": self.task_history,
        }

    def clear(self):
        self.context = {}
        self.agent_states = {}
        self.task_history = []
        self.current_task = ""

    def to_mind_map(self) -> Dict[str, Any]:
        return {
            "type": "short_term_memory",
            "session_id": self.session_id,
            "current_task": self.current_task,
            "agents": [
                {"name": name, "state": state}
                for name, state in self.agent_states.items()
            ],
            "tasks": self.task_history,
            "context_keys": list(self.context.keys()),
        }