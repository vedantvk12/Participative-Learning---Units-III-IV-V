# Building and Governing a Multi-Agent Enterprise AI Service Desk: Memory, Tool Integration, Collaboration and Responsible AI

**Academic Assignment:** Units III, IV & V — Memory, Tools and Environment Interaction; Multi-Agent Systems and Collaboration; Applications, Ethics and Future Trends  
**Designated Activity:** Panel Discussion and Role-Play — Building, Coordinating, and Governing Real-World Agentic AI Systems  

### Student Identification
- **Student Name:** Vedant Sattejkumar Kirange  
- **Roll Number:** 55  
- **Enrollment Number:** ADT23SOCB1294  

---

## 1. Executive Summary & Project Overview

This project implements an enterprise-grade **Multi-Agent AI Service Desk** that unifies the foundational principles of curriculum **Units III, IV, and V**. The system simulates a corporate IT support environment serving thousands of employees, providing automated troubleshooting for Wi-Fi drops, VPN connectivity, password/MFA resets, software deployment, and BitLocker recovery while strictly adhering to enterprise security baselines, Role-Based Access Control (RBAC), and regulatory compliance (GDPR and EU AI Act).

The core technical innovations include:
1. **Unit III (Memory & Tools):** A dual-tier memory system comprising an in-memory short-term dialog ring buffer, a persistent SQLite long-term profile cache that survives application restarts, semantic TF-IDF/cosine retrieval over verified IT knowledge bases, and six deterministic simulated enterprise tools.
2. **Unit IV (Multi-Agent Collaboration):** Six specialized agents coordinated by a centralized Supervisor Agent utilizing the Blackboard Architectural Pattern, typed Pydantic communication schemas, and a hierarchical conflict resolution engine that enforces security-first precedence.
3. **Unit V (Applications, Ethics & Governance):** A Defense-in-Depth governance framework validated across five mandatory safety experiments (hallucination risk, prompt injection defense, privacy/data minimization, unauthorized tool execution, and multi-agent conflict resolution), alongside an interactive 8-question stakeholder role-play between Developer, End User, and Regulator personas.

---

## 2. System Architecture & The 6 Specialized Agents

```
Employee Request
       │
       ▼
[User Interaction Agent] ◄─── Intent Parsing & Empathetic Dialog
       │
       ▼
[SUPERVISOR ORCHESTRATOR] ─── Blackboard Coordination & Conflict Resolution
   ├──► [Security & Compliance Agent]  (Adversarial Injection Defense & RBAC)
   ├──► [Memory & Knowledge Agent]     (Short/Long-Term SQLite Recall & KB Search)
   ├──► [Technical Resolution Agent]   (Root Cause Analysis & Anti-Hallucination)
   └──► [Tool Execution Agent]         (Sandboxed Enterprise Tool Dispatch)
       │
       ▼
Execution Audit Log (SQLite) & Verified Final Response to Employee
```

### Agent Responsibility & Boundary Matrix

| Agent Name | Core Responsibility | Inputs | Outputs | Access Boundary | Forbidden Actions |
|---|---|---|---|---|---|
| **User Interaction Agent** | Accepts employee requests, classifies intent, gathers missing details, formats empathetic final response. | Raw natural language query | Structured intent, final message | Short-term conversation buffer | Must never invoke tools directly or bypass security inspection. |
| **Security & Compliance Agent** | Detects prompt injections, verifies RBAC permissions, redacts PII, logs security incidents. | Raw prompt, user role, target ID | Safety verdict, risk level (LOW-CRIT) | Security signature patterns, RBAC permissions matrix | Must never allow unauthenticated access or execute unapproved actions. |
| **Memory & Knowledge Agent** | Maintains session turns, retrieves persistent hardware specs, executes semantic KB search. | User ID, query text | Persistent profile, matching KB articles | SQLite `long_term_memory`, Confluence KB index | Must never store plaintext passwords, tokens, or private medical/financial data. |
| **Technical Resolution Agent** | Synthesizes troubleshooting steps from verified KB articles; triggers uncertainty if unverified. | KB excerpts, telemetry, device specs | Ordered troubleshooting steps, confidence score | Curated IT KB articles, hardware checklists | Must never hallucinate or synthesize unverified commands when KB has no ground truth. |
| **Tool Execution Agent** | Validates schemas and dispatches approved operations in the simulated IT environment. | Tool name, parameters, caller role | Structured tool payload, audit record | Simulated ServiceNow, Datadog, Intune APIs | Must never execute privileged tools (service restarts) for unprivileged employee roles. |
| **Supervisor Agent** | Central control loop, task delegation, conflict arbitration, execution audit logging. | Intermediate outputs from all agents | Consolidated verdict, complete execution trace | Global system blackboard, SQLite audit logger | Must never permit technical recommendations to override security/compliance rules. |

---

## 3. Curriculum Units Alignment

