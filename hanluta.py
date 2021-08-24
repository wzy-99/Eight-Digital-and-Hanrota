class Hanluota:
    def __init__(self, src, dst, n):
        self.src = src
        self.dst = dst
        self.n = n
        self.hierarchy = [[] for _ in range(n)]
        print('The process of the problem:')
        self.hanluota(self.src, self.dst, self.n)
        print('The hierarchy struct of question:')
        for i, h in enumerate(self.hierarchy[1:]):
            print(str(i + 1) + 'layer:')
            print(h)
        print(str(n) + 'layer:')
        print([self.src, self.dst])

    def hanluota(self, src, dst, n):
        # 如果到最底层了，那么停止
        if n == 1:
            # self.hierarchy[n - 1].append([src, dst])
            print('from', src, 'to', dst)
            return

        # 找到一个临时柱子，用于存放挪动的盘子
        col = [1, 2, 3]
        for i, t in enumerate(col):
            if t in src[:n] or t in dst[:n]:
                col[i] = 0
        temp = sum(col)
        temp = [temp for _ in range(n - 1)]

        # 第一步
        self.hierarchy[n - 1].append([src, temp + src[n - 1:]])
        self.hanluota(src, temp + src[n - 1:], n - 1)

        # 第二步
        self.hierarchy[n - 1].append([temp + src[n - 1:], temp + dst[n - 1:]])
        print('from', temp + src[n - 1:], 'to', temp + dst[n - 1:])

        # 第三步
        self.hierarchy[n - 1].append([temp + dst[n - 1:], dst])
        self.hanluota(temp + dst[n - 1:], dst, n - 1)


Hanluota([1, 1, 1, 1], [3, 3, 3, 3], 4)

input('return')