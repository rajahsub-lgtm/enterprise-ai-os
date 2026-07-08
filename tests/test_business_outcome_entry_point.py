from src.eaios.runtime.business_outcome_manager import BusinessOutcomeManager
from src.eaios.runtime.capability_assessor import CapabilityAssessor
from src.eaios.runtime.task_planner import TaskPlanner
from src.eaios.runtime.skill_matcher import SkillMatcher
from src.eaios.runtime.agent_orchestrator import AgentOrchestrator


def test_existing_eaios_entry_point_starts_with_business_outcome():
    manager = BusinessOutcomeManager()

    trace = manager.start("Maintain Application Health")

    assert trace.business_outcome == "Maintain Application Health"
    assert trace.capability == ""
    assert trace.tasks == []
    assert trace.skills == []
    assert trace.agents == []


def test_business_outcome_flows_to_capability_tasks_skills_and_agents():
    trace = BusinessOutcomeManager().start("Maintain Application Health")

    capability = CapabilityAssessor().assess(trace)
    tasks = TaskPlanner().plan(trace)
    skills = SkillMatcher().match(trace)
    agents = AgentOrchestrator().orchestrate(trace)

    assert capability == "Application Health Management"
    assert trace.business_outcome == "Maintain Application Health"

    assert "Collect Telemetry" in tasks
    assert "Search Knowledge" in tasks
    assert "Perform KT Analysis" in tasks
    assert "Recommend Action" in tasks

    assert "Impact Analysis" in skills
    assert "Information Retrieval" in skills
    assert "Problem Analysis" in skills
    assert "Decision Analysis" in skills

    assert "Telemetry Agent" in agents
    assert "Knowledge Agent" in agents
    assert "Reasoning Agent" in agents
    assert "Recommendation Agent" in agents