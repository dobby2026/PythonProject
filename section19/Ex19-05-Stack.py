"""
파일명: Ex19-05-Stack.py

스택 (Stack)
    한 쪽 끝에서만 자료를 넣거나 뺄 수 있는 선형 구조로
    후입선출(LIFO - Last In First Out)로 되어 있다

"""

class Stack:
    def __init__(self):
        self.stack = []


    def push(self, value):
        self.stack.append(value)

    def pop(self):
        return self.stack.pop()

    def print_stack(self):
        print(self.stack)


# 실행 코드
stack = Stack()
stack.push(1)
stack.push(2)
stack.push(3)

stack.print_stack()

print(f'pop(): {stack.pop()}')
stack.print_stack()



