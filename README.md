# SNU_sugang_helper
서울대학교 수강신청에 도움이 될만한 Selenium 기반 여석 확인 프로그램입니다.  
코드 내부에 있는 HOW TO USE 를 참고하시길 바랍니다.  

qowodyd0116@snu.ac.kr
## 실행시 모습
![Image1](./sample.JPG)

## 사용 설명 추가 (08/12/2022)
* Woohyeon Baek (whnbaek@gmail.com)에 의해 수정

1. Linux 환경에서 Chrome 설치 (stable version)
```
$ wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
$ sudo apt install -y ./google-chrome-stable_current_amd64.deb
```

2. 그밖의 필요한 패키지 설치
```
$ sudo apt install -y ffmpeg                       # alarm 실행을 위함
$ pip install selenium, numpy, webdriver-manager   # 프로그램에 필요한 파이썬 패키지
```

이하 설명은 `sugang_crawl.py` 내 HOW TO USE에 적혀있음

## 수정사항 (08/16/2022)
1. 잔여좌석 존재 시 알람음 출력
2. 분반 검색 기능 추가 ex. 035.001(001) (전체 분반 검색은 035.001 와 같이 하면 됨)
3. 학과명, 교수명 등 누락 시 출력 형태 오류 수정
