import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
import time
import easyocr
import chromedriver_autoinstaller
chromedriver_autoinstaller.install()
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

class NoSeat(Exception):
    def __str__(self) -> str:
        return '좌석 없음'

# 좌석 탐색
def select():
    print('******************************select')
    part1 = 0 # 구역 번호 
    part2 = 1 # 세부 구역 번호 
    trNum = 3
    seatCount = 2 # 선택할 좌석 개수 
    # driver.switch_to.window(driver.window_handles[-1])
    # driver.switch_to.frame(driver.find_element(By.XPATH,'//*[@id="ifrmSeat"]'))
    
    while True:
        try:
            part1Xpath = '//*[@id="GradeRow"]/td[1]/div/span[2]'
            # part2Xpath = '//*[@id="GradeDetail"]/div/ul/li[{0}]/a'.format(part2)
            part2Xpath = '/html/body/form[1]/div/div[1]/div[3]/div/div[1]/div/div/div/div/table/tbody/tr[{0}]/td/div/ul/li[{1}]/a'.format(trNum ,part2)
            # 구역선택
            driver.find_elements(By.XPATH,part1Xpath)[part1].click()
            
            # 세부구역 선택
            driver.find_element(By.XPATH,part2Xpath).click()
            
            
            #좌석선택
            driver.switch_to.frame(driver.find_element(By.XPATH,'//*[@id="ifrmSeatDetail"]'))
            getSeats = driver.find_elements(By.XPATH,'//*[@id="Seats"]') # 남은 좌석 가져오기 
            print('남은 좌석 개수: {3}, part1: {0}, part2: {1}, trNum: {2}'.format(part1, part2, trNum, len(getSeats)))
            # print('남은 좌석 개수 가져오기 : {0}'.format(len(getSeats)))
            
            currentSeat = 0 # 선택한 좌석 개수
            if len(getSeats) > 1 :
                    for Seat in getSeats :
                        Seat.click()
                        currentSeat = currentSeat + 1
                        print('선택한 좌석 currentSeat: {0}'.format(currentSeat))
                        if currentSeat == seatCount :
                            time.sleep(1)
                            # 다음단계 버튼 클릭 
                            print('다음단계 버튼 클릭')
                            driver.switch_to.default_content()
                            driver.switch_to.frame(driver.find_element(By.XPATH,'//*[@id="ifrmSeat"]'))
                            driver.find_element(By.XPATH,'//*[@id="NextStepImage"]').click()
                            break
            else: 
                print('좌석 없음')
                raise NoSeat
        
            # payment()
            break
        except Exception as ex:
            print('******************************다시선택')
            print(ex)
            driver.switch_to.default_content()
            driver.switch_to.frame(driver.find_element(By.XPATH,'//*[@id="ifrmSeat"]'))
            driver.find_elements(By.XPATH,part1Xpath)[part1].click()
            # 세부 구역 번호 1 or 2
            if part2 == 1:
                part2 = 2
            elif part2 == 2:
                part2 = 1
                # 구역 번호 0 or 1
                if part1 == 0:
                    part1 = 1
                    trNum = 5
                elif part1 == 1:
                    part1 = 0
                    trNum = 3
                
            time.sleep(0.5)
            

def payment():
    print('******************************payment')
    try: 
        # driver.switch_to.default_content()
        # driver.switch_to.frame(driver.find_element(By.XPATH,'//*[@id="ifrmSeat"]'))
        # driver.find_element(By.XPATH,'//*[@id="NextStepImage"]').click()
            
        #가격선택
        driver.switch_to.default_content()
        driver.switch_to.frame(driver.find_element(By.XPATH, "//*[@id='ifrmBookStep']"))
        
        select = Select(driver.find_element(By.XPATH, '//*[@id="PriceRow002"]/td[3]/select'))
        
        select.select_by_index(1)
        driver.switch_to.default_content()
        driver.find_element(By.XPATH,'//*[@id="SmallNextBtnImage"]').click()

        #주문자 확인
        driver.switch_to.frame(driver.find_element(By.XPATH, "//*[@id='ifrmBookStep']"))
        driver.find_element(By.XPATH,'//*[@id="YYMMDD"]').send_keys('010302')
        driver.switch_to.default_content()
        driver.find_element(By.XPATH,'//*[@id="SmallNextBtnImage"]').click()

        #결제
        driver.switch_to.frame(driver.find_element(By.XPATH,'//*[@id="ifrmBookStep"]'))
        driver.find_element(By.XPATH,'//*[@id="Payment_22004"]/td/input').click()
                
        select2 = Select(driver.find_element(By.XPATH, '//*[@id="BankCode"]'))
        select2.select_by_index(1)
        driver.switch_to.default_content()
        driver.find_element(By.XPATH,'//*[@id="SmallNextBtnImage"]').click()
                
        driver.switch_to.frame(driver.find_element(By.XPATH,'//*[@id="ifrmBookStep"]'))
        driver.find_element(By.XPATH,'//*[@id="checkAll"]').click()
        driver.switch_to.default_content()
        driver.find_element(By.XPATH,'//*[@id="LargeNextBtnImage"]').click()
        
    except Exception as ex:
        print(ex)
        time.sleep(0.5)
        

