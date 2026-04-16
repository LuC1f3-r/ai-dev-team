from textwrap import dedent

import streamlit as st

from gui.components.agent_status import AgentStatusComponent
from gui.components.output_viewer import OutputViewerComponent
from gui.components.task_board import TaskBoardComponent
from gui.components.task_input import TaskInputComponent
from gui.utils.crew_controller import CrewController


TRANSACTIONS = [
    {
        "section": "Today",
        "name": "Eva Novak",
        "status": "Received",
        "amount": "+$5,710.20",
        "amount_class": "positive",
        "avatar_class": "avatar-photo avatar-eva",
        "avatar_markup": "E",
    },
    {
        "section": "Today",
        "name": "Binance",
        "status": "Received",
        "amount": "+$714.00",
        "amount_class": "positive",
        "avatar_class": "avatar-logo avatar-binance",
        "avatar_markup": "◆",
    },
    {
        "section": "Yesterday",
        "name": "Henrik Jansen",
        "status": "Received",
        "amount": "+$428.00",
        "amount_class": "positive",
        "avatar_class": "avatar-photo avatar-henrik",
        "avatar_markup": "H",
    },
    {
        "section": "Yesterday",
        "name": "Multiplex",
        "status": "Paid",
        "amount": "-$124.55",
        "amount_class": "negative",
        "avatar_class": "avatar-logo avatar-multiplex",
        "avatar_markup": "M",
    },
]

DOT_CHART_VALUES = [
    12, 0, 5, 0, 7, 3, 0, 5, 6, 24, 0, 0,
    15, 6, 11, 0, 4, 13, 18, 22, 15, 8, 1, 0,
    4, 7, 11, 8, 0, 5, 0, 6, 3, 0, 0, 0,
    0, 12, 8, 5, 9, 0, 11,
]

BELL_ICON = """
<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
  <path d="M15 17H9a3 3 0 0 1-3-3v-3.3a6 6 0 1 1 12 0V14a3 3 0 0 1-3 3Z"></path>
  <path d="M10 20a2 2 0 0 0 4 0"></path>
</svg>
"""

CHART_ICON = """
<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
  <path d="M4 16l5-5 4 4 7-8"></path>
  <path d="M20 8v7h-7"></path>
  <rect x="3" y="3" width="18" height="18" rx="4"></rect>
</svg>
"""

EYE_OFF_ICON = """
<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
  <path d="M3 3l18 18"></path>
  <path d="M10.6 10.7a2 2 0 0 0 2.7 2.7"></path>
  <path d="M9.4 5.1A10.9 10.9 0 0 1 12 4.8c5.1 0 8.7 3.8 9.9 7.2a1 1 0 0 1 0 .6 11.8 11.8 0 0 1-4 5.1"></path>
  <path d="M6.1 6.1A12 12 0 0 0 2.1 12a1 1 0 0 0 0 .6c1.2 3.4 4.8 7.2 9.9 7.2 1 0 2-.1 2.8-.4"></path>
</svg>
"""

PAY_ICON = """
<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
  <circle cx="12" cy="12" r="8.5"></circle>
  <path d="M12 8v8"></path>
  <path d="m9.3 10.7 2.7-2.7 2.7 2.7"></path>
</svg>
"""

TRANSFER_ICON = """
<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
  <path d="M7 7h10"></path>
  <path d="m13 3 4 4-4 4"></path>
  <path d="M17 17H7"></path>
  <path d="m11 21-4-4 4-4"></path>
</svg>
"""

RECEIVE_ICON = """
<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
  <circle cx="12" cy="12" r="8.5"></circle>
  <path d="M12 8v8"></path>
  <path d="m9.3 13.3 2.7 2.7 2.7-2.7"></path>
</svg>
"""

HOME_ICON = """
<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
  <path d="M4 11.5 12 5l8 6.5"></path>
  <path d="M7 10.5V19h10v-8.5"></path>
</svg>
"""


