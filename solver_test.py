import os
from threading import Event, Thread
from solver import Solver
from time import perf_counter
from utils import SATSolverResult
from collections import defaultdict
from math import ceil


class Tests:
    def __init__(self, TIME_LIMIT: float):
        self.results = defaultdict(lambda: SATSolverResult.UNKNOWN)
        self.TIME_LIMIT = TIME_LIMIT
        self.tests_dir = os.path.join(os.getcwd(), "tests")

    def worker(self, path, event):
        self.results[path] = Solver(path, event).solve()

    def runner(self, path):
        event = Event()
        thread = Thread(target=self.worker, args=(path, event))
        t1 = perf_counter()
        thread.start()
        thread.join(self.TIME_LIMIT)
        event.set()
        thread.join()
        delta_t = perf_counter() - t1
        return delta_t

    def test_folder(self, folder: str, gold_result: SATSolverResult):
        for entry in os.scandir(os.path.join(self.tests_dir, folder)):
            print("Solving", entry.path)
            delta_t = self.runner(entry.path)
            result = self.results[entry.path]
            print(f"Result: {result} and delta: {delta_t}")

    def solver(self, tests):
        for folder, gold_result in tests:
            self.test_folder(folder, gold_result)

    def test_dpll(self):
        self.solver([("sat-dpll", SATSolverResult.SAT), ("unsat-dpll", SATSolverResult.UNSAT)])
        self.RANK = 0


if __name__ == "__main__":
    Tests(TIME_LIMIT=60.0).test_dpll()
