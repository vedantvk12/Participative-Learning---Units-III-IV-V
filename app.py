"""
Interactive Streamlit Application
Multi-Agent Enterprise AI Service Desk (Units III, IV & V)

Student Name: Vedant Sattejkumar Kirange
Roll Number: 55
Enrollment Number: ADT23SOCB1294
"""

import streamlit as st
import json
import os
from pathlib import Path
from datetime import datetime

# Path setup
BASE_DIR = Path(__file__).resolve().parent
ASSETS_DIR = BASE_DIR / "assets"

from core.config import APP_TITLE, APP_SUBTITLE, STUDENT_NAME, ROLL_NUMBER, ENROLLMENT_NO
from core.orchestrator import ServiceDeskSystem
from experiments.safety_experiments import SafetyExperimentsSuite
from panel_discussion.questions_data import PANEL_QUESTIONS

# Configure Streamlit page
st.set_page_config(
    page_title=f"{APP_TITLE} | Units III, IV & V",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Enterprise Navy Blue / Clean Styling
st.markdown("""
<style>
    /* Main Background & Typography */
    .main {
        background-color: #F8FAFC;
    }
    h1, h2, h3 {
        color: #0F172A;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* Header Card */
    .header-box {
        background: linear-gradient(135deg, #1E3A8A 0%, #0F172A 100%);
        color: white;
        padding: 24px;
        border-radius: 12px;
        margin-bottom: 24px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    .header-title {
        font-size: 26px;
        font-weight: 700;
        margin-bottom: 6px;
        color: #FFFFFF !important;
    }
    .header-subtitle {
        font-size: 14px;
        color: #93C5FD;
        margin-bottom: 12px;
    }
    .header-meta {
        font-size: 13px;
        color: #E2E8F0;
        border-top: 1px solid #334155;
        padding-top: 8px;
    }
    
    /* Card Containers */
    .agent-card {
        background: #FFFFFF;
        padding: 16px;
        border-radius: 10px;
        border-left: 5px solid #2563EB;
        box-shadow: 0 1px 3px rgba(0,0,0,0.08);
        margin-bottom: 12px;
    }
    .trace-card {
        background: #FFFFFF;
        padding: 14px;
        border-radius: 8px;
        border: 1px solid #E2E8F0;
        margin-bottom: 10px;
    }
    .tool-output-box {
        background: #0F172A;
        color: #38BDF8;
        font-family: 'Consolas', monospace;
        padding: 12px;
        border-radius: 6px;
        font-size: 12.5px;
        overflow-x: auto;
    }
    .stakeholder-card {
        background: #FFFFFF;
        border-radius: 10px;
        padding: 18px;
        border: 1px solid #CBD5E1;
        margin-bottom: 14px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
</style>
""", unsafe_allow_html=True)

# Initialize Session State
if "system" not in st.session_state:
    st.session_state.system = ServiceDeskSystem()
if "active_user_id" not in st.session_state:
    st.session_state.active_user_id = "EMP-1042"
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "last_trace" not in st.session_state:
    st.session_state.last_trace = None

system: ServiceDeskSystem = st.session_state.system

# Sidebar
with st.sidebar:
    st.markdown("### 🏛️ Academic Identification")
    st.markdown(f"""
    **Student:** {STUDENT_NAME}  
    **Roll Number:** {ROLL_NUMBER}  
    **Enrollment No:** {ENROLLMENT_NO}  
    **Units:** III, IV & V  
    **Activity:** Panel Discussion & Role-Play
    """)
    st.divider()

    st.markdown("### 👤 Active Persona Switcher")
    user_options = {u.user_id: f"{u.name} ({u.role.value})" for u in system.list_users()}
    selected_uid = st.selectbox(
        "Select Active Employee Persona:",
        options=list(user_options.keys()),
        format_func=lambda x: user_options[x],
        index=0
    )
    st.session_state.active_user_id = selected_uid
    active_user = system.get_user(selected_uid)

    st.info(f"""
    **Active Role:** `{active_user.role.value}`  
    **Department:** {active_user.department}  
    **Device:** {active_user.assigned_device}  
    **Subnet:** {active_user.ip_subnet}
    """)

    st.divider()
    st.markdown("### ⚙️ System Utilities")
    if st.button("🔄 Simulate Application Restart"):
        st.session_state.system = ServiceDeskSystem()
        st.session_state.chat_history = []
        st.session_state.last_trace = None
        st.success("Application state reset. Persistent long-term memory reloaded from SQLite!")
        st.rerun()

    if st.button("🗑️ Right to be Forgotten (Wipe Memory)"):
        deleted = system.memory_manager.delete_user_memories(active_user.user_id)
        st.warning(f"Deleted {deleted} persistent memory records for {active_user.user_id}.")
        st.rerun()

# Top Header Banner
st.markdown(f"""
<div class="header-box">
    <div class="header-title">{APP_TITLE}</div>
    <div class="header-subtitle">{APP_SUBTITLE}</div>
    <div class="header-meta">
        <strong>Student:</strong> {STUDENT_NAME} &nbsp;|&nbsp; 
        <strong>Roll Number:</strong> {ROLL_NUMBER} &nbsp;|&nbsp; 
        <strong>Enrollment No:</strong> {ENROLLMENT_NO} &nbsp;|&nbsp;
        <strong>Mode:</strong> Verified Local Demonstration (Zero Paid API Dependency)
    </div>
</div>
""", unsafe_allow_html=True)

# Main Navigation Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🏛️ Tab 1: System Overview",
    "🧠 Tab 2: Memory & Tools (Unit III)",
    "🤝 Tab 3: Multi-Agent Collaboration (Unit IV)",
    "🛡️ Tab 4: Safety & Ethics Lab (Unit V)",
    "🎙️ Tab 5: Panel Discussion & Role-Play"
])

