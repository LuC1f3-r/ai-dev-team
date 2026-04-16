import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv()

import json
import threading
import time
from datetime import datetime
from typing import Any, Dict, List

import streamlit as st

from gui.utils.crew_controller import CrewController


PAGES = ["Dashboard", "Agent Roster", "Task Queue", "Memory Store", "Settings"]

AGENTS = [
    {"key": "manager", "role": "Manager Agent", "model": "GPT-4o (Cloud)", "icon": "👑", "tier": "manager"},
    {"key": "senior", "role": "Senior Dev", "model": "Claude 3.5 Sonnet", "icon": "🧠", "tier": "sub"},
    {"key": "frontend", "role": "Frontend Dev", "model": "Llama 3 (Local)", "icon": "🎨", "tier": "sub"},
    {"key": "backend", "role": "Backend Dev", "model": "GPT-4o (Cloud)", "icon": "🛠️", "tier": "sub"},
    {"key": "tester", "role": "QA Tester", "model": "Llama 3 (Local)", "icon": "🛡️", "tier": "sub"},
]

STATE_LABEL = {
    "idle": ("Idle", "#64748b", "rgba(100,116,139,0.12)"),
    "waiting": ("Waiting", "#d97706", "rgba(245,158,11,0.12)"),
    "active": ("Active", "#059669", "rgba(16,185,129,0.12)"),
    "completed": ("Completed", "#2563eb", "rgba(37,99,235,0.12)"),
    "error": ("Error", "#dc2626", "rgba(239,68,68,0.12)"),
}


def inject_global_styles():
    st.markdown(
        """
        <style>
        :root {
            --background: #f8fafc;
            --foreground: #0f172a;
            --card: #ffffff;
            --border: #e2e8f0;
            --primary: #2563eb;
            --muted: #f1f5f9;
            --muted-foreground: #64748b;
        }
        header[data-testid="stHeader"], #MainMenu, footer { display: none !important; }
        .block-container { padding-top: 1rem !important; padding-bottom: 2rem !important; max-width: 1400px !important; }

        .topbar {
            background: var(--card); border: 1px solid var(--border);
            border-radius: 12px; padding: 18px 24px;
            display: flex; justify-content: space-between; align-items: center;
            margin-bottom: 16px;
        }
        .topbar-title { font-size: 18px; font-weight: 600; color: var(--foreground); }
        .topbar-sub { font-size: 13px; color: var(--muted-foreground); margin-top: 2px; }

        .status-pill {
            display: inline-flex; align-items: center; gap: 6px;
            padding: 4px 12px; border-radius: 999px; font-size: 12px; font-weight: 500;
        }
        .status-dot { width: 8px; height: 8px; border-radius: 50%; }

        .agent-card {
            background: var(--card); border: 1px solid var(--border);
            border-radius: 12px; padding: 18px; height: 100%;
            transition: transform 0.15s ease, box-shadow 0.15s ease;
        }
        .agent-card:hover { transform: translateY(-2px); box-shadow: 0 6px 16px -4px rgba(15,23,42,0.08); }
        .agent-card.manager { border-color: var(--primary); box-shadow: 0 4px 6px -1px rgba(37,99,235,0.08); }
        .agent-card.active { animation: pulse 2s ease-in-out infinite; }

        @keyframes pulse {
            0%, 100% { box-shadow: 0 0 0 0 rgba(16,185,129,0.4); }
            50% { box-shadow: 0 0 0 8px rgba(16,185,129,0); }
        }

        .agent-head { display: flex; gap: 12px; align-items: flex-start; margin-bottom: 12px; }
        .agent-avatar {
            width: 40px; height: 40px; border-radius: 8px;
            background: #dbeafe; color: #1d4ed8;
            display: flex; align-items: center; justify-content: center;
            font-size: 22px; flex-shrink: 0;
        }
        .agent-card.manager .agent-avatar { background: var(--primary); color: white; }
        .agent-role { font-size: 15px; font-weight: 600; color: var(--foreground); }
        .agent-model { font-size: 12px; color: var(--muted-foreground); margin-top: 2px; }
        .agent-task {
            font-size: 13px; color: var(--muted-foreground);
            background: var(--muted); border: 1px solid var(--border);
            padding: 10px 12px; border-radius: 8px; margin-top: 12px;
        }
        .agent-task strong {
            display: block; font-size: 11px; text-transform: uppercase;
            letter-spacing: 0.05em; color: var(--foreground); margin-bottom: 4px;
        }

        .empty-state {
            background: var(--card); border: 2px dashed var(--border);
            border-radius: 12px; padding: 48px 24px; text-align: center;
        }
        .empty-state-icon { font-size: 42px; margin-bottom: 12px; }
        .empty-state-title { font-size: 18px; font-weight: 600; color: var(--foreground); margin-bottom: 6px; }
        .empty-state-text { font-size: 14px; color: var(--muted-foreground); }

        .logs-container {
            background: #0f172a; color: #e2e8f0;
            border-radius: 8px; padding: 16px;
            font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
            font-size: 12px; line-height: 1.6;
            max-height: 320px; overflow-y: auto;
        }
        .log-entry { display: flex; gap: 12px; }
        .log-time { color: #64748b; flex-shrink: 0; }
        .log-agent { color: #38bdf8; flex-shrink: 0; min-width: 110px; font-weight: 500; }
        .log-msg.info { color: #f8fafc; }
        .log-msg.success { color: #4ade80; }
        .log-msg.error { color: #f87171; }
        .log-msg.warning { color: #fbbf24; }

        .panel-card {
            background: var(--card); border: 1px solid var(--border);
            border-radius: 12px; padding: 18px;
        }
        .panel-title {
            font-size: 14px; font-weight: 600; color: var(--foreground);
            margin-bottom: 14px; display: flex; align-items: center; gap: 8px;
        }

        .stButton > button {
            border-radius: 8px !important; font-weight: 500 !important;
            transition: all 0.15s ease !important;
        }
        .stButton > button:hover { transform: translateY(-1px); }
        </style>
        """,
        unsafe_allow_html=True,
    )


