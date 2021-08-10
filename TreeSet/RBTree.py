class Node:
    def __init__(self, value, color, parent, left=None, right=None):
        self.value = value
        self.color = color
        self.parent = parent
        self.left = left
        self.right = right

    def __repr__(self):
        return 'Node:{color},{val}'.format(color=self.color, val=self.value)

    def __iter__(self):             # 中序遍历
        if self.left.color != 'NULL':
            yield from self.left.__iter__()
        yield self.value
        if self.right.color != 'NULL':
            yield from self.right.__iter__()

    def has_children(self):     # 是否有孩子
        return bool(self.get_children_count())

    def get_children_count(self):            # 孩子结点的数量
        if self.color == 'NULL':
            return 0
        return sum([int(self.left.color != 'NULL'), int(self.right.color != 'NULL')])

class RedBlackTree:
    NULL_leave = Node(value=None, color='NULL', parent=None)
    def __init__(self):
        self.count = 0
        self.root = None
        self.ROTATIONS = {
            # 后面左旋和右旋用的比较多，因此分别用L和R来代替
            'L': self.rightRotation,
            'R': self.leftRotation
        }

    def __iter__(self):
        '''
        使红黑树本身变成一个迭代器，作为visitor，在treeset中作为参数传入
        '''
        if not self.root:
            return list()
        yield from self.root.__iter__()

    def insert(self, value):
        '''
        增加结点操作
        :param value: 数值，表示往treeset对象中增加的数据
        '''
        if not self.root:           # 如果树空，那么直接当作根结点插入（注意根结点必须是黑色的）
            self.root = Node(value, color='BLACK', parent=None, left=self.NULL_leave, right=self.NULL_leave)
            self.count += 1
            return
        parent, node_direction = self.search(value,self.root)             # 如果树不空，那么找到需要插入的位置
        if node_direction is None:      # value已经存在，无需插入
            return
        new_node = Node(value=value, color='RED', parent=parent, left=self.NULL_leave, right=self.NULL_leave)         # 创建一个红节点准备插入
        # 策略是先插入后调整
        if node_direction == 'L':
            parent.left = new_node
        else:
            parent.right = new_node

        self.rebalance(new_node)           # 调整平衡
        self.count += 1

    def delete(self, value):
        '''
        将待删除的值调整成只有0个或1个孩子，然后调用红黑树的删除操作（本函数不执行删除，通过调用_remove函数实现删除）
        :param value: 数值
        '''
        node_to_remove, position = self.search(value,self.root)      # 先找到需要删除的结点
        if position != None:  # 不存在这个结点
            return
        if node_to_remove.get_children_count() == 2:            # 如果待删除结点有两个孩子
            # 找到中序后继（必定只有0或1个孩子），交换本结点与中序后继的值，然后删除中序后继
            successor = self.findInOrderSuc(node_to_remove)
            node_to_remove.value = successor.value
            node_to_remove = successor

        # 调整之后必定只有0或1个孩子，直接_remove（注意_remove才是红黑树删除操作的核心）
        self.remove(node_to_remove)
        self.count -= 1

    def contains(self, value):      # 查看红黑树中是否存在value值
        node, position=self.search(value,self.root)
        return position==None

    def remove(self, node):
        """
        对结点执行删除操作
        :param node: Node对象，必须只能有0或1个孩子
        """
        left_child = node.left
        right_child = node.right
        not_NULL = left_child if left_child != self.NULL_leave else right_child      # 从左右孩子中找到不是'NULL'的
        if node == self.root:       # 待删除的是根结点
            if not_NULL != self.NULL_leave:      # 根结点有一个孩子，则直接让这个孩子变成根结点
                self.root = not_NULL
                self.root.parent = None
                self.root.color = 'BLACK'
            else:       # 如果左右孩子都是'NULL'，直接删除根结点
                self.root = None
        elif node.color == 'RED':     # 如果删除的是非根的红结点
            if not node.has_children():     # 红节点没有孩子就直接删除
                self.removeLeaf(node)
            else:               # 因为在remove函数中已经对待删除的结点进行了调整，所以不会出现这种情况
                raise Exception('不可能只有一个黑孩子，中序后继调整有误')
        else:  # 如果删除的是非根的黑结点，则需要看其子结点是否为黑，可能导致双黑缺陷，需要一系列处理
            if right_child.has_children() or left_child.has_children():  # 不会出现
                raise Exception('左右孩子均不会有孩子结点，中序后继调整有误')
            if not_NULL.color == 'RED':      # 直接用红结点代替黑结点，因为调整之后只有一个孩子，因此保证红节点下面不再有孩子了
                node.value = not_NULL.value
                node.left = not_NULL.left
                node.right = not_NULL.right
            else:  # 黑孩子————双黑缺陷
                self.removeBlack(node)

    def removeLeaf(self, leaf):
        '''
        删除叶子结点
        :param leaf: Node对象
        '''
        # 只需要让叶子结点的父节点的孩子变成'NULL'结点即可
        if leaf.value >= leaf.parent.value:
            leaf.parent.right = self.NULL_leave
        else:
            leaf.parent.left = self.NULL_leave

    def removeBlack(self, node):         # 对双黑缺陷进行调整的入口函数
        self.adjust(node)         # 从case1开始调整，最终退出的时候node一定被调整为叶结点
        self.removeLeaf(node)         # 删除黑色的叶子结点

    def adjust(self, node):
        if self.root == node:           # 不断向上调整的出口
            node.color = 'BLACK'
            return
        self.BB_3(node)

    def BB_3(self, node):       # 双黑缺陷根据兄弟结点是黑还是红分类处理
        parent = node.parent
        sibling, direction = self.getSibling(node)
        if sibling.color == 'RED' and parent.color == 'BLACK' and sibling.left.color != 'RED' and sibling.right.color != 'RED':     # BB-3: 只要兄弟节点是红就肯定是父亲和儿子都是黑，应该执行左旋或右旋操作（取决于兄弟结点是父结点的左孩子还是右孩子）
            self.ROTATIONS[direction](node=None, parent=sibling, grandfather=parent)
            parent.color = 'RED'
            sibling.color = 'BLACK'
            return self.adjust(node)          # 转化成BB-1或者BB-2R
        self.BB_2B(node)     # 兄弟结点是黑，转到BB-2的情况


    def BB_2B(self, node):       # 先检查是否是BB-2B
        parent = node.parent
        sibling, _ = self.getSibling(node)
        if (sibling.color == 'BLACK' and parent.color == 'BLACK'
           and sibling.left.color != 'RED' and sibling.right.color != 'RED'):               # BB-2B的情况：兄弟结点是黑，且孩子结点全是黑，父亲结点是黑
            sibling.color = 'RED'             # 保持父节点和孩子节点不变，将兄弟结点染红
            return self.adjust(parent)  # 由于父结点发生下溢，因此对parent递归处理

        self.BB_2R(node)         # 不是BB-2B，转到BB-2R

    def BB_2R(self, node):       # 先检查是否是BB-2R的情况
        parent = node.parent
        if parent.color == 'RED':             # 如果确实是BB-2R：兄弟结点是黑，且孩子结点全是黑，父亲结点是红，则只需要重新染色
            sibling, direction = self.getSibling(node)
            if sibling.color == 'BLACK' and sibling.left.color != 'RED' and sibling.right.color != 'RED':
                parent.color, sibling.color = sibling.color, parent.color  # 兄弟变红，父亲变黑
                return  # 此时红黑树全局的性质就已经恢复了，不用再向上检查
        self.BB_1_preprocess(node)         # 转到BB-1

    def BB_1_preprocess(self, node):           # 在转到BB-1之前先进行预处理
        sibling, direction = self.getSibling(node)
        closer_node = sibling.right if direction == 'L' else sibling.left
        outer_node = sibling.left if direction == 'L' else sibling.right
        if closer_node.color == 'RED' and outer_node.color != 'RED' and sibling.color == 'BLACK':       # 调整完之后保证closer_node是红的
            if direction == 'L':
                self.leftRotation(node=None, parent=closer_node, grandfather=sibling)
            else:
                self.rightRotation(node=None, parent=closer_node, grandfather=sibling)
            closer_node.color = 'BLACK'
            sibling.color = 'RED'

        self.BB_1(node)

    def BB_1(self, node):           # BB-1：兄弟结点为黑，而且至少有一个孩子是红（此时p的颜色无所谓），而且经过预处理确保红色的结点已经确保在外侧了，只需要根据兄弟节点是左还是右来相应地进行左旋和右旋
        sibling, direction = self.getSibling(node)
        outer_node = sibling.left if direction == 'L' else sibling.right

        def BB_1_rotation(direction):
            parent_color = sibling.parent.color
            self.ROTATIONS[direction](node=None, parent=sibling, grandfather=sibling.parent)
            sibling.color = parent_color            # 旋转之后兄弟变成父结点，继承父节点的颜色，而左右孩子都变黑
            sibling.right.color = 'BLACK'
            sibling.left.color = 'BLACK'

        if sibling.color == 'BLACK' and outer_node.color == 'RED':          # 实际上此处红黑树就已经恢复全局性质
            return BB_1_rotation(direction)

        raise Exception('没有转化到BB-1，某处调整有误！')

    def rebalance(self, node):
        '''
        给定一个新插入的结点，对树进行重新调整
        :param node: Node对象
        '''
        parent = node.parent
        value = node.value
        if (parent is None or parent.parent is None or (node.color != 'RED' or parent.color != 'RED')):  # 不需要调整的情况
            return
        # 判断不平衡子树的结构：LL,RR,LR,RL中的某一种
        grandfather = parent.parent
        node_direction = 'L' if parent.value > value else 'R'
        parent_dir = 'L' if grandfather.value > parent.value else 'R'
        uncle = grandfather.right if parent_dir == 'L' else grandfather.left
        general_direction = node_direction + parent_dir

        # 插入之后的调整实际上分叔父结点是黑的还是红的两种情况：
        if uncle == self.NULL_leave or uncle.color == 'BLACK':          # 叔父结点不是红，需要左右旋
            # 旋转操作实际上和AVL树是同样的道理，下面借鉴AVL树的旋转处理
            if general_direction == 'LL':
                self.rightRotation(node, parent, grandfather, to_recolor=True)
            elif general_direction == 'RR':
                self.leftRotation(node, parent, grandfather, to_recolor=True)
            elif general_direction == 'LR':
                self.rightRotation(node=None, parent=node, grandfather=parent)
                self.leftRotation(node=parent, parent=node, grandfather=grandfather, to_recolor=True)
            elif general_direction == 'RL':
                self.leftRotation(node=None, parent=node, grandfather=parent)
                self.rightRotation(node=parent, parent=node, grandfather=grandfather, to_recolor=True)
            else:
                raise Exception("{} 不是一个合法的方向组合！".format(general_direction))
        else:               # 叔父结点是红的只需要重染色即可
            self.recolor(grandfather)

    def updateParent(self, node, parent_old_child, new_parent):
        """
        node取代parent_old_child，new_parent作为node的父结点
        """
        node.parent = new_parent
        if new_parent:
            if new_parent.value > parent_old_child.value:           # 找到parent_old_child的位置
                new_parent.left = node
            else:
                new_parent.right = node
        else:
            self.root = node

    def rightRotation(self, node, parent, grandfather, to_recolor=False):     # 右旋
        grand_grandfather = grandfather.parent
        self.updateParent(node=parent, parent_old_child=grandfather, new_parent=grand_grandfather)       

        old_right = parent.right
        parent.right = grandfather
        grandfather.parent = parent

        grandfather.left = old_right  
        old_right.parent = grandfather

        if to_recolor:          # 重新染色
            parent.color = 'BLACK'
            node.color = 'RED'
            grandfather.color = 'RED'

    def leftRotation(self, node, parent, grandfather, to_recolor=False):          # 左旋
        grand_grandfather = grandfather.parent
        self.updateParent(node=parent, parent_old_child=grandfather, new_parent=grand_grandfather)

        old_left = parent.left
        parent.left = grandfather
        grandfather.parent = parent

        grandfather.right = old_left  
        old_left.parent = grandfather

        if to_recolor:          # 重新染色
            parent.color = 'BLACK'
            node.color = 'RED'
            grandfather.color = 'RED'

    def recolor(self, grandfather):            # 父亲、叔父变黑，祖父变红
        grandfather.right.color = 'BLACK'
        grandfather.left.color = 'BLACK'
        if grandfather != self.root:
            grandfather.color = 'RED'
        self.rebalance(grandfather)            # 向上递归调整

    def search(self, value,parent):
        '''
        :param value: 待查找的值
        :param parent: Node对象，表示从哪个结点开始找
        :return: parent: Node对象，表示新插入结点的父结点
                'L' or 'R': 表示应该插入到parent的左侧还是右侧
        '''
        if value == parent.value:
            return parent, None
        elif parent.value < value:
            if parent.right.color == 'NULL':  # 右边没有那么就直接插入在右边
                return parent, 'R'
            return self.search(value, parent.right)         # 右边仍然有则向右查找
        elif value < parent.value:
            if parent.left.color == 'NULL':  # 左边没有那么就直接插入在右边
                return parent, 'L'
            return self.search(value, parent.left)      # 右边仍然有则向右查找

    def findInOrderSuc(self, node):           # 查找中序后继
        right_node = node.right
        left_node = right_node.left
        if left_node == self.NULL_leave:
            return right_node
        while left_node.left != self.NULL_leave:          # 不断循环，直到找到最左下的中序后继
            left_node = left_node.left
        return left_node

    def getSibling(self, node):           # 找到兄弟结点及所处的位置
        parent = node.parent
        if node.value >= parent.value:
            sibling = parent.left
            direction = 'L'
        else:
            sibling = parent.right
            direction = 'R'
        return sibling, direction
    def size(self):
        return self.count
    def isEmpty(self):
        return self.count==0
    def clear(self):
        self.__init__()