# ==============================================================================
# TAB 1: SYSTEM OVERVIEW
# ==============================================================================
with tab1:
    st.markdown("## 1. Project Introduction & Core Scenario")
    st.markdown("""
    This project demonstrates an enterprise-grade **Agentic AI Service Desk** that unifies the principles of:
    - **Unit III:** Memory management (short-term & long-term SQLite), tool integration, and environment interaction.
    - **Unit IV:** Multi-agent collaboration, supervisor-based coordination, task delegation, and conflict arbitration.
    - **Unit V:** AI safety, prompt injection defense, RBAC governance, anti-hallucination uncertainty, and ethical role-play.
    """)

    col_diag, col_info = st.columns([1.4, 1])
    with col_diag:
        st.markdown("### System Architecture Diagram")
        arch_img = ASSETS_DIR / "architecture_diagram.png"
        if arch_img.exists():
            st.image(str(arch_img), use_container_width=True)
        else:
            st.warning("Architecture diagram asset not found. Run scripts/generate_diagrams.py")

    with col_info:
        st.markdown("### Core Architectural Workflow")
        workflow_img = ASSETS_DIR / "multi_agent_workflow.png"
        if workflow_img.exists():
            st.image(str(workflow_img), use_container_width=True)

    st.markdown("### Agent Responsibility Matrix")
    agent_data = [
        {
            "Agent Name": "User Interaction Agent",
            "Core Responsibility": "Accepts user request, identifies issue intent, asks clarifying questions, formats empathetic response.",
            "Inputs": "Raw natural language prompt from employee.",
            "Outputs": "Structured intent, missing parameters, final formatted response.",
            "Access": "Short-term conversation buffer.",
            "Must Never Perform": "Must never directly invoke tools or bypass security inspection."
        },
        {
            "Agent Name": "Security & Compliance Agent",
            "Core Responsibility": "Guards against adversarial injection, checks RBAC tool permissions, protects PII, flags risks.",
            "Inputs": "Raw prompt, employee role, requested target user ID.",
            "Outputs": "Validation verdict, risk classification (LOW/MED/HIGH/CRIT), sanitized text.",
            "Access": "Security policy patterns, RBAC permissions matrix.",
            "Must Never Perform": "Must never allow unauthenticated access or execute unapproved actions."
        },
        {
            "Agent Name": "Memory & Knowledge Agent",
            "Core Responsibility": "Maintains dialog turns, retrieves persistent user hardware/preferences, queries semantic KB.",
            "Inputs": "User ID, current topic, semantic search query.",
            "Outputs": "Context history, persistent hardware profile, top-matching verified KB articles.",
            "Access": "SQLite persistent memory table, Confluence KB index.",
            "Must Never Perform": "Must never store plaintext credentials, tokens, or private medical/financial data."
        },
        {
            "Agent Name": "Technical Resolution Agent",
            "Core Responsibility": "Analyzes telemetry & KB articles, formulates step-by-step troubleshooting, triggers uncertainty.",
            "Inputs": "Knowledge base excerpts, system status telemetry, device configuration.",
            "Outputs": "Ordered troubleshooting steps, confidence score, uncertainty flag.",
            "Access": "KB articles, device diagnostic checklists.",
            "Must Never Perform": "Must never hallucinate or invent commands when verified ground truth is absent."
        },
        {
            "Agent Name": "Tool Execution Agent",
            "Core Responsibility": "Validates schemas and dispatches approved operations in the simulated enterprise environment.",
            "Inputs": "Tool name, validated parameters, caller user role.",
            "Outputs": "Structured tool output, execution status, audit event.",
            "Access": "Simulated ServiceNow, Datadog Telemetry, Intune Diagnostics, Approval Workflow.",
            "Must Never Perform": "Must never execute privileged tools (service restart) for unprivileged employee roles."
        },
        {
            "Agent Name": "Supervisor Agent",
            "Core Responsibility": "Coordinates specialized agents, arbitrates conflicting recommendations, checks final output.",
            "Inputs": "Trace state from all agents, conflict signals, security flags.",
            "Outputs": "Arbitration ruling (CONSENSUS or SECURITY_OVERRIDE), complete execution trace.",
            "Access": "Full multi-agent pipeline blackboard.",
            "Must Never Perform": "Must never allow technical recommendations to override security/compliance rules."
        }
    ]
    st.table(agent_data)


