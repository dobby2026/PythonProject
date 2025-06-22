"""
파일명: Ex08-03-loop-homework.py

1번
*
**
***
****
*****
******
*******

2번
   *
  **
 ***
****

3번
   *
  ***
 *****
*******

4번

   *
  ***
 *****
*******
 *****
  ***
   *
            i    j
   *        0    4 5 6  j > 3 + i
  ***       1    5 6    j > 3 + i
 *****      2    6      j > 3 + i
*******     3           j > 3 + i
 *****      4    6      j > 9 - i
  ***       5    5 6    j > 9 - i
   *        6    4 5 6  j > 9 - i

"""
i = 0
while i < 7:
    j = 0
    while j < 7:
        if i < 4:
            if j < 3 - i:
                print(' ', end='')
            elif j > 3 + i:
                print(' ', end='')
            else:
                print('*', end='')

        else:
            if j < i - 3:
                print(' ', end='')
            elif j > 9 - i:
                print(' ', end='')
            else:
                print('*', end='')

        j+=1

    print()
    i+=1










