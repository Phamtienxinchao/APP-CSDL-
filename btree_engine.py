RED = "ĐỎ"
BLACK = "ĐEN"

class Node:
    def __init__(self, key):
        self.key = key
        self.color = RED  
        self.parent = None
        self.left = None
        self.right = None

class BTree:
    def __init__(self, m=3): 
        self.T_NIL = Node(0)
        self.T_NIL.color = BLACK
        self.root = self.T_NIL

    def left_rotate(self, x):
        y = x.right
        x.right = y.left
        if y.left != self.T_NIL:
            y.left.parent = x
        y.parent = x.parent
        if x.parent == None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

    def right_rotate(self, x):
        y = x.left
        x.left = y.right
        if y.right != self.T_NIL:
            y.right.parent = x
        y.parent = x.parent
        if x.parent == None:
            self.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y
        y.right = x
        x.parent = y

    def insert(self, key):
        node = Node(key)
        node.parent = None
        node.left = self.T_NIL
        node.right = self.T_NIL
        node.color = RED

        y = None
        x = self.root

        while x != self.T_NIL:
            y = x
            if node.key < x.key:
                x = x.left
            elif node.key > x.key:
                x = x.right
            else:
                return 

        node.parent = y
        if y == None:
            self.root = node
        elif node.key < y.key:
            y.left = node
        else:
            y.right = node

        if node.parent == None:
            node.color = BLACK
            return
        if node.parent.parent == None:
            return

        self._insert_fixup(node)

    def _insert_fixup(self, k):
        while k.parent.color == RED:
            if k.parent == k.parent.parent.right:
                u = k.parent.parent.left
                if u.color == RED:
                    u.color = BLACK
                    k.parent.color = BLACK
                    k.parent.parent.color = RED
                    k = k.parent.parent
                else:
                    if k == k.parent.left:
                        k = k.parent
                        self.right_rotate(k)
                    k.parent.color = BLACK
                    k.parent.parent.color = RED
                    self.left_rotate(k.parent.parent)
            else:
                u = k.parent.parent.right
                if u.color == RED:
                    u.color = BLACK
                    k.parent.color = BLACK
                    k.parent.parent.color = RED
                    k = k.parent.parent
                else:
                    if k == k.parent.right:
                        k = k.parent
                        self.left_rotate(k)
                    k.parent.color = BLACK
                    k.parent.parent.color = RED
                    self.right_rotate(k.parent.parent)
            if k == self.root:
                break
        self.root.color = BLACK

    def delete(self, key):
        node = self.search_tree(self.root, key)
        if node != self.T_NIL:
            self._delete_node(node)

    def search_tree(self, node, key):
        if node == self.T_NIL or key == node.key:
            return node
        if key < node.key:
            return self.search_tree(node.left, key)
        return self.search_tree(node.right, key)

    def _transplant(self, u, v):
        if u.parent == None:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.parent = u.parent

    def _delete_node(self, z):
        y = z
        y_original_color = y.color
        if z.left == self.T_NIL:
            x = z.right
            self._transplant(z, z.right)
        elif z.right == self.T_NIL:
            x = z.left
            self._transplant(z, z.left)
        else:
            y = self._minimum(z.right)
            y_original_color = y.color
            x = y.right
            if y.parent == z:
                x.parent = y
            else:
                self._transplant(y, y.right)
                y.right = z.right
                y.right.parent = y
            self._transplant(z, y)
            y.left = z.left
            y.left.parent = y
            y.color = z.color
            
        if y_original_color == BLACK:
            self._delete_fixup(x)

    def _delete_fixup(self, x):
        while x != self.root and x.color == BLACK:
            if x == x.parent.left:
                s = x.parent.right
                if s.color == RED:
                    s.color = BLACK
                    x.parent.color = RED
                    self.left_rotate(x.parent)
                    s = x.parent.right

                if s.left.color == BLACK and s.right.color == BLACK:
                    s.color = RED
                    x = x.parent
                else:
                    if s.right.color == BLACK:
                        s.left.color = BLACK
                        s.color = RED
                        self.right_rotate(s)
                        s = x.parent.right

                    s.color = x.parent.color
                    x.parent.color = BLACK
                    s.right.color = BLACK
                    self.left_rotate(x.parent)
                    x = self.root
            else:
                s = x.parent.left
                if s.color == RED:
                    s.color = BLACK
                    x.parent.color = RED
                    self.right_rotate(x.parent)
                    s = x.parent.left

                if s.right.color == BLACK and s.left.color == BLACK:
                    s.color = RED
                    x = x.parent
                else:
                    if s.left.color == BLACK:
                        s.right.color = BLACK
                        s.color = RED
                        self.left_rotate(s)
                        s = x.parent.left

                    s.color = x.parent.color
                    x.parent.color = BLACK
                    s.left.color = BLACK
                    self.right_rotate(x.parent)
                    x = self.root
        x.color = BLACK

    def _minimum(self, node):
        while node.left != self.T_NIL:
            node = node.left
        return node

    def get_visual(self, node=None, prefix="", is_last=True, is_root=True):
        if node is None: 
            node = self.root
            
        if node == self.T_NIL:
            return ""
            
        res = prefix
        
        if is_root:
            res += f"[{node.key}]\n"
            new_prefix = ""
        else:
            res += ("└── " if is_last else "├── ") + f"[{node.key}]\n"
            new_prefix = prefix + ("    " if is_last else "│   ")
            
        children = []
        if node.left != self.T_NIL: children.append(node.left)
        if node.right != self.T_NIL: children.append(node.right)
            
        for i, child in enumerate(children):
            res += self.get_visual(child, new_prefix, i == len(children) - 1, False)
            
        return res