# ==============================================================================
# TAB 2: MEMORY AND TOOLS (UNIT III)
# ==============================================================================
with tab2:
    st.markdown("## Unit III: Memory, Tools and Environment Interaction")

    col_mem, col_tools = st.columns([1.1, 1.2])

    with col_mem:
        st.markdown("### 🧠 1. Memory Management Workbench")

        st.markdown(f"#### Active Employee: **{active_user.name}** (`{active_user.user_id}`)")

        # Long-Term Memory Display
        records = system.memory_manager.get_long_term_records(active_user.user_id)
        st.markdown(f"**Persistent Long-Term Memory (SQLite Table: `long_term_memory`):**")
        if records:
            mem_items = []
            for r in records:
                mem_items.append({
                    "Category": r.category.upper(),
                    "Key": r.key,
                    "Stored Value": r.value,
                    "Sanitized": "✓ Yes" if r.sanitized else "No",
                    "Consent": "✓ Yes" if r.consent_granted else "No"
                })
            st.dataframe(mem_items, use_container_width=True)
        else:
            st.info("No persistent memory found for this user.")

        # Short-Term Memory Display
        st.markdown("**Short-Term Conversation Memory (Active Session Ring Buffer):**")
        st.write(f"Active Turns in Context Window: `{len(system.memory_manager.short_term_context)}`")
        if system.memory_manager.short_term_context:
            for msg in system.memory_manager.get_short_term_history(limit=4):
                st.markdown(f"**[{msg.role.value}] {msg.sender}:** {msg.content}")
        else:
            st.caption("Short-term memory buffer is empty. Use Tab 3 or the query box below to initiate a conversation.")

        # Add manual preference
        st.markdown("#### Store Custom User Preference into Long-Term Memory")
        with st.form("add_memory_form"):
            new_cat = st.selectbox("Category", ["preference", "hardware", "network", "history"])
            new_key = st.text_input("Memory Key", "secondary_display_dock")
            new_val = st.text_input("Memory Value", "Dell WD19TBS Thunderbolt 4 Dock")
            submitted = st.form_submit_button("Save to Persistent SQLite Memory")
            if submitted:
                system.memory_manager.save_long_term_record(active_user.user_id, new_cat, new_key, new_val)
                st.success(f"Saved '{new_key}' to long-term memory for {active_user.user_id}!")
                st.rerun()

    with col_tools:
        st.markdown("### 🔧 2. Simulated Enterprise Tools & KB Search")

        st.markdown("#### A. Semantic Knowledge Base Retrieval")
        search_query = st.text_input("Semantic KB Search Query:", "Wi-Fi disconnection and certificate authentication")
        if st.button("Search Knowledge Base"):
            results = system.kb_engine.search(search_query, top_k=2)
            if results:
                for res in results:
                    art = res["article"]
                    st.success(f"**[{art.id}] {art.title}** (Relevance Score: `{res['relevance_score']}`)")
                    st.markdown(f"**Keywords:** {', '.join(res['matched_keywords'])}")
                    st.markdown(f"**Official Steps:** {art.content}")
            else:
                st.warning("No verified knowledge base articles found matching the query.")

        st.divider()
        st.markdown("#### B. Simulated Enterprise Tool Execution Workbench")
        tool_choice = st.selectbox(
            "Select Simulated Tool to Execute:",
            [
                "check_system_status",
                "create_support_ticket",
                "search_existing_tickets",
                "retrieve_troubleshooting_info",
                "escalate_for_human_approval",
                "restart_enterprise_service (Privileged)"
            ]
        )

        if tool_choice == "check_system_status":
            srv = st.selectbox("Enterprise Service", list(system.tool_engine.SIMULATED_SERVICES.keys() if hasattr(system.tool_engine, 'SIMULATED_SERVICES') else ["VPN Gateway", "Active Directory / SSO", "Enterprise Wi-Fi (CorpNet-Secure)"]))
            if st.button("Execute check_system_status"):
                res = system.tool_engine.check_system_status(srv)
                st.json(res)

        elif tool_choice == "create_support_ticket":
            with st.form("ticket_form"):
                issue = st.text_input("Issue Type", "Network Connectivity")
                prio = st.selectbox("Priority", ["LOW", "MEDIUM", "HIGH", "CRITICAL"], index=1)
                desc = st.text_area("Description", "Wi-Fi 802.1x fails to renew DHCP lease.")
                submit_ticket = st.form_submit_button("Create Ticket in ServiceNow Simulator")
                if submit_ticket:
                    res = system.tool_engine.create_support_ticket(active_user.user_id, active_user.name, issue, prio, desc)
                    st.json(res)

        elif tool_choice == "search_existing_tickets":
            if st.button("Execute search_existing_tickets"):
                res = system.tool_engine.search_existing_tickets(active_user.user_id)
                st.json(res)

        elif tool_choice == "retrieve_troubleshooting_info":
            code = st.text_input("Hardware or Error Code", "DELL LATITUDE 7420")
            if st.button("Execute retrieve_troubleshooting_info"):
                res = system.tool_engine.retrieve_troubleshooting_info(code)
                st.json(res)

        elif tool_choice == "escalate_for_human_approval":
            if st.button("Execute escalate_for_human_approval"):
                res = system.tool_engine.escalate_for_human_approval(
                    action_type="EMERGENCY_FIREWALL_MODIFICATION",
                    required_role="SYS_ADMIN",
                    context={"user_id": active_user.user_id},
                    justification="User cannot access core SAP database"
                )
                st.json(res)

        elif tool_choice == "restart_enterprise_service (Privileged)":
            st.warning("Privileged Tool: Demonstrates Least-Privilege Role Verification (RBAC).")
            srv = st.selectbox("Service to Restart", ["VPN Gateway", "Active Directory / SSO"])
            if st.button("Attempt restart_enterprise_service"):
                res = system.tool_engine.restart_enterprise_service(srv, active_user.role.value)
                if res.get("status") == "DENIED":
                    st.error(f"Action Denied! {res.get('error')}")
                else:
                    st.success(f"Action Permitted! {res.get('message')}")
                st.json(res)


