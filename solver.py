import sys
from copy import copy
from threading import Event
from utils import read_DIMACS, SATSolverResult


class Solver:
    def __init__(self, filename: str, sigkill: Event):
        self.sigkill = sigkill
        self.variables_count, self.clauses = read_DIMACS(filename)

    def solve(self) -> SATSolverResult:
        response = self.__solve(self.clauses)
        return response

    def __solve(self, cnf, assignments=[]) -> SATSolverResult:
        if self.sigkill.is_set():
            return SATSolverResult.UNKNOWN

        cnf, assignments = self.__unit_propagation(cnf, assignments)

        if len(cnf) == 0:
            return SATSolverResult.SAT

        if any([len(c) == 0 for c in cnf]):
            return SATSolverResult.UNSAT

        l = self.__select_literal(cnf)

        new_cnf = [c for c in cnf if l not in c]
        new_cnf = [list(set(c) - {-l}) for c in new_cnf]

        new_assignments = copy(assignments)
        new_assignments.append(l)

        sat = self.__solve(new_cnf, new_assignments)
        if sat != SATSolverResult.UNSAT:
            return sat

        new_cnf = [c for c in cnf if -l not in c]
        new_cnf = [list(set(c) - {l}) for c in new_cnf]

        new_assignments = copy(assignments)
        new_assignments.append(-l)

        return self.__solve(new_cnf, new_assignments)

    def __select_literal(self, clauses):
        for c in clauses:
            for literal in c:
                return abs(literal)

    def __unit_propagation(self, clauses, assignment=[]):
        flag = True
        while flag:
            flag = False
            for clause in clauses:
                if len(clause) == 1:
                    literal = clause[0]
                    clauses = self.__remove_literal(clauses, literal)
                    assignment += [literal]
                    flag = True
                if not clauses:
                    return clauses, assignment
        return clauses, assignment

    def __remove_literal(self, clauses, literal):
        clauses_copy = [x[:] for x in clauses]
        for x in reversed(clauses_copy):
            if literal in x:
                clauses_copy.remove(x)
            if -literal in x:
                x.remove(-literal)
        return clauses_copy


if __name__ == "__main__":
    print("Print cnf file path:")
    filename = input()
    result = Solver(filename, Event()).solve()
    if result == SATSolverResult.SAT:
        print("sat")
    elif result == SATSolverResult.UNSAT:
        print("unsat")
    else:
        print("unknown")
