# 1. 띄워진 브라우저에서 원하는 페이지로 이동
# 이 예시에서는 이미 브라우저가 띄워져 있다는 가정하에 'https://www.google.com'으로 이동합니다.

# 2. 띄워진 브라우저에서 사용되는 웹 드라이버 포트 확인
# 띄워진 브라우저에서 사용되는 웹 드라이버 포트를 확인하려면
# 주소창에 'chrome://version'을 입력하고 엔터를 누르면 나오는 'Command Line' 항목에서 '--remote-debugging-port=xxxx' 값을 확인합니다.
# 이 예시에서는 포트 번호로 9222를 사용합니다.

from selenium.webdriver import Remote

url = 'http://localhost:9222' # 띄워진 브라우저의 URL
options = Remote.webdriver.ChromeOptions()
options.add_experimental_option('debuggerAddress', 'localhost:9222') # 띄워진 브라우저의 주소 및 포트 번호 입력
driver = Remote(command_executor=url, options=options)

# 3. 원격으로 브라우저 제어
# 이제 `driver` 변수를 사용하여 브라우저를 제어할 수 있습니다.
# 예를 들어, 구글 검색창에 '셀레니움'을 검색하려면 아래와 같이 작성합니다.
search_box = driver.find_element_by_name('q')
search_box.send_keys('셀레니움')
search_box.submit()