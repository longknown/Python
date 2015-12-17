__author__ = 'Thomas'


class Interval:
    __name__ = 'Interval'

    def __init__(self, start=0, end=0):
        self.start = start
        self.end = end

    def __cmp__(self, other):
        if self.start > other.end:
            return 1  # self > other
        elif self.end < other.start:
            return -1  # self < other
        else:
            return 0  # intersect

    def __add__(self, other):  # only fuses intersects
        if self == other:
            start = min(self.start, other.start)
            end = max(self.end, other.end)
            return Interval(start, end)
        else:
            return None

    def __len__(self):
        return self.end-self.start

    def __contains__(self, item):  # self covers the item interval
        if item.start >= self.start and item.end <= self.end:
            return True
        else:
            return False

    def print_interval(self):
        print '['+str(self.start)+', '+str(self.end)+']'


class IntervalSet:
    __name__ = 'IntervalSet'

    def __init__(self, other=None):  # other is another Interval type
        if other is None:
            self.items = []  # items is a list of class Interval
            self.number = 0
            self.lower = 0
            self.upper = 0
        elif other.__name__ == 'Interval':
            self.items = [other]
            self.number = 1
            self.lower = other.start
            self.upper = other.end
        elif other.__name__ == 'IntervalSet':
            self.items = []
            for i in other.items:
                temp = Interval(i.start, i.end)
                self.items.append(temp)
            self.number = other.number
            self.lower = other.lower
            self.upper = other.upper

    def __getitem__(self, key):
        if isinstance(key, slice):
            return [self.items[i] for i in xrange(*key.indices(self.number))]
        elif isinstance(key, int):
            return self.items[key]
        else:
            raise TypeError, 'Invalid argument type.'

    def print_intervalset(self):
        printout = ''
        if self.number != 0:
            for item in self.items:
                printout += '['+str(item.start)+', '+str(item.end)+'] '
        print printout

    def insert(self, ins_item, pos=0):  # you can specify the starting position to perform insertion
        fuse_start = pos-1  # fuse_start and fuse_end represent the intervals that intersect with ins_item
        fuse_end = pos
        for i in xrange(pos, self.number):
            item = Interval(self.items[i].start, self.items[i].end)
            if item > ins_item:
                break
            elif item < ins_item:
                    fuse_start += 1
                    fuse_end += 1
            else:
                ins_item += self.items[i]
                fuse_end += 1
                continue
        self.items = self.items[:fuse_start+1] + [ins_item] + self.items[fuse_end:]
        self.number = len(self.items)
        self.lower = self.items[0].start
        self.upper = self.items[-1].end

    def insert_inorder(self, ins_item):
        self.items.append(ins_item)
        self.number += 1
        self.lower = self.items[0].start
        self.upper = ins_item.end

    def __contains__(self, item):  # whether IntervalSet fully covers the interval
        if item.__name__ != 'Interval':
            raise TypeError
        else:
            start = 0
            end = self.number-1
            if not self.items[0] <= item <= self.items[-1]:
                return False
            elif item == self.items[0]:
                return item in self.items[0]
            elif item == self.items[-1]:
                return item in self.items[-1]

            while True:
                node = (start + end) / 2
                if (end - start) == 1:
                    return False
                if item == self.items[node]:
                    return item in self.items[node]
                elif item < self.items[node]:
                    end = node
                elif item > self.items[node]:
                    start = node


def test():
    a = Interval(1, 40)
    b = Interval(55, 69)
    c = Interval(74, 86)
    g = Interval(102, 114)
    f = Interval(150, 300)
    h = Interval(400, 500)
    intervals = [a, b, c, f, g, h]

    test1 = Interval(120, 203)
    test2 = Interval(55, 69)
    test3 = Interval(550, 600)
    test4 = Interval(-10, 0)
    test5 = Interval(80, 90)
    test6 = Interval(0, 1000)
    test7 = Interval(200, 250)
    testset = [test1, test2, test3, test4, test5, test6, test7]

    set1 = IntervalSet()
    for i in intervals:
        set1.insert(i)
    for j in testset:
        if j in set1:
            j.print_interval()

if __name__ == '__main__':
    test()
