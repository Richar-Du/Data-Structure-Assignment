class Node:
    '''
    二叉搜索树的一个结点
    '''
    def __init__(self, element):
        self.element = element
        self.lchild = None
        self.rchild = None

    def __iter__(self):
        '''
        迭代器，按照中序遍历可以使其有序
        '''
        if self.lchild != None:         # 左子树
            yield from self.lchild.__iter__()
        yield self.element              # 自身
        if self.rchild != None:
            yield from self.rchild.__iter__()           # 右子树

class BinarySearchTree:
    '''
    一棵二叉搜索树
    '''
    def __init__(self, node_list=[]):
        '''
        通过列表的方式初始化BST
        :param node_list: 准备构建二叉树的列表
        '''
        if len(node_list)!=0:       # 传入列表，则通过列表初始化
            self.root = Node(node_list[0])
            self.count=1
            for element in node_list[1:]:
                self.insert(element)
        else:           # 没传列表，初始化为空树
            self.root=None
            self.count=0

    def __iter__(self):
        '''
        使二叉搜索树本身变成一个迭代器，作为visitor，在treeset中作为参数传入
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

    def search(self, node, parent, element):
        '''
        在二叉搜索树中搜索数据，如果查找失败，返回node和parent
        :param node: Node, 搜索开始的结点
        :param parent: Node, 搜索开始结点的父节点
        :param element: 待搜索的数据
        :return: Node, Node, 查找结果及其父结点
        '''
        if node is None:            # 递归出口
            return node, parent
        if node.element == element:     # 递归出口
            return node, parent
        if node.element > element:            # 在右子树中搜索
            return self.search(node.lchild, node, element)
        else:                           # 在左子树中搜索
            return self.search(node.rchild, node, element)

    def insert(self, element):
        '''
        在二叉搜索树中插入数据
        :param element, 待插入的数据
        :return: bool, 是否插入成功的标志
        '''
        n, p = self.search(self.root, self.root, element)      # 通过search函数找到应该插入的位置
        if n==None and p==None:         # 本身初始化的时候就是一棵空树
            self.root=Node(element)
            self.count=1
            return True
        elif n==None and p!=None:
            new_node = Node(element)
            if element > p.element:           # 作为右孩子插入
                p.rchild = new_node
            else:
                p.lchild = new_node     # 作为左孩子插入
            self.count+=1
            return True
        else:
            print("结点已存在！")
            return False

    def delete(self, element):
        '''
        在二叉树中删除数据element
        :param element: 二叉树中存储的数据
        :return: bool, 是否删除成功的标志
        '''
        node, p = self.search(self.root, self.root, element)        # 通过search函数找到应该删除结点的位置
        if node==None:          # 结点不存在
            print("无该关键字，删除失败")
            return False
        else:       # 结点存在
            self.count -= 1
            if node.lchild is None:            # 如果没有左孩子，用node的右孩子代替自己
                if node == p.lchild:
                    p.lchild = node.rchild
                else:
                    p.rchild = node.rchild
                del node
                return True
            elif node.rchild is None:              # 如果没有右孩子，用node的左孩子代替自己
                if node == p.lchild:
                    p.lchild = node.lchild
                else:
                    p.rchild = node.lchild
                del node
                return True
            else:                       # 如果左右孩子都有，在右子树中找直接后继来替代node
                pre = node.rchild
                if pre.lchild is None:      # 如果右子树没有左孩子，那么右子树的根结点就是node的直接后继
                    node.element = pre.element
                    node.rchild = pre.rchild
                    del pre
                    return True
                else:               # 如果右子树有左孩子，那么顺着左子树一直找到最左下的结点就是node的直接后继
                    next = pre.lchild
                    while next.lchild is not None:
                        pre = next
                        next = next.lchild
                    node.element = next.element
                    pre.lchild = next.rchild            # n的直接后继的右孩子顶替它的位置
                    del node
                    return True

    def contains(self,element):
        '''
        查看二叉搜索树中是否有element
        :param element, 二叉搜索树中存储的数据类型
        :return: bool, 是否存在的标志
        '''
        node,p=self.search(self.root, self.root, element)
        return node!=None