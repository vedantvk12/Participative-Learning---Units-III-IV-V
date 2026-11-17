"""
Package Deliverables into Agentic_AI_Units_III_IV_V_Source_Code.zip
And verify all deliverables.
"""

import os
import zipfile
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
ZIP_OUT = BASE_DIR / "Agentic_AI_Units_III_IV_V_Source_Code.zip"

INCLUDED_EXTENSIONS = [".py", ".json", ".md", ".txt", ".toml", ".png", ".db"]
EXCLUDED_DIRS = ["__pycache__", ".git", ".idea", ".vscode"]


def create_zip():
    print(f"Building source archive: {ZIP_OUT}...")
    if ZIP_OUT.exists():
        ZIP_OUT.unlink()

    with zipfile.ZipFile(ZIP_OUT, 'w', zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(BASE_DIR):
            # Prune excluded directories
            dirs[:] = [d for d in dirs if d not in EXCLUDED_DIRS]

            for file in files:
                file_path = Path(root) / file
                rel_path = file_path.relative_to(BASE_DIR)

                # Skip existing zip
                if file.endswith(".zip") or file.endswith(".tmp"):
                    continue

                if file_path.suffix.lower() in INCLUDED_EXTENSIONS:
                    zf.write(file_path, arcname=str(rel_path))
                    print(f"  Added: {rel_path}")

    size_mb = ZIP_OUT.stat().st_size / (1024 * 1024)
    print(f"Source code zip created successfully ({size_mb:.2f} MB)")


def verify_all_deliverables():
    required_files = [
        "Agentic_AI_Units_III_IV_V_Assignment.pdf",
        "Agentic_AI_Units_III_IV_V_Assignment.docx",
        "Agentic_AI_Units_III_IV_V_Source_Code.zip",
        "README.md",
        "Panel_Discussion_Role_Play_Script.pdf",
        "assets/architecture_diagram.png",
        "assets/multi_agent_workflow.png",
        "assets/memory_hierarchy.png",
        "assets/governance_framework.png",
        "assets/screenshot_tab1_overview.png",
        "assets/screenshot_tab2_memory_tools.png",
        "assets/screenshot_tab3_collaboration.png",
        "assets/screenshot_tab4_safety_lab.png",
        "assets/screenshot_tab5_panel.png",
        "assets/demonstration_logs.txt",
    ]

    print("\n--- DELIVERABLES VERIFICATION ---")
    all_ok = True
    for req in required_files:
        p = BASE_DIR / req
        if p.exists():
            size = p.stat().st_size
            print(f"  [OK] {req} ({size:,} bytes)")
        else:
            print(f"  [MISSING] {req}")
            all_ok = False

    if all_ok:
        print("\nAll deliverables are present and verified!")
    else:
        print("\nWARNING: Some deliverables are missing!")
    return all_ok


if __name__ == "__main__":
    create_zip()
    verify_all_deliverables()

