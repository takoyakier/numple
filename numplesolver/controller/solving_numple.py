"""Controller for solving sudoku"""
import time

from numplesolver.controller import cmd
from numplesolver.models import numples
from numplesolver.models import grids
from numplesolver.models import solvers
from numplesolver.views import gui

class NumpleSover():
    def __init__(self):
        self.grid = grids.Grid()
        self.solver = solvers.Solver(self.grid)
        self.grid.set_solver(self.grid)
        commander = cmd.CompositeCommand(self.grid)
        self.shower = gui.Shower(commander)
        commander.set_shower(self.shower)

    def solve(self):
        self.solver.solve()

    def load_values(self):
        self.grid.load_values

    def show(self):
        self.shower.show()


def solve_normal_numple():
    """Function to solve normal sudoku"""
    # solve(numples.Normal9x9())


def solve_numple():
    num_grid = 9
    while num_grid:
        print('solving_numple,  make num_grid:', num_grid)
        grid = grids.Grid(num_grid)
        solver = solvers.Solver(grid)
        commander = cmd.CompositeCommand(grid)
        shower = gui.Window(commander)
        shower.set_grid(grid.num_grid)
        grid.set_solver(solver)
        commander.set_shower(shower)

        num_grid = shower.show(grid)

def solve_16x16numple():
    solve(numples.Numple16())


def solve_combain_9x9numple():
    solve(numples.Combain9())


def solve_jigzag_9x9numple():
    solve(numples.JigZag9())


def solve(numple_kind):
    numple_solver = numple_kind
    numple_solver.show()
    numple_solver.solve()





def solve_diagonal_numple():
    grid = loader.make_9x9_grid()
    diagonal_solver = solvers.DiagnoalSolver(grid)
    gui.normal_show(grid)


def solve_ineqality_numple():
    pass


def solve_combain_numple():
    while True:
        grid = loader.make_9x9_grids()


def solve_jigzag_numple():
    grid = grids.Grid('jigzag')


def chooce_kind():
    kind = input('the kind is:')
    if kind == 'normal9x9':
        solve_normal_numple()
    elif kind == 'arrow':
        solve_arrow_numple()
    else:
        print('ダメー!')
