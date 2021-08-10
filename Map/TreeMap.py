from BST import BinarySearchTree

class TreeMap:
    def __init__(self):
        self.bst=BinarySearchTree()
        self.count = self.bst.count
        self.root = None

    def size(self):
        '''
        :return: int, 一个TreeMap对象存储的数据量
        '''
        return self.bst.size()

    def IsEmpty(self):
        '''
        :return: bool, 一个TreeMap对象是否为空的标志
        '''
        return self.bst.count==0

    def clear(self):
        '''
        将一个TreeMap对象清空
        '''
        self.bst.clear()

    def put(self,key,value):
        '''
        在一个TreeMap对象中增加键值对(key, value)
        :param  key: 待存储的键，必须是可比较的数据类型（如果是自定义的数据类型则需要在类的内部重写__eq__,__lt__,__gt__等各种比较方法）
                value: 待存储的值
        :return: bool, 是否成功添加的标志
        '''
        return self.bst.insert(key,value)

    def get(self,key):
        '''
        在TreeMap中根据键key寻找对应的值value
        :param key: 可比较的数据类型（如果是自定义的数据类型则需要在类的内部重写__eq__,__lt__,__gt__等各种比较方法）
        :return: key对应的value
        '''
        n,p=self.bst.search(self.bst.root,self.bst.root,key)
        return n.value

    def remove(self,key):
        '''
        在一个TreeMap对象中删除key所对应的键值对
        :param key: 键，可比较的数据类型（如果是自定义的数据类型则需要在类的内部重写__eq__,__lt__,__gt__等各种比较方法）
        :return: bool, 是否成功删除的标志
        '''
        return self.bst.delete(key)

    def containsKey(self,key):
        '''
        在一个TreeMap对象中是否存在key
        :param key: 键，可比较的数据类型（如果是自定义的数据类型则需要在类的内部重写__eq__,__lt__,__gt__等各种比较方法）
        :return: bool: 是否存在key的标志
        '''
        return self.bst.containsKey(key)

    def containsValue(self,value):
        '''
        在一个TreeMap对象中是否存在value
        :param value: 值
        :return: bool: 是否存在value的标志
        '''
        return self.bst.containsValue(value)

    def traversal(self,visitor):
        '''
        按照键从小到大的顺序输出一个TreeMap对象中的所有的键值对
        :param visitor: 迭代器类型的对象
        '''
        print(list(visitor))


if __name__=='__main__':
    treemap=TreeMap()
    treemap.put('apple',10)     # 添加元素
    treemap.put('banana',20)
    treemap.put('pear',30)
    treemap.put('peach',40)
    treemap.put('water',50)
    treemap.remove('apple')     # 删除元素
    treemap.put('banana',200)   # 修改元素
    print(treemap.size())       # 获取map大小
    print(treemap.get('banana'))    # 根据key获取value
    print(treemap.containsKey('water'))     # 查看map是否包含key
    print(treemap.containsValue(20))        # 查看map是否包含value
    treemap.traversal(treemap.bst)          # 按照key从小到大的顺序遍历map
    treemap.clear()         # 清空map
    print(treemap.IsEmpty())    # 检查map是否被清空
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
    car1=Car(100,200)
    car2=Car(110,210)
    car3=Car(120,220)
    car4=Car(130,230)
    car5=Car(140,240)
    car6=Car(120,300)
    treemap.clear()
    treemap.put(car2,2)
    treemap.put(car5,5)
    treemap.put(car3,3)
    treemap.put(car1,1)
    treemap.put(car4,4)
    treemap.put(car6,6)
    treemap.traversal(treemap.bst)