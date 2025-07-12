'''
파일명: Ex19-6-BinaryTree.py

트리 자료구조
    단 하나의 루트 노드가 있고, 루트 노드에서 하위 노드들이 연결된
    비선형 계층구조이다.

이진트리(Binary Tree)
    모든 노드가 최대 2개의 자식 노드를 가질 수 있는 구조를 말한다.
    왼쪽 서브 트리의 값은 루트의 값보다 작고, 오른쪽 서브트리의 값은 루트보다
    큰 값을 가지도록 구성한다.
'''
class TreeNode:
    def __init__(self, value):
        self.value = value # 노드의 값
        self.left = None # 왼쪽 서브트리 노드
        self.right = None # 오른쪽 서브트리 노드

class BinaryTree:
    def __init__(self, root):
        self.root = TreeNode(root) # 루트노드

    def preorder_traversal(self, start, traversal):
        '''
    preorder_traversal(bt.root, "")
        start = TreeNode(5)
        traversal = "5#"
        preorder_traversal(TreeNode(3), "5#")  -> 5#3#2#4#
                start = TreeNode(3)
                traversal = "5#3#"
                preorder_traversal(TreeNode(2), "5#3#") -> "5#3#2#"
                    start = TreeNode(2)
                    traversal = "5#3#2#"
                    preorder_traversal(None, "5#3#2#")  -> "5#3#2#"
                        start = None
                        traversal = "5#3#2#"
                    preorder_traversal(None, "5#3#2#")  -> "5#3#2#"
                        start = None
                        traversal = "5#3#2#"

                preorder_traversal(TreeNode(4), "5#3#2#") -> 5#3#2#4#
                     start = TreeNode(4)
                     traversal = "5#3#2#4#"
                     preorder_traversal(None, "5#3#2#4#")  -> "5#3#2#4#"
                        start = None
                        traversal = "5#3#2#4#"
                     preorder_traversal(None, "5#3#2#4#")  -> "5#3#2#4#"
                        start = None
                        traversal = "5#3#2#4#"

        preorder_traversal(TreeNode(7), "5#3#2#4#")  ->

        '''

        if start:
            traversal += (str(start.value) + '#')
            traversal = self.preorder_traversal(start.left, traversal)
            traversal = self.preorder_traversal(start.right, traversal)
        return traversal

    def inorder_traversal(self, start, traversal):
        if start:
            traversal = self.inorder_traversal(start.left, traversal)
            traversal += (str(start.value)+ '#')
            traversal = self.inorder_traversal(start.right, traversal)
        return traversal

    # 후위순회 left -> right -> root
    def postorder_traversal(self, start, traversal):
        if start:
            traversal = self.postorder_traversal(start.left, traversal)
            traversal = self.postorder_traversal(start.right, traversal)
            traversal += (str(start.value) + ' ')
        return traversal

    def search(self, value):
        return self._search(value, self.root)

    def _search(self, value, current_node):
        if not current_node:
            return False
        elif current_node.value == value:
            return True
        elif value < current_node.value:
            return self._search(value, current_node.left)
        else:
            return self._search(value, current_node.right)


    '''
        3 
        7 
        2 
        4 
        6 8 
    '''
    def insert(self, value):
        '''
        value = 2



        '''
        if not self.root:
            self.root = TreeNode(value)
        else:
            self._insert(value, self.root)

    def _insert(self, value, current_node):
        '''
        value = 3
        current_node = TreeNode(5)
        current_node.left = TreeNode(3)
        value = 7
        current_node = TreeNode(5)
        current_node.right = TreeNode(7)

        value = 2
        current_node = TreeNode(5)

            _insert(2, TreeNode(3))
                value = 2
                current_node = TreeNode(3)
                current_node.left = TreeNode(2)

        value = 4
        current_node = TreeNode(5)
            _insert(4, TreeNode(3))
                current_node = TreeNode(3)
                current_node.right = TreeNode(4)

        value = 6
        current_node = TreeNode(5)
            _insert(6, TreeNode(7))
                current_node = TreeNode(7)
                current_node.left = TreeNode(6)

        value = 8
        current_node = TreeNode(5)
            _insert(8, TreeNode(7))
                current_node = TreeNode(7)
                current_node.right = TreeNode(8)


        '''

        if value < current_node.value:
            if not current_node.left:   # current_node.left 값이 None 실행
                current_node.left = TreeNode(value)
            else:
                self._insert(value, current_node.left)

        elif value > current_node.value:

            if not current_node.right:
                current_node.right = TreeNode(value)
            else:
                self._insert(value, current_node.right)
        else:
            print('이미 존재하는 값입니다.')

    def delete(self, value):
        if not self.root:
            return
        else:
            self.root = self._delete(value, self.root)

    def _delete(self, value, current_node):
        if not current_node:
            return current_node
        elif value < current_node.value:
            current_node.left = self._delete(value, current_node.left)
        elif value > current_node.value:
            current_node.right = self._delete(value, current_node.right)
        else:
            if not current_node.left and not current_node.right:
                current_node = None
            elif not current_node.left:
                current_node = current_node.right
            elif not current_node.right:
                current_node = current_node.left
            else:
                min_node = self._find_min(current_node.right)
                current_node.value = min_node.value
                current_node.right = self._delete(min_node.value, current_node.right)

        return current_node

    def _find_min(self, current_node):
        while current_node.left:
            current_node = current_node.left
        return current_node

# 실행 코드
bt = BinaryTree(5) # 루트 노드 5인 이진트리 객체 생성

# 값 삽입
bt.insert(3)
bt.insert(7)
bt.insert(2)
bt.insert(4)
bt.insert(6)
bt.insert(8)

# 이진 트리를 전위 순회한 결과 출력
print('전위 순회: ', bt.preorder_traversal(bt.root, ""))

# 이진 트리를 중위 순회한 결과 출력
print('중위 순회: ', bt.inorder_traversal(bt.root, ""))

# 이진 트리를 후위 순회한 결과 출력
print('후위 순회: ', bt.postorder_traversal(bt.root, ""))

# 값 검색
print('값 4가 트리에 존재하는가? ', bt.search(4))
print('값 9가 트리에 존재하는가? ', bt.search(9))

# 값 삭제
bt.delete(3)
print('값 3을 삭제한 후 중위 순회: ', bt.inorder_traversal(bt.root, ""))