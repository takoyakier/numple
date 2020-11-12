# coding=utf-8

from abc import ABCMeta, abstractmethod
import copy

from traitlets import directional_link

from numplesolver.views import gui

class Command(metaclass=ABCMeta):
    ax_values = {}
    ax = None
    coord_qst = set()
    coord_self = set()

    @abstractmethod
    def excute(self):
        pass

    @abstractmethod
    def unexcute(self):
        pass


class CompositeCommand(Command):
    """
        window の各マスと ax.text をつなげる．
        values (クラス変数) に格納
    """
    grid = None

    def __init__(self, grid):
        self.history = []
        self.shower = None
        CompositeCommand.grid = grid

    def append_cmd(self, cmd):
        self.history.append(copy.deepcopy(cmd))

    def excute(self, cmd):
        if cmd.excute():
            self.append_cmd(cmd)
            self.update_show()

    def unexcute(self):
        if self.history == []:
            print('none')
            return
        self.history.pop().unexcute()
        self.update_show()

    def set_shower(self, shower):
        self.shower = shower

    def update_show(self):
        self.shower.update(self.grid)


class AllDel(Command):
    def __init__(self):
        self.pre_values = 0
        self.inputers = list()
        self.pre_requirments = copy.deepcopy(CompositeCommand.grid.requirements)

    def excute(self):
        grid = CompositeCommand.grid
        if grid.is_all_zero() and grid.requirements == dict():
            return
        for x in range(grid.num_grid):
            for y in range(grid.num_grid):
                inputer = InputNum((x, y), 0)
                if inputer.excute():
                    self.inputers.append(inputer)
        CompositeCommand.grid.set_requirements(None)
        return True

    def unexcute(self):
        for inputer in self.inputers:
            inputer.unexcute()
        CompositeCommand.grid.requirements = copy.deepcopy(self.pre_requirments)


class InputNum(Command):
    def __init__(self, coord, n):
        self.coord = coord
        self.new_n = int(n)
        self.pre_valuse_qst = None
        self.pre_n = None

    def excute(self):
        values = CompositeCommand.grid.values_qst
        self.pre_n = CompositeCommand.grid.values_qst[self.coord[1]][self.coord[0]]
        if self.pre_n == self.new_n:
            return False

        self.pre_valuse_qst = values
        CompositeCommand.grid.set_values({(tuple(self.coord), int(self.new_n))})
        return True

    def unexcute(self):
        CompositeCommand.grid.set_values([[tuple(self.coord), int(self.pre_n)]])

class SetRequirments(Command):
    def __init__(self, requirement, coords=None, direction=None):
        self.requirement = requirement
        self.coords = coords
        self.direction = direction

    def excute(self):
        if self.requirement in {'diagonal'}:
            if self.requirement in CompositeCommand.grid.requirements:
                del CompositeCommand.grid.requirements[self.requirement]
            else:
                CompositeCommand.grid.requirements[self.requirement] = True
            return True

        if self.requirement in {'inequality'}:
            err_tmp = {'vertical': set(), 'horizontal': set()}
            if not 'inequality' in CompositeCommand.grid.requirements:
                content = {'vertical': dict(), 'horizontal': dict()}
            else:
                content = CompositeCommand.grid.requirements['inequality']

            if self.direction in {'up', 'down'}:
                if self.direction == 'up':
                    if self.coords[1] == 0:
                        return False
                    coord_sign = (self.coords[0], self.coords[1] - 1)
                if self.direction =='down':
                    if self.coords[1] == 8:
                        return False
                    coord_sign = tuple(self.coords)
                if coord_sign in content['vertical'] and\
                        self.direction == content['vertical'][coord_sign]:
                    print('cmd,SetRequiremtns,  同じ内容なのでdelする', [coord_sign], content['vertical'][coord_sign])
                    print('cmd,SetRequirments, delする前', CompositeCommand.grid.requirements['inequality'])
                    del content['vertical'][coord_sign]
                    print('cmd,SetRequirments, delした後', CompositeCommand.grid.requirements['inequality'])
                    if len(content['vertical']) == 0 and len(content['horizontal']) == 0:
                        print('cmd, SetRequiremnts,  何もないので Falseをセットしてdel')
                        CompositeCommand.grid.set_requirements('inequality', False)
                        return True
                else:
                    content['vertical'][coord_sign] = self.direction
                print('cmd,SetRequirmetns  gridにrequireをセット', content)
                CompositeCommand.grid.set_requirements('inequality', content, err_tmp)
                return True
            else:
                if self.direction == 'left':
                    if self.coords[0] == 0:
                        return False
                    coord_sign = (self.coords[0] - 1, self.coords[1])
                elif self.direction == 'right':
                    if self.coords[0] == 8:
                        return False
                    coord_sign = tuple(self.coords)
                if coord_sign in content['horizontal'] and \
                        self.direction == content['horizontal'][coord_sign]:
                    del content['horizontal'][coord_sign]
                    if len(content['vertical']) == 0 and len(
                            content['horizontal']) == 0:
                        CompositeCommand.grid.set_requirements('inequality', False)
                        return True
                else:
                    content['horizontal'][coord_sign] = self.direction
                CompositeCommand.grid.set_requirements('inequality', content, err_tmp)
                return True


        return False

    def unexcute(self):
        print('undo まだ書いてないよ', self.requirement)
