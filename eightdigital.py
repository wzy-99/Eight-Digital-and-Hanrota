import copy
import matplotlib.pyplot as plt
import numpy as np

H, W = 3, 3
SOURCE = [[2, 8, 3], [1, 6, 4], [7, 0, 5]]
TARGET = [[1, 2, 3], [8, 0, 4], [7, 6, 5]]

fig = plt.figure(1)

class EightDigtal:
    def __init__(self, source, target, cost_fuc):
        self.source = source
        self.target = target
        self.cost_func = cost_fuc
        self.open = []
        self.close = []
        self.result = False
        self.index = 0

        # 把S放入OPEN表，计算估价函数
        root_node = {}
        root_node['from'] = -1
        root_node['depth'] = 0
        root_node['cost'] = cost_fuc(self.source, self.target, root_node['depth'])
        root_node['state'] = self.source
        self.open.append(root_node)

    def search(self):
        # 判断OPEN表是否为空表
        while len(self.open):
            # 如果不是空表
            # 选取OPEN表中f值最小的节点i放入CLOSED表
            node = self.open.pop(0)
            node['id'] = self.index
            self.index += 1
            self.close.append(node)
            # 判断是否为目标节点
            if node['state'] == self.target:
                # 如果是目标节点
                # 则成功
                self.result = True
                return self
            else:
                # 如果不是目标节点
                # 扩展节点，得后继节点节点，计算节点的代价，提供返回父节点的指针
                self.expand(node, self.cost_func)
                # 利用代价对OPEN表重新排序，调整亲子关系及指针
                self.rearragne()
        # 如果是空表
        # 则失败
        self.result = True
        return self

    def expand(self, parent_node, cost_func):
        """
            节点扩展
        """
        state = parent_node['state']

        # h, w = state.shape
        h, w = H, W

        # 找到空格的位置
        break_flag = False
        for i in range(0, h):
            for j in range(0, w):
                if state[i][j] == 0:
                    break_flag = True
                    break
            if break_flag:
                break
        
        new_nodes = []
        
        # 如果空格可以上移
        if i - 1 >= 0:
            new_state = copy.deepcopy(state)
            new_state[i - 1][j] = state[i][j]
            new_state[i][j] = state[i - 1][j]
            # 计算新节点
            new_node = {}
            new_node['state'] = new_state
            new_node['from'] = parent_node['id']
            new_node['depth'] = parent_node['depth'] + 1
            new_node['cost'] = cost_func(new_state, self.target, new_node['depth'])
            new_nodes.append(new_node)
        # 如果空格可以下移
        if i + 1 <= h - 1:
            new_state = copy.deepcopy(state)
            new_state[i + 1][j] = state[i][j]
            new_state[i][j] = state[i + 1][j]
            new_node = {}
            new_node['state'] = new_state
            new_node['from'] = parent_node['id']
            new_node['depth'] = parent_node['depth'] + 1
            new_node['cost'] = cost_func(new_state, self.target, new_node['depth'])
            new_nodes.append(new_node)
        # 如果空格可以左移
        if j - 1 >= 0:
            new_state = copy.deepcopy(state)
            new_state[i][j - 1] = state[i][j]
            new_state[i][j] = state[i][j - 1]
            new_node = {}
            new_node['state'] = new_state
            new_node['from'] = parent_node['id']
            new_node['depth'] = parent_node['depth'] + 1
            new_node['cost'] = cost_func(new_state, self.target, new_node['depth'])
            new_nodes.append(new_node)
        # 如果空格可以右移
        if j + 1 <= h - 1:
            new_state = copy.deepcopy(state)
            new_state[i][j + 1] = state[i][j]
            new_state[i][j] = state[i][j + 1]
            new_node = {}
            new_node['state'] = new_state
            new_node['from'] = parent_node['id']
            new_node['depth'] = parent_node['depth'] + 1
            new_node['cost'] = cost_func(new_state, self.target, new_node['depth'])
            new_nodes.append(new_node)

        for new_node in new_nodes:
            existed_flag, old_node = self.exist(new_node)
            # 如果新节点已在CLOSE表中
            if existed_flag == 1:
                # 如果新节点的cost比之前要小
                if new_node['cost'] < old_node['cost']:
                    # 从CLOSE中删除旧节点
                    for i in range(len(self.close)):
                        if self.close[i]['id'] == old_node['id']:
                            self.close.remove(i)
                            break
                    # 将新节点加入OPEN表中
                    self.open.append(new_node)
            # 如果新节点已在OPEN表中
            elif existed_flag == 2:
                # 如果新节点的cost比之前要小
                if new_node['cost'] < old_node['cost']:
                    # 更新旧节点
                    old_node['from'] = new_node['from']
                    old_node['cost'] = new_node['cost']
                    old_node['depth'] = new_node['depth']
            # 如果新节点不存在
            elif existed_flag == 0:
                # 直接加入到OPEN表中
                self.open.append(new_node)


    def rearragne(self):
        """
            OPEN表重排
        """
        new_open = []

        while len(self.open):
            min_cost = 10000000

            # 查找最小代价的节点
            for idx in range(len(self.open)):
                if self.open[idx]['cost'] < min_cost:
                    min_cost = self.open[idx]['cost']
                    min_cost_idx = idx
            
            min_cost_node = self.open.pop(min_cost_idx)

            new_open.append(min_cost_node)
    
        self.open = new_open

    def exist(self, node):
        """
            判断存在
        """
        state = node['state']

        # h, w = state.shape
        h, w = H, W

        for visist_node in self.close:
            visist = visist_node['state']
            different = False
            for i in range(h):
                for j in range(w):
                    if visist[i][j] != state[i][j]:
                        different = True
                        break
                # 只要有一处不同则停止判断
                if different:
                    break
            # 如果完全相同，则返回存在
            if different is False:
                return 1, visist_node
        
        for visist_node in self.open:
            visist = visist_node['state']
            different = False
            for i in range(h):
                for j in range(w):
                    if visist[i][j] != state[i][j]:
                        different = True
                        break
                # 只要有一处不同则停止判断
                if different:
                    break
            # 如果完全相同，则返回存在
            if different is False:
                return 2, visist_node
        
        return 0, None

    def print(self, title):
        print('*' * 45 + '\n' + ' ' * 15 + title + '\n' + '*' * 45)
        print('ID\tfrom\t\t\t\t\t\t\tstate\t\t\t\t\t\t\tcost\tdepth\t')
        for node in self.close:
            print('{:2d}\t{:2d}\t{}\t{:2d}\t{:2d}\t'.format(node['id'], node['from'], node['state'], node['cost'], node['depth']))
        return self
        
    def show(self, title):
        show_state = []
        froms = []
        for node in self.close:
            froms.append(node['from'])
        froms.append(self.close[-1]['from'])
        for node in self.close:
            if node['id'] in froms:
                show_state.append(node['state'])
        show_state.append(self.target)
        fig.canvas.set_window_title(title)
        for state in show_state:
            mat = np.array(state)
            plt.clf()
            plt.matshow(mat, fignum=0)
            for i in range(mat.shape[0]):
                for j in range(mat.shape[1]):
                    plt.text(x=j, y=i, s=mat[i, j])
            plt.pause(1)
        return self

