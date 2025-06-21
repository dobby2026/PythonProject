'''
파일명: Ex10-02-method-set.py
'''

s1 = {'apple', 'banana', 'cherry'}
s2 = {'apple', 'banana', 'orange'}

# 교집합 intersection()
result = s1.intersection(s2)
print(result)
print(s1 & s2)

# 합집합 union()
result = s1.union(s2)
print(result)
print(s1 | s2)

# 차집합 difference
result = s1.difference(s2)
print(result)
print(s1 - s2)