#consert_url = 'https://tickets.interpark.com/goods/24007166' # 싸이 콘서트 (과천)

# consert_url = 'https://tickets.interpark.com/goods/24004862' # 테스트 1 
# consert_url = 'https://tickets.interpark.com/goods/24007889' # 테스트 2
consert_url = 'https://tickets.interpark.com/goods/24006691' # Test 3


# 사이트 열기 
co = Options()
co.add_experimental_option('debuggerAddress', '127.0.0.1:9222')
driver = webdriver.Chrome(options=co)
driver.get(url=consert_url)

for i in range(0, 10) :
    time.sleep(10)
    print('---{0}분 경과----'.format(i+1))

# 예매하기 버튼 클릭 
print('예매하기 버튼 클릭--------------------')
print(driver.window_handles)
driver.switch_to.window(driver.window_handles[-1])
while True:
    try:
        selectprod = driver.find_element(By.XPATH,'//*[@id="productSide"]/div/div[2]/a[1]')
        print(selectprod)
        selectprod.click()
    except:
        continue
        time.sleep(0.1)
    break;
    

# 예매 창 전환
issub = False
while issub:
    try: 
        print('예매 창 전환 --------------------')
        print(driver.window_handles)
        driver.switch_to.window(driver.window_handles[-1])

        driver.switch_to.frame((driver.find_element(By.XPATH, "//*[@id='ifrmSeat']")))
    except Exception as ex:
        print(ex)
        time.sleep(0.5)
        continue
    issub = True
        
 

# 부정예매방지 문자
reader = easyocr.Reader(['en'])
capchaPng = None
while True:
    try:
        print('부정예매방지 문자 --------------------')
        driver.switch_to.window(driver.window_handles[-1])
        driver.switch_to.frame(driver.find_element(By.XPATH,'//*[@id="ifrmSeat"]'))
        
        capchaPng = driver.find_element(By.XPATH,'//*[@id="imgCaptcha"]')
    
    except Exception as ex:
        print(ex)
        continue
        
    break
    

try:
    # capchaPng = driver.find_element(By.XPATH,'//*[@id="imgCaptcha"]')

    while capchaPng:
        print('---------------capcha')
        result = reader.readtext(capchaPng.screenshot_as_png, detail=0)
        capchaValue = result[0].replace(' ', '').replace('5', 'S').replace('0', 'O').replace('$', 'S').replace(',', '')\
            .replace(':', '').replace('.', '').replace('+', 'T').replace("'", '').replace('`', '')\
            .replace('1', 'L').replace('e', 'Q').replace('3', 'S').replace('€', 'C').replace('{', '').replace('-', '')
            
        # 입력
        driver.find_element(By.XPATH,'//*[@id="divRecaptcha"]/div[1]/div[3]').click()
        chapchaText = driver.find_element(By.XPATH,'//*[@id="txtCaptcha"]')
        chapchaText.send_keys(capchaValue)
            
        #입력완료 버튼 클릭
        driver.find_element(By.XPATH,'//*[@id="divRecaptcha"]/div[1]/div[4]/a[2]').click()

        display = driver.find_element(By.XPATH,'//*[@id="divRecaptcha"]').is_displayed()
        if display:
            # 새로고침
            driver.find_element(By.XPATH,'//*[@id="divRecaptcha"]/div[1]/div[1]/a[1]').click()
        else:
            select()
            break
except Exception as ex:
    print(ex)


# select()