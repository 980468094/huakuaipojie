from selenium import webdriver
import time
chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument('--headless') # 隐藏浏览器
driver=webdriver.Chrome('chromedriver.exe',options=chrome_options) # 浏览器对象
driver.set_window_size(width=1920,height=1080)
#driver.get('http://www.baidu.com') # 加载百度页面 和浏览器加载的形式一样 js，css
url='https://music.163.com/#/song?id=864506579'
driver.get(url) # 加载完毕以后，页面的所有东西都在driver中
#driver.save_screenshot('test.jpg')
driver.switch_to_frame('g_iframe')  # 切换页面
for i in range(2):
    js = "var q=document.documentElement.scrollTop=100000"  # 执行js固定翻页代码
    driver.execute_script(js)
    nodes=driver.find_elements_by_xpath('//div[@class="cnt f-brk"]')
    for node in nodes:
        print(node.text)
    a=driver.find_element_by_xpath('//a[text()="下一页"]') # 获取下一页的a标签
    a.click()  # 触发单击事件
    time.sleep(1) # 让浏览器加载一会
    print('-----------')