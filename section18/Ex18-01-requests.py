"""
Ex18-01-requests.py

requests 라이브러리
    Http 요청을 보내기 위한 간편하고 인기있는 라이브러리
    이를 사용하여 웹페이지 데이터를 가져오거나,
    API와 상호 작용할 수 있다

라이브러리 설치 방법
pip install requests

https://n.news.naver.com/article/015/0005150831?ntype=RANKING

URL(Uniform Resource Locator)
    인터넷에서 웹페이지, 이미지, 동영상 등과 같은 리소스를 찾을 수 있는 주소

프로토콜(protocol)
    네트워크를 통해 통신을 수행히기 위한 표준화된 규칙, 절차, 통신 프로세스를 의미

    ex) http/https - 웹 서버 프로토콜
        ftp - 파일서버 프로토콜
        mailto - 메일 서버 프로토콜
        telnet - 원격지 프로토콜
호스트(host)
    리소스가 위치한 서버의 이름
    ex) n.news.naver.com

포트(Port)
    서버에서 사용하는 방번호
    ex) http - 80, https - 443

경로(Path)
    웹 서버에서 자원에 대한 경로
    ex) /article/015/0005150831

쿼리(Query)
    추가로 서버에 보내는 데이터 (Parameter)
    ex) ?
        ntype=RANKING

"""

import requests

url = 'https://n.news.naver.com/article/015/0005150831?ntype=RANKING'

response = requests.get(url)
print(response.text)
