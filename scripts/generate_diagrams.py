"""
Generate Publication-Grade Diagrams for System Architecture, Workflows & Governance
Multi-Agent Enterprise AI Service Desk
"""

import os
os.environ["MPLCONFIGDIR"] = os.path.join(os.path.expanduser("~"), "AppData", "Local", "Temp", "mpl_cache")
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
ASSETS_DIR = BASE_DIR / "assets"
ASSETS_DIR.mkdir(parents=True, exist_ok=True)

# Set high-DPI style
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['axes.edgecolor'] = '#1E3A8A'
plt.rcParams['axes.linewidth'] = 1.2


def generate_architecture_diagram():
    fig, ax = plt.subplots(figsize=(14, 8), dpi=300)
    ax.set_facecolor('#F8FAFC')
    fig.patch.set_facecolor('#F8FAFC')
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 8)
    ax.axis('off')

    # Title
    ax.text(7, 7.6, "Enterprise Multi-Agent AI Service Desk Architecture",
            ha='center', va='center', fontsize=18, fontweight='bold', color='#0F172A')
    ax.text(7, 7.2, "Units III, IV & V: Memory, Tools, Multi-Agent Collaboration & Safety Governance",
            ha='center', va='center', fontsize=11, color='#475569')

    # Employee Box
    emp_box = patches.FancyBboxPatch((0.4, 3.2), 2.2, 1.6, boxstyle="round,pad=0.2",
                                    fc='#1E293B', ec='#0F172A', lw=2)
    ax.add_patch(emp_box)
    ax.text(1.5, 4.2, "[USER] Employee", ha='center', va='center', fontsize=12, fontweight='bold', color='#FFFFFF')
    ax.text(1.5, 3.7, "IT Support Request\n& System Feedback", ha='center', va='center', fontsize=9, color='#E2E8F0')

    # User Interaction Agent Box
    ui_box = patches.FancyBboxPatch((3.2, 3.2), 2.4, 1.6, boxstyle="round,pad=0.2",
                                   fc='#0284C7', ec='#0369A1', lw=2)
    ax.add_patch(ui_box)
    ax.text(4.4, 4.2, "User Interaction\nAgent", ha='center', va='center', fontsize=11, fontweight='bold', color='#FFFFFF')
    ax.text(4.4, 3.6, "Intent Parsing &\nResponse Synthesis", ha='center', va='center', fontsize=8.5, color='#F0F9FF')

    # Supervisor Agent Box (Central Orchestrator)
    sup_box = patches.FancyBboxPatch((6.2, 2.6), 2.6, 2.8, boxstyle="round,pad=0.25",
                                    fc='#1E3A8A', ec='#172554', lw=2.5)
    ax.add_patch(sup_box)
    ax.text(7.5, 4.8, "[SUPERVISOR]\nORCHESTRATOR", ha='center', va='center', fontsize=12, fontweight='bold', color='#FFFFFF')
    ax.text(7.5, 3.8, "• Orchestration\n• Task Delegation\n• Conflict Resolution\n• Policy Precedence\n• Execution Tracing",
            ha='center', va='center', fontsize=8.5, color='#DBEAFE')

    # Specialized Agents Group (Right Column)
    sec_box = patches.FancyBboxPatch((9.5, 5.7), 2.4, 1.2, boxstyle="round,pad=0.15",
                                    fc='#DC2626', ec='#991B1B', lw=1.8)
    ax.add_patch(sec_box)
    ax.text(10.7, 6.4, "[SECURITY] Compliance", ha='center', va='center', fontsize=10, fontweight='bold', color='#FFFFFF')
    ax.text(10.7, 6.0, "Injection Defense & RBAC", ha='center', va='center', fontsize=8, color='#FEE2E2')

    mem_box = patches.FancyBboxPatch((9.5, 4.2), 2.4, 1.2, boxstyle="round,pad=0.15",
                                    fc='#0D9488', ec='#115E59', lw=1.8)
    ax.add_patch(mem_box)
    ax.text(10.7, 4.9, "[MEMORY] Knowledge", ha='center', va='center', fontsize=10, fontweight='bold', color='#FFFFFF')
    ax.text(10.7, 4.5, "Short/Long Memory & KB", ha='center', va='center', fontsize=8, color='#CCFBF1')

    tech_box = patches.FancyBboxPatch((9.5, 2.7), 2.4, 1.2, boxstyle="round,pad=0.15",
                                     fc='#4F46E5', ec='#3730A3', lw=1.8)
    ax.add_patch(tech_box)
    ax.text(10.7, 3.4, "[TECH] Resolution", ha='center', va='center', fontsize=10, fontweight='bold', color='#FFFFFF')
    ax.text(10.7, 3.0, "Root Cause & Guidance", ha='center', va='center', fontsize=8, color='#E0E7FF')

    tool_box = patches.FancyBboxPatch((9.5, 1.2), 2.4, 1.2, boxstyle="round,pad=0.15",
                                     fc='#D97706', ec='#B45309', lw=1.8)
    ax.add_patch(tool_box)
    ax.text(10.7, 1.9, "[TOOLS] Execution", ha='center', va='center', fontsize=10, fontweight='bold', color='#FFFFFF')
    ax.text(10.7, 1.5, "Simulated Tool Dispatch", ha='center', va='center', fontsize=8, color='#FEF3C7')

    # Environment Layer (Far Right)
    env_box = patches.FancyBboxPatch((12.4, 1.0), 1.4, 6.0, boxstyle="round,pad=0.15",
                                    fc='#F1F5F9', ec='#94A3B8', lw=1.5, linestyle='--')
    ax.add_patch(env_box)
    ax.text(13.1, 6.4, "ENVIRONMENT\n& DATA", ha='center', va='center', fontsize=9, fontweight='bold', color='#334155')
    ax.text(13.1, 5.0, "[DB] SQLite DB\n(Persistent)\n\n[KB] Confluence\nKB Articles\n\n[TICKET] ServiceNow\nTickets API\n\n[MONITOR] Datadog\nTelemetry",
            ha='center', va='center', fontsize=8, color='#475569')

    # Arrows
    arrow_props = dict(arrowstyle="->", lw=1.8, color="#334155")
    double_arrow = dict(arrowstyle="<->", lw=1.8, color="#1E3A8A")

    ax.annotate("", xy=(3.2, 4.0), xytext=(2.6, 4.0), arrowprops=arrow_props)
    ax.annotate("", xy=(6.2, 4.0), xytext=(5.6, 4.0), arrowprops=double_arrow)

    # Connections from Supervisor to specialized agents
    ax.annotate("", xy=(9.5, 6.3), xytext=(8.8, 4.8), arrowprops=double_arrow)
    ax.annotate("", xy=(9.5, 4.8), xytext=(8.8, 4.3), arrowprops=double_arrow)
    ax.annotate("", xy=(9.5, 3.3), xytext=(8.8, 3.7), arrowprops=double_arrow)
    ax.annotate("", xy=(9.5, 1.8), xytext=(8.8, 3.0), arrowprops=double_arrow)

    # Connections to Environment
    ax.annotate("", xy=(12.4, 4.8), xytext=(11.9, 4.8), arrowprops=double_arrow)
    ax.annotate("", xy=(12.4, 1.8), xytext=(11.9, 1.8), arrowprops=double_arrow)

    # Governance Badge at bottom
    gov_badge = patches.FancyBboxPatch((2.0, 0.4), 10.0, 0.5, boxstyle="round,pad=0.1",
                                      fc='#EFF6FF', ec='#3B82F6', lw=1)
    ax.add_patch(gov_badge)
    ax.text(7.0, 0.65, "[GOVERNANCE] Continuous Policy: Human-in-the-Loop • RBAC Least Privilege • Prompt Injection Defense • Immutable Audit Logs",
            ha='center', va='center', fontsize=8.5, fontweight='bold', color='#1E40AF')

    plt.tight_layout()
    output_path = ASSETS_DIR / "architecture_diagram.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Generated: {output_path}")


