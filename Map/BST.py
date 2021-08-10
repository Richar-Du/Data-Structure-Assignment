class Node:
    def __init__(self, key=None, value=None):
        self.key = key
        self.value = value
        self.lchild = None
        self.rchild = None

    def __str__(self):
        return "key:{},Value:{}".format(str(self.key), str(self.value))

    def __iter__(self):
        '''
        迭代器，按照中序遍历可以使其有序
        '''
        if self.lchild != None:
            yield from self.lchild.__iter__()
        yield self.key,self.value
        if self.rchild != None:
            yield from self.rchild.__iter__()

class BinarySearchTree:
    '''
    一棵二叉搜索树
    '''
    def __init__(self):
        self.root=None
        self.count=0

    def __iter__(self):
        '''
        使二叉搜索树本身变成一个迭代器，作为visitor，在treeset作为参数传入
        '''
        if not self.root:
            return list()
        yield from self.root.__iter__()

    def size(self):
        '''
        :return:  int, 二叉搜索树结点的数量
        '''
        return self.count

    def isEmpty(self):
        '''
        :return:   bool, 二叉搜索树是否为空
        '''
        return self.count==0

    def clear(self):
        '''
        将二叉搜索树清空
        '''
        self.__init__()

    def search(self, node, parent, key):
        '''
        在二叉搜索树中搜索数据，如果查找失败，返回node和parent
        :param node: Node, 搜索开始的结点
        :param parent: Node, 搜索开始结点的父节点
        :param key: 待搜索的键
        :return: Node, Node, 查找结果及其父结点
        '''
        if node is None:
            return node, parent
        if node.key == key:
            return node, parent
        if node.key > key:            # 在右子树中搜索
            return self.search(node.lchild, node, key)
        else:                           # 在左子树中搜索
            return self.search(node.rchild, node, key)

    def insert(self, key, value):
        '''
        在二叉搜索树中插入数据
        :param  key, 待插入的键
                value, 待插入的值
        :return: bool, 是否插入成功的标志
        '''
        n, p = self.search(self.root, self.root, key)      # 通过search函数找到应该插入的位置
        if n==None and p==None:         # 本身初始化的时候就是一棵空树
            self.root=Node(key,value)
            self.count=1
            return True
        elif n==None and p!=None:
            new_node = Node(key,value)
            if key > p.key:           # 作为右孩子
                p.rchild = new_node
            else:
                p.lchild = new_node     # 作为左孩子
            self.count+=1
            return True
        elif n!=None and p!=None:
            n.value=value
            return True

    def delete(self, key):
        '''
        在二叉树中删除数据value
        :param key: 二叉树中存储的键
        :return: bool, 是否删除成功的标志
        '''
        node, p = self.search(self.root, self.root, key)
        if node==None:
            print("无该关键字，删除失败")
            return False
        else:
            self.count -= 1
            if node.lchild is None:            # 如果没有左孩子
                if node == p.lchild:
                    p.lchild = node.rchild
                else:
                    p.rchild = node.rchild
                del node
                return True
            elif node.rchild is None:              # 如果没有右孩子
                if node == p.lchild:
                    p.lchild = node.lchild
                else:
                    p.rchild = node.lchild
                del node
                return True
            else:                       # 左右孩子都有
                pre = node.rchild              # 在右子树中找直接前驱来替代n
                if pre.lchild is None:
                    node.value = pre.value
                    node.rchild = pre.rchild
                    del pre
                    return True
                else:
                    next = pre.lchild
                    while next.lchild is not None:    # 顺着左子树一直找到最左下的结点就是n的直接前驱
                        pre = next
                        next = next.lchild
                    node.value = next.value
                    pre.lchild = next.rchild            # n的直接前驱的右孩子顶替它的位置
                    del node
                    return True

    def containsKey(self,key):
        '''
        查看二叉搜索树中是否有key作为键
        :param key: 二叉搜索树中存储的键
        :return: 是否存在的标志
        '''
        node, p = self.search(self.root, self.root, key)
        return node != None

    def containsValue(self,value):
        '''
        查看二叉搜索树中是否有value作为值
        :param value, 二叉搜索树中存储的值
        :return: bool, 是否存在的标志
        '''
        for k,v in list(self):
            if v==value:
                return True
        return False