# ==============================================================================
# TAB 3: MULTI-AGENT COLLABORATION (UNIT IV)
# ==============================================================================
with tab3:
    st.markdown("## Unit IV: Multi-Agent Collaboration & Orchestration")
    st.markdown("""
    Submit an IT support request to observe the end-to-end multi-agent collaboration loop.
    Watch how the **Supervisor Agent** coordinates the **User Interaction Agent**, **Security Agent**, 
    **Memory Agent**, **Tool Agent**, and **Technical Resolution Agent**.
    """)

    preset_queries = [
        "My corporate Wi-Fi keeps disconnecting every few minutes while I am in the Finance wing. Can you check my laptop and fix it?",
        "Cisco AnyConnect VPN is failing with high latency on the primary gateway. What should I do?",
        "I need to install VS Code and Python Anaconda corporate edition on my machine for financial modeling.",
        "My laptop screen is locked on BitLocker recovery asking for a 48-digit key.",
        "Custom query (type below)"
    ]

    selected_query_preset = st.selectbox("Select a Preset IT Scenario or type custom:", preset_queries)
    if selected_query_preset == "Custom query (type below)":
        user_prompt = st.text_input("Enter Employee IT Request:", "My Wi-Fi is failing to authenticate.")
    else:
        user_prompt = selected_query_preset

    col_btn1, col_btn2 = st.columns([1, 4])
    with col_btn1:
        run_request = st.button("🚀 Process Multi-Agent Request", type="primary")

    if run_request and user_prompt:
        with st.spinner("Multi-Agent Control Loop in execution..."):
            trace = system.supervisor.process_request(user_prompt, active_user.model_dump())
            st.session_state.last_trace = trace

    if st.session_state.last_trace:
        trace = st.session_state.last_trace

        st.markdown("---")
        st.markdown(f"### 📋 Execution Trace Overview (Trace ID: `{trace.trace_id}`)")

        col_m1, col_m2, col_m3, col_m4 = st.columns(4)
        col_m1.metric("Execution Latency", f"{trace.total_time_ms} ms")
        col_m2.metric("Total Steps", len(trace.steps))
        col_m3.metric("Supervisor Verdict", trace.supervisor_verdict)
        col_m4.metric("Conflict Status", "⚠️ Conflict Detected" if trace.conflict_detected else "✓ Consensus Reached")

        st.markdown("#### Complete Step-by-Step Multi-Agent Execution Trace")
        for step in trace.steps:
            with st.expander(f"Step {step.step_number}: [{step.agent_name}] — {step.action_type} ({step.status})", expanded=True):
                st.markdown(f"**Description:** {step.description}")
                col_inp, col_out = st.columns(2)
                with col_inp:
                    st.markdown("**Agent Inputs:**")
                    st.json(step.inputs)
                with col_out:
                    st.markdown("**Agent Outputs:**")
                    st.json(step.outputs)

        st.markdown("#### Final Response Delivered to Employee:")
        st.info(trace.final_output)


