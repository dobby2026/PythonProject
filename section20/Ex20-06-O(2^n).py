"""
파일명: Ex20-06-O(2^n).py

O(2^n)
    지수 시간 복잡도, 피보나치 수열처럼 재귀적 알고리즘
"""

'''
fibonacci(10)
    fibonacci(9)
        fibonacci(8)
            fibonacci(7)
                fibonacci(6)    -> return 8
                    fibonacci(5)    -> return 5
                        fibonacci(4)    -> return 3
                            fibonacci(3)    ->  return 2
                                fibonacci(2) -> return 1 
                                    fibonacci(1) -> 1
                                    fibonacci(0) -> 0
                                fibonacci(1) -> return 1  
                            fibonacci(2) -> return 1 
                                    fibonacci(1) -> 1
                                    fibonacci(0) -> 0
                        fibonacci(3)    ->  return 2
                                fibonacci(2) -> return 1 
                                    fibonacci(1) -> 1
                                    fibonacci(0) -> 0
                                fibonacci(1) -> return 1  
                    fibonacci(4)    -> return 3
                            fibonacci(3)    ->  return 2
                                fibonacci(2) -> return 1 
                                    fibonacci(1) -> 1
                                    fibonacci(0) -> 0
                                fibonacci(1) -> return 1  
                            
                                    

'''

def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

print(fibonacci(100))



