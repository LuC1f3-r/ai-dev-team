import streamlit as st

AGENT_DISPLAY_NAMES = {
    "manager": "Manager",
    "senior": "Senior Dev",
    "frontend": "Frontend Dev",
    "backend": "Backend Dev",
    "tester": "Tester"
}

AGENT_ICONS = {
    "manager": "🤖",
    "senior": "👨‍💻",
    "frontend": "🎨",
    "backend": "⚙️",
    "tester": "🧪"
}

STATUS_COLORS = {
    "idle": "⚪",
    "waiting": "🟡",
    "active": "🟢",
    "completed": "✅",
    "error": "🔴"
}

STATUS_COLORS_HTML = {
    "idle": "#9CA3AF",
    "waiting": "#F59E0B",
    "active": "#10B981",
    "completed": "#10B981",
    "error": "#EF4444"
}

class AgentStatusComponent:
    @staticmethod
    def render(controller):
        st.subheader("Agent Status")

        agent_states = controller.get_agent_states()

        cols = st.columns(5)

        for idx, (agent_key, display_name) in enumerate(AGENT_DISPLAY_NAMES.items()):
            with cols[idx]:
                state = agent_states.get(agent_key, "idle")
                icon = STATUS_COLORS.get(state, "⚪")

                color = STATUS_COLORS_HTML.get(state, "#9CA3AF")

                st.markdown(f"""
                <div style="
                    background-color: {color}20;
                    border: 2px solid {color};
                    border-radius: 10px;
                    padding: 15px;
                    text-align: center;
                    margin: 5px 0;
                ">
                    <div style="font-size: 24px; margin-bottom: 5px;">{icon}</div>
                    <div style="font-weight: bold; color: white;">{display_name}</div>
                    <div style="font-size: 12px; color: {color}; text-transform: uppercase;">{state}</div>
                </div>
                """, unsafe_allow_html=True)

        task_status = controller.get_task_status()
        status_color = STATUS_COLORS_HTML.get(task_status, "#9CA3AF")

        st.markdown(f"""
        <div style="
            background-color: {status_color}20;
            border: 1px solid {status_color};
            border-radius: 5px;
            padding: 10px;
            text-align: center;
            margin-top: 15px;
        ">
            <span style="color: {status_color}; font-weight: bold;">Overall Status: {task_status.upper()}</span>
        </div>
        """, unsafe_allow_html=True)