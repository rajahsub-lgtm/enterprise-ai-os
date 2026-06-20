from src.eaios.runtime.business_outcome_manager import BusinessOutcomeManager
from src.eaios.runtime.capability_assessor import CapabilityAssessor
from src.eaios.runtime.task_planner import TaskPlanner
from src.eaios.runtime.skill_matcher import SkillMatcher
from src.eaios.runtime.agent_orchestrator import AgentOrchestrator
from src.eaios.runtime.safety_gate import SafetyGate
from src.eaios.runtime.learning_manager import LearningManager


def main() -> None:
    manager = BusinessOutcomeManager()
    assessor = CapabilityAssessor()
    planner = TaskPlanner()
    matcher = SkillMatcher()
    orchestrator = AgentOrchestrator()
    safety_gate = SafetyGate()
    learning_manager = LearningManager()

    trace = manager.start("Maintain Application Health")

    assessor.assess(trace)
    planner.plan(trace)
    matcher.match(trace)
    orchestrator.orchestrate(trace)
    safety_gate.evaluate(trace)
    learning_manager.capture(trace)

    print("\n=== EAIOS Demo: Application Health ===")
    print(f"Business Outcome: {trace.business_outcome}")
    print(f"Capability: {trace.capability}")

    print("\nTasks:")
    for task in trace.tasks:
        print(f"- {task}")

    print("\nSkills:")
    for skill in trace.skills:
        print(f"- {skill}")

    print("\nAgents:")
    for agent in trace.agents:
        print(f"- {agent}")

    print(f"\nSafety Status: {trace.safety_status}")
    print(f"\nEnterprise Learning: {trace.learning_summary}")


if __name__ == "__main__":
    main()