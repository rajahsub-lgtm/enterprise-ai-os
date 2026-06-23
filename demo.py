import json

from src.eaios.agents.telemetry_agent import TelemetryAgent
from src.eaios.agents.knowledge_agent import KnowledgeAgent
from src.eaios.agents.reasoning_agent import ReasoningAgent
from src.eaios.agents.recommendation_agent import RecommendationAgent

from src.eaios.runtime.business_outcome_manager import BusinessOutcomeManager
from src.eaios.runtime.capability_assessor import CapabilityAssessor
from src.eaios.runtime.task_planner import TaskPlanner
from src.eaios.runtime.skill_matcher import SkillMatcher
from src.eaios.runtime.agent_orchestrator import AgentOrchestrator
from src.eaios.runtime.safety_gate import SafetyGate
from src.eaios.runtime.learning_manager import LearningManager
from src.eaios.runtime.execution_reporter import ExecutionReporter


def main() -> None:
    manager = BusinessOutcomeManager()
    assessor = CapabilityAssessor()
    planner = TaskPlanner()
    matcher = SkillMatcher()
    orchestrator = AgentOrchestrator()
    safety_gate = SafetyGate()
    learning_manager = LearningManager()
    reporter = ExecutionReporter()

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

    with open("examples/application-health/telemetry.json") as f:
        telemetry = json.load(f)

    with open("examples/application-health/incidents.json") as f:
        incidents = json.load(f)

    with open("examples/application-health/knowledge.json") as f:
        knowledge = json.load(f)

    telemetry_result = TelemetryAgent().execute(telemetry)
    knowledge_result = KnowledgeAgent().execute(incidents, knowledge)
    reasoning_result = ReasoningAgent().execute(
        telemetry_result,
        knowledge_result,
    )
    recommendation_result = RecommendationAgent().execute(
        reasoning_result,
        knowledge_result,
    )

    print("\n=== Agent Outputs ===")

    print("\nTelemetry Agent")
    print(telemetry_result)

    print("\nKnowledge Agent")
    print(knowledge_result)

    print("\nReasoning Agent")
    print(reasoning_result)

    print("\nRecommendation Agent")
    print(recommendation_result)

    print(
        reporter.generate(
            trace,
            telemetry_result,
            knowledge_result,
            reasoning_result,
            recommendation_result,
        )
    )


if __name__ == "__main__":
    main()