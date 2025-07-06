"""
파일명: Ex18-06-selenium.py

selenium 패키지
    어플리케이션 테스트하기 위한 프레임웍
    웹 어플리케이션 다양한 브라우저 동작 테스트용!
    크롤링으로 많이 사용된다

패키지 설치
    pip install selenium
    pip install webdriver-manager

** 패키지설치 에러시 **
    visual studio build tools 설치 >> C++ 빌드 설치
"""

# import traceback

import os
import time
import urllib.request

from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from webdriver_manager.chrome import ChromeDriverManager

def scroll_to_end(driver):
    """스크롤을 끝까지 내려서 모든 이미지를 로드 하는 함수"""

    previous_image_count = 0
    no_change_count = 0

    while True:
        # 페이지 끝까지 스크롤
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # 페이지가 로드될 시간 대기
        time.sleep(2)

        thumbnails = driver.find_elements(By.CSS_SELECTOR, '.H8Rx8c')
        current_image_count = len(thumbnails)

        print(f'현재 로드된 이미지 수: {current_image_count}')

        # 이미지 수가 변하지 않으면 카운트 증가
        if current_image_count == previous_image_count:
            no_change_count += 1

            print(f'이미지 수 변화 없음({no_change_count})')

            # 3번 연속 변화가 없으면 종료
            if no_change_count >= 3:
                print('더 이상 로드할 이미지가 없습니다. 스크롤 완료!')
                break
        else:
            no_change_count = 0

        previous_image_count = current_image_count

    final_thumbnails = driver.find_elements(By.CSS_SELECTOR, '.H8Rx8c')
    print(f'총 {len(final_thumbnails)}개의 이미지를 찾았습니다.')
    return final_thumbnails

def download_images(keyword, num_images=10, output_dir='images'):

    # Chrome driver 자동 설치 및 서비스 생성
    service = Service(ChromeDriverManager().install())

    # Chrome 드라이버 인스턴스 생성
    driver = webdriver.Chrome(service=service)

    # 드라이버를 통해 Google 페이지 접속
    driver.get('https://images.google.com/')

    """
    <textarea class="gLFyf" aria-controls="Alh6id" aria-owns="Alh6id" autofocus="" title="검색" value="" aria-label="검색" placeholder="" aria-autocomplete="both" aria-expanded="false" aria-haspopup="false" autocapitalize="off" autocomplete="off" autocorrect="off" id="APjFqb" maxlength="2048" name="q" role="combobox" rows="1" spellcheck="false" jsaction="paste:puy29d" data-ved="0ahUKEwipncublqWOAxVuoa8BHYloGaIQ39UDCAM" aria-activedescendant="" style=""></textarea>
    """
    search_bar = driver.find_element(By.NAME, 'q')
    search_bar.send_keys(keyword)
    search_bar.send_keys(Keys.RETURN)

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)


    time.sleep(2)
    # thumbnails = driver.find_elements(By.CSS_SELECTOR, '.H8Rx8c')
    thumbnails = scroll_to_end(driver)


    for idx, thumbnail in enumerate(thumbnails[:num_images]):

        try:
            thumbnail.click()
            time.sleep(2)


            # sFlh5c FyHeAf iPVvYb
            image = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, '.sFlh5c.FyHeAf.iPVvYb')
                )
            )

            # 이미지 url 가져오기
            image_url = image.get_attribute('src')

            if image_url.startswith('data:'):
                continue

            print(image_url)

            check_ext = ['jpg', 'jpeg', 'png', 'gif']

            ext = image_url.split('.')[-1].split('?')[0].lower()
            if not ext in check_ext:
                continue

            headers = {'User-Agent': 'Mozilla/5.0'}

            request = urllib.request.Request(image_url, headers=headers)
            with urllib.request.urlopen(request) as response:
                with open(f'{output_dir}/{keyword}_{idx}.{ext}', 'wb') as file:
                    file.write(response.read())
        except TimeoutException as te:
            print(f'{idx} - continue')
            continue
        except:
            print('알수 없는 에러!')
            continue


    time.sleep(10)

    # 드라이버 종료
    driver.quit()

# 실행코드
keyword = '차은우'
num_images = 1000
output_dir = 'images'
# 이미지 다운로드 함수 호출
download_images(keyword, num_images, output_dir)