def simple_cost(source_state, target_state, depth):
    # 最简单的估价函数：取一格局与目的格局相比，其位置不符的棋子数目

    # h, w = target_state.shape
    h, w = H, W

    cost = 0

    for i in range(0, h):
        for j in range(0, w):
            if target_state[i][j] != 0:
                if source_state[i][j] != target_state[i][j]:
                    cost += 1
    
    cost += depth

    return cost

def distance_cost(source_state, target_state, depth):
    # 各棋子移到目的位置所需移动距离的总和

    # h, w = target_state.shape
    h, w = H, W

    cost = 0

    for i in range(0, h):
        for j in range(0, w):
            if source_state[i][j] != 0:
                for m in range(0, h):
                    for n in range(0, w):
                        if target_state[m][n] == source_state[i][j]:
                            cost += abs(m - i) + abs(n - j)

    cost += depth

    return cost

def inserve_cost(source_state, target_state, depth):
    # 对每一对逆转棋子乘以一个倍数

    # h, w = target_state.shape
    h, w = H, W

    cost = 0

    source_array = []

    p = 4

    for i in range(0, w):
        source_array.append(source_state[0][i])
    for i in range(1, h - 1):
        source_array.append(source_state[i][w - 1])
    for i in range(w - 1, -1, -1):
        source_array.append(source_state[h - 1][i])
    for i in range(h - 2, 0, -1):
        source_array.append(source_state[i][0])
    source_array.append(source_state[0][0])

    for i in range(len(source_array) - 1):
        if source_array[i] > source_array[i + 1]:
            cost += p

    cost += depth

    return cost

def mixed_cost(source_state, target_state, depth):
    # 将位置不符棋子数目的总和与3倍棋子逆转数目相加
    
    h, w = H, W
    
    cost = 0

    source_array = []

    p = 3

    for i in range(0, w):
        source_array.append(source_state[0][i])
    for i in range(1, h - 1):
        source_array.append(source_state[i][w - 1])
    for i in range(w - 1, -1, -1):
        source_array.append(source_state[h - 1][i])
    for i in range(h - 2, 0, -1):
        source_array.append(source_state[i][0])
    source_array.append(source_state[0][0])

    for i in range(len(source_array) - 1):
        if source_array[i] > source_array[i + 1]:
            cost += p

    for i in range(0, h):
        for j in range(0, w):
            if target_state[i][j] != 0:
                if source_state[i][j] != target_state[i][j]:
                    cost += 1

    cost += depth

    return cost

def my_cost(source_state, target_state, depth):
    # 将位置不符棋子数目的总和与3倍棋子逆转数目相加再加上各棋子移到目的位置所需移动距离的总和
    
    h, w = H, W
    
    cost = 0

    source_array = []

    p = 3

    for i in range(0, w):
        source_array.append(source_state[0][i])
    for i in range(1, h - 1):
        source_array.append(source_state[i][w - 1])
    for i in range(w - 1, -1, -1):
        source_array.append(source_state[h - 1][i])
    for i in range(h - 2, 0, -1):
        source_array.append(source_state[i][0])
    source_array.append(source_state[0][0])

    for i in range(len(source_array) - 1):
        if source_array[i] > source_array[i + 1]:
            cost += p

    for i in range(0, h):
        for j in range(0, w):
            if target_state[i][j] != 0:
                if source_state[i][j] != target_state[i][j]:
                    cost += 1
    
    for i in range(0, h):
        for j in range(0, w):
            if source_state[i][j] != 0:
                for m in range(0, h):
                    for n in range(0, w):
                        if target_state[m][n] == source_state[i][j]:
                            cost += abs(m - i) + abs(n - j)

    cost += depth

    return cost

EightDigtal(SOURCE, TARGET, simple_cost).search().print('simple cost').show('simple cost')
EightDigtal(SOURCE, TARGET, distance_cost).search().print('distance cost').show('distance cost')
EightDigtal(SOURCE, TARGET, inserve_cost).search().print('inserve cost').show('inserve cost')
EightDigtal(SOURCE, TARGET, mixed_cost).search().print('mixed cost').show('mixed cost')
EightDigtal(SOURCE, TARGET, my_cost).search().print('my cost').show('my cost')