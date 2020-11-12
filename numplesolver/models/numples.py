from abc import ABCMeta, abstractmethod

from numplesolver.models import grids
from numplesolver.models import solvers
from numplesolver.views import gui


class NumpleSolver(metaclass=ABCMeta):
    def solve(self):
        self.solver.solve()

    def show(self):
        self.window.show()


class Numple9(NumpleSolver):
    def __init__(self):
        self.grid = grids.NormalGrid(9)
        self.window = gui.Window(self.grid)
        self.grid.set_shower(self.window)

        self.solver = solvers.NormalSolver(self.grid)
        self.grid.set_solver(self.solver)

        # self.window.update()

    def load_grid(self):
        self.grid._load_values()


class Normal16(NumpleSolver):
    def load_grid(self):
        self.grid = grid.Grid12x12()

    def make_solver(self):
        self.solver = sover.NormalSolver()


class Combain(NumpleSolver):
    def load_grid(self):
        self.grid = grid.Grid9()
