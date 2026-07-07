import json
import sys


if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

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

from src.eaios.runtime.capability_visualizer import CapabilityVisualizer
from src.eaios.runtime.ecosystem_visualizer import EcosystemVisualizer
from src.eaios.runtime.experiment_visualizer import ExperimentVisualizer

from src.eaios.runtime.strategy_selector import StrategySelector
from src.eaios.runtime.strategy_visualizer import StrategyVisualizer

from src.eaios.runtime.implementation_registry import ImplementationRegistry
from src.eaios.runtime.agent_selector import AgentSelector
from src.eaios.runtime.agent_selection_visualizer import AgentSelectionVisualizer

from src.eaios.runtime.business_impact_visualizer import BusinessImpactVisualizer

from src.eaios.runtime.enterprise_memory import EnterpriseMemory
from src.eaios.runtime.confidence_engine import ConfidenceEngine
from src.eaios.runtime.confidence_visualizer import ConfidenceVisualizer

from src.eaios.runtime.execution_logger import ExecutionLogger

from src.eaios.runtime.learning_engine import LearningEngine

from src.eaios.runtime.learning_summary_visualizer import LearningSummaryVisualizer


def main() -> None:
    manager = BusinessOutcomeManager()
    assessor = CapabilityAssessor()
    planner = TaskPlanner()
    matcher = SkillMatcher()
    orchestrator = AgentOrchestrator()
    safety_gate = SafetyGate()
    learning_manager = LearningManager()
    reporter = ExecutionReporter()
    visualizer = CapabilityVisualizer()
    ecosystem = EcosystemVisualizer()
    experiment = ExperimentVisualizer()
    strategy_selector = StrategySelector()
    strategy_visualizer = StrategyVisualizer()
    implementation_registry = ImplementationRegistry()
    agent_selector = AgentSelector()
    agent_selection_visualizer = AgentSelectionVisualizer()
    business_impact = BusinessImpactVisualizer()
    enterprise_memory = EnterpriseMemory()
    confidence_engine = ConfidenceEngine()
    confidence_visualizer = ConfidenceVisualizer()
    execution_logger = ExecutionLogger()
    learning_engine = LearningEngine()
    learning_summary_visualizer = LearningSummaryVisualizer()
    

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

    with open("examples/application-health-realistic/telemetry_alert.json") as f:
        telemetry = json.load(f)

    with open("examples/application-health/incidents.json") as f:
        incidents = json.load(f)

    with open("examples/application-health/knowledge.json") as f:
        knowledge = json.load(f)

        print("\n==================================================")
        print("EAIOS ENTERPRISE ALERT")
        print("==================================================")
        print(f"Source: {telemetry['source']}")
        print(f"Service: {telemetry['service']}")
        print(f"Business Service: {telemetry['business_service']}")
        print(f"Signal: {telemetry['metric']}")
        print(f"Current Value: {telemetry['current_value']}")
        print(f"Threshold: {telemetry['threshold']}")
        print(f"Severity: {telemetry['severity']}")
        print("Enterprise Reasoning: INITIATED")
        print("==================================================")
    
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

    memory_result = enterprise_memory.lookup("payment gateway timeout")

    current_context = {
        "context_match_score": 0.91,
        "recent_failure_signal": "LOW",
        "business_risk": "HIGH",
    }

    confidence = confidence_engine.evaluate(
        memory_result,
        current_context,
    )

    print(confidence_visualizer.render(confidence))

    strategy = strategy_selector.select(confidence)
    print(strategy_visualizer.render(strategy))

    print(business_impact.render())
        
    implementations = implementation_registry.get_implementations(
        "Knowledge Retrieval"
    )

    selection = agent_selector.select(
        skill="Knowledge Retrieval",
        context="Application Health Investigation",
        implementations=implementations,
    )

    print(agent_selection_visualizer.render(selection))

    print(visualizer.render(trace))
    print(ecosystem.render())
    print(experiment.render())

    record = execution_logger.build_record(
        trace,
        confidence,
        strategy,
        recommendation_result,
    )

    execution_logger.record(record)

    updated_memory = learning_engine.update_memory(
    "payment gateway timeout"
)

    print(learning_summary_visualizer.render(updated_memory))

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