"""
파일명: Ex04-02-assignment.py

대입 연산자
    변수에 값을 할당하는 연산자

    단순 대입: (=)
    복합 대입:
        (+=, -=, *=, /=, %=)

"""
# 기본 대입
student_name = '김철수'
grade = 3
print(f'학생: {student_name}, 학년: {grade}')

# 다중 대입
math_score, english_score = 85, 92
print(f'수학: {math_score}점, 영어: {english_score}점')

# 교환
math_score, english_score = english_score, math_score
print(f'교환 후 수학: {math_score}점, 영어: {english_score}점')

# 복합 대입
total_score = 0             # tatal_score = 0
total_score += math_score   # tatal_score = total_score + math_score
total_score += english_score # tatal_score = total_score + english_score

print(f'누적 점수: {total_score}점')


