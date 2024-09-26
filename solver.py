import sys
from copy import copy
from threading import Event

#!/usr/bin/env python3
from enum import Enum

class SATSolverResult(Enum):
    SAT = 1
    UNSAT = 2
    UNKNOWN = 3


def read_DIMACS(fname):
    def read_text_file(fname):
        with open(fname) as f:
            content = f.readlines()
        return [x.strip() for x in content]

    content = [line for line in read_text_file(fname) if line and not line.startswith("c")]

    header = content[0].split(" ")

    assert header[0] == "p" and header[1] == "cnf", content
    variables_total, clauses_total = int(header[2]), int(header[3])

    # array idx=number (of line) of clause
    # val=list of terms
    # term can be negative signed integer
    clauses = []
    for c in content[1:]:
        if c.startswith("c "):
            continue
        clause = []
        for var_s in c.split(None):
            var = int(var_s)
            if var != 0:
                clause.append(var)

        clauses.append(clause)

    if clauses_total != len(clauses):
        print("warning: header says ", clauses_total, " but read ", len(clauses))
    return variables_total, clauses



class Solver:
    def __init__(self, filename: str, sigkill: Event):
        self.sigkill = sigkill
        self.variables_count, self.clauses = read_DIMACS(filename)

    def solve(self) -> SATSolverResult:
        response = self.__solve(self.clauses)
        return response

    def __solve(self, cnf, assignments=[]) -> (SATSolverResult, {}):
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
        new_assignments.append(l)

        sat = self.__solve(new_cnf, new_assignments)
        if sat != SATSolverResult.UNSAT:
            return sat

        return SATSolverResult.UNSAT

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