def generate_workflow_diagram():
    fig, ax = plt.subplots(figsize=(13, 7), dpi=300)
    ax.set_facecolor('#FFFFFF')
    fig.patch.set_facecolor('#FFFFFF')
    ax.set_xlim(0, 13)
    ax.set_ylim(0, 7)
    ax.axis('off')

    ax.text(6.5, 6.6, "Multi-Agent Coordination & Execution Flow",
            ha='center', va='center', fontsize=17, fontweight='bold', color='#0F172A')

    steps_data = [
        ("Step 1: Input Elicitation", "User Interaction Agent parses intent,\nverifies mandatory parameters", "#0284C7", 1.2, 4.8),
        ("Step 2: Security Gate", "Security Agent runs injection scan,\nchecks RBAC & privacy constraints", "#DC2626", 4.2, 4.8),
        ("Step 3: Memory Recall", "Memory Agent fetches persistent\nhardware specs & queries KB", "#0D9488", 7.2, 4.8),
        ("Step 4: Tech Synthesis", "Technical Agent formulates verified\nsteps or triggers uncertainty", "#4F46E5", 10.2, 4.8),
        ("Step 5: Tool Execution", "Tool Agent validates parameters &\nexecutes simulated IT tools", "#D97706", 10.2, 2.0),
        ("Step 6: Supervisor Gate", "Supervisor Agent arbitrates conflicts\n& enforces policy precedence", "#1E3A8A", 7.2, 2.0),
        ("Step 7: Audit & Response", "Audit Logger commits trace to SQLite;\nUser Agent delivers clear response", "#059669", 3.2, 2.0),
    ]

    for title, desc, color, x, y in steps_data:
        box = patches.FancyBboxPatch((x - 1.2, y - 0.7), 2.4, 1.4, boxstyle="round,pad=0.15",
                                    fc=color, ec='#0F172A', lw=1.5)
        ax.add_patch(box)
        ax.text(x, y + 0.35, title, ha='center', va='center', fontsize=9.5, fontweight='bold', color='#FFFFFF')
        ax.text(x, y - 0.15, desc, ha='center', va='center', fontsize=7.5, color='#F8FAFC')

    # Flow arrows
    arrow = dict(arrowstyle="->", lw=2.0, color="#1E293B")
    ax.annotate("", xy=(3.0, 4.8), xytext=(2.4, 4.8), arrowprops=arrow)
    ax.annotate("", xy=(6.0, 4.8), xytext=(5.4, 4.8), arrowprops=arrow)
    ax.annotate("", xy=(9.0, 4.8), xytext=(8.4, 4.8), arrowprops=arrow)
    # Down arrow from Step 4 to Step 5
    ax.annotate("", xy=(10.2, 2.7), xytext=(10.2, 4.1), arrowprops=arrow)
    # Left arrows in bottom row
    ax.annotate("", xy=(8.4, 2.0), xytext=(9.0, 2.0), arrowprops=arrow)
    ax.annotate("", xy=(4.4, 2.0), xytext=(6.0, 2.0), arrowprops=arrow)

    # Return arrow to Employee
    ax.annotate("Verified Response to Employee", xy=(1.2, 3.8), xytext=(2.0, 2.0),
                arrowprops=dict(arrowstyle="->", lw=2.0, color="#059669", connectionstyle="angle,angleA=0,angleB=90,rad=10"),
                fontsize=8.5, fontweight='bold', color="#059669")

    plt.tight_layout()
    output_path = ASSETS_DIR / "multi_agent_workflow.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Generated: {output_path}")


