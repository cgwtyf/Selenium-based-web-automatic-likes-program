from selenium import webdriver as web
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver import ChromeOptions
import pyautogui
import pyperclip
import time


#模拟点击
def mouseClick(img):
    location=pyautogui.locateCenterOnScreen(img)
    if location is not None:
        pyautogui.click(location.x,location.y,clicks=1,button="left")
        print("点击成功")
        return True
    else:
        print("没找到图片")
        return False
    
#模拟拖动滑块
def dragSlider(img):
    location=pyautogui.locateCenterOnScreen(img)
    if location is not None:
        pyautogui.moveTo(location.x, location.y, duration=1)
        # pyautogui.click(location.x+316,location.y+0,clicks=1,interval=1,button="left")
        pyautogui.dragTo(location.x+400,location.y, duration=0.1)  # drag mouse to XY
        print("拖动成功")
        return True
    else:
        print("没找到滑块")
        return False



#自定义文章关键词
keyWord=input("请输入您想点赞的博主的文章关键词或文章标题：")


#打开驱动
wd=web.Chrome()
wd.maximize_window()
wd.implicitly_wait(20)

# 绕过浏览器检测
option = ChromeOptions()
option.add_experimental_option('excludeSwitches', ['enable-automation'])
option.add_argument("disable-blink-features=AutomationControlled")
option.add_experimental_option('useAutomationExtension', False)
wd.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
    "source": """
    Object.defineProperty(navigator, 'webdriver', {
      get: () => false
    })
  """
})


# 进CSDN
wd.get("https://www.csdn.net/")


# 登录
login=wd.find_element(By.CSS_SELECTOR,"#csdn-toolbar > div > div > div.toolbar-container-right > div > div.toolbar-btn.toolbar-btn-login.toolbar-btn-login-new.csdn-toolbar-fl > a")
login.click()

# time.sleep(2)

# 选择密码登录
for i in range(5):#这里有时候图片加载慢，写一下隐式等待
    if mouseClick("login.png"):
        break
    time.sleep(0.5)

time.sleep(1)
# 输入账号
mouseClick("account.png")
# time.sleep(0.5)
pyperclip.copy("你的账号")
pyautogui.hotkey("ctrl","v")
# time.sleep(0.5)

# 输入密码
mouseClick("password.png")
# time.sleep(0.5)
pyperclip.copy("你的密码")
pyautogui.hotkey("ctrl","v")
# time.sleep(0.5)

# 点击登录
mouseClick("login_button.png")
time.sleep(0.1)

# 处理一下滑块
# 关键时刻还是得pyautogui hhh
for i in range(5):#手写一个隐式等待,时长为5秒
    location=pyautogui.locateCenterOnScreen("slider.png")
    if location is not None:
        dragSlider("slider.png")
        break
    time.sleep(1)

#检查是否弹出刷新 发现只要拖滑块的时候骗得过CSDN就不会弹出刷新  如果后面遇到弹出再说吧
for i in range(2):#这里可以把循环次数设短一点，因为这个刷新一旦要弹出就会很快
    location=pyautogui.locateCenterOnScreen("update.png")
    if location is not None:
        mouseClick("update.png")
        time.sleep(1)
        #重新拖滑块
        while True:#手写一个隐式等待
            if dragSlider("slider.png"):
                break
            time.sleep(1)
    else:
        time.sleep(0.5)


# 再次点击登录
mouseClick("login_button.png")
time.sleep(1)

# 搜索
search=wd.find_element(By.CSS_SELECTOR,"#toolbar-search-input")
search.send_keys(keyWord+"\n")

# 切换到新标签页-
time.sleep(3)
tips= wd.window_handles
wd.switch_to.window(tips[1])

# 定位到第一篇文章
paper=wd.find_element(By.CSS_SELECTOR,"#app > div.so-list-detail > div.main.clearfix > div.main-lt > div.list-container > div > div.list-item.isFirst > div > div.item-hd > h3 > a")
if paper != None:
    paper.click()
else:
    print("没找到文章")


# 切换到新标签页
time.sleep(3)
tips= wd.window_handles
wd.switch_to.window(tips[-1])

# 再来一个隐式等待
while True:#不点赞不罢休
    if mouseClick("like.png"):
        print("点赞成功")
        break
    else:
        time.sleep(1)

input()

