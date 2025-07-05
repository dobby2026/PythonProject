"""
파일명: Ex18-05-getRankPage.py


https://music.bugs.co.kr/chart

<p class="title" adult_yn="N">
<a href="javascript:;" adultcheckval="1" onclick="bugs.wiselog.area('list_tr_09_chart');bugs.music.listen('6316357',true);
" title="FAMOUS" aria-label="새창">FAMOUS</a>
</p>

<p class="artist">
<a href="https://music.bugs.co.kr/artist/80408176?wl_ref=list_tr_10_chart" title="ALLDAY PROJECT" onclick="
">ALLDAY PROJECT</a>
</p>

"""

import requests
from bs4 import BeautifulSoup
url = 'https://music.bugs.co.kr/chart'
response = requests.get(url)

html = response.text

soup = BeautifulSoup(html, 'html.parser')
title_list = soup.find_all('p', class_='title')
artist_list = soup.find_all('p', class_='artist')

for idx, title in enumerate(title_list, 1):
    artist = artist_list[idx-1].find_all('a')[0]
    print(f'{idx} {title.text.strip()} - {artist.text.strip()}')

