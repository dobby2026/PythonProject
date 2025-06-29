"""
파일명: Ex17-06-Exception.py

"""
import traceback

try:
    raise Exception('강제로 발생시킨 예외')
except Exception as e:
    print('발생한 예외 메시지는 다음과 같습니다')
    print(e)
    traceback.print_exc()