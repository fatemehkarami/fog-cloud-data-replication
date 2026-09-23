import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from replication_simulation import (
    AdapterSnapshot,
    DecisionKind,
    DecisionStatus,
    EIMORMAdapter,
    EIMORMClassification,
    EIMORMUnresolvedError,
    EimormContext,
    EimormCostEntry,
    EimormRequest,
    File,
    Node,
    Scenario,
    SimulationState,
    Site,
    aggregate_replication_cost,
    budget_reached,
    executable_etbdf_score,
    earf_one,
    interpretation_required,
    source_etbdf_semantics,
)


class EIMORMTests(unittest.TestCase):
    def setUp(self):
        scenario = Scenario(
            scenario_id="scenario-eimorm",
            sites={"site-1": Site("site-1", ("node-1",))},
            nodes={"node-1": Node("node-1", "site-1")},
            files={"file-1": File("file-1", 2.0)},
        )
        self.state = SimulationState(scenario)
        self.snapshot = AdapterSnapshot.from_state(self.state, run_id="run-1")

    def context(self):
        return EimormContext(
            file_id="file-1",
            current_time=10.0,
            historical_time=2.0,
            lambda_value=1,
            recent_replica_factor=3.0,
            old_replica_factor=1.0,
            replication_cost=12.0,
            user_budget=10.0,
        )

    def test_earf_preserves_explicit_source_relation(self):
        self.assertEqual(earf_one(3.0, 1.0), 0.75)
        with self.assertRaises(EIMORMUnresolvedError):
            earf_one(0.0, 0.0)

    def test_researcher_etbdf_interpretation_is_deterministic(self):
        self.assertEqual(executable_etbdf_score(10.0, 2.0, 1), 0.00033546262790251185)
        with self.assertRaises(EIMORMUnresolvedError):
            source_etbdf_semantics(10.0, 2.0, None)

    def test_cost_aggregation_and_budget_condition(self):
        cost = aggregate_replication_cost((
            EimormCostEntry("dc-1", 2.0, 3.0),
            EimormCostEntry("dc-2", 4.0, 1.0),
        ))
        self.assertEqual(cost, 10.0)
        self.assertTrue(budget_reached(10.0, 10.0))
        self.assertFalse(budget_reached(9.0, 10.0))

    def test_earf_adapter_returns_formula_without_downstream_mapping(self):
        result = EIMORMAdapter(EimormRequest(self.context(), operation="earf")).compute(self.snapshot)
        self.assertEqual(result.kind, DecisionKind.REPLICA_COUNT)
        self.assertEqual(result.status, DecisionStatus.ACCEPTED)
        self.assertEqual(dict(result.payload)["earf_one"], 0.75)
        self.assertEqual(dict(result.provenance)["downstream_mapping"], EIMORMClassification.UNRESOLVED.value)

    def test_etbdf_adapter_uses_fixed_researcher_policy(self):
        result = EIMORMAdapter(EimormRequest(self.context(), operation="etbdf")).compute(self.snapshot)
        self.assertEqual(result.status, DecisionStatus.ACCEPTED)
        self.assertGreater(dict(result.payload)["etbdf_score"], 0.0)

    def test_budget_reached_uses_deterministic_iek_interpretation(self):
        result = EIMORMAdapter(EimormRequest(self.context(), operation="cost_budget")).compute(self.snapshot)
        self.assertEqual(result.kind, DecisionKind.PLACEMENT)
        self.assertEqual(result.status, DecisionStatus.ACCEPTED)

    def test_iek_has_deterministic_budget_compatible_path(self):
        result = EIMORMAdapter(EimormRequest(self.context(), operation="iek")).compute(self.snapshot)
        self.assertIn(result.status, (DecisionStatus.ACCEPTED, DecisionStatus.NO_OP))

    def test_replication_manager_returns_executable_placement(self):
        result = EIMORMAdapter(EimormRequest(self.context())).compute(self.snapshot)
        self.assertEqual(result.kind, DecisionKind.PLACEMENT)
        self.assertEqual(result.status, DecisionStatus.ACCEPTED)

    def test_policy_classification_is_explicit(self):
        interpretation = interpretation_required("ETBDF", "OCR-damaged executable formula")
        self.assertEqual(interpretation.classification, EIMORMClassification.RESEARCHER_REQUIRED)
        self.assertEqual(interpretation.component, "ETBDF")

    def test_adapter_does_not_mutate_authoritative_state(self):
        before = dict(self.state.scenario.files)
        EIMORMAdapter(EimormRequest(self.context(), operation="earf")).compute(self.snapshot)
        self.assertEqual(before, self.state.scenario.files)


if __name__ == "__main__":
    unittest.main()