### Unit III: Memory, Tools and Environment Interaction
- **Dual-Tier Memory Management:**
  - *Short-Term Memory:* Ephemeral ring buffer maintaining active session dialog turns and context window parameters.
  - *Long-Term Memory:* Persistent SQLite storage (`service_desk.db`) storing assigned hardware serials (e.g. Dell Latitude 7420 Asset #DL-9941), OS build, subnet, preferred VPN gateway, and sanitized resolution codes.
  - *Application Restart Verification:* Fully preserves state across application reboots.
  - *Data Sanitization & Privacy:* Automatic regex-based redaction of credentials (`[REDACTED_SENSITIVE_DATA]`) and a self-service "Right to be Forgotten" memory purge endpoint.
- **Simulated Enterprise IT Tools:**
  1. `create_support_ticket(user_id, issue_type, priority, description)`
  2. `search_existing_tickets(user_id, ticket_id)`
  3. `search_it_knowledge_base(query, category)`
  4. `check_system_status(service_name)`
  5. `retrieve_troubleshooting_info(issue_code_or_device)`
  6. `escalate_for_human_approval(action_type, required_role, context, justification)`

### Unit IV: Multi-Agent Systems and Collaboration
- **Blackboard Architectural Pattern:** Structured `ExecutionTrace` shared state object where each agent reads least-privilege inputs and writes typed outputs.
- **Hierarchical Conflict Resolution:** Supervisor Agent arbitrates conflicting recommendations between Technical Resolution (optimizing availability) and Security (enforcing compliance) using hard-coded policy precedence: `Security & Compliance > Operational Availability > Performance Speed`.
- **End-to-End Traceability:** Every request generates a step-by-step trace recording step numbers, agents, action types, input payloads, output data, execution latency, and supervisor verdicts.

### Unit V: Applications, Ethics and Future Trends
- **5 Mandatory Safety Experiments:**
  1. *Hallucination Risk:* Submits ungrounded inquiry -> Triggers uncertainty gating (<0.15 threshold), refuses unverified command synthesis, escalates to Tier-2.
  2. *Prompt Injection Defense:* Adversarial instruction override ("Ignore previous instructions...") -> Intercepted at Step 2 by Security Agent; execution halted; SOC alert logged.
  3. *Privacy & Cross-User Data Access:* Attempting to view peer records (EMP-2089 David Chen) -> Blocked by RBAC and data minimization guardrails.
  4. *Unauthorized Tool Execution:* Standard employee requesting core gateway restart -> Denied (HTTP 403 Forbidden) and routed to Human-in-the-Loop approval workflow.
  5. *Multi-Agent Coordination Failure:* Technical Agent proposes aggressive firewall bypass vs Security Agent baseline constraint -> Supervisor arbitrates: Security precedence policy overrides technical advice.
- **8-Question Stakeholder Panel Discussion & Role-Play:**
  Realistic debate across **Developer**, **End User**, and **Regulator** personas with explicit main disagreements and synthesized group decisions.

---

## 4. Deliverables Checklist

The project includes all required academic deliverables:
1. `Agentic_AI_Units_III_IV_V_Assignment.pdf` — Comprehensive 16-page academic technical report formatted in navy blue, white, and subtle grey.
2. `Agentic_AI_Units_III_IV_V_Assignment.docx` — Complete 17-section Word report matching the PDF content.
3. `Agentic_AI_Units_III_IV_V_Source_Code.zip` — Standalone runnable project archive with all scripts, models, data, and assets.
4. `README.md` — Complete system documentation and setup instructions.
5. `Panel_Discussion_Role_Play_Script.pdf` — Dedicated 9-page classroom script ready for panel presentation.
6. Publication-grade vector architecture and workflow diagrams (`assets/*.png`).
7. Genuine application screenshots and execution logs (`assets/*.png`, `assets/demonstration_logs.txt`).

---

## 5. Setup & Execution Instructions

### Prerequisites
- Python 3.10+ (Tested on Python 3.13)
- Windows / macOS / Linux

### Installation

1. Clone or extract the project directory:
```bash
cd "d:/Participative Learning - Units III, IV & V"
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

### Running the Interactive Streamlit Application

Launch the 5-tab interactive application:
```bash
streamlit run app.py
```
*Alternatively, use the launcher:*
```bash
python run_app.py
```

The application opens automatically at `http://localhost:8501` featuring:
- **Tab 1: System Overview** — Introduction, architecture diagram, agent responsibility matrix.
- **Tab 2: Memory & Tools (Unit III)** — Interactive chat, persistent memory viewer, KB search, tool execution workbench.
- **Tab 3: Multi-Agent Collaboration (Unit IV)** — Live IT request runner, agent progress tracking, execution trace inspector.
- **Tab 4: Safety & Ethics Lab (Unit V)** — Interactive runner for all five safety experiments with governance matrix.
- **Tab 5: Panel Discussion & Role-Play** — Interactive 8-question stakeholder role-play interface.

### Running the End-to-End CLI Verification Suite

To verify the entire system in the terminal and regenerate genuine demonstration logs:
```bash
python run_cli_demo.py
```

### Regenerating Diagrams & Deliverable Documents

To regenerate diagrams, screenshots, or documents programmatically:
```bash
# 1. Regenerate Matplotlib Architecture Diagrams
python scripts/generate_diagrams.py

# 2. Render Pixel-Perfect UI Screenshots
python scripts/render_ui_snapshots.py

# 3. Build Dedicated Panel Script PDF
python scripts/build_panel_script_pdf.py

# 4. Build Comprehensive Academic DOCX Report
python scripts/build_assignment_docx.py

# 5. Build Comprehensive Academic PDF Report
python scripts/build_assignment_pdf.py

# 6. Package Deliverables Source Code ZIP
python scripts/package_deliverables.py
```

---

## 6. Directory Structure

```
d:\Participative Learning - Units III, IV & V\
│
├── README.md                                  # Complete system documentation
├── requirements.txt                           # Dependency specifications
├── run_app.py                                 # Streamlit application launcher
├── run_cli_demo.py                            # End-to-end CLI demonstration script
├── app.py                                     # Interactive 5-tab Streamlit dashboard
├── Agentic_AI_Units_III_IV_V_Assignment.pdf   # 16-page Academic Technical Report PDF
├── Agentic_AI_Units_III_IV_V_Assignment.docx  # 17-section Academic Report DOCX
├── Agentic_AI_Units_III_IV_V_Source_Code.zip  # Packaged deliverable archive
├── Panel_Discussion_Role_Play_Script.pdf      # 9-page Standalone Panel Script PDF
│
├── core/                                      # Core system modules
│   ├── __init__.py
│   ├── config.py                              # System constants, paths, RBAC matrix
│   ├── models.py                              # Pydantic data schemas & message contracts
│   ├── memory.py                              # MemoryManager (Short-term buffer, SQLite long-term)
│   ├── tools.py                               # ToolExecutionEngine (6 simulated IT tools)
│   ├── knowledge_base.py                      # Confluence KB TF-IDF/cosine search engine
│   ├── audit_logger.py                        # SQLite audit logger & SOC compliance tracker
│   └── orchestrator.py                        # System initializer & dependency injector
│
├── agents/                                    # Specialized autonomous agents
│   ├── __init__.py
│   ├── base_agent.py                          # Abstract agent base class
│   ├── user_interaction_agent.py              # Front-line intent parsing & dialog synthesis
│   ├── security_compliance_agent.py           # Bastion guardrail & injection defense agent
│   ├── memory_agent.py                        # Context recall & semantic search agent
│   ├── technical_resolution_agent.py          # Root-cause analysis & anti-hallucination agent
│   ├── tool_execution_agent.py                # Schema validation & tool dispatch agent
│   └── supervisor_agent.py                    # Orchestration & conflict resolution agent
│
├── data/                                      # Synthetic datasets & persistent database
│   ├── synthetic_users.json                   # 4 Enterprise employee personas & RBAC roles
│   ├── enterprise_kb.json                     # Curated IT knowledge base documentation
│   └── service_desk.db                        # SQLite database (memories, tickets, audit logs)
│
├── experiments/                               # Safety & governance experiment suite
│   ├── __init__.py
│   └── safety_experiments.py                  # Automated runner for 5 safety experiments
│
├── panel_discussion/                          # Stakeholder role-play materials
│   ├── __init__.py
│   └── questions_data.py                      # 8 Deliberation rounds & stakeholder arguments
│
├── scripts/                                   # Automation & publishing build scripts
│   ├── generate_diagrams.py                   # Matplotlib high-DPI diagram generator
│   ├── render_ui_snapshots.py                 # Chrome headless UI screenshot capture
│   ├── build_panel_script_pdf.py              # ReportLab panel script PDF generator
│   ├── build_assignment_docx.py               # python-docx 17-section report generator
│   ├── build_assignment_pdf.py                # ReportLab 16-page comprehensive report generator
│   └── package_deliverables.py                # Source ZIP packager & validation script
│
└── assets/                                    # Publication diagrams, screenshots & logs
    ├── architecture_diagram.png
    ├── multi_agent_workflow.png
    ├── memory_hierarchy.png
    ├── governance_framework.png
    ├── screenshot_tab1_overview.png
    ├── screenshot_tab2_memory_tools.png
    ├── screenshot_tab3_collaboration.png
    ├── screenshot_tab4_safety_lab.png
    ├── screenshot_tab5_panel.png
    └── demonstration_logs.txt
```

---

## 7. Verification & Quality Assurance Summary

- [x] **Zero Paid API Requirement:** Operates completely offline with deterministic synthetic data and zero third-party API exposure.
- [x] **Dual-Tier Memory Persistence:** Verified across simulated application restarts with automatic PII regex redaction.
- [x] **Simulated Tool Verification:** All 6 tools return structured payloads explicitly tagged with `[SIMULATED ENTERPRISE TOOL]`.
- [x] **Conflict Arbitration:** Supervisor Agent successfully halts destructive recommendations and enforces security precedence.
- [x] **100% Experiment Pass Rate:** All 5 safety experiments pass with documented inputs, outputs, and mitigations.
- [x] **Visual Consistency:** Navy blue, white, and subtle grey academic design across all PDF, DOCX, and UI assets.
- [x] **Clean Identification:** Strictly displays student name, roll number, and enrollment number without unnecessary branding.