def build_transactions_html() -> str:
    chunks = []
    current_section = None

    for item in TRANSACTIONS:
        section = item["section"]
        if section != current_section:
            chunks.append(f"<div class='section-label'>{section}</div>")
            current_section = section

        chunks.append(
            f"""
            <div class="txn-card">
                <div class="txn-meta">
                    <div class="txn-avatar {item['avatar_class']}">{item['avatar_markup']}</div>
                    <div>
                        <div class="txn-name">{item['name']}</div>
                        <div class="txn-status">
                            <span>{item['status']}</span>
                            <span class="txn-status-icon">{RECEIVE_ICON}</span>
                        </div>
                    </div>
                </div>
                <div class="txn-amount {item['amount_class']}">{item['amount']}</div>
            </div>
            """
        )

    return "".join(chunks)


def build_dot_chart_html() -> str:
    bars = []
    highlight_index = 9

    for index, value in enumerate(DOT_CHART_VALUES):
        dots = []
        for dot_index in range(value):
            dot_class = "chart-dot chart-dot--active" if index == highlight_index else "chart-dot"
            if index == highlight_index and dot_index == value - 1:
                dot_class += " chart-dot--ring"
            dots.append(f"<span class='{dot_class}'></span>")

        bars.append(f"<div class='chart-bar'>{''.join(dots)}</div>")

    return "".join(bars)


def render_hero_screen():
    transactions_html = build_transactions_html()
    dot_chart_html = build_dot_chart_html()

    st.markdown(
        dedent(
            f"""
            <section class="hero-shell">
                <div class="hero-grid">
                    <div class="hero-panel hero-panel--list">
                        <div class="soft-glow soft-glow--lime"></div>
                        <div class="soft-glow soft-glow--mint"></div>
                        {transactions_html}
                    </div>

                    <div class="hero-panel hero-panel--chart">
                        <div class="total-rate-card">
                            <div class="total-rate-head">
                                <span>Total Rate</span>
                                <span class="rate-select">Yearly</span>
                            </div>
                            <div class="chart-tooltip">
                                <div class="chart-tooltip-amount">$118,952.34</div>
                                <div class="chart-tooltip-label">Total Spend</div>
                            </div>
                            <div class="dot-chart">{dot_chart_html}</div>
                        </div>
                    </div>

                    <div class="hero-panel hero-panel--phone">
                        <div class="phone-ambient phone-ambient--left"></div>
                        <div class="phone-ambient phone-ambient--right"></div>
                        <div class="phone-holder">
                            <div class="phone-frame">
                                <div class="phone-notch"></div>
                                <div class="phone-screen">
                                    <div class="phone-status-row">
                                        <span>9:41</span>
                                        <div class="phone-status-icons">
                                            <span class="signal-bars"><i></i><i></i><i></i></span>
                                            <span class="wifi-icon"></span>
                                            <span class="battery-icon"></span>
                                        </div>
                                    </div>

                                    <div class="app-toolbar">
                                        <div class="app-user">
                                            <div class="phone-avatar">L</div>
                                            <span>Hi, Leandro!</span>
                                        </div>
                                        <div class="toolbar-icons">
                                            <span>{BELL_ICON}</span>
                                            <span>{CHART_ICON}</span>
                                        </div>
                                    </div>

                                    <div class="balance-card">
                                        <div class="balance-card-top">
                                            <span>USD</span>
                                            <span class="eye-off">{EYE_OFF_ICON}</span>
                                        </div>
                                        <div class="exchange-rate">1 USD = EUR 0.95 = GBR 0.79</div>
                                        <div class="balance-value">$26,887.09</div>
                                        <div class="balance-delta">+$421.03</div>
                                    </div>

                                    <div class="action-strip">
                                        <div class="action-item">
                                            <span>{PAY_ICON}</span>
                                            <span>Pay</span>
                                        </div>
                                        <div class="action-divider"></div>
                                        <div class="action-item">
                                            <span>{TRANSFER_ICON}</span>
                                            <span>Transfer</span>
                                        </div>
                                        <div class="action-divider"></div>
                                        <div class="action-item">
                                            <span>{RECEIVE_ICON}</span>
                                            <span>Receive</span>
                                        </div>
                                    </div>

                                    <div class="phone-section-head">
                                        <span>Latest Transactions</span>
                                        <span>See All</span>
                                    </div>

                                    <div class="latest-card">
                                        <div class="latest-meta">
                                            <div class="latest-icon">▣</div>
                                            <div>
                                                <div class="latest-name">Megogo</div>
                                                <div class="latest-time">1 min ago</div>
                                            </div>
                                        </div>
                                        <div class="latest-amount">-$24.99</div>
                                    </div>

                                    <div class="phone-section-head phone-section-head--currency">
                                        <span>Currency</span>
                                    </div>

                                    <div class="currency-grid">
                                        <div class="currency-card">
                                            <div class="currency-symbol currency-symbol--green">€</div>
                                            <div class="currency-name">Euro</div>
                                            <div class="currency-rate">0.97</div>
                                        </div>
                                        <div class="currency-card">
                                            <div class="currency-symbol currency-symbol--blue">£</div>
                                            <div class="currency-name">British pound</div>
                                            <div class="currency-rate">0.82</div>
                                        </div>
                                        <div class="currency-card currency-card--dark">
                                            <div class="currency-plus">+</div>
                                            <div class="currency-card-copy">
                                                <span>Add</span>
                                                <span>Currency</span>
                                            </div>
                                        </div>
                                    </div>

                                    <div class="phone-bottom-nav">
                                        <button class="nav-icon">{PAY_ICON}</button>
                                        <button class="nav-icon nav-icon--active">{HOME_ICON}</button>
                                        <button class="nav-icon">{RECEIVE_ICON}</button>
                                    </div>

                                    <div class="home-indicator"></div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </section>
            """
        ),
        unsafe_allow_html=True,
    )