def generate_memory_hierarchy_diagram():
    fig, ax = plt.subplots(figsize=(11, 6), dpi=300)
    ax.set_facecolor('#F8FAFC')
    fig.patch.set_facecolor('#F8FAFC')
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 6)
    ax.axis('off')

    ax.text(5.5, 5.5, "Memory & Retrieval Architecture (Unit III)",
            ha='center', va='center', fontsize=16, fontweight='bold', color='#0F172A')

    # Short-Term Memory
    b1 = patches.FancyBboxPatch((0.8, 1.8), 2.8, 3.0, boxstyle="round,pad=0.2",
                               fc='#E0F2FE', ec='#0284C7', lw=2)
    ax.add_patch(b1)
    ax.text(2.2, 4.4, "[SHORT-TERM MEMORY]", ha='center', va='center', fontsize=11, fontweight='bold', color='#0369A1')
    ax.text(2.2, 3.2, "• In-Memory Ring Buffer\n• Active Dialog Turns\n• Parameter Accumulation\n• Immediate Context Window\n• Ephemeral (Session Lifetime)",
            ha='center', va='center', fontsize=8.5, color='#0F172A')

    # Long-Term Persistent Memory
    b2 = patches.FancyBboxPatch((4.1, 1.8), 2.8, 3.0, boxstyle="round,pad=0.2",
                               fc='#F0FDF4', ec='#16A34A', lw=2)
    ax.add_patch(b2)
    ax.text(5.5, 4.4, "[LONG-TERM PERSISTENT]", ha='center', va='center', fontsize=11, fontweight='bold', color='#15803D')
    ax.text(5.5, 3.2, "• Persistent SQLite Storage\n• Assigned Hardware Specs\n• Preferred VPN Gateway\n• Past Resolution Codes\n• Survives System Restart\n• Right to be Forgotten",
            ha='center', va='center', fontsize=8.5, color='#0F172A')

    # Semantic Knowledge Base
    b3 = patches.FancyBboxPatch((7.4, 1.8), 2.8, 3.0, boxstyle="round,pad=0.2",
                               fc='#FEF3C7', ec='#D97706', lw=2)
    ax.add_patch(b3)
    ax.text(8.8, 4.4, "[SEMANTIC KNOWLEDGE BASE]", ha='center', va='center', fontsize=10.5, fontweight='bold', color='#B45309')
    ax.text(8.8, 3.2, "• Curated Enterprise Docs\n• Cosine / Keyword Scoring\n• Verified Solutions Only\n• Relevance Threshold (0.15)\n• Anti-Hallucination Gating\n• Multi-Category Taxonomy",
            ha='center', va='center', fontsize=8.5, color='#0F172A')

    # Privacy Banner
    p_box = patches.FancyBboxPatch((0.8, 0.4), 9.4, 0.9, boxstyle="round,pad=0.1",
                                  fc='#F1F5F9', ec='#64748B', lw=1.5)
    ax.add_patch(p_box)
    ax.text(5.5, 0.85, "[DATA SANITIZATION LAYER] Automatic Credential Scrubbing (Regex) • User Consent Tracking • Zero Plaintext PII",
            ha='center', va='center', fontsize=8.5, fontweight='bold', color='#334155')

    plt.tight_layout()
    output_path = ASSETS_DIR / "memory_hierarchy.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Generated: {output_path}")


