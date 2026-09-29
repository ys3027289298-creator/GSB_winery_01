import unittest

import core


class TestCore(unittest.TestCase):
    def test_01_no_duplicate_crush(self):
        state = core.new_game()
        self.assertTrue(core.crush(state, 1, 10))
        self.assertFalse(core.crush(state, 1, 10))

    def test_02_tank_capacity(self):
        state = core.new_game()
        state["tank_load"] = 2
        result = core.ferment(state, 2, 1)
        self.assertFalse(result)

    def test_03_temp_boundary(self):
        state = core.new_game()
        self.assertEqual(core.check_temp(state, 35), "over")

    def test_04_cancel_releases_tank(self):
        state = core.new_game()
        core.ferment(state, 1, 1)
        core.cancel(state, 1)
        self.assertEqual(state["tank_load"], 0)

    def test_05_inspect_failure_refunds(self):
        state = core.new_game()
        core.crush(state, 1, 10)
        state["batches"][1]["defect"] = True
        before = state["material"]
        result = core.inspect(state, 1)
        self.assertFalse(result)
        self.assertEqual(state["material"], before + 10)

    def test_06_no_produce_on_fault(self):
        state = core.new_game()
        state["cold_fault"] = True
        result = core.produce(state, 5)
        self.assertFalse(result)

    def test_07_age_once(self):
        state = core.new_game()
        state["batches"] = {1: {"amount": 0, "defect": False}}
        core.age(state, 1)
        self.assertEqual(state["batches"][1]["amount"], 10)

    def test_08_load_preserves_batch(self):
        state = core.new_game()
        state["batch_id"] = 4
        loaded = core.load_state(core.save_state(state))
        self.assertEqual(loaded["batch_id"], 4)


if __name__ == "__main__":
    unittest.main()
