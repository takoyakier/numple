# SOLVER 1.0
# no assamptions

import copy
import numplesolver.models.grids


class Solver(object):
    """
        grid の変更は grid.set_value で行いたい．(window に通知するので)
        そのため，_solver 内で帰るための self.value を準備，最後にまとめて grid.set_value
    """
    def __init__(self, grid):
        self.grid = grid
        self.grid.coords_err = self._find_errors()
        self.opts = self._find_opts()
        self.test = (0,0)
        self.solve()

    def all_determine(self):
        """
        決まるところはできるだけ決める
        Return:
            何も決まらない:False
            何か決まった:True
        """
        while True:
            determined = self.determine()
            if determined is False:
                determined_something = False
                break
            else:
                coord, num = determined
                self.del_around_opts(coord, num)
                for n in range(1, self.grid.num_grid + 1):
                    if n != num:
                        self.opts[coord].discard(n)
                determined_something = True
        return determined_something

    def block_numbers(self, row, col):
        for row_blocks in self.grid.block_def:
            for belongs_block in row_blocks:
                if (row, col) in belongs_block:
                    return [self.grid.values_qst[y][x] for y, x in belongs_block]
        else:
            return []

    def _comparison_opts(self, coord_small, coord_large):
        anything_deleted = False
        try:
            for n in range(max(self.opts[coord_large]), 10):
                if anything_deleted:
                    self.opts[coord_small].discard(n)
                else:
                    try:
                        self.opts[coord_small].remove(n)
                        anything_deleted = True
                    except:
                        pass

            for n in range(1, min(self.opts[coord_small]) + 1):
                if anything_deleted:
                    self.opts[coord_large].discard(n)
                else:
                    try:
                        self.opts[coord_large].remove(n)
                        anything_deleted = True
                    except:
                        pass
            return anything_deleted
        except:
            return 'error'

    def del_opts(self):
        # 行列箱内でその文字が1つしかない：そのcellの他の文字を消す
        # BOxないに数字が1行しかない:他のBOX内で同列のその数字を消す
        anything_deleted = False
        for n in range(1, self.grid.num_grid + 1):
            for line in range(self.grid.num_grid):
                coords_opts_n = self._find_line_opts_coords_have(n, row=line)
                if coords_opts_n is []:
                    pass
                else:
                    if 1 < len(coords_opts_n) < 4:
                        ys = [xy[1] for xy in coords_opts_n]
                        if (max(ys) <= 2) or (3 <= min(ys) and max(ys) <= 5) or (6 <= min(ys)):
                            if self.del_box(coords_opts_n, n):
                                anything_deleted = True
                coords_opts_n = self._find_line_opts_coords_have(n, col=line)
                if coords_opts_n is []:
                    pass
                else:
                    if 1 < len(coords_opts_n) < 4:
                        xs = [xy[0] for xy in coords_opts_n]
                        if max(xs) <= 2 or (3 <= min(xs) and max(xs) <= 5) or 6 <= min(xs):
                            if self.del_box(coords_opts_n, n):
                                anything_deleted = True
            if self.grid.block_def:
                for i in range(int(self.grid.num_grid ** .5)):
                    for j in range(int(self.grid.num_grid ** .5)):
                        coords_opts_n = self._find_box_opts_coods_have(n, i, j)
                        if coords_opts_n == []:
                            continue
                        if 1 < len(coords_opts_n) < 4:
                            xs = [xy[0] for xy in coords_opts_n]
                            ys = [xy[1] for xy in coords_opts_n]
                            if xs.count(xs[0]) == len(xs):
                                if self.del_col(coords_opts_n, n):
                                    anything_deleted = True
                            if ys.count(ys[0]) == len(ys):
                                if self.del_row(coords_opts_n, n):
                                    anything_deleted = True

        if 'inequality' in self.grid.requirements:
            for coord_sign, direction in self.grid.requirements['inequality']['vertical'].items():
                if direction == 'up':
                    coord_large = (coord_sign[0], coord_sign[1] + 1)
                    coord_small = coord_sign
                if direction == 'down':
                    coord_large = coord_sign
                    coord_small = (coord_sign[0], coord_sign[1] + 1)
                tmp = self._comparison_opts(coord_small, coord_large)
                if tmp == 'error':
                    self.grid.err_requirments['inequality']['vertical'].add(coord_sign)
                    return False
                if tmp:
                    self.grid.err_requirments['inequality']['vertical'].clear()
                    anything_deleted = True

            for coord_sign, direction in self.grid.requirements['inequality']['horizontal'].items():
                if direction == 'left':
                    coord_small = coord_sign
                    coord_large = (coord_sign[0] + 1, coord_sign[1])
                if direction == 'right':
                    coord_small = (coord_sign[0] + 1, coord_sign[1])
                    coord_large = coord_sign
                tmp = self._comparison_opts(coord_small, coord_large)
                if tmp == 'error':
                    self.grid.err_requirments['inequality']['horizontal'].add(coord_sign)

                    return False
                if tmp:
                    self.grid.err_requirments['inequality']['horizontal'].clear()
                    anything_deleted = True

        return anything_deleted

    def del_around_opts(self, coord, num):
        self.del_row([coord], num)
        self.del_col([coord], num)
        self.del_box([coord], num)

    def del_box(self, coords, num):
        anything_deleted = False
        for row_block in self.grid.block_def:
            for belongs_block in row_block:
                if coords[0] in belongs_block:
                    for around_coord in belongs_block:
                        if not around_coord in coords:
                            try:
                                self.opts[around_coord].remove(num)
                                anything_deleted = True
                            except:
                                pass
        return anything_deleted

    def del_col(self, coords, num):
        x = coords[0][0]
        anything_deleted = False
        for y in range(self.grid.num_grid):
            if (x, y) in self.opts and (x, y) not in coords:
                try:
                    self.opts[(x,y)].remove(num)
                    anything_deleted = True
                except:
                    pass
        return anything_deleted

    def del_row(self, coords, num):
        y = coords[0][1]
        anything_deleted = False
        for x in range(self.grid.num_grid):
            if (x, y) in self.opts and (x, y) not in coords:
                try:
                    self.opts[(x, y)].remove(num)
                    anything_deleted = True
                except:
                    pass
        return anything_deleted

    def determine(self):
        """空欄 cell で opts の中に1つしかないものをvalueに入れる
            lineだけ見て，一つしかないものをvalueにいれる
        Return:
            決まるものがある : coordinate::(x,y), num ::int
            決まるものがない : False
        """
        for coord, nums in self.opts.items():
            x, y = coord
            if len(nums) == 1 and self.grid.values_ans[y][x] == 0:
                self.grid.values_ans[y][x] = list(nums)[0]
                return coord, list(nums)[0]

        for n in range(1, self.grid.num_grid + 1):
            for line in range(self.grid.num_grid):
                coords_opts_n = self._find_line_opts_coords_have(n, row=line)
                if len(coords_opts_n) == 1:
                    x, y = coords_opts_n[0]
                    if self.grid.values_ans[y][x] == 0:
                        self.grid.values_ans[y][x] = n
                        return (x, y), n
                coords_opts_n = self._find_line_opts_coords_have(n, col=line)
                if len(coords_opts_n) == 1:
                    x, y = coords_opts_n[0]
                    if self.grid.values_ans[y][x] == 0:
                        self.grid.values_ans[y][x] = n
                        return (x, y), n

            if self.grid.block_def:
                for i in range(int(self.grid.num_grid ** .5)):
                    for j in range(int(self.grid.num_grid ** .5)):
                        coords_opts_n = self._find_box_opts_coods_have(n, i, j)
                        if len(coords_opts_n) == 1:
                            x, y = coords_opts_n[0]
                            if self.grid.values_ans[y][x] == 0:
                                self.grid.values_ans[y][x] = n
                                return (x, y), n


        else:
            return False

    def _find_errors(self):
        errors = set()
        found_error = errors.add
        for y, rows in enumerate(self.grid.values_qst):
            count_num = rows.count
            for n in range(1, self.grid.num_grid + 1):
                if count_num(n) > 1:
                    for x, num in enumerate(rows):
                        if num == n:
                            found_error((x, y))

        nums = []
        adding = nums.append
        for x in range(self.grid.num_grid):
            nums.clear()
            for y in range(self.grid.num_grid):
                n = self.grid.values_qst[y][x]
                if n in nums and n > 0:
                    found_error((x, y))
                    found_error((x, nums.index(n)))
                else:
                    adding(n)

        root_num = self.grid.num_grid ** .5
        if abs(int(root_num) ** 2 - self.grid.num_grid) < 1e-6:
            root_num = int(root_num)
            for i in range(root_num):
                for j in range(root_num):
                    nums = self.block_numbers(root_num * i, root_num * j)
                    for n in range(1, self.grid.num_grid + 1):
                        if nums.count(n) > 1:
                            for x, y in self.grid.block_def[j][i]:
                                if self.grid.values_qst[y][x] == n:
                                    found_error((x, y))

        return errors

    def _find_opts(self):
        opts = {}
        for y in range(self.grid.num_grid):
            for x in range(self.grid.num_grid):
                if self.grid.values_qst[y][x] == 0:
                    opts[(x,y)] = self._possible_numbers_for_cell(x, y)
                else:
                    opts[(x, y)] = {self.grid.values_qst[y][x]}
        return opts

    def _find_line_opts_coords_have(self, n, row=None, col=None):
        coords = []
        if row == None:
            for row in range(self.grid.num_grid):
                try:
                    if n in self.opts[(row, col)]:
                        coords.append((row, col))
                except:
                    pass
            return coords
        if col == None:
            for col in range(self.grid.num_grid):
                try:
                    if n in self.opts[(row, col)]:
                        coords.append((row, col))
                except:
                    pass
            return coords

    def _find_box_opts_coods_have(self, n, ib, jb):
        coords = []
        for coord_block in self.grid.block_def[jb][ib]:
            if n in self.opts[coord_block]:
                coords.append(coord_block)
        return coords

    def _possible_numbers_for_cell(self, col, row):
        row_numbers = {x for x in self.grid.values_ans[row]}
        col_numbers = {row[col] for row in self.grid.values_ans}
        block_numbers = set(self.block_numbers(row, col))
        return {x for x in range(1, self.grid.num_grid + 1)
            if (x not in row_numbers)
            and (x not in col_numbers)
            and (x not in block_numbers)}


    def solve(self):
        print('----------'*5)
        while True:
            anything_deleted = self.del_opts()
            console.show_all(self.grid, self.opts)
            anything_determined = self.all_determine()
            console.show_all(self.grid, self.opts)

            if anything_deleted or anything_determined:
                pass
            else:
                break

    def update(self):
        self.grid.values_ans = copy.deepcopy(self.grid.values_qst)
        self.grid.coords_err = self._find_errors()
        self.opts = self._find_opts()
        self.solve()


class NormalSolver(Solver):
    def qualify(self, coord, num):
        pass

class ArrowSolver(Solver):
    def __init__(self):
        pass

    def del_opts():
        pass
