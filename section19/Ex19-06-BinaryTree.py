"""
파일명: Ex19-06-BinaryTree.py

트리 자료구조
    단 하나의 루트 노드가 있고, 루트 노드에서 하위 노드들이 연결된
    비선형 계층구조이다.

이진트리 (Binary Tree)
    모든 노드가 최대 2개의 자식 노드를 가질 수 있는 구조를 말한다.

    예) 기준 - 왼쪽 서브트리의 값은 루트의 값보다 작고, 오른쪽 서브트리의 값은 루트보다
            큰 값을 가지도록 구성

"""

class TreeNode:

    def __init__(self, value):
        self.value = value  # 노드의 값
        self.left = None    # 왼쪽 서브트리 노드
        self.right = None   # 오른쪽 서브트리 노드


class BinaryTree:

    def __init__(self, root):
        self.root = TreeNode(root)  # 루트 노드

    def insert(self, value):
        '''
        value = 4
        '''


        if not self.root:
            self.root = TreeNode(value)
        else:
           self._insert(value, self.root)

    def _insert(self, value, current_node):
        '''
        value = 4
        current_node = TreeNode(5)
        '''
        if value < current_node.value:
            if not current_node.left:
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

    def preorder(self, start, traversal):

        if start:
            traversal += (str(start.value) + '#')
            traversal = self.preorder(start.left, traversal)
            traversal = self.preorder(start.right, traversal)

        return traversal


# 실행코드
bt = BinaryTree(5)  # 루트 노드 5인 이진트리 객체 생성

# 값 삽입
bt.insert(3)
bt.insert(7)
bt.insert(2)
bt.insert(4)
bt.insert(6)
bt.insert(8)

# 이진 트리를 전위 순회한 결과 출력
print(f'전위 순회: {bt.preorder(bt.root, '')}')




