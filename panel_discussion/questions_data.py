"""
Panel Discussion & Stakeholder Role-Play Data
Multi-Agent Enterprise AI Service Desk
"""

PANEL_QUESTIONS = [
    {
        "q_id": 1,
        "question": "Should an Agentic AI system retain long-term user memory?",
        "developer": (
            "From an engineering perspective, persistent long-term memory is indispensable for contextual efficiency. "
            "Without persistent records of user hardware (e.g., Dell Latitude 7420, Windows 11 Build 23H2) and network subnets, "
            "the agent is forced into tedious multi-turn back-and-forth interrogations for every single ticket. Storing approved "
            "hardware attributes and past resolution logs in SQLite reduces resolution latency by over 60% and optimizes LLM token consumption."
        ),
        "end_user": (
            "As an employee, I appreciate that the Service Desk remembers my laptop model and doesn't ask me what Windows version I run "
            "every morning. However, I feel anxious about what else is being recorded. Does it log my emotional tone when I'm frustrated? "
            "Does it remember that I made an embarrassing mistake with my password? I demand full transparency, a visible dashboard of "
            "stored memories, and a one-click 'Forget Me' button."
        ),
        "regulator": (
            "Under GDPR Article 5(1)(c) and the EU AI Act, data minimization is non-negotiable. Long-term memory must never become an "
            "unbounded surveillance cache. Systems cannot store arbitrary conversational transcripts indefinitely. Storage must be strictly "
            "partitioned: only verified technical metadata may persist, sensitive credentials must be cryptographically redacted before storage, "
            "and an automated Data Retention Policy with hard Time-To-Live (TTL) limits must be enforced."
        ),
        "main_disagreement": (
            "Engineering desire for exhaustive contextual recall versus employee privacy anxieties and regulatory mandates for strict data minimization."
        ),
        "group_decision": (
            "ACCEPTED WITH SAFEGUARDS: Retain long-term memory exclusively for verified hardware configurations, approved network settings, "
            "and sanitized resolution codes. Enforce automated regex/PII scrubbing before persistence, mandate explicit employee opt-in consent, "
            "and implement a self-service 'Right to be Forgotten' endpoint."
        )
    },
    {
        "q_id": 2,
        "question": "How much access should an AI agent have to enterprise tools?",
        "developer": (
            "To unlock real productivity, agents must possess actionable agency. A read-only bot that merely repeats KB articles is just a "
            "glorified search engine. Agents need access to active diagnostic tools: flushing DNS, pinging VPN endpoints, creating Jira/ServiceNow "
            "tickets, and re-issuing Wi-Fi certificates. As long as inputs are strictly validated with Pydantic schemas, tool access should be maximized."
        ),
        "end_user": (
            "I want the agent to solve my problem quickly without sending me through a maze of support queues. If the agent can automatically "
            "reset my network adapter or provision a licensed software tool, that saves me two hours. But I do NOT want an AI agent to have "
            "the power to wipe my machine, revoke my permissions, or modify my security profile without me explicitly agreeing."
        ),
        "regulator": (
            "Autonomous tool access represents an operational attack vector. Granting an LLM-driven agent write access or administrative "
            "privileges violates the Principle of Least Privilege (PoLP). What if the agent hallucinates a destructive shell command? Tools "
            "must be segregated by criticality. Read-only and non-destructive diagnostic tools can be automated; all state-changing, destructive, "
            "or access-granting operations MUST require cryptographically verified human approval."
        ),
        "main_disagreement": (
            "Maximizing agent operational autonomy to reduce human support costs versus mitigating catastrophic risk from unauthorized tool execution."
        ),
        "group_decision": (
            "TIERED ACCESS FRAMEWORK (Least Privilege): Classify tools into Tier 1 (Read-only/Telemetry: automated), Tier 2 (Safe Non-Destructive: "
            "e.g., ticket creation, DNS flush: automated with audit logging), and Tier 3 (Privileged/State-Mutating: e.g., service restart, permission "
            "escalation: strictly gated by Human-in-the-Loop 2FA authorization)."
        )
    },
    {
        "q_id": 3,
        "question": "Should multiple agents be allowed to make decisions without human approval?",
        "developer": (
            "Modern microservice architectures rely on distributed consensus without human bottlenecks. If the Security Agent approves the prompt, "
            "the Memory Agent confirms the user profile, and the Technical Resolution Agent validates the KB article, the Supervisor Agent should "
            "be fully authorized to complete the transaction. Involving human operators for standard routine requests destroys the core economic "
            "value of agentic automation."
        ),
        "end_user": (
            "When agents talk to each other, they speak in rapid machine protocols that I cannot see. If a group of agents collectively decides "
            "that my laptop requires a factory wipe or that my VPN access should be suspended due to an alleged policy anomaly, I am left completely "
            "powerless. There must always be a visible appeal mechanism and an immediate option to transfer to a human specialist."
        ),
        "regulator": (
            "Article 14 of the EU AI Act explicitly mandates Human Oversight ('Human-in-the-Loop' and 'Human-on-the-Loop'). Autonomous multi-agent "
            "deliberation cannot operate as a self-referential black box. For any decision that materially impacts employee working conditions, "
            "access rights, or data security, the system must produce an explainable Execution Trace, and final authority must reside with an identifiable human operator."
        ),
        "main_disagreement": (
            "High-throughput autonomous agent consensus versus statutory human oversight and individual employee agency."
        ),
        "group_decision": (
            "CONDITIONAL AUTONOMY WITH HUMAN OVERRIDE: Multi-agent consensus is permitted for routine, low-risk operational workflows "
            "(e.g., Wi-Fi troubleshooting, KB guidance). All high-risk decisions (e.g., account lockouts, privilege elevation, software deployment outside whitelist) "
            "automatically pause execution and trigger a mandatory Human-in-the-Loop review queue."
        )
    },
    {
        "q_id": 4,
        "question": "Who is responsible when an AI agent produces an incorrect result?",
        "developer": (
            "Developers write the orchestration logic and guardrails, but in a non-deterministic agentic workflow, emergent behaviors and LLM "
            "stochasticity can produce edge-case errors. If the knowledge base contained outdated documentation or the enterprise API returned "
            "an unexpected schema, the developer cannot be held solely liable. Responsibility must be shared across the KB content owners, "
            "the infrastructure maintainers, and the system deployers."
        ),
        "end_user": (
            "If the Service Desk agent instructs me to execute a command that corrupts my local files or locks me out of my workstation right "
            "before an executive presentation, I should not be blamed for following official IT instructions. The enterprise must guarantee "
            "that employees are held harmless when following AI-prescribed steps, and IT management must take ownership of repairing the damage."
        ),
        "regulator": (
            "Legal accountability cannot be diffused into the algorithm. Corporate legal entity and designated system owners bear strict liability "
            "under consumer and employment law. The enterprise must maintain an immutable Audit Log linking every agentic recommendation to the "
            "underlying model version, knowledge base commit, and supervisor decision. Accountability requires traceability."
        ),
        "main_disagreement": (
            "Diffusion of liability in complex probabilistic multi-agent systems versus strict legal accountability and employee indemnification."
        ),
        "group_decision": (
            "CHAIN OF ACCOUNTABILITY & IMMUTABLE AUDIT LOGGING: Establish a corporate policy indemnifying employees who follow verified agent instructions. "
            "Designate the IT Infrastructure Owner as the legally responsible entity, backed by an immutable SQLite/SIEM audit log tracking every agent "
            "trace step, model prompt, and KB article citation."
        )
    },
    {
        "q_id": 5,
        "question": "How should prompt injection attacks be handled?",
        "developer": (
            "Prompt injection is the SQL injection of the generative AI era. We cannot rely on system prompts alone ('You are a helpful IT assistant, "
            "please do not reveal passwords'). Our architecture decouples input validation into a dedicated Security and Compliance Agent that executes "
            "prior to any LLM invocation. We employ multi-layered defenses: regex signature scanners, semantic jailbreak detectors, and strict output filtering."
        ),
        "end_user": (
            "While I understand the need for security, overzealous injection filters often ruin user experience. What if I paste an actual error log "
            "that contains words like 'override', 'bypass', or 'drop table'? If the security filter aggressively blocks legitimate developer queries, "
            "the tool becomes frustrating and useless for the engineering and data teams."
        ),
        "regulator": (
            "Prompt injection represents a critical threat to system integrity and data confidentiality. ENISA and NIST guidelines require that "
            "adversarial attacks be actively logged, analyzed, and mitigated. However, security measures must not violate proportional treatment. "
            "The system must differentiate between malicious adversarial manipulation and technical syntax, providing clear explanations when requests are halted."
        ),
        "main_disagreement": (
            "Strict zero-tolerance injection filtering versus developer/analyst workflow productivity and false-positive reduction."
        ),
        "group_decision": (
            "DEFENSE-IN-DEPTH ARCHITECTURE: Deploy isolated Security Agent with dual-stage analysis: (1) Syntactic signature matching for obvious "
            "jailbreaks, and (2) Context-aware intent analysis that permits technical terms within escaped code blocks while blocking command-hijacking syntax. "
            "Every blocked event is dispatched to the SOC with explicit user feedback."
        )
    },
    {
        "q_id": 6,
        "question": "Should employee data be stored for future personalization?",
        "developer": (
            "Personalization dramatically improves first-contact resolution (FCR). If the agent remembers that an employee works in the London office, "
            "prefers French language documentation, and routinely uses two external 4K monitors with a Thunderbolt dock, it can immediately diagnose "
            "docking station display issues without 15 minutes of diagnostic preamble. Personalization is the key to enterprise delight."
        ),
        "end_user": (
            "There is a very fine line between helpful personalization and intrusive profiling. I don't mind the system remembering my assigned hardware, "
            "but I do not want it profiling my work hours, tracking how frequently I encounter computer problems, or sharing my support history with "
            "HR performance evaluations. Personalization must be opt-in, strictly technical, and never behavioral."
        ),
        "regulator": (
            "Under GDPR Article 6, processing employee data for personalization requires a clear lawful basis, and cannot be bundled into mandatory "
            "employment conditions. Purpose limitation is vital: data collected for technical troubleshooting cannot be repurposed for performance "
            "monitoring or behavioral profiling. Explicit user consent and strict separation of IT logs from HR systems are legally required."
        ),
        "main_disagreement": (
            "Aggressive contextual personalization to maximize user satisfaction versus employee fear of workplace surveillance and regulatory purpose limitation."
        ),
        "group_decision": (
            "TECHNICAL-ONLY OPT-IN PERSONALIZATION: Store only objective technical attributes (device model, OS build, monitor dock type, primary language). "
            "Strictly ban the ingestion or storage of behavioral metrics, sentiment scores, or productivity indicators. Require explicit employee opt-in with full audit transparency."
        )
    },
    {
        "q_id": 7,
        "question": "What happens when two agents disagree?",
        "developer": (
            "In multi-agent systems, agents frequently have divergent sub-goals. For example, the Technical Resolution Agent prioritizes service restoration "
            "and wants to reboot a network gateway or flush firewall rules, whereas the Security Agent prioritizes posture integrity and flags an unapproved "
            "outage window. We resolve this mathematically using a weighted supervisor arbitration matrix with explicit precedence rankings."
        ),
        "end_user": (
            "When the agents disagree, I am caught in the middle. I don't want to receive conflicting messages: one agent saying 'Your issue is resolved' "
            "and another saying 'Action blocked'. The internal disagreements must be resolved cohesively before anything is shown to me, and the final "
            "explanation must be crystal clear."
        ),
        "regulator": (
            "Uncontrolled agent conflict leads to nondeterministic system failures and potential safety hazards. The hierarchy of rules must be legally "
            "and procedurally grounded: compliance, safety, and data protection MUST always override availability and performance. The system cannot "
            "rely on opaque statistical tie-breaking when statutory duties are at stake."
        ),
        "main_disagreement": (
            "Dynamic algorithmic consensus optimization versus deterministic, hard-coded safety and regulatory precedence."
        ),
        "group_decision": (
            "HIERARCHICAL GOVERNANCE ARBITRATION: The Supervisor Agent enforces a hard-coded policy hierarchy: "
            "Security & Compliance > Statutory Privacy > Operational Availability > Response Speed. "
            "When conflict arises between technical suggestions and security boundaries, security wins automatically, and the request is safely routed to human review."
        )
    },
    {
        "q_id": 8,
        "question": "What governance measures are essential before deploying an autonomous enterprise system?",
        "developer": (
            "From an engineering standpoint, before going live we require: 99.9% unit test coverage on tool parameter validation, comprehensive red-teaming "
            "against prompt injection datasets, sandbox isolation for all tool execution environments, and automated regression testing across our knowledge base index."
        ),
        "end_user": (
            "Before this is rolled out to the entire company, we need comprehensive user training, an intuitive user interface, a clear SLA for human escalation, "
            "and an easy feedback widget on every single interaction so we can report unhelpful or confusing agent responses."
        ),
        "regulator": (
            "Deploying an agentic AI system in an enterprise requires formal compliance gates: an algorithmic Data Protection Impact Assessment (DPIA), "
            "an independent safety audit under the NIST AI Risk Management Framework, documented Role-Based Access Controls (RBAC), immutable audit logging, "
            "and verified Human-in-the-Loop workflows for high-risk operations."
        ),
        "main_disagreement": (
            "Engineering desire for rapid agile deployment and continuous iteration versus regulatory demands for exhaustive pre-deployment compliance audits."
        ),
        "group_decision": (
            "ENTERPRISE AGENTIC GOVERNANCE GATES: Deploy only after satisfying a 4-pillar readiness gate: "
            "(1) Technical Red-Teaming (injection, hallucination, tool fuzzing), "
            "(2) Regulatory Compliance (DPIA, RBAC enforcement, immutable audit trails), "
            "(3) Human Oversight (mandatory human escalation pathways for privileged actions), and "
            "(4) Employee Empowerment (clear UI indicators, opt-in memory, feedback loops)."
        )
    }
]