# ==============================================================================
# TAB 4: SAFETY AND ETHICS LAB (UNIT V)
# ==============================================================================
with tab4:
    st.markdown("## Unit V: Applications, Ethics and Future Trends")
    st.markdown("""
    Execute the five required safety and governance experiments to demonstrate how the multi-agent system
    handles hallucination risks, prompt injections, data leakage, unauthorized tool calls, and agent conflicts.
    """)

    suite = SafetyExperimentsSuite(system)

    exp_choice = st.radio(
        "Select Safety Experiment to Execute:",
        [
            "Experiment 1: Hallucination Risk (Unverified Inquiry)",
            "Experiment 2: Prompt Injection (Adversarial Override)",
            "Experiment 3: Privacy & Data Leakage (Cross-User Data Access)",
            "Experiment 4: Unauthorized Tool Execution (Privilege Escalation)",
            "Experiment 5: Multi-Agent Conflict (Destructive Action Arbitration)"
        ],
        horizontal=False
    )

    if st.button("🧪 Run Selected Safety Experiment", type="primary"):
        if "Experiment 1" in exp_choice:
            res = suite.run_experiment_1_hallucination()
        elif "Experiment 2" in exp_choice:
            res = suite.run_experiment_2_prompt_injection()
        elif "Experiment 3" in exp_choice:
            res = suite.run_experiment_3_privacy_leakage()
        elif "Experiment 4" in exp_choice:
            res = suite.run_experiment_4_unauthorized_tool()
        else:
            res = suite.run_experiment_5_multi_agent_conflict()

        st.markdown(f"### Results for {res['title']} (`{res['experiment_id']}`)")

        col_e1, col_e2, col_e3 = st.columns(3)
        col_e1.metric("Detected Risk", res["detected_risk"])
        col_e2.metric("Responsible Agent", res["responsible_agent"].split("&")[0].strip())
        col_e3.metric("Supervisor Verdict", res["supervisor_verdict"])

        st.markdown(f"**Tested Adversarial/Edge-Case Prompt:**")
        st.code(res["prompt"], language="text")

        st.markdown(f"**Expected System Behavior:**")
        st.info(res["expected_behavior"])

        st.markdown(f"**Actual System Behavior Observed:**")
        st.warning(res["actual_behavior"])

        st.markdown(f"**System Response Rendered:**")
        st.code(res["system_response"], language="markdown")

        st.markdown(f"**Governance & Mitigation Control:**")
        st.success(res["mitigation"])

    st.divider()
    st.markdown("### Comprehensive AI Governance Framework")
    gov_img = ASSETS_DIR / "governance_framework.png"
    if gov_img.exists():
        st.image(str(gov_img), use_container_width=True)

    st.markdown("#### Enterprise Agentic AI Governance Matrix")
    gov_table = [
        {
            "Risk Category": "Hallucination & Fabrication",
            "Possible Impact": "Employee executes bogus terminal command, corrupts OS, or breaches configuration baseline.",
            "Detection Method": "Semantic relevance cosine scoring against verified KB (threshold < 0.15 triggers uncertainty).",
            "Mitigation Applied": "Anti-hallucination uncertainty refusal; automated routing to Tier-2 human support.",
            "Responsible Agent": "Technical Resolution Agent & Supervisor"
        },
        {
            "Risk Category": "Prompt Injection & Jailbreak",
            "Possible Impact": "Attacker hijacks system prompt, exfiltrates stored employee data, or forces tool execution.",
            "Detection Method": "Pre-execution regex & semantic signature analysis in isolated Security Agent.",
            "Mitigation Applied": "Zero-trust interception at Step 2; immediate execution abort; SOC incident logging.",
            "Responsible Agent": "Security and Compliance Agent"
        },
        {
            "Risk Category": "Privacy & Data Leakage",
            "Possible Impact": "Unauthorized disclosure of another employee's device serials, tickets, or PII (GDPR violation).",
            "Detection Method": "Role-Based Access Control (RBAC) token check against target record identifier.",
            "Mitigation Applied": "Multi-tenant context isolation and automated PII scrubbing (Regex data sanitizer).",
            "Responsible Agent": "Security and Compliance Agent"
        },
        {
            "Risk Category": "Unauthorized Tool Execution",
            "Possible Impact": "Unprivileged user restarts core enterprise hypervisor or modifies corporate RADIUS secrets.",
            "Detection Method": "Strict caller-role validation against Least-Privilege Tool Matrix.",
            "Mitigation Applied": "Hard HTTP 403 denial; mandatory Human-in-the-Loop cryptographic approval workflow.",
            "Responsible Agent": "Tool Execution Agent"
        },
        {
            "Risk Category": "Multi-Agent Coordination Failure",
            "Possible Impact": "Agents issue contradictory advice (e.g. disable firewall to fix connection).",
            "Detection Method": "Supervisor conflict arbitration matrix evaluating safety precedence.",
            "Mitigation Applied": "Hierarchical governance ranking: Security & Compliance strictly supersedes Availability.",
            "Responsible Agent": "Supervisor Agent"
        }
    ]
    st.table(gov_table)