def render_memory_panel(controller: CrewController):
    memory_data = controller.get_memory_data()
    projects = memory_data.get("long_term_projects", [])
    mind_map = memory_data.get("short_term", {})

    action_col, project_col = st.columns([1, 2], gap="large")

    with action_col:
        if st.button("Clear Session", key="clear_session_main", use_container_width=True):
            controller.clear_session()
            st.rerun()

    with project_col:
        if projects:
            selected_project = st.selectbox("Stored Projects", projects, key="memory_project_selector")
            delete_col, details_col = st.columns([1, 3], gap="medium")

            with delete_col:
                if st.button("Delete Project", key=f"delete_{selected_project}", use_container_width=True):
                    controller.clear_project(selected_project)
                    st.rerun()

            with details_col:
                st.caption(f"Selected project: `{selected_project}`")
        else:
            st.info("No projects in memory yet.")

    st.subheader("Session Mind Map")
    st.json(mind_map, expanded=True)


def inject_styles():
    st.markdown(
        dedent(
            """
            <style>
            @import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&display=swap');

            :root {
                --page-bg: #eef4ec;
                --page-ink: #141414;
                --muted-ink: #7a7d74;
                --line-soft: rgba(20, 20, 20, 0.08);
                --white: #ffffff;
                --accent-yellow: #fff566;
                --accent-green: #17a53a;
                --accent-red: #b0221e;
                --chart-dot: #73746e;
                --phone-shadow: 0 36px 90px rgba(0, 0, 0, 0.18);
            }

            html, body, [class*="css"] {
                font-family: "Manrope", sans-serif;
            }

            .stApp {
                background:
                    radial-gradient(circle at 12% 8%, rgba(241, 249, 179, 0.8), transparent 24%),
                    radial-gradient(circle at 75% 18%, rgba(223, 250, 206, 0.7), transparent 24%),
                    linear-gradient(135deg, #eef6f0 0%, #dff0f0 48%, #ebf7de 100%);
                color: var(--page-ink);
            }

            .block-container {
                max-width: 100%;
                padding: 0 0 3rem;
            }

            header[data-testid="stHeader"],
            div[data-testid="stToolbar"],
            #MainMenu,
            footer,
            section[data-testid="stSidebar"] {
                display: none;
            }

            .hero-shell {
                padding: 12px;
            }

            .hero-grid {
                display: grid;
                grid-template-columns: minmax(0, 1.02fr) minmax(0, 1fr);
                grid-template-rows: minmax(460px, auto) minmax(460px, auto);
                gap: 10px;
                background: rgba(255, 255, 255, 0.96);
                min-height: calc(100vh - 24px);
            }

            .hero-panel {
                position: relative;
                overflow: hidden;
                background:
                    radial-gradient(circle at 15% 10%, rgba(243, 251, 181, 0.92), transparent 28%),
                    radial-gradient(circle at 70% 24%, rgba(208, 252, 224, 0.78), transparent 32%),
                    linear-gradient(135deg, #e4f2ef 0%, #d9eef1 48%, #e3f4db 100%);
            }

            .hero-panel--list {
                padding: 56px 68px 48px;
            }

            .hero-panel--chart {
                padding: 58px 58px 48px;
                display: flex;
                align-items: flex-end;
            }

            .hero-panel--phone {
                grid-row: 1 / span 2;
                display: flex;
                align-items: center;
                justify-content: center;
                padding: 34px;
            }

            .soft-glow,
            .phone-ambient {
                position: absolute;
                border-radius: 999px;
                filter: blur(22px);
                opacity: 0.55;
                pointer-events: none;
            }

            .soft-glow--lime {
                inset: auto auto 8% -7%;
                width: 220px;
                height: 220px;
                background: rgba(232, 247, 117, 0.45);
            }

            .soft-glow--mint {
                inset: -6% 8% auto auto;
                width: 280px;
                height: 280px;
                background: rgba(199, 255, 223, 0.38);
            }

            .section-label {
                color: #707568;
                font-size: 1.02rem;
                font-weight: 500;
                margin: 0 0 14px;
            }

            .section-label:not(:first-child) {
                margin-top: 22px;
            }

            .txn-card {
                display: flex;
                align-items: center;
                justify-content: space-between;
                background: rgba(255, 255, 255, 0.92);
                border-radius: 30px;
                padding: 20px 24px;
                margin-bottom: 12px;
                box-shadow: 0 16px 35px rgba(115, 135, 120, 0.08);
            }

            .txn-meta {
                display: flex;
                align-items: center;
                gap: 14px;
            }

            .txn-avatar {
                width: 54px;
                height: 54px;
                border-radius: 50%;
                display: inline-flex;
                align-items: center;
                justify-content: center;
                font-size: 1.15rem;
                font-weight: 800;
                color: #fff;
                flex-shrink: 0;
                letter-spacing: 0.02em;
            }

            .avatar-photo {
                color: rgba(255, 255, 255, 0);
                background-size: cover;
                background-position: center;
                box-shadow: inset 0 0 0 1px rgba(0, 0, 0, 0.04);
            }

            .avatar-eva {
                background:
                    radial-gradient(circle at 50% 30%, #ffe5d0 0 24%, transparent 25%),
                    radial-gradient(circle at 50% 82%, #e7cfba 0 18%, transparent 19%),
                    radial-gradient(circle at 50% 40%, #6d4c41 0 46%, transparent 47%),
                    linear-gradient(135deg, #a87c63 0%, #f4efe7 100%);
            }

            .avatar-henrik {
                background:
                    radial-gradient(circle at 50% 30%, #f0d7c3 0 24%, transparent 25%),
                    radial-gradient(circle at 50% 82%, #d7c1aa 0 19%, transparent 20%),
                    radial-gradient(circle at 50% 38%, #60463a 0 46%, transparent 47%),
                    linear-gradient(135deg, #b09a83 0%, #f6f1ea 100%);
            }

            .avatar-logo {
                box-shadow: inset 0 0 0 1px rgba(255, 255, 255, 0.06);
            }

            .avatar-binance {
                background: #161616;
                color: #f3c84d;
            }

            .avatar-multiplex {
                background: #141414;
                color: #ff4f4f;
            }

            .txn-name {
                font-size: 1.15rem;
                font-weight: 600;
                color: #131313;
                line-height: 1.2;
            }

            .txn-status {
                display: flex;
                align-items: center;
                gap: 8px;
                font-size: 0.95rem;
                color: var(--muted-ink);
                margin-top: 4px;
            }

            .txn-status-icon {
                width: 18px;
                height: 18px;
                display: inline-flex;
                color: #8a8d86;
            }

            .txn-status-icon svg {
                width: 100%;
                height: 100%;
            }

            .txn-amount {
                font-size: 1.1rem;
                font-weight: 600;
                letter-spacing: -0.03em;
            }

            .txn-amount.positive {
                color: var(--accent-green);
            }

            .txn-amount.negative {
                color: var(--accent-red);
            }

            .total-rate-card {
                position: relative;
                width: min(100%, 760px);
                min-height: 520px;
                background: rgba(255, 255, 255, 0.93);
                border-radius: 34px;
                padding: 30px 34px 20px;
                box-shadow: 0 20px 44px rgba(115, 135, 120, 0.08);
            }

            .total-rate-head {
                display: flex;
                align-items: center;
                justify-content: space-between;
                font-size: 1rem;
                color: #171717;
                margin-bottom: 28px;
            }

            .rate-select {
                color: var(--muted-ink);
            }

            .chart-tooltip {
                position: absolute;
                top: 104px;
                left: 228px;
                background: var(--accent-yellow);
                border-radius: 14px;
                padding: 12px 18px 10px;
                box-shadow: 0 14px 26px rgba(244, 238, 84, 0.28);
            }

            .chart-tooltip-amount {
                font-size: 0.96rem;
                font-weight: 700;
                color: #1b1b1b;
            }

            .chart-tooltip-label {
                margin-top: 2px;
                font-size: 0.92rem;
                color: #4c4f45;
            }

            .dot-chart {
                position: absolute;
                inset: auto 34px 0 34px;
                height: 380px;
                display: flex;
                align-items: flex-end;
                justify-content: space-between;
                gap: 7px;
            }

            .chart-bar {
                display: flex;
                flex: 1 1 0;
                min-width: 5px;
                flex-direction: column-reverse;
                align-items: center;
                gap: 6px;
            }

            .chart-dot {
                width: 7px;
                height: 7px;
                border-radius: 50%;
                background: var(--chart-dot);
            }

            .chart-dot--active {
                background: #ffea00;
            }

            .chart-dot--ring {
                width: 15px;
                height: 15px;
                border: 5px solid #ffea00;
                background: #fff;
                box-sizing: border-box;
            }

            .phone-holder {
                position: relative;
                display: flex;
                align-items: center;
                justify-content: center;
                width: 100%;
                height: 100%;
            }

            .phone-holder::after {
                content: "";
                position: absolute;
                right: 8%;
                bottom: 5%;
                width: 270px;
                height: 320px;
                border-radius: 140px 140px 36px 36px;
                background:
                    radial-gradient(circle at 30% 24%, rgba(255, 224, 202, 0.78), transparent 24%),
                    linear-gradient(180deg, rgba(140, 87, 57, 0.45) 0%, rgba(87, 50, 32, 0.78) 100%);
                filter: blur(4px);
                transform: rotate(-10deg);
                opacity: 0.78;
                z-index: 0;
            }

            .phone-ambient--left {
                width: 220px;
                height: 220px;
                left: 10%;
                bottom: 18%;
                background: rgba(224, 251, 168, 0.42);
            }

            .phone-ambient--right {
                width: 260px;
                height: 260px;
                right: 4%;
                top: 8%;
                background: rgba(208, 255, 220, 0.4);
            }

            .phone-frame {
                position: relative;
                z-index: 2;
                width: min(100%, 420px);
                border: 10px solid #0a0a0a;
                border-radius: 44px;
                background: #0d0d0d;
                box-shadow: var(--phone-shadow);
                padding: 10px;
            }

            .phone-screen {
                position: relative;
                overflow: hidden;
                border-radius: 34px;
                padding: 18px 18px 22px;
                background:
                    radial-gradient(circle at 15% 12%, rgba(244, 251, 183, 0.9), transparent 28%),
                    radial-gradient(circle at 72% 24%, rgba(213, 252, 224, 0.78), transparent 34%),
                    linear-gradient(135deg, #e7f4ec 0%, #dff1ef 46%, #e6f7dc 100%);
            }

            .phone-notch {
                position: absolute;
                left: 50%;
                top: 12px;
                transform: translateX(-50%);
                width: 112px;
                height: 32px;
                background: #060606;
                border-radius: 18px;
                z-index: 5;
            }

            .phone-status-row {
                display: flex;
                align-items: center;
                justify-content: space-between;
                font-size: 0.86rem;
                font-weight: 700;
                padding: 8px 10px 0;
                color: #111;
            }

            .phone-status-icons {
                display: flex;
                align-items: center;
                gap: 7px;
            }

            .signal-bars {
                display: flex;
                align-items: end;
                gap: 2px;
                height: 11px;
            }

            .signal-bars i {
                display: block;
                width: 3px;
                background: #111;
                border-radius: 2px;
            }

            .signal-bars i:nth-child(1) { height: 5px; }
            .signal-bars i:nth-child(2) { height: 7px; }
            .signal-bars i:nth-child(3) { height: 10px; }

            .wifi-icon {
                width: 13px;
                height: 9px;
                border: 2px solid #111;
                border-top-color: #111;
                border-left-color: transparent;
                border-right-color: transparent;
                border-bottom: 0;
                border-radius: 10px 10px 0 0;
                transform: scaleX(1.15);
            }

            .battery-icon {
                position: relative;
                width: 21px;
                height: 10px;
                border: 2px solid #111;
                border-radius: 3px;
            }

            .battery-icon::after {
                content: "";
                position: absolute;
                right: -4px;
                top: 2px;
                width: 2px;
                height: 4px;
                border-radius: 1px;
                background: #111;
            }

            .app-toolbar {
                display: flex;
                align-items: center;
                justify-content: space-between;
                margin-top: 22px;
                padding: 0 2px;
            }

            .app-user {
                display: flex;
                align-items: center;
                gap: 10px;
                font-size: 0.9rem;
                font-weight: 600;
                color: #1a1a1a;
            }

            .phone-avatar {
                width: 40px;
                height: 40px;
                border-radius: 50%;
                display: inline-flex;
                align-items: center;
                justify-content: center;
                color: rgba(255, 255, 255, 0);
                background:
                    radial-gradient(circle at 50% 30%, #ffddb8 0 24%, transparent 25%),
                    radial-gradient(circle at 50% 82%, #cfb094 0 18%, transparent 19%),
                    radial-gradient(circle at 50% 40%, #4a3a31 0 46%, transparent 47%),
                    linear-gradient(135deg, #0bb09d 0%, #31d0ae 100%);
                box-shadow: inset 0 0 0 1px rgba(0, 0, 0, 0.03);
            }

            .toolbar-icons {
                display: flex;
                align-items: center;
                gap: 12px;
                color: #1a1a1a;
            }

            .toolbar-icons span,
            .eye-off {
                width: 19px;
                height: 19px;
                display: inline-flex;
            }

            .toolbar-icons svg,
            .eye-off svg {
                width: 100%;
                height: 100%;
            }

            .balance-card {
                background: var(--accent-yellow);
                border-radius: 32px;
                padding: 20px 22px 18px;
                margin-top: 22px;
                text-align: center;
                box-shadow: inset 0 0 0 7px rgba(255, 255, 255, 0.9);
            }

            .balance-card-top {
                display: flex;
                align-items: center;
                justify-content: space-between;
                margin-bottom: 6px;
                font-size: 0.86rem;
                font-weight: 700;
                color: #141414;
            }

            .exchange-rate {
                font-size: 0.72rem;
                color: rgba(20, 20, 20, 0.56);
            }

            .balance-value {
                margin-top: 8px;
                font-size: clamp(2rem, 4vw, 3.35rem);
                line-height: 1;
                font-weight: 800;
                letter-spacing: -0.06em;
                color: #131313;
            }

            .balance-delta {
                margin-top: 8px;
                font-size: 0.86rem;
                font-weight: 700;
                color: #1a1a1a;
            }

            .action-strip {
                display: flex;
                align-items: center;
                justify-content: space-between;
                background: rgba(255, 255, 255, 0.92);
                border-radius: 0 0 28px 28px;
                padding: 15px 18px;
                margin-top: -8px;
                box-shadow: 0 14px 30px rgba(128, 144, 122, 0.08);
            }

            .action-item {
                display: flex;
                flex: 1;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                gap: 6px;
                font-size: 0.82rem;
                color: #6d7068;
            }

            .action-item span:first-child {
                width: 22px;
                height: 22px;
                color: #7d7f79;
            }

            .action-item svg {
                width: 100%;
                height: 100%;
            }

            .action-divider {
                width: 1px;
                align-self: stretch;
                background: rgba(20, 20, 20, 0.08);
            }

            .phone-section-head {
                display: flex;
                align-items: center;
                justify-content: space-between;
                margin-top: 18px;
                padding: 0 2px;
                color: #191919;
                font-size: 0.78rem;
                font-weight: 600;
            }

            .phone-section-head span:last-child {
                color: #707568;
                font-weight: 500;
            }

            .phone-section-head--currency {
                margin-top: 20px;
            }

            .latest-card {
                display: flex;
                align-items: center;
                justify-content: space-between;
                gap: 12px;
                margin-top: 10px;
                background: rgba(255, 255, 255, 0.94);
                border-radius: 18px;
                padding: 12px 14px;
                box-shadow: 0 10px 22px rgba(128, 144, 122, 0.08);
            }

            .latest-meta {
                display: flex;
                align-items: center;
                gap: 10px;
            }

            .latest-icon {
                width: 38px;
                height: 38px;
                border-radius: 50%;
                background: #1b1b1b;
                color: #28d6cc;
                display: inline-flex;
                align-items: center;
                justify-content: center;
                font-size: 1.1rem;
            }

            .latest-name {
                font-size: 0.82rem;
                font-weight: 700;
                color: #151515;
            }

            .latest-time {
                margin-top: 2px;
                font-size: 0.72rem;
                color: #80847d;
            }

            .latest-amount {
                color: var(--accent-red);
                font-size: 0.82rem;
                font-weight: 700;
            }

            .currency-grid {
                display: grid;
                grid-template-columns: repeat(3, minmax(0, 1fr));
                gap: 12px;
                margin-top: 10px;
            }

            .currency-card {
                min-height: 118px;
                background: rgba(255, 255, 255, 0.94);
                border-radius: 18px;
                padding: 14px;
                display: flex;
                flex-direction: column;
                justify-content: space-between;
                box-shadow: 0 10px 22px rgba(128, 144, 122, 0.08);
            }

            .currency-symbol {
                width: 34px;
                height: 34px;
                border-radius: 50%;
                display: inline-flex;
                align-items: center;
                justify-content: center;
                font-size: 1.15rem;
                background: rgba(17, 165, 58, 0.08);
            }

            .currency-symbol--green {
                color: #34cf53;
            }

            .currency-symbol--blue {
                color: #5a8fe6;
                background: rgba(90, 143, 230, 0.08);
            }

            .currency-name {
                font-size: 0.78rem;
                color: #707568;
            }

            .currency-rate {
                font-size: 0.9rem;
                font-weight: 700;
                color: #191919;
            }

            .currency-card--dark {
                background: #171717;
                color: #fff;
                align-items: center;
                justify-content: center;
                gap: 10px;
                text-align: center;
            }

            .currency-plus {
                font-size: 2rem;
                line-height: 1;
            }

            .currency-card-copy {
                display: flex;
                flex-direction: column;
                gap: 2px;
                font-size: 0.9rem;
            }

            .phone-bottom-nav {
                display: flex;
                align-items: center;
                justify-content: center;
                gap: 14px;
                margin-top: 22px;
            }

            .nav-icon {
                width: 46px;
                height: 46px;
                border: 0;
                border-radius: 50%;
                background: rgba(255, 255, 255, 0.88);
                color: #707568;
                display: inline-flex;
                align-items: center;
                justify-content: center;
                cursor: default;
                box-shadow: 0 10px 18px rgba(128, 144, 122, 0.08);
            }

            .nav-icon svg {
                width: 19px;
                height: 19px;
            }

            .nav-icon--active {
                background: #171717;
                color: #fff;
                transform: scale(1.08);
            }

            .home-indicator {
                width: 42%;
                height: 5px;
                background: #121212;
                border-radius: 999px;
                margin: 18px auto 0;
                opacity: 0.92;
            }

            .workspace-head {
                padding: 28px 30px 8px;
            }

            .workspace-kicker {
                display: inline-flex;
                align-items: center;
                gap: 8px;
                padding: 6px 12px;
                border-radius: 999px;
                background: rgba(255, 255, 255, 0.74);
                border: 1px solid rgba(20, 20, 20, 0.06);
                font-size: 0.78rem;
                font-weight: 700;
                letter-spacing: 0.04em;
                text-transform: uppercase;
                color: #5e6358;
            }

            .workspace-head h1 {
                margin: 14px 0 8px;
                font-size: clamp(2rem, 5vw, 3.35rem);
                line-height: 1;
                letter-spacing: -0.05em;
                color: #111;
            }

            .workspace-head p {
                max-width: 740px;
                margin: 0;
                color: #63675f;
                font-size: 1rem;
                line-height: 1.6;
            }

            .stTabs [data-baseweb="tab-list"] {
                gap: 8px;
                padding: 0 30px;
                margin-bottom: 20px;
            }

            .stTabs [data-baseweb="tab"] {
                background: rgba(255, 255, 255, 0.72);
                border-radius: 999px;
                padding: 10px 18px;
                border: 1px solid rgba(20, 20, 20, 0.06);
                color: #5e6358;
            }

            .stTabs [aria-selected="true"] {
                background: #171717 !important;
                color: #fff !important;
            }

            .stTabs [data-baseweb="tab-panel"] {
                padding: 0 30px;
            }

            .stTextArea textarea,
            .stTextInput input,
            .stSelectbox [data-baseweb="select"] > div,
            .stMultiSelect [data-baseweb="select"] > div {
                border-radius: 18px !important;
                border: 1px solid rgba(20, 20, 20, 0.08) !important;
                background: rgba(255, 255, 255, 0.86) !important;
                color: #111 !important;
                box-shadow: none !important;
            }

            .stButton > button,
            .stFormSubmitButton > button {
                border: 0 !important;
                border-radius: 999px !important;
                background: #171717 !important;
                color: #fff !important;
                padding: 0.7rem 1.2rem !important;
                font-weight: 700 !important;
                box-shadow: none !important;
            }

            .stAlert {
                border-radius: 20px;
            }

            .stSubheader,
            .stMarkdown,
            .stCaption,
            .stText,
            .stJson {
                color: #151515;
            }

            div[data-testid="stVerticalBlock"] > div:has(> .element-container .stSubheader) {
                background: rgba(255, 255, 255, 0.62);
                border: 1px solid rgba(20, 20, 20, 0.05);
                border-radius: 28px;
                padding: 22px;
                backdrop-filter: blur(12px);
            }

            @media (max-width: 1280px) {
                .hero-grid {
                    grid-template-columns: 1fr;
                    grid-template-rows: auto;
                    min-height: auto;
                }

                .hero-panel--phone {
                    grid-row: auto;
                    min-height: 760px;
                }

                .chart-tooltip {
                    left: 190px;
                }
            }

            @media (max-width: 980px) {
                .hero-panel--list,
                .hero-panel--chart,
                .hero-panel--phone {
                    padding: 30px 22px;
                }

                .total-rate-card {
                    min-height: 420px;
                    padding: 24px 22px 20px;
                }

                .dot-chart {
                    inset: auto 18px 0 18px;
                    gap: 5px;
                }

                .chart-tooltip {
                    top: 94px;
                    left: 110px;
                }

                .txn-card {
                    padding: 16px 18px;
                    border-radius: 24px;
                }

                .phone-holder::after {
                    display: none;
                }

                .stTabs [data-baseweb="tab-list"],
                .stTabs [data-baseweb="tab-panel"],
                .workspace-head {
                    padding-left: 18px;
                    padding-right: 18px;
                }
            }
            </style>
            """
        ),
        unsafe_allow_html=True,
    )


