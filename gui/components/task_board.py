import streamlit as st

TASK_COLUMNS = ["Backlog", "In Progress", "Review", "Done"]

COLUMN_COLORS = {
    "Backlog": "#6B7280",
    "In Progress": "#3B82F6",
    "Review": "#F59E0B",
    "Done": "#10B981"
}

class TaskBoardComponent:
    @staticmethod
    def render(controller):
        st.subheader("Task Board")

        memory_data = controller.get_memory_data()
        short_term = memory_data.get("short_term", {})
        task_history = short_term.get("task_history", [])

        cols = st.columns(4)

        tasks_by_column = {
            "Backlog": [],
            "In Progress": [],
            "Review": [],
            "Done": []
        }

        current_task = short_term.get("current_task", "")

        if current_task and memory_data.get("short_term", {}).get("agent_states"):
            task_status = controller.get_task_status()
            if task_status == "running":
                tasks_by_column["In Progress"].append({
                    "task": current_task,
                    "status": "running"
                })
            elif task_status == "completed":
                tasks_by_column["Done"].append({
                    "task": current_task,
                    "status": "completed"
                })

        for task in task_history:
            task_text = task.get("task", "")
            status = task.get("status", "unknown")

            if status == "completed":
                tasks_by_column["Done"].append({"task": task_text, "status": status})
            elif status == "running":
                tasks_by_column["In Progress"].append({"task": task_text, "status": status})
            else:
                tasks_by_column["Backlog"].append({"task": task_text, "status": status})

        for idx, column_name in enumerate(TASK_COLUMNS):
            with cols[idx]:
                color = COLUMN_COLORS.get(column_name, "#6B7280")

                st.markdown(f"""
                <div style="
                    background-color: {color}20;
                    border-left: 4px solid {color};
                    padding: 10px;
                    margin-bottom: 10px;
                ">
                    <span style="font-weight: bold; color: {color};">{column_name}</span>
                    <span style="float: right; color: white;">{len(tasks_by_column[column_name])}</span>
                </div>
                """, unsafe_allow_html=True)

                for task in tasks_by_column[column_name]:
                    status_icon = "🔄" if task["status"] == "running" else "✅"

                    st.markdown(f"""
                    <div style="
                        background-color: #1F2937;
                        border-radius: 5px;
                        padding: 10px;
                        margin-bottom: 5px;
                        font-size: 12px;
                    ">
                        {status_icon} {task['task'][:50]}{'...' if len(task['task']) > 50 else ''}
                    </div>
                    """, unsafe_allow_html=True)