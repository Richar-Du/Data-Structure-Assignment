from BST import BinarySearchTree
class TreeSet:
    '''
    TreeSet是一个具有去重效果的数据结构，比如添加1、1、2、3、3、4、4、4、5到TreeSet中。最终TreeSet会将数据排序，并且只会保存1、2、3、4、5共5个元素。
    '''
    def __init__(self,node_list=[]):
        self.bst=BinarySearchTree(node_list)
        # self.bst=RedBlackTree()           # 如果使用红黑树作为底层也可以，接口完全一样
    def size(self):
        '''
        :return: int型, 表示一个TreeSet对象存储的数据量
        '''
        return self.bst.size()

    def isEmpty(self):
        '''
        :return: bool型, 一个TreeSet对象是否为空的标志
        '''
        return self.bst.isEmpty()

    def clear(self):
        '''
        将一个TreeSet对象清空
        '''
        self.bst.clear()

    def add(self,element):
        '''
        在一个TreeSet对象中增加元素element
        :param element: 泛型，必须是可比较的数据类型（如果是自定义的数据类型则需要在类的内部重写__eq__,__lt__,__gt__等各种比较方法）
        '''
        self.bst.insert(element)

    def remove(self,element):
        '''
        在一个TreeSet对象中删除元素element
        :param element: 泛型，必须是可比较的数据类型（如果是自定义的数据类型则需要在类的内部重写__eq__,__lt__,__gt__等各种比较方法）
        '''
        self.bst.delete(element)

    def contains(self,element):
        '''
        在一个TreeSet对象中是否存在element
        :param element: 泛型，必须是比较的数据类型（如果是自定义的数据类型则需要在类的内部重写__eq__,__lt__,__gt__等各种比较方法）
        :return: bool型, 是否存在element的标志
        '''
        return self.bst.contains(element)

    def traversal(self,visitor):
        '''
        按照从小到大的顺序输出一个TreeSet对象中的所有元素
        :param visitor: 迭代器类型的对象
        '''
        print(list(visitor))        # 迭代器可以直接以列表的形式输出

if __name__=="__main__":
    a = [49, 38, 65, 97, 60, 76, 13, 27, 5, 1, 20, 21]
    ts = TreeSet(a)  # 初始化列表的形式创建treeset
    ts.add(10)      # 添加元素
    ts.add(49)
    ts.add(38)
    ts.add(65)
    ts.add(97)
    ts.add(60)
    ts.add(76)
    ts.add(13)
    ts.add(27)
    ts.add(5)
    ts.add(1)
    ts.add(20)
    ts.add(21)
    ts.remove(13)   # 删除元素
    print(ts.size())    # 获取treeset大小
    print(ts.isEmpty()) # 查看是否为空
    print(ts.contains(49))      # 查看是否存在49
    print(ts.contains(99))      # 查看是否存在99
    ts.traversal(ts.bst)    # 从小到大遍历treeset
    ts.clear()      # 清空treeset
    print(ts.isEmpty())     # 验证是否清空

    class Car:
        def __init__(self,weight,price):
            self.weight=weight
            self.price=price

        def __lt__(self,other):
            if self.weight!=other.weight:
                return self.weight<other.weight
            elif self.price!=other.price:
                return self.price<other.price
            return False

        def __gt__(self,other):
            if self.weight!=other.weight:
                return self.weight>other.weight
            elif self.price!=other.price:
                return self.price>other.price
            return False

        def __eq__(self, other):
            return self.weight==other.weight and self.price==other.price

        def __repr__(self):
            return "(Car: weight:{},price:{})".format(str(self.weight), str(self.price))

    car1 = Car(100, 200)
    car2 = Car(110, 210)
    car3 = Car(120, 220)
    car4 = Car(130, 230)
    car5 = Car(140, 240)
    car6 = Car(120, 300)
    ts.clear()
    ts.add(car1)
    ts.add(car3)
    ts.add(car2)
    ts.add(car6)
    ts.add(car5)
    ts.add(car4)
    ts.traversal(ts.bst)