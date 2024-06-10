from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time
import easyocr
import chromedriver_autoinstaller
chromedriver_autoinstaller.install()
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

part1 = 2 # 구역 번호 
part2 = 1 # 세부 구역 번호 
seatCount = 2 # 선택할 좌석 개수 

part1Xpath = '//*[@id="GradeRow"]/td[1]/div/span[{part1}]'
part2Xpath = '//*[@id="GradeDetail"]/div/ul/li[{part2}]/a'

print(part1Xpath)
print(part2Xpath)

part1Xpath = '//*[@id="GradeRow"]/td[1]/div/span[{0}]'.format(part1)
part2Xpath = '//*[@id="GradeDetail"]/div/ul/li[{0}]/a'.format(part2)

print(part1Xpath)
print(part2Xpath)

def GoInterpark(url) : 
    option = Options()
    option.add_argument("user-data-dir=C:/ChromeTEMP")
    option.add_argument("disable-blink-features=AutomationControlled")
    option.add_experimental_option("detach", True)
    option.add_experimental_option("excludeSwitches", ["enable-logging"])

    driver = webdriver.Chrome(options=option)
    driver.maximize_window()

    driver.get(url=url)
    
# 좌석 탐색
def select():
    print('******************************select seat')
   
    # driver.switch_to.window(driver.window_handles[-1])
    # driver.switch_to.frame(driver.find_element(By.XPATH,'//*[@id="ifrmSeat"]'))

    # 구역선택
    driver.find_element(By.XPATH,'//*[@id="GradeRow"]/td[1]/div/span[2]').click()
    
    while True:
        # 세부구역 선택
        try:
            driver.find_element(By.XPATH,'//*[@id="GradeDetail"]/div/ul/li[2]/a').click()
            driver.switch_to.frame(driver.find_element(By.XPATH,'//*[@id="ifrmSeatDetail"]'))
     
            driver.find_element(By.XPATH,'//*[@id="Seats"]').click()
        #   driver.find_element(By.XPATH,'//*[@id="Seats"]').click()
            payment()
            break
        except:
            print('******************************다시선택')
            driver.switch_to.default_content()
            driver.switch_to.frame(driver.find_element(By.XPATH,'//*[@id="ifrmSeat"]'))
            # driver.find_element(By.XPATH,'/html/body/form[1]/div/div[1]/div[3]/div/p/a/img').click()
            time.sleep(1)     
    

def payment():
    print('******************************payment')
    #좌석선택
    driver.switch_to.default_content()
    driver.switch_to.frame(driver.find_element(By.XPATH,'//*[@id="ifrmSeat"]'))
    driver.find_element(By.XPATH,'//*[@id="NextStepImage"]').click()

    #가격선택
    driver.switch_to.default_content()
    driver.switch_to.frame(driver.find_element(By.XPATH, "//*[@id='ifrmBookStep']"))
    select = Select(driver.find_element(By.XPATH, '//*[@id="PriceRow001"]/td[3]/select'))
    select.select_by_index(1)
    driver.switch_to.default_content()
    driver.find_element(By.XPATH,'//*[@id="SmallNextBtnImage"]').click()

    #주문자 확인
    driver.switch_to.frame(driver.find_element(By.XPATH, "//*[@id='ifrmBookStep']"))
    driver.find_element(By.XPATH,'//*[@id="YYMMDD"]').send_keys('010302')
    driver.switch_to.default_content()
    driver.find_element(By.XPATH,'//*[@id="SmallNextBtnImage"]').click()

    #결제
    # driver.switch_to.frame(driver.find_element(By.XPATH,'//*[@id="ifrmBookStep"]'))
    # driver.find_element(By.XPATH,'//*[@id="Payment_22004"]/td/input').click()
            
    # select2 = Select(driver.find_element(By.XPATH, '//*[@id="BankCode"]'))
    # select2.select_by_index(1)
    # driver.switch_to.default_content()
    # driver.find_element(By.XPATH,'//*[@id="SmallNextBtnImage"]').click()
            
    # driver.switch_to.frame(driver.find_element(By.XPATH,'//*[@id="ifrmBookStep"]'))
    # driver.find_element(By.XPATH,'//*[@id="checkAll"]').click()
    # driver.switch_to.default_content()
    # driver.find_element(By.XPATH,'//*[@id="LargeNextBtnImage"]').click()
