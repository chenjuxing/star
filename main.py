import time
import os
import random
import tkinter
import threading


# 生命地图保存模块
class MapStorage:
    length = 100
    width = 100
    map = []

    def __init__(self, length, width):
        self.length = length
        self.width = width
        # 初始化图
        for i in range(0, length + 2):
            self.map.append([])
            for j in range(0, width + 2):
                if random.random() > 0.8:
                    self.map[i].append(1)
                else:
                    self.map[i].append(0)


# 生命逻辑控制模块
class LifeChanger:

    def life_change(self, map0, x, y):
        num = 0
        for i in range(x - 1, x + 2):
            for j in range(y - 1, y + 2):
                if map0.map[i][j] == 1 and not (x == i and y == j):
                    num += 1
        if num < 2 or num > 3:
            return 0
        elif num == 2:
            return map0.map[x][y]
        elif num == 3:
            return 1


# 生命周期控制模块
class LifeCycleController:
    cycle_time = 0.5  # 一次演变周期的时间
    temp_map = []  # 临时存图变量

    def __init__(self, cycle_time):
        self.cycle_time = cycle_time

    def cycle(self, map0):
        # 初始化临时图
        for i in range(0, map0.length + 2):
            self.temp_map.append([])
            for j in range(0, map0.width + 2):
                self.temp_map[i].append(0)
        # 计算生命情况
        changer = LifeChanger()
        for i in range(1, map0.length + 1):
            for j in range(1, map0.width + 1):
                self.temp_map[i][j] = changer.life_change(map0, i, j)
        # 更新地图
        for i in range(1, map0.length + 1):
            for j in range(1, map0.width + 1):
                map0.map[i][j] = self.temp_map[i][j]

    def run_cycle(self, map0):
        while True:
            time.sleep(self.cycle_time)
            os.system('clear')
            self.cycle(map0)
            for i in range(1, map0.length + 1):
                for j in range(1, map0.width + 1):
                    if map0.map[i][j] == 1:
                        print('#', end='')
                    else:
                        print(' ', end='')
                print('')

    # GUI输出
    class UpdateThread(threading.Thread):

        generation = 0

        def __init__(self, ref, map0):
            threading.Thread.__init__(self)
            self.ref = ref
            self.map0 = map0

        # 用于画布的刷新
        def run(self):
            while True:
                time.sleep(1)
                self.generation += 1
                print('generation ', self.generation)
                # 内存中数据更新
                self.ref.cycle(self.map0)
                # 删除原图案
                canvas.delete('life')
                cell_size = 20
                for i in range(0, self.map0.length + 2):
                    for j in range(0, self.map0.width + 2):
                        if self.map0.map[i][j] == 1:
                            canvas.create_rectangle(i * cell_size, j * cell_size,
                                                    (i + 1) * cell_size, (j + 1) * cell_size, fill='blue',
                                                    outline='blue', tag='life')
                        else:
                            canvas.create_rectangle(i * cell_size, j * cell_size,
                                                    (i + 1) * cell_size, (j + 1) * cell_size, fill='black',
                                                    outline='black', tag='life')

    def run_cycle_gui(self, map0):
        # 主框架
        # global main_frame
        main_frame = tkinter.Tk()
        main_frame.title('Game Of Life  --by cl&cjx')
        main_frame.geometry('600x500+400+200')
        # 画布
        cell_size = 20
        global canvas
        canvas = tkinter.Canvas(main_frame, bg='black', width=cell_size * map0.width,
                                height=cell_size * map0.length)
        # 进入启动循环
        for i in range(0, map0.length + 2):
            for j in range(0, map0.width + 2):
                if map0.map[i][j] == 1:
                    canvas.create_rectangle(i * cell_size, j * cell_size,
                                            (i + 1) * cell_size, (j + 1) * cell_size, fill='blue', outline='blue', tag='life')
                else:
                    canvas.create_rectangle(i * cell_size, j * cell_size,
                                            (i + 1) * cell_size, (j + 1) * cell_size, fill='black', outline='black', tag='life')
        canvas.pack()  # 放到主窗口
        # 循环代码
        self.UpdateThread(self, map0).start()
        main_frame.mainloop()


# 主函数
if __name__ == "__main__":
    a = 30
    b = 30
    world = MapStorage(a, b)
    controller = LifeCycleController(0.2)
    controller.run_cycle_gui(world)
