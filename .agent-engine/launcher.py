#!/usr/bin/env python3
"""
Vibing Agent Engine - Standalone Launcher
Automatically builds projects using autonomous AI agents
"""

import os
import sys
from pathlib import Path
import subprocess
import json
from datetime import datetime

# Colors for terminal output
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_header(text):
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*70}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{text.center(70)}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'='*70}{Colors.ENDC}\n")

def print_success(text):
    print(f"{Colors.OKGREEN}✅ {text}{Colors.ENDC}")

def print_error(text):
    print(f"{Colors.FAIL}❌ {text}{Colors.ENDC}")

def print_info(text):
    print(f"{Colors.OKCYAN}ℹ️  {text}{Colors.ENDC}")

def print_warning(text):
    print(f"{Colors.WARNING}⚠️  {text}{Colors.ENDC}")

def check_dependencies():
    """Check if required dependencies are installed."""
    print_header("Checking Dependencies")
    
    # Check Python version
    if sys.version_info < (3, 9):
        print_error(f"Python 3.9+ required. Current: {sys.version}")
        return False
    print_success(f"Python {sys.version_info.major}.{sys.version_info.minor}")
    
    # Check for required packages
    required_packages = ['crewai', 'langchain', 'openai']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print_success(f"{package} installed")
        except ImportError:
            missing_packages.append(package)
            print_error(f"{package} NOT installed")
    
    if missing_packages:
        print_warning("Installing missing dependencies...")
        agent_engine_root = Path(__file__).parent
        requirements_file = agent_engine_root / "requirements.txt"
        
        if requirements_file.exists():
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", str(requirements_file)])
                print_success("Dependencies installed successfully")
            except subprocess.CalledProcessError:
                print_error("Failed to install dependencies")
                print_info(f"Please run: pip install -r {requirements_file}")
                return False
        else:
            print_error(f"requirements.txt not found at {requirements_file}")
            return False
    
    return True

def check_environment():
    """Check environment variables."""
    print_header("Checking Environment")
    
    # Check for .env file
    agent_engine_root = Path(__file__).parent
    env_file = agent_engine_root / ".env"
    env_example = agent_engine_root / ".env.example"
    
    if not env_file.exists():
        if env_example.exists():
            print_warning(".env file not found")
            print_info(f"Please copy {env_example} to {env_file}")
            print_info("Then add your API keys")
            return False
        else:
            print_warning("No .env file found, will use environment variables")
    else:
        print_success(".env file found")
        # Load .env
        try:
            from dotenv import load_dotenv
            load_dotenv(env_file)
            print_success("Environment variables loaded")
        except ImportError:
            print_warning("python-dotenv not installed, skipping .env loading")
    
    # Check for required env vars
    required_vars = ['OPENAI_API_KEY', 'SERPER_API_KEY']
    optional_vars = ['GITHUB_COPILOT_TOKEN', 'ANTHROPIC_API_KEY']
    
    missing_required = []
    for var in required_vars:
        if os.getenv(var):
            print_success(f"{var} set")
        else:
            missing_required.append(var)
            print_error(f"{var} NOT set")
    
    for var in optional_vars:
        if os.getenv(var):
            print_success(f"{var} set (optional)")
        else:
            print_info(f"{var} not set (optional)")
    
    if missing_required:
        print_error(f"Missing required environment variables: {', '.join(missing_required)}")
        print_info("Add them to .env file or set as environment variables")
        return False
    
    return True

def human_in_the_loop_gate(gate_name: str, artifact_path: Path) -> str:
    """Implement human-in-the-loop approval gate."""
    print_header(f"Human Approval Required: {gate_name}")
    
    # Open artifact for review
    if artifact_path.exists():
        print_info(f"Opening {artifact_path.name} for review...")
        
        # Open in default editor
        if sys.platform == "win32":
            os.startfile(artifact_path)
        elif sys.platform == "darwin":
            subprocess.run(["open", artifact_path])
        else:
            subprocess.run(["xdg-open", artifact_path])
        
        print_info("Please review the document")
    else:
        print_warning(f"{artifact_path.name} not found yet")
    
    print("\nOptions:")
    print("  [A] Approve - Continue to next phase")
    print("  [R] Revise  - Request changes")
    print("  [C] Cancel  - Stop the project")
    
    while True:
        choice = input("\nYour decision (A/R/C): ").strip().upper()
        
        if choice == 'A':
            print_success("Approved! Continuing to next phase...")
            return "APPROVED"
        elif choice == 'R':
            feedback = input("What changes are needed? ")
            print_warning(f"Revision requested: {feedback}")
            return f"REVISE: {feedback}"
        elif choice == 'C':
            print_error("Project cancelled by user")
            return "CANCELLED"
        else:
            print_warning("Invalid choice. Please enter A, R, or C")