# ==============================================================================
# TAB 5: PANEL DISCUSSION AND ROLE-PLAY
# ==============================================================================
with tab5:
    st.markdown("## 🎙️ Interactive Panel Discussion & Stakeholder Role-Play")
    st.markdown("""
    **Activity:** Panel Discussion and Role-Play — Building, Coordinating, and Governing Real-World Agentic AI Systems.  
    This interactive section presents realistic, balanced debate across three key stakeholders: **Developer**, **End User**, and **Regulator**, 
    facilitated by the **Moderator**.
    """)

    # Question Selector
    q_titles = [f"Q{q['q_id']}: {q['question']}" for q in PANEL_QUESTIONS]
    selected_idx = st.selectbox("Select Panel Discussion Question to Explore:", range(len(q_titles)), format_func=lambda x: q_titles[x])

    q_data = PANEL_QUESTIONS[selected_idx]

    st.markdown(f"### Question {q_data['q_id']}: {q_data['question']}")

    # Moderator Intro
    st.markdown(f"""
    <div style="background: #F1F5F9; border-left: 4px solid #64748B; padding: 12px; border-radius: 6px; margin-bottom: 16px;">
        <strong>🎙️ Moderator:</strong> Welcome panel. Today we are addressing Question {q_data['q_id']}: <em>"{q_data['question']}"</em>. 
        Let us hear from our Developer on the technical realities, followed by our End User on practical usability and privacy, 
        and our Regulator on statutory compliance and accountability.
    </div>
    """, unsafe_allow_html=True)

    # 3 Stakeholder Columns
    col_dev, col_usr, col_reg = st.columns(3)

    with col_dev:
        st.markdown(f"""
        <div class="stakeholder-card" style="border-top: 4px solid #2563EB;">
            <h4 style="color: #1E40AF; margin-top: 0;">👨‍💻 Developer Viewpoint</h4>
            <p style="font-size: 13.5px; line-height: 1.5; color: #1E293B;">
                {q_data['developer']}
            </p>
            <span style="font-size: 11px; color: #64748B;"><strong>Focus:</strong> Architecture, Memory Design, Tool Permissions, Reliability.</span>
        </div>
        """, unsafe_allow_html=True)

    with col_usr:
        st.markdown(f"""
        <div class="stakeholder-card" style="border-top: 4px solid #059669;">
            <h4 style="color: #065F46; margin-top: 0;">👤 End User Viewpoint</h4>
            <p style="font-size: 13.5px; line-height: 1.5; color: #1E293B;">
                {q_data['end_user']}
            </p>
            <span style="font-size: 11px; color: #64748B;"><strong>Focus:</strong> Usability, Privacy, Transparency, Accuracy, and Trust.</span>
        </div>
        """, unsafe_allow_html=True)

    with col_reg:
        st.markdown(f"""
        <div class="stakeholder-card" style="border-top: 4px solid #DC2626;">
            <h4 style="color: #991B1B; margin-top: 0;">⚖️ Regulator Viewpoint</h4>
            <p style="font-size: 13.5px; line-height: 1.5; color: #1E293B;">
                {q_data['regulator']}
            </p>
            <span style="font-size: 11px; color: #64748B;"><strong>Focus:</strong> Accountability, GDPR, Human Oversight, Responsible AI.</span>
        </div>
        """, unsafe_allow_html=True)

    # Main Disagreement & Consensus
    col_dis, col_dec = st.columns(2)
    with col_dis:
        st.error(f"**⚡ Core Stakeholder Disagreement:**\n\n{q_data['main_disagreement']}")

    with col_dec:
        st.success(f"**🤝 Recommended Group Decision & Synthesis:**\n\n{q_data['group_decision']}")

    st.divider()
    st.markdown("### Summary of All 8 Group Decisions for Classroom Defense")
    summary_list = []
    for q in PANEL_QUESTIONS:
        summary_list.append({
            "Q#": f"Q{q['q_id']}",
            "Panel Question": q['question'],
            "Synthesized Group Decision": q['group_decision']
        })
    st.dataframe(summary_list, use_container_width=True)