def main():
    st.set_page_config(
        page_title="AI Dev Team",
        layout="wide",
        initial_sidebar_state="collapsed",
    )

    inject_styles()

    if "controller" not in st.session_state:
        st.session_state.controller = CrewController()

    controller = st.session_state.controller

    render_hero_screen()

    st.markdown(
        dedent(
            """
            <section class="workspace-head">
                <span class="workspace-kicker">AI Dev Team</span>
                <h1>Command Center</h1>
                <p>Launch new build requests, monitor the agent crew, and inspect the generated output without losing the new landing screen aesthetic.</p>
            </section>
            """
        ),
        unsafe_allow_html=True,
    )

    tab1, tab2, tab3 = st.tabs(["Task Studio", "Team Board", "Memory"])

    with tab1:
        left_col, right_col = st.columns([1.05, 0.95], gap="large")

        with left_col:
            TaskInputComponent.render(controller, key="task_studio_input")

        with right_col:
            AgentStatusComponent.render(controller)

        st.divider()
        TaskBoardComponent.render(controller)
        st.divider()
        OutputViewerComponent.render(controller)

    with tab2:
        AgentStatusComponent.render(controller)
        st.divider()
        TaskBoardComponent.render(controller)
        st.divider()
        OutputViewerComponent.render(controller)

    with tab3:
        render_memory_panel(controller)


if __name__ == "__main__":
    main()