def save_gate_decision(gate_name: str, decision: str, project_root: Path):
    """Save HITL gate decision to file."""
    gates_dir = project_root / ".agent-engine" / "gates"
    gates_dir.mkdir(parents=True, exist_ok=True)
    
    decision_file = gates_dir / f"{gate_name.lower()}_decision.txt"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    with open(decision_file, 'w') as f:
        f.write(f"Gate: {gate_name}\n")
        f.write(f"Timestamp: {timestamp}\n")
        f.write(f"Decision: {decision}\n")
    
    print_success(f"Decision saved to {decision_file}")

def run_agent_engine(project_root: Path, project_scope: str):
    """Run the agent engine to build the project."""
    print_header("Starting Agent Engine")
    
    print_info(f"Project Root: {project_root}")
    print_info(f"Scope: {project_scope[:100]}...")
    
    # Import the orchestrator
    agent_engine_root = Path(__file__).parent
    sys.path.insert(0, str(agent_engine_root / "src"))
    
    try:
        from orchestrators.crewai_orchestrator import VibingCrewAIOrchestrator
        
        print_success("Orchestrator imported successfully")
        
        # Initialize orchestrator
        print_info("Initializing agents...")
        orchestrator = VibingCrewAIOrchestrator(str(project_root))
        
        print_success(f"Initialized {len(orchestrator.agents)} agents")
        
        # Phase 1: PRD Generation
        print_header("Phase 1: Requirements & Planning")
        print_info("Generating Product Requirements Document...")
        
        # Run PRD generation (you would integrate the actual crew tasks here)
        # For now, we'll do a simplified version
        
        # HITL Gate 1: PRD Approval
        prd_path = project_root / "docs" / "PRD.md"
        decision = human_in_the_loop_gate("PRD Approval", prd_path)
        save_gate_decision("PRD", decision, project_root)
        
        if decision == "CANCELLED":
            print_error("Project build cancelled")
            return False
        
        if decision.startswith("REVISE"):
            print_info("PRD revision requested. Please modify and re-run.")
            return False
        
        # Phase 2: Tech Research & Scaffolding
        print_header("Phase 2: Research & Scaffolding")
        print_info("Researching tech stack and creating project structure...")
        
        # Run full build
        print_info("Running autonomous agent workflow...")
        result = orchestrator.build_project(project_scope)
        
        print_success("Project build completed!")
        print_info(f"Artifacts created: {result.get('artifacts_created', 'unknown')}")
        print_info(f"Project memory: {result.get('project_memory', 'unknown')}")
        
        return True
        
    except ImportError as e:
        print_error(f"Failed to import orchestrator: {e}")
        print_info("Make sure all dependencies are installed")
        return False
    except Exception as e:
        print_error(f"Error during build: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main entry point for the agent engine launcher."""
    print_header("Vibing Agent Engine - Standalone Launcher")
    print_info("Framework Version: 1.1.0")
    print_info(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Determine project root (parent of .agent-engine)
    agent_engine_root = Path(__file__).parent
    project_root = agent_engine_root.parent
    
    print_info(f"Project: {project_root.name}")
    
    # Pre-flight checks
    if not check_dependencies():
        print_error("Dependency check failed")
        sys.exit(1)
    
    if not check_environment():
        print_error("Environment check failed")
        sys.exit(1)
    
    # Load project configuration
    config_file = agent_engine_root / "config" / "project.json"
    project_scope = "Vehicle panel beating workflow management system with RBAC for different organizational roles and various workflow touchpoints"
    
    if config_file.exists():
        try:
            with open(config_file, 'r') as f:
                config = json.load(f)
                if 'project_scope' in config:
                    project_scope = config['project_scope']
                    print_success("Loaded project scope from config")
        except Exception as e:
            print_warning(f"Could not load project config: {e}")
    
    # Show project scope
    print_header("Project Scope")
    print(f"{project_scope}\n")
    
    # Confirm to proceed
    proceed = input("Start the agent engine? (y/n): ").strip().lower()
    if proceed != 'y':
        print_warning("Cancelled by user")
        sys.exit(0)
    
    # Run the agent engine
    success = run_agent_engine(project_root, project_scope)
    
    if success:
        print_header("Build Complete!")
        print_success("Your project is ready")
        print_info(f"Location: {project_root}")
        print_info("Next steps:")
        print("  1. Review the generated code")
        print("  2. Install dependencies (npm install or pip install)")
        print("  3. Start development!")
    else:
        print_header("Build Failed")
        print_error("The agent engine encountered an error")
        print_info("Check the logs above for details")
        sys.exit(1)

if __name__ == "__main__":
    main()
