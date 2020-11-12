# coding=utf-8
""" Guraphical Unter Interface of numplesolver """

import copy
import matplotlib.pyplot as plt
import matplotlib.collections as mc
import math
import sys

from numplesolver.controller import cmd


class Window(object):
    """
        grid を表示する
        grid を変更する
    """
    def __init__(self, commander):
        self.num_grid = None
        self.square_coord = [None, None]
        self.commander = commander
        self.show_values = dict()
        self.show_inequality_sign = {'vertical': dict(), 'horizontal': dict()}
        self.make_new_grid = False
        self.fig = None
        self.ax = None
        self.surround, = None,

    def flush(self):
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()

    def press_key(self, event):
        if event.key in {'up', 'down', 'left', 'right'}:
            self.move_square_coord(event.key)
            self.update_square()
            return

        if event.key in {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
                         ' ', 'backspace'}:
            if event.key in {' ', 'backspace'}:
                event.key = '0'
            self.update_square()
            self.commander.excute(cmd.InputNum(self.square_coord, event.key))
            return

        if event.key in {'n'}:
            print('gui, press_key   全部消去')
            self.commander.excute(cmd.AllDel())
            return

        if event.key == 'cmd+z':
            self.commander.unexcute()
            return

        if event.key == 'x':
            self.commander.excute(cmd.SetRequirments('diagonal'))
            return

        if event.key in {'alt+up', 'alt+down', 'alt+left', 'alt+right'}:
            direction = event.key[4:]
            self.commander.excute(cmd.SetRequirments('inequality', self.square_coord, direction))
            self.move_square_coord(direction)
            self.update_square()
            self.flush()
            return

        if event.key in {'cmd+n'}:
            def press_key(event):
                if event.key in {'1', '2', '3', '4', '5', '6', '7', '8', '9', '0'}:
                    self.make_new_grid *= 10
                    self.make_new_grid %= 100
                    self.make_new_grid += int(event.key)
                elif event.key in {'backspace', ' '}:
                    self.make_new_grid //= 10
                elif event.key == 'enter':
                    plt.clf()
                    if self.make_new_grid == 0:
                        plt.close()
                    elif self.make_new_grid > 25:
                        print('25まで')
                        plt.close()
                    else:
                        plt.close(fig='all')
                elif event.key in {'cmd+n'}:
                    plt.clf()
                    plt.close()
                num_place.set_text(self.make_new_grid)
                fig.canvas.draw()
                fig.canvas.flush_events()
            fig = plt.figure(figsize=(2.5,1))
            self.make_new_grid = 0
            fig.canvas.mpl_connect('key_press_event', press_key)
            ax = fig.add_subplot(111)
            ax.text(0, 0.5, 'Input num of grid: ')
            num_place = ax.text(0.8, 0.5, '', fontsize=20)
            ax.tick_params(bottom=False, left=False)
            ax.tick_params(labelbottom=False, labelleft=False)
            plt.gca().spines['right'].set_visible(False)
            plt.gca().spines['top'].set_visible(False)
            plt.gca().spines['left'].set_visible(False)
            plt.gca().spines['bottom'].set_visible(False)
            plt.show()
            return

        # test
        if event.key == 'r':
            print(self.test)

        else:
            print(event.key)

    def mouse_move(self, event):
        if not event.inaxes:
            return

        x = math.floor(event.xdata)
        y = self.num_grid - 1 - math.floor(event.ydata)
        if x != self.square_coord[0] or y != self.square_coord[1]:
            self.square_coord = [x, y]
            self.update_square()


    def move_square_coord(self, direction):
        if direction == 'up':
            self.square_coord[1] -= 1
            self.square_coord[1] %= self.num_grid
            return
        if direction == 'down':
            self.square_coord[1] += 1
            self.square_coord[1] %= self.num_grid
            return
        if direction == 'right':
            self.square_coord[0] += 1
            self.square_coord[0] %= self.num_grid
            return
        if direction == 'left':
            self.square_coord[0] -= 1
            self.square_coord[0] %= self.num_grid
            return

    def set_grid(self, num_grid):
        self.num_grid = num_grid
        self.fig = plt.figure(figsize=(0.5 * num_grid, 0.5 * num_grid))
        self.ax = self.fig.add_subplot(111,
                                       aspect='1', xlim=(0, num_grid), ylim=(0,num_grid))
        self.set_lines(num_grid)
        self.surround, = plt.plot([], [], lw=3)
        self.fig.canvas.mpl_connect('motion_notify_event', self.mouse_move)
        self.fig.canvas.mpl_connect('key_press_event', self.press_key)
        for x in range(num_grid):
            for y in range(num_grid):
                self.show_values[(x, y)] = self.ax.text(x + 0.25, num_grid - 1 - y + 0.2,
                                                        '', fontsize=20)
        for i in range(num_grid):
            for j in range(num_grid - 1):
                self.show_inequality_sign['vertical'][(i, j)] = \
                    self.ax.text(i + 0.3, num_grid - 1 - j, '', fontsize=14, rotation='vertical')
                self.show_inequality_sign['horizontal'][(j, i)] = \
                    self.ax.text(j + 0.85, num_grid- 1 - i + 0.35, '', fontsize=14)
        self.square_coord = [num_grid // 2,
                             num_grid // 2]




    def set_lines(self, num):
        root_num = num ** .5
        lines = [[[i, 0.2], [i, num - 0.2]] for i in range(1, num) if (i % root_num) != 0]
        lines += [[[0.2, i], [num - 0.2, i]] for i in range(1, num) if (i % root_num) != 0]
        lc = mc.LineCollection(lines, color='k', linewidths=0.5)
        self.ax.add_collection(lc)

        if abs(int(root_num) ** 2 - num) < 1e-6:
            bold_lines = [[[root_num * i, 0.1], [root_num * i, num - 0.1]] for i in range(1, int(root_num))]
            bold_lines += [[[0.1, root_num * i], [num - 0.1, root_num * i, ]] for i in range(1, int(root_num))]
            lc_bold = mc.LineCollection(bold_lines, color='k', linewidths=2)
            self.ax.add_collection(lc_bold)

        self.ax.tick_params(bottom=False, left=False)
        self.ax.tick_params(labelbottom=False, labelleft=False)

    def show(self, grid):
        self.update(grid)
        # todo: delete
        self.test = grid.requirements
        plt.show()

        return self.make_new_grid

    def update_square(self):
        self.surround.set_data([self.square_coord[0], self.square_coord[0], self.square_coord[0] + 1, self.square_coord[0] + 1, self.square_coord[0]],
                               [self.num_grid - 1 - self.square_coord[1], self.num_grid - 1 - self.square_coord[1] + 1, self.num_grid - 1 - self.square_coord[1] + 1, self.num_grid - 1 - self.square_coord[1], self.num_grid - 1 - self.square_coord[1]])

        self.flush()

    def update(self, grid):
        for y, rows in enumerate(grid.values_ans):
            for x, n in enumerate(rows):
                if n == 0:
                    n = ''
                if (x, y) in grid.coords_err:
                    self.show_values[(x, y)].set_text(str(n))
                    self.show_values[(x, y)].set_color('#ff0000')
                elif (x, y) in grid.coords_input:
                    self.show_values[(x, y)].set_text(str(n))
                    self.show_values[(x, y)].set_color('#8a2be2')
                elif (x, y) in grid.coords_qst:
                    self.show_values[(x, y)].set_text(str(n))
                    self.show_values[(x, y)].set_color('#000000')
                else:
                    self.show_values[(x, y)].set_text(str(n))
                    self.show_values[(x, y)].set_color('#00ff00')

        for i in range(self.num_grid):
            for j in range(self.num_grid - 1):
                self.show_inequality_sign['vertical'][(i, j)].set_text('')
                self.show_inequality_sign['horizontal'][(j, i)].set_text('')
                if 'inequality' in grid.requirements:
                    if (i, j) in grid.requirements['inequality']['vertical']:
                        if grid.requirements['inequality']['vertical'][(i, j)] == 'up':
                            self.show_inequality_sign['vertical'][(i, j)].set_text('>')
                        else:
                            self.show_inequality_sign['vertical'][(i, j)].set_text('<')
                        if (i, j) in grid.err_requirments['inequality']['vertical']:
                            self.show_inequality_sign['vertical'][(i, j)].set_color('#ff0000')
                        else:
                            self.show_inequality_sign['vertical'][(i, j)].set_color('#000000')
                    else:
                        self.show_inequality_sign['vertical'][(i, j)].set_text('')

                    if (j, i) in grid.requirements['inequality']['horizontal']:
                        if grid.requirements['inequality']['horizontal'][(j, i)] == 'left':
                            self.show_inequality_sign['horizontal'][(j, i)].set_text('<')
                        else:
                            self.show_inequality_sign['horizontal'][(j, i)].set_text('>')
                        if (j, i) in grid.err_requirments['inequality']['horizontal']:
                            self.show_inequality_sign['horizontal'][(j, i)].set_color('#ff0000')
                        else:
                            self.show_inequality_sign['horizontal'][(j, i)].set_color('#000000')
                    else:
                        self.show_inequality_sign['horizontal'][(j, i)].set_text('')

        self.flush()
