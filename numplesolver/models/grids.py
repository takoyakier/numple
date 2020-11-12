"""Load a grid"""
from abc import ABCMeta, abstractmethod
import copy
import sys

class Grid(object):
    """数独のクイズを表すグリッド
    class Grid object has two variables
        dict: coordinates of 0
    """
    def __init__(self, num_grid):
        self.num_grid = num_grid
        # self.values_qst = [[0 for _ in range(9)] for _ in range(9)]

        # test
        # self.principas_values = self.load_plane_grid(num_grid)
        self.principas_values = self.load_test_grid(num_grid)

        self.values_qst = copy.deepcopy(self.principas_values)
        self.values_ans = copy.deepcopy(self.principas_values)
        if abs(int(num_grid ** .5) ** 2 - num_grid) < 1e-6:
            root_num = int(num_grid ** .5)
            self.block_def = [[{(j + root_num * k, i + root_num * l)
                                for i in range(root_num)
                                for j in range(root_num)}
                                for k in range(root_num)]
                                for l in range(root_num)]
        else:
            self.block_def = []
        self.requirements = dict()
        self.err_requirments = dict()
        self.coords_err = None
        self.coords_input = set()
        self.coords_qst = self._find_coords_qst()
        self._solver = None

    def _find_coords_qst(self):
        coords_qst = set()
        for x in range(self.num_grid):
            for y in range(self.num_grid):
                if self.values_qst[y][x] != 0:
                    coords_qst.add((x, y))
        return coords_qst

    def is_all_zero(self):
        if self.coords_qst:
            return False

        return True

    def _load_values(self):
        pass

    def set_solver(self, solver):
        self._solver = solver

    def set_requirements(self, requirment, contents=None, err_tmp=None):
        if requirment == None:
            self.requirements = dict()

        if contents == False:
            del self.requirements[requirment]
            del self.err_requirments[requirment]
            print('grid,set_requirments  削除')
            print('grid,set_requirments  self.requirments', self.requirements)
        else:
            self.requirements[requirment] = contents
            if err_tmp:
                self.err_requirments[requirment] = err_tmp

        self.re_solve()


    def set_values(self, coords_and_n):
        """
            {coord, new_n}  -> value を変更する
            0ならinputからはずす．それ以外は追加．
        """
        for coord, n in coords_and_n:
            self.values_qst[coord[1]][coord[0]] = n
            if n == 0:
                self.coords_qst.remove((coord))
                self.coords_input.discard((coord))
            elif n == self.principas_values[coord[1]][coord[0]]:
                self.coords_qst.add((coord))
                self.coords_input.discard((coord))
            else:
                self.coords_qst.add((coord))
                self.coords_input.add((coord))
        self.re_solve()

    def re_solve(self):
        self._solver.update()

    # テスト用
    def load_plane_grid(self, num):
        values=   [[0 for _ in range(num)] for _ in range(num)]
        return values

    def load_test_grid(self, num_grid):
        values=   [
            [0, 0, 0, 0, 0, 0, 3, 0, 0],
            [0, 0, 0, 0, 0, 0, 9, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 4],
            [0, 0, 0, 5, 0, 8, 0, 0, 6],
            [0, 0, 0, 0, 0, 0, 0, 9, 0],
            [0, 0, 0, 7, 0, 2, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 6, 7],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 5, 0, 0]
        ]
        return values


class NormalGrid(Grid):
    def __init__(self, num):
        super().__init__
        self.num_grid = int(num ** 0.5)
        if self.num_grid ** 2 != num:
            raise ValueError('平方数じゃない！')

    def _load_values(self):
        values=   [
            [0, 3, 0, 0, 0, 0, 0, 0, 0],
            [0, 3, 0, 0, 0, 0, 0, 0, 0],
            [0, 3, 0, 0, 0, 0, 0, 0, 0],
            [0, 3, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0]
        ]
        return values

        # 未実装
        return load_by_camera(self.nums)


class Grid16(Grid):
    def __init__(self):
        super().__init__()
        self.nums = 4

    def _load_values(self):
        values = [
            [],
            [],
            [],
            [],
            [],
            [],
            [],
            [],
            [],
            [],
            []
        ]
        return values
        # 未実装
        return load__by_camera(self.nums)


class GridJigZag(Grid):
    def __init__(self):
        super().__init__()
        self.nums = 9

    def _load_values(self):
        values =   [
            [5, 1, 0, 0, 7, 1, 0, 0, 2],
            [6, 0, 0, 1, 9, 5, 0, 0, 0],
            [0, 9, 8, 0, 0, 0, 0, 6, 0],
            [8, 0, 0, 0, 6, 0, 0, 0, 3],
            [4, 0, 0, 8, 0, 3, 0, 0, 1],
            [7, 0, 0, 1, 2, 0, 0, 0, 6],
            [0, 6, 0, 0, 0, 0, 2, 8, 0],
            [0, 0, 0, 4, 1, 9, 0, 2, 5],
            [0, 0, 0, 0, 4, 0, 0, 0, 0]
        ]
        return values

    def block_numbers(self, row, col):
        pass
