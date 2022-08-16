from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import numpy as np
import time
from subprocess import call

from datetime import datetime
import re
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class GetCourseData:

    def __init__(self):
        # 옵션 생성
        options = webdriver.ChromeOptions()
        # 창 숨기는 옵션 추가
        options.add_argument("headless")

        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

        self.driver.get('https://sugang.snu.ac.kr/')
        self.wait = WebDriverWait(self.driver, 10)

        print("Driver Connected to URL")

    def main_page(self):
        # Go to the main page
        self.driver.switch_to.default_content()
        self.wait.until(EC.frame_to_be_available_and_switch_to_it((By.ID, "main")))
        content = self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="header"]/div[2]/div[1]/h1')))
        content.click()

    def crawl_data(self, *course_list):
        while True:
            for course_id in course_list:
                self.course_data(course_id)

    def course_data(self, course_id: str):
        pos = course_id.find('(')
        keyword = course_id if pos == -1 else course_id[: pos]

        # search - In main page
        self.main_page()

        # Go to search page
        self.driver.switch_to.default_content()
        self.wait.until(EC.frame_to_be_available_and_switch_to_it((By.ID, "main")))
        content = self.wait.until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="header"]/div[2]/div[1]/button[1]')))
        content.click()

        # Send key and wait for search results
        content = self.wait.until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="hMobileTotalSearch"]')))
        content.send_keys(f"{keyword}")
        content = self.wait.until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="HD100"]/div/div/div[1]/fieldset/div[3]/button[1]')))
        content.click()

        # Get course data
        self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "course-info-detail")))

        contents = self.driver.find_elements(By.CLASS_NAME, "course-info-detail")

        # Printing results
        for content in contents:
            html = content.get_attribute('innerHTML')
            data = re.compile("[]가-힣[0-9:A-Z.()· ~]+").findall(html)
            data = [i for i in data if i != " "]
            # 유형 # 강의 제목 # 교수 # 학과 # 코드 # 수강신청인원 # 정원(재학생) # 현재인원 # 가능인원(재학생)
            # 학점 # 학점(int) # 수업시간 ---- "관심강좌" "인원"
            idx = np.where(np.isin(data, "총수강인원 "))[0][0]
            curr_num = int(data[idx - 2])
            max_num = int(data[idx - 1].split(sep=" ")[0])
            if curr_num < max_num and course_id in data[idx - 5]:
                print("현재 시간 : ", datetime.now())
                for i in range(idx - 4):
                    print(data[i], end = ' ')
                print("인원 현황 : ", f"{data[idx - 2]}/{data[idx - 1]}")
                print("수강신청 가능 - 잔여 여석 : ", f"{max_num - curr_num}")
                call(['ffplay', 'alarm.mp3', '-t', '0.9', '-autoexit', '-nodisp', '-hide_banner', '-loglevel', 'error'])
        time.sleep(3)


if __name__ == "__main__":
    """
    HOW TO USE
    app.crawl_data(*args) 함수의 *args 에 자신이 찾고자 하는 수업의 ID 값을 연속적으로 입력.
    ex) app.crawl_data("406.304", "4190.407", "4190.408", "430.329")
    
    ※ 서버 자체에 트래픽이 과다해지는 경우 오류가 발생할 수 있습니다.
    ※ 그럴경우 self.wait 의 변수 10초를 더욱 증가시켜 해결될 수 있으나(20, 30 등), 
      오류가 발생하지 않으리라고는 보장할 수 없습니다.
    """

    app = GetCourseData()
    # "406.304", "4190.407", "4190.408", "430.329", "M0000.000500",
    # "M1522.000600", "M2177.003100", "M2177.004300", "M3244.000400"
    # 분반 검색: "035.001(001)", "035.001(002)", etc

    app.crawl_data("045.012(005)")