def init_session():
    if "controller" not in st.session_state:
        st.session_state.controller = CrewController()
    if "page" not in st.session_state:
        st.session_state.page = "Dashboard"
    if "logs" not in st.session_state:
        st.session_state.logs: List[Dict[str, str]] = []
    if "has_submitted" not in st.session_state:
        st.session_state.has_submitted = False
    if "current_project" not in st.session_state:
        st.session_state.current_project = "default"
    if "exec_thread" not in st.session_state:
        st.session_state.exec_thread = None
    if "exec_result" not in st.session_state:
        st.session_state.exec_result = None


def add_log(agent: str, message: str, level: str = "info"):
    st.session_state.logs.append({
        "time": datetime.now().strftime("%H:%M:%S"),
        "agent": agent,
        "message": message,
        "level": level,
    })


def render_sidebar():
    with st.sidebar:
        st.markdown(
            """
            <div style="display:flex; align-items:center; gap:12px; padding: 8px 0 16px;">
                <div style="width:36px; height:36px; background:#2563eb; border-radius:8px;
                            display:flex; align-items:center; justify-content:center;
                            color:white; font-size:20px;">🧠</div>
                <div style="font-size:16px; font-weight:600;">CrewAI Studio</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.caption("MONITORING")
        for page in PAGES[:3]:
            if st.button(page, key=f"nav_{page}", use_container_width=True,
                         type="primary" if st.session_state.page == page else "secondary"):
                st.session_state.page = page
                st.rerun()

        st.caption("SYSTEM")
        for page in PAGES[3:]:
            if st.button(page, key=f"nav_{page}", use_container_width=True,
                         type="primary" if st.session_state.page == page else "secondary"):
                st.session_state.page = page
                st.rerun()

        st.markdown("---")
        controller = st.session_state.controller
        memory_data = controller.get_memory_data()
        project_count = len(memory_data.get("long_term_projects", []))
        log_count = len(st.session_state.logs)

        st.markdown(
            f"""
            <div style="background:#f1f5f9; border:1px solid #e2e8f0; border-radius:8px; padding:12px; font-size:12px;">
                <div style="display:flex; justify-content:space-between; margin-bottom:6px;">
                    <span style="color:#64748b;">Vector DB</span>
                    <span style="color:#059669; font-weight:500;">ChromaDB</span>
                </div>
                <div style="display:flex; justify-content:space-between; margin-bottom:6px;">
                    <span style="color:#64748b;">Projects</span><span>{project_count}</span>
                </div>
                <div style="display:flex; justify-content:space-between;">
                    <span style="color:#64748b;">Log Entries</span><span>{log_count}</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_topbar(controller: CrewController):
    task_status = controller.get_task_status()
    project = st.session_state.current_project

    if task_status == "running":
        pill_color, pill_bg, pill_text = "#059669", "rgba(16,185,129,0.12)", "Crew Running"
    elif task_status == "completed":
        pill_color, pill_bg, pill_text = "#2563eb", "rgba(37,99,235,0.12)", "Completed"
    elif task_status == "error":
        pill_color, pill_bg, pill_text = "#dc2626", "rgba(239,68,68,0.12)", "Error"
    else:
        pill_color, pill_bg, pill_text = "#64748b", "rgba(100,116,139,0.12)", "Idle"

    left, right = st.columns([2, 1])
    with left:
        st.markdown(
            f"""
            <div class="topbar">
                <div>
                    <div class="topbar-title">{project}</div>
                    <div class="topbar-sub">Multi-agent dev team workspace</div>
                </div>
                <div class="status-pill" style="background:{pill_bg}; color:{pill_color};">
                    <div class="status-dot" style="background:{pill_color};"></div>
                    {pill_text}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with right:
        st.markdown('<div style="height:18px;"></div>', unsafe_allow_html=True)
        b1, b2 = st.columns(2)
        with b1:
            if st.button("📥 Export Mind Map", use_container_width=True, key="export_mindmap"):
                handle_export(controller)
        with b2:
            stop_disabled = task_status != "running"
            if st.button("⏹ Stop", use_container_width=True, key="stop_exec",
                         disabled=stop_disabled, type="primary"):
                handle_stop(controller)


def handle_export(controller: CrewController):
    memory = controller.get_memory_data()
    payload = json.dumps(memory, indent=2, default=str)
    st.download_button(
        "Download mind_map.json",
        data=payload,
        file_name=f"mind_map_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
        mime="application/json",
        key="dl_mindmap",
    )
    add_log("System", "Exported current mind map snapshot.", "success")


def handle_stop(controller: CrewController):
    controller.clear_session()
    st.session_state.has_submitted = False
    add_log("System", "Stop requested. Session reset.", "warning")
    st.rerun()


def render_prompt_input(controller: CrewController):
    st.markdown('<div class="panel-card">', unsafe_allow_html=True)
    st.markdown('<div class="panel-title">✨ New Task</div>', unsafe_allow_html=True)

    with st.form("prompt_form", clear_on_submit=False):
        c1, c2 = st.columns([3, 1])
        with c1:
            task = st.text_area(
                "Describe what you want the team to build",
                placeholder="e.g., Build a tic-tac-toe game in React with score tracking",
                height=110,
                label_visibility="collapsed",
            )
        with c2:
            project = st.text_input(
                "Project",
                value=st.session_state.current_project,
                label_visibility="collapsed",
                placeholder="Project name",
            )
            submitted = st.form_submit_button("🚀 Run Crew", use_container_width=True, type="primary")

        if submitted:
            if not task.strip():
                st.warning("Please describe a task before submitting.")
            else:
                st.session_state.current_project = project or "default"
                st.session_state.has_submitted = True
                st.session_state.logs = []
                add_log("System", f"Task accepted: {task.strip()[:80]}", "info")
                add_log("Manager", "Orchestrating workflow…", "info")
                with st.spinner("Crew is working… this can take a moment."):
                    result = controller.execute_task(task.strip(), st.session_state.current_project)
                if result["status"] == "success":
                    add_log("Manager", "Workflow complete.", "success")
                    add_log("System", "Task completed successfully.", "success")
                else:
                    add_log("System", f"Task failed: {result.get('error', 'Unknown error')}", "error")
                st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)


def agent_state_for(controller: CrewController, agent_key: str) -> str:
    states = controller.get_agent_states()
    return states.get(agent_key, "idle")


def render_agent_card(agent: Dict[str, str], state: str, current_task: str):
    label, color, bg = STATE_LABEL.get(state, STATE_LABEL["idle"])
    classes = ["agent-card"]
    if agent["tier"] == "manager":
        classes.append("manager")
    if state == "active":
        classes.append("active")

    task_html = ""
    if current_task and state in ("active", "completed"):
        task_text = current_task[:140] + ("…" if len(current_task) > 140 else "")
        task_html = f'<div class="agent-task"><strong>Current Task</strong>{task_text}</div>'

    st.markdown(
        f"""
        <div class="{' '.join(classes)}">
            <div class="agent-head">
                <div class="agent-avatar">{agent['icon']}</div>
                <div>
                    <div class="agent-role">{agent['role']}</div>
                    <div class="agent-model">{agent['model']}</div>
                </div>
            </div>
            <div class="status-pill" style="background:{bg}; color:{color};">
                <div class="status-dot" style="background:{color};"></div>
                {label}
            </div>
            {task_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_team_section(controller: CrewController):
    st.markdown("### Team Activity")
    current_task = controller.get_memory_data().get("short_term", {}).get("current_task", "")

    manager_col = st.columns([1, 2, 1])[1]
    with manager_col:
        render_agent_card(AGENTS[0], agent_state_for(controller, AGENTS[0]["key"]), current_task)

    st.markdown('<div style="height:16px;"></div>', unsafe_allow_html=True)

    sub_cols = st.columns(4)
    for col, agent in zip(sub_cols, AGENTS[1:]):
        with col:
            render_agent_card(agent, agent_state_for(controller, agent["key"]), current_task)


def render_logs_panel():
    st.markdown('<div class="panel-card">', unsafe_allow_html=True)

    head_l, head_r = st.columns([3, 1])
    with head_l:
        st.markdown('<div class="panel-title">📟 Real-time Execution Logs</div>', unsafe_allow_html=True)
    with head_r:
        if st.button("Clear", key="clear_logs", use_container_width=True):
            st.session_state.logs = []
            st.rerun()

    if not st.session_state.logs:
        st.markdown(
            '<div class="logs-container" style="color:#64748b;">No log entries yet.</div>',
            unsafe_allow_html=True,
        )
    else:
        rows = []
        for entry in st.session_state.logs[-100:]:
            rows.append(
                f'<div class="log-entry">'
                f'<span class="log-time">{entry["time"]}</span>'
                f'<span class="log-agent">[{entry["agent"]}]</span>'
                f'<span class="log-msg {entry["level"]}">{entry["message"]}</span>'
                f'</div>'
            )
        st.markdown(
            f'<div class="logs-container">{"".join(rows)}</div>',
            unsafe_allow_html=True,
        )

    st.markdown("</div>", unsafe_allow_html=True)


def render_memory_panel(controller: CrewController):
    memory_data = controller.get_memory_data()
    projects = memory_data.get("long_term_projects", [])

    st.markdown('<div class="panel-card">', unsafe_allow_html=True)
    st.markdown('<div class="panel-title">💾 Memory System</div>', unsafe_allow_html=True)

    st.markdown(
        f"""
        <div style="margin-bottom:14px;">
            <div style="display:flex; justify-content:space-between; font-size:13px; margin-bottom:6px;">
                <span>Projects stored</span><span>{len(projects)}</span>
            </div>
            <div style="background:#f1f5f9; height:6px; border-radius:999px; overflow:hidden;">
                <div style="background:#10b981; width:{min(len(projects)*10, 100)}%; height:100%;"></div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.button("🔄 Sync Memory", use_container_width=True, key="sync_memory"):
        add_log("System", "Memory synced — refreshed view.", "success")
        st.rerun()

    if st.button("🧹 Clear Session", use_container_width=True, key="clear_session_panel"):
        controller.clear_session()
        st.session_state.has_submitted = False
        st.session_state.logs = []
        add_log("System", "Session cleared.", "warning")
        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)


def render_output(controller: CrewController):
    result = controller.get_crew_result()
    if result is None:
        return

    st.markdown("### Output")
    with st.expander("Full Result", expanded=True):
        st.markdown(str(result))


def render_dashboard(controller: CrewController):
    render_topbar(controller)
    render_prompt_input(controller)

    st.markdown('<div style="height:16px;"></div>', unsafe_allow_html=True)

    if not st.session_state.has_submitted:
        st.markdown(
            """
            <div class="empty-state">
                <div class="empty-state-icon">🚀</div>
                <div class="empty-state-title">Ready when you are</div>
                <div class="empty-state-text">Submit a task above to spin up the crew.
                Agent activity, logs and outputs will appear here.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        return

    render_team_section(controller)
    st.markdown('<div style="height:24px;"></div>', unsafe_allow_html=True)

    left, right = st.columns([2, 1])
    with left:
        render_logs_panel()
    with right:
        render_memory_panel(controller)

    st.markdown('<div style="height:16px;"></div>', unsafe_allow_html=True)
    render_output(controller)


def render_agent_roster(controller: CrewController):
    render_topbar(controller)
    st.markdown("### Agent Roster")
    cols = st.columns(2)
    current_task = controller.get_memory_data().get("short_term", {}).get("current_task", "")
    for i, agent in enumerate(AGENTS):
        with cols[i % 2]:
            render_agent_card(agent, agent_state_for(controller, agent["key"]), current_task)
            st.markdown('<div style="height:12px;"></div>', unsafe_allow_html=True)


def render_task_queue(controller: CrewController):
    render_topbar(controller)
    st.markdown("### Task Queue")

    memory_data = controller.get_memory_data()
    short_term = memory_data.get("short_term", {})
    history = short_term.get("tasks", [])
    current_task = short_term.get("current_task", "")
    status = controller.get_task_status()

    columns = {"Backlog": [], "In Progress": [], "Review": [], "Done": []}
    if current_task:
        if status == "running":
            columns["In Progress"].append({"task": current_task, "status": "running"})
        elif status == "completed":
            columns["Done"].append({"task": current_task, "status": "completed"})
        elif status == "error":
            columns["Backlog"].append({"task": current_task, "status": "error"})

    for entry in history:
        text = entry.get("task", "")
        s = entry.get("status", "unknown")
        if text == current_task:
            continue
        if s == "completed":
            columns["Done"].append({"task": text, "status": s})
        elif s == "running":
            columns["In Progress"].append({"task": text, "status": s})
        else:
            columns["Backlog"].append({"task": text, "status": s})

    palette = {"Backlog": "#6b7280", "In Progress": "#3b82f6", "Review": "#f59e0b", "Done": "#10b981"}
    cols = st.columns(4)
    for col, name in zip(cols, columns.keys()):
        with col:
            color = palette[name]
            st.markdown(
                f"""
                <div style="background:{color}1a; border-left:4px solid {color};
                            padding:10px 12px; border-radius:6px; margin-bottom:10px;
                            display:flex; justify-content:space-between; font-weight:600;">
                    <span style="color:{color};">{name}</span>
                    <span>{len(columns[name])}</span>
                </div>
                """,
                unsafe_allow_html=True,
            )
            for task in columns[name]:
                icon = {"running": "🔄", "completed": "✅", "error": "❌"}.get(task["status"], "📋")
                preview = task["task"][:70] + ("…" if len(task["task"]) > 70 else "")
                st.markdown(
                    f"""
                    <div style="background:#fff; border:1px solid #e2e8f0;
                                border-radius:8px; padding:10px 12px; margin-bottom:8px;
                                font-size:13px; color:#0f172a;">
                        {icon} {preview}
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            if not columns[name]:
                st.markdown(
                    '<div style="font-size:12px; color:#94a3b8; text-align:center; padding:12px;">Empty</div>',
                    unsafe_allow_html=True,
                )


def render_memory_store(controller: CrewController):
    render_topbar(controller)
    st.markdown("### Memory Store")

    memory_data = controller.get_memory_data()
    projects = memory_data.get("long_term_projects", [])
    mind_map = memory_data.get("short_term", {})

    left, right = st.columns([1, 2])
    with left:
        render_memory_panel(controller)

    with right:
        st.markdown('<div class="panel-card">', unsafe_allow_html=True)
        st.markdown('<div class="panel-title">📁 Stored Projects</div>', unsafe_allow_html=True)
        if projects:
            selected = st.selectbox("Select a project", projects, key="memory_select")
            if st.button(f"Delete '{selected}'", key="del_proj", type="secondary"):
                controller.clear_project(selected)
                add_log("System", f"Deleted project '{selected}'.", "warning")
                st.rerun()
        else:
            st.info("No projects stored yet.")
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div style="height:16px;"></div>', unsafe_allow_html=True)
    st.markdown("#### Session Mind Map")
    st.json(mind_map, expanded=False)


def render_settings(controller: CrewController):
    render_topbar(controller)
    st.markdown("### Settings")

    st.markdown('<div class="panel-card">', unsafe_allow_html=True)
    st.markdown('<div class="panel-title">⚙️ Runtime</div>', unsafe_allow_html=True)
    st.text_input("Default project name", value=st.session_state.current_project, key="settings_project",
                  on_change=lambda: st.session_state.update(current_project=st.session_state.settings_project))
    st.selectbox("Preferred LLM", ["gpt-4 (cloud)", "ollama/llama3 (local)", "claude-3.5-sonnet"],
                 key="settings_llm")
    st.toggle("Verbose agent logging", value=True, key="settings_verbose")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div style="height:16px;"></div>', unsafe_allow_html=True)
    st.markdown('<div class="panel-card">', unsafe_allow_html=True)
    st.markdown('<div class="panel-title">🔐 API Keys</div>', unsafe_allow_html=True)
    st.caption("Set keys via environment variables (OPENAI_API_KEY, ANTHROPIC_API_KEY) — they are read at runtime.")
    st.markdown("</div>", unsafe_allow_html=True)


def main():
    st.set_page_config(page_title="AI Dev Team", layout="wide", initial_sidebar_state="expanded")
    inject_global_styles()
    init_session()

    render_sidebar()

    controller = st.session_state.controller
    page = st.session_state.page

    if page == "Dashboard":
        render_dashboard(controller)
    elif page == "Agent Roster":
        render_agent_roster(controller)
    elif page == "Task Queue":
        render_task_queue(controller)
    elif page == "Memory Store":
        render_memory_store(controller)
    elif page == "Settings":
        render_settings(controller)


if __name__ == "__main__":
    main()
