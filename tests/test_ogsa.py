import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from replication_simulation import (
    AdapterSnapshot,
    DecisionKind,
    DecisionStatus,
    File,
    Node,
    OGSAAdapter,
    OGSAUnresolvedError,
    OgsaAgent,
    OgsaAssignment,
    OgsaConfig,
    OgsaObjectiveContext,
    OgsaRequest,
    OgsaWeights,
    Scenario,
    SimulationState,
    Site,
    acceleration,
    ec,
    gravitational_constant,
    masses,
    ml,
    mof,
    mst,
    mfu,
    opposite_position,
    update_agent,
    validate_assignment,
    lv,
    objective_vector,
)


class OGSATests(unittest.TestCase):
    def assignment(self):
        return OgsaAssignment(
            matrix=((1, 0), (0, 1)),
            file_sizes=(2.0, 3.0),
            node_capacities=(4.0, 4.0),
        )

    def context(self):
        return OgsaObjectiveContext(
            unavailable_probabilities=(0.1, 0.2),
            service_time_by_file_node=((1.0, 2.0), (3.0, 4.0)),
            access_by_file_node=((2.0, 1.0), (1.0, 3.0)),
            node_load_values=(1.0, 3.0),
            energy_load_by_file_node=((1.0, 0.0), (0.0, 2.0)),
            pmax_by_node=(10.0, 10.0),
            pidle_by_node=(2.0, 2.0),
            q=2.0,
            latency_by_file=(2.0, 4.0),
        )

    def setUp(self):
        scenario = Scenario(
            scenario_id="scenario-ogsa",
            sites={"site-1": Site("site-1", ("node-1", "node-2"))},
            nodes={
                "node-1": Node("node-1", "site-1"),
                "node-2": Node("node-2", "site-1"),
            },
            files={"file-1": File("file-1", 2.0), "file-2": File("file-2", 3.0)},
        )
        self.state = SimulationState(scenario)
        self.snapshot = AdapterSnapshot.from_state(self.state, run_id="run-1")

    def test_assignment_integrity_and_capacity_constraints(self):
        validate_assignment(self.assignment())
        with self.assertRaises(OGSAUnresolvedError):
            validate_assignment(OgsaAssignment(((0, 0), (0, 1)), (2.0, 3.0), (4.0, 4.0)))
        with self.assertRaises(OGSAUnresolvedError):
            validate_assignment(OgsaAssignment(((1, 0), (1, 0)), (3.0, 3.0), (4.0, 4.0)))

    def test_objectives_are_independently_identifiable(self):
        context = self.context()
        assignment = self.assignment()
        self.assertAlmostEqual(mfu(assignment, context), 0.15)
        self.assertGreater(mst(assignment, context), 0.0)
        self.assertEqual(lv(context), 2.0)
        self.assertGreater(ec(assignment, context), 0.0)
        self.assertEqual(ml(context), 3.0)
        self.assertEqual(len(objective_vector(assignment, context).values), 5)

    def test_mof_uses_explicit_source_reported_equal_weights(self):
        vector = objective_vector(self.assignment(), self.context())
        self.assertAlmostEqual(mof(vector, OgsaWeights.source_reported_equal()), sum(vector.values) / 5.0)

    def test_obl_equation(self):
        self.assertEqual(opposite_position((2.0, 5.0), (0.0, 1.0), (10.0, 9.0)), (8.0, 5.0))

    def test_gsa_mass_gravity_and_updates(self):
        values = masses((1.0, 3.0))
        self.assertEqual(sum(values), 1.0)
        self.assertEqual(gravitational_constant(10.0, 2, 10), 8.0)
        agents = (
            OgsaAgent((0.0, 0.0), (1.0, 1.0)),
            OgsaAgent((2.0, 0.0), (0.0, 0.0)),
        )
        accel = acceleration(0, agents, values, 1.0, 0.1, (0, 1), 0.5)
        updated = update_agent(agents[0], accel, 0.5)
        self.assertEqual(len(accel), 2)
        self.assertEqual(len(updated.position), 2)

    def test_adapter_executes_obl_gsa_and_returns_placement(self):
        request = OgsaRequest(
            assignment=self.assignment(),
            objective_context=self.context(),
            weights=OgsaWeights.source_reported_equal(),
            config=OgsaConfig(population_size=4, generations=2),
            file_id="file-1",
        )
        result = OGSAAdapter(request).compute(self.snapshot)
        self.assertEqual(result.kind, DecisionKind.PLACEMENT)
        self.assertEqual(result.status, DecisionStatus.ACCEPTED)
        self.assertTrue(dict(result.payload)["placement_node_ids"])
        self.assertEqual(self.state.scenario.files["file-1"].file_id, "file-1")

    def test_fixed_equal_weights_and_defaults_are_executable(self):
        request = OgsaRequest(assignment=self.assignment(), objective_context=self.context(), file_id="file-1")
        result = OGSAAdapter(request).compute(self.snapshot)
        self.assertEqual(result.status, DecisionStatus.ACCEPTED)


if __name__ == "__main__":
    unittest.main()
