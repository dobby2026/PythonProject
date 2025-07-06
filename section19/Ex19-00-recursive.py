"""
파일명: Ex19-00-recursive.py

재귀함수(Recursive Function)
    함수 내부에서 자기 자신을 호출하는 함수
"""

def recursive_count_number(n):
    """
    recursive_count_number(5)
    n = 5
    print(5)
        recursive_count_number(4)
        n = 4
        print(4)
             recursive_count_number(3)
             n = 3
             print(3)
                recursive_count_number(2)
                n = 2
                print(2)
                    recursive_count_number(1)
                    n = 1
                    print(1)
                        recursive_count_number(0)
                        n = 0
    """

    if(n <= 0):
        return

    print(n)
    recursive_count_number(n - 1)


# 실행코드
recursive_count_number(5)