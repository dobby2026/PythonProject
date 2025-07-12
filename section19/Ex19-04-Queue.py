"""
파일명: Ex19-04-Queue.py

큐(Queue)
    기본적인 자료구조의 종류로
    먼저 집어 넣은 데이터가 먼저 나오는
    FIFO(First In First Out) 구조로
    저장하는 형식

"""

class Queue:

    def __init__(self):
        self.queue = []     # 빈 리스트로 큐 초기화

    def is_empty(self):
        return len(self.queue) == 0

    def enqueue(self, item):
        self.queue.append(item)

    def dequeue(self):
        if self.is_empty():
            return "큐가 비어있습니다"

        item = self.queue.pop(0)
        return item

    def peek(self):
        if self.is_empty():
            return "큐가 비어있습니다"
        return self.queue[0]

    def size(self):
        return len(self.queue)

    def display(self):
        if self.is_empty():
            print('큐가 비어있습니다')
        else:
            print(f'현재 큐: {self.queue}')


# 실행코드
q = Queue()

q.enqueue('첫번째 고객')
q.enqueue('두번째 고객')
q.enqueue('세번째 고객')


# 현재 큐 상태 출력
q.display()

# 큐에서 데이터 제거
q.dequeue()
q.display()

# 현재 첫번째 데이터 확인
print(f'다음 고객: {q.peek()}')
print(f'대기중 고객 수: {q.size()}')