def generate_governance_diagram():
    fig, ax = plt.subplots(figsize=(12, 6.5), dpi=300)
    ax.set_facecolor('#FFFFFF')
    fig.patch.set_facecolor('#FFFFFF')
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 6.5)
    ax.axis('off')

    ax.text(6, 6.0, "Defense-in-Depth AI Governance & Safety Framework (Unit V)",
            ha='center', va='center', fontsize=16, fontweight='bold', color='#0F172A')

    pillars = [
        ("1. Input Guardrails", ["Adversarial Injection Filtering", "Regex / Semantic Signatures", "Data Sanitization & Redaction"], "#DC2626", 1.8),
        ("2. Architectural RBAC", ["Least-Privilege Tool Matrix", "Role-Based Tool Gating", "Tenant Context Isolation"], "#2563EB", 4.6),
        ("3. Runtime Arbitration", ["Anti-Hallucination Thresholds", "Supervisor Conflict Precedence", "Uncertainty Escalation"], "#7C3AED", 7.4),
        ("4. Accountability & Logs", ["Human-in-the-Loop Gating", "Immutable SQLite Audit Trails", "Execution Traceability"], "#059669", 10.2),
    ]

    for title, items, color, x in pillars:
        box = patches.FancyBboxPatch((x - 1.2, 1.4), 2.4, 3.8, boxstyle="round,pad=0.15",
                                    fc='#F8FAFC', ec=color, lw=2.2)
        ax.add_patch(box)
        header_box = patches.FancyBboxPatch((x - 1.2, 4.4), 2.4, 0.8, boxstyle="round,pad=0.1",
                                           fc=color, ec=color, lw=1)
        ax.add_patch(header_box)
        ax.text(x, 4.8, title, ha='center', va='center', fontsize=9.5, fontweight='bold', color='#FFFFFF')

        y_pos = 3.8
        for item in items:
            ax.text(x, y_pos, f"• {item}", ha='center', va='center', fontsize=8.5, color='#1E293B')
            y_pos -= 0.8

    # Bottom Standard
    b_box = patches.FancyBboxPatch((0.6, 0.3), 10.8, 0.65, boxstyle="round,pad=0.1",
                                  fc='#EFF6FF', ec='#3B82F6', lw=1.2)
    ax.add_patch(b_box)
    ax.text(6.0, 0.62, "Aligned with NIST AI Risk Management Framework, EU AI Act Article 14, and Enterprise Zero-Trust Architecture",
            ha='center', va='center', fontsize=8.5, fontweight='bold', color='#1E40AF')

    plt.tight_layout()
    output_path = ASSETS_DIR / "governance_framework.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Generated: {output_path}")


if __name__ == "__main__":
    generate_architecture_diagram()
    generate_workflow_diagram()
    generate_memory_hierarchy_diagram()
    generate_governance_diagram()
    print("All architecture and governance diagrams generated successfully!")
