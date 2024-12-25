import os
import sys
import time
import psutil
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urlparse
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

def check_route_cookie(driver):#检查cookie是否有效
    """
    检查当前页面的 cookies 中是否包含特定的 route 值。

    参数:
    driver: WebDriver 实例

    返回:
    1 - 如果 cookies 中存在 route 且其值为 "adef3cfba742b03d8aed0b1f92f60144"
    0 - 否则
    """
    try:
        # 获取当前页面的所有 cookies
        cookies = driver.get_cookies()

        # 遍历 cookies，检查是否存在目标 route 值
        for cookie in cookies:
            if cookie['name'] == 'route' and cookie['value'] == 'adef3cfba742b03d8aed0b1f92f60144':
                return 1
        return 0  # 如果未找到符合条件的 route 值，则返回 0
    except Exception as e:
        print(f"检查 cookie 时发生错误: {e}")
        return 0



def modify_cookie_and_navigate(driver):#修改cookie并重跳登录界面
    """
    当 `check_route_cookie(driver)` 返回 0 时，修改当前页面的 cookie 中的 route 值，
    刷新页面后跳转到指定链接。
    """
    # 检查 cookie 中的 route 值
    if check_route_cookie(driver) == 0:
        # 修改 cookie 的 route 值
        new_cookie = {
            'domain': urlparse(driver.current_url).netloc,  # 使用当前页面的域名
            'name': 'route',
            'path': '/',
            'value': 'adef3cfba742b03d8aed0b1f92f60144'
        }
        driver.delete_cookie('route')  # 删除旧的 route cookie
        driver.add_cookie(new_cookie)  # 添加新的 route cookie

        print("已修改 cookie 中的 route 值为 'adef3cfba742b03d8aed0b1f92f60144'")
    
        # 刷新页面
    
    # 跳转到指定页面
    navigate_with_retry(driver, "https://portal.nxist.com/sso/dskjlogin")


# 示例调用
# from selenium import webdriver
# driver = webdriver.Edge()
# driver.get("https://example.com")  # 替换为实际页面
# modify_cookie_and_navigate(driver)

def navigate_with_retry(driver, url, retries=3, wait_time=5):#带重试功能的打开链接
    attempt = 0
    while attempt < retries:
        try:
            driver.get(url)  # 尝试访问URL
            return  # 如果成功访问，则直接返回
        except WebDriverException as e:
            if 'ERR_CONNECTION_TIMED_OUT' in str(e):  # 如果是连接超时错误
                print(f"连接超时，正在重试 {attempt + 1}/{retries}...")
                attempt += 1
                time.sleep(wait_time)  # 等待一段时间后重试
                driver.refresh()  # 刷新页面
            else:
                print(f"发生错误：{e}")
                break
    print("所有重试次数已用完，无法加载页面。")

# 使用示例
#driver = webdriver.Edge()  # 或者你使用其他浏览器，例如 Chrome
#url = "https://portal.nxist.com/sso/dskjlogin"
#navigate_with_retry(driver, "https://portal.nxist.com/sso/dskjlogin")


# 启动 Edge 浏览器并打开指定的初始页面
def start_browser_initial_page():
    options = webdriver.ChromeOptions()
    options.add_argument('--start-maximized')  # 启动时最大化窗口
    driver = webdriver.Chrome(options=options)
    navigate_with_retry(driver, "https://www.baidu.com/")
    update_status_in_browser(driver, "欢迎使用小易教务快速登录系统！2秒后自动打开教务系统！")
    return driver

# 检查并确保浏览器进入指定域名
def check_and_navigate_to_correct_domain(driver):
    navigate_with_retry(driver, "https://portal.nxist.com/sso/dskjlogin")
      # 跳转到登录页面
    while True:
        current_url = driver.current_url
        parsed_url = urlparse(current_url)
        current_domain = parsed_url.netloc  # 获取域名部分
        
        if current_domain in ["portal.nxist.com", "10.100.100.141", "cas.nist.edu.cn", "login.work.weixin.qq.com"]:
            update_status_in_browser(driver, f"已进入指定域名: {current_domain}")
            break  # 如果是指定域名，退出循环
        else:
            update_status_in_browser(driver, f"当前域名 ({current_domain}) 非预期，正在跳转...")
            navigate_with_retry(driver, "https://portal.nxist.com/sso/dskjlogin")  # 跳转到指定页面


        time.sleep(1)  # 每秒检查一次

    update_status_in_browser(driver, "欢迎使用小易教务快速登录系统！若界面非登录界面请复制连接打开（多试几次）：https://portal.nxist.com/sso/dskjlogin")



def new_cookie(driver):  
    

    # 定义要添加的 Cookie
    new_cookie = {
        "domain": "10.100.100.141",
        "name": "route",
        "path": "/",
        "value": "adef3cfba742b03d8aed0b1f92f60144"
    }

    # 添加 Cookie
    driver.add_cookie(new_cookie)

    # 验证 Cookie 是否添加成功
    cookies = driver.get_cookies()
    print(f"当前所有 Cookies: {cookies}")


def new_cookie1(driver): 
    # 获取当前页面的所有 cookies 
    cookies = driver.get_cookies() 
     
    # 创建新的 route cookie（JSON字符串）
    new_route_cookie_str = '{"domain": "portal.nxist.com", "name": "route", "path": "/", "value": "adef3cfba742b03d8aed0b1f92f60144"}'
    
    # 将 JSON 字符串解析为字典
    new_route_cookie = json.loads(new_route_cookie_str)
 
    # 将旧 cookie 和新创建的 route cookie 一起添加到浏览器 
    for cookie in cookies: 
        driver.delete_cookie(cookie['name'])  # 删除旧的 cookie（确保不会重复） 
        driver.add_cookie(cookie)  # 重新添加原有 cookie 
    
    # 添加新创建的 route cookie 
    driver.add_cookie(new_route_cookie) 
    update_status_in_browser(driver, "test")  # 显示 
    
    
    # 刷新页面 
    driver.refresh() 
    update_status_in_browser(driver, "已添加新的 route cookie，正在刷新页面...")
    time.sleep(1) 

def update_status_in_browser(driver, message):
    script = f"""
        var statusDiv = document.getElementById("status");

        if (!statusDiv) {{
            statusDiv = document.createElement("div");
            statusDiv.id = "status";
            statusDiv.style.position = "fixed";
            statusDiv.style.top = "10px";
            statusDiv.style.left = "10px";
            statusDiv.style.padding = "10px";
            statusDiv.style.backgroundColor = "rgba(0, 0, 0, 0.7)";
            statusDiv.style.color = "white";
            statusDiv.style.fontSize = "16px";
            statusDiv.style.zIndex = "9999";
            document.body.appendChild(statusDiv);
        }}

        statusDiv.innerText = "{message}";
    """
    try:
        driver.execute_script(script)
    except Exception as e:
        print(f"执行 JavaScript 时出错: {e}")




# 检查当前页面域名是否为指定的域名
def check_and_wait_for_correct_domain(driver):
    update_status_in_browser(driver, "正在检测当前页面域名...")
    
    while True:
        current_url = driver.current_url
        parsed_url = urlparse(current_url)
        current_domain = parsed_url.netloc  # 获取域名部分
        
        if current_domain in ["portal.nxist.com", "10.100.100.141","cas.nist.edu.cn","login.work.weixin.qq.com"]:
            update_status_in_browser(driver, f"已进入指定域名: {current_domain}")
            break  # 如果是指定域名，退出循环
        else:
            update_status_in_browser(driver, f"当前域名 ({current_domain}) 非预期，正在跳转...")
            navigate_with_retry(driver, "https://portal.nxist.com/sso/dskjlogin")  # 跳转到指定页面


        time.sleep(1)  # 每秒检查一次

# 检查当前页面域名是否为指定的域名
def check_and_wait_for_correct_domain1(driver):
    update_status_in_browser(driver, "正在检测当前页面域名...")
    
    while True:
        current_url = driver.current_url
        parsed_url = urlparse(current_url)
        current_domain = parsed_url.netloc  # 获取域名部分
        
        if current_domain in ["portal.nxist.com", "10.100.100.141","cas.nist.edu.cn"]:
            update_status_in_browser(driver, f"已进入指定域名: {current_domain}")
            break  # 如果是指定域名，退出循环
        else:
            update_status_in_browser(driver, f"当前域名 ({current_domain}) 非预期，正在跳转...")
            navigate_with_retry(driver, "https://portal.nxist.com/sso/dskjlogin")  # 跳转到指定页面


        time.sleep(1)  # 每秒检查一次

# 等待页面加载完成，直到页面 URL 包含特定字符串
def wait_for_login(driver):#防跳转其他界面。
    #check_and_wait_for_correct_domain(driver)  # 检查并等待正确域名

    #current_url = driver.current_url
   # parsed_url = urlparse(current_url)
   # current_domain = parsed_url.netloc  # 获取域名部分
    while True:
        current_url = driver.current_url
        parsed_url = urlparse(current_url)
        current_domain = parsed_url.netloc
        if current_domain!="cas.nist.edu.cn":
            check_and_wait_for_correct_domain
            break
        else:
            update_status_in_browser(driver, "欢迎使用小易教务快速登录系统！请耐心等待...")

        time.sleep(1)

    while True:
        current_url = driver.current_url
        parsed_url = urlparse(current_url)
        current_domain = parsed_url.netloc
        if current_domain!="login.work.weixin.qq.com":
            check_and_wait_for_correct_domain1
            break
        else:
            update_status_in_browser(driver, "欢迎使用小易教务快速登录系统！请耐心等待...")

        time.sleep(1)

    while True:
        current_url = driver.current_url
        parsed_url = urlparse(current_url)
        current_domain = parsed_url.netloc
        if current_domain!="cas.nist.edu.cn":
            check_and_wait_for_correct_domain
            break
        else:
            update_status_in_browser(driver, "欢迎使用小易教务快速登录系统！请耐心等待...")

        time.sleep(1)

    update_status_in_browser(driver, "欢迎使用小易教务快速登录系统！请耐心等待...")
    WebDriverWait(driver, 600).until(EC.url_contains("https://portal.nxist.com/jwglxt/xtgl/index_initMenu.html"))
    update_status_in_browser(driver, f"登录成功! 当前页面: {driver.current_url}")



# 获取当前页面的 cookies
def get_cookies(driver):
    update_status_in_browser(driver, "获取用户信息。。。")
    cookies = driver.get_cookies()

    return cookies

# 修改 cookies 中的 'route' 值
def modify_route_cookie(cookies, driver):
    for cookie in cookies:
        if cookie['name'] == 'route':
            cookie['value'] = 'adef3cfba742b03d8aed0b1f92f60144'  # 修改 route 值
            driver.delete_cookie('route')
            driver.add_cookie(cookie)
    update_status_in_browser(driver, "修改参数。。。")


# 刷新页面并获取更新后的 cookies
def refresh_and_get_cookies(driver):
    update_status_in_browser(driver, "向服务器请求内网登录。。。")
    driver.refresh()
    time.sleep(3)
     # 获取当前 cookies
    cookies = driver.get_cookies()


    # 查找并验证 'route' cookie
    route_cookie = next((cookie for cookie in cookies if cookie['name'] == 'route'), None)
    while True:
        if route_cookie and route_cookie['value'] == 'adef3cfba742b03d8aed0b1f92f60144':
            update_status_in_browser(driver, "route cookie 修改成功！")
            break
        else:
            update_status_in_browser(driver, "route cookie 修改失败，正在重试...")
        time.sleep(1)



    time.sleep(1)  # 等待页面刷新完成
    while True:
        current_url = driver.current_url
        parsed_url = urlparse(current_url)
        current_domain = parsed_url.netloc  # 获取域名部分
        
        if current_domain in ["portal.nxist.com", "10.100.100.141","cas.nist.edu.cn"]:
            update_status_in_browser(driver, f"已进入指定域名: {current_domain}")
            break  # 如果是指定域名，退出循环
        else:
            update_status_in_browser(driver, f"当前域名 ({current_domain}) 非预期，正在跳转...")
            navigate_with_retry(driver, "https://portal.nxist.com/jwglxt/xtgl/index_initMenu.html")
            

        time.sleep(1)  # 每秒检查一次
    cookies = driver.get_cookies()

    return cookies

# 将 cookies 写回浏览器
def set_cookies_in_browser(driver, cookies):
    update_status_in_browser(driver, "写入值。。。")
    for cookie in cookies:
        if isinstance(cookie, dict):  # 确保cookie是字典
            driver.delete_cookie(cookie['name'])
            driver.add_cookie(cookie)



# 打开目标页面
def open_target_page(driver):
    navigate_with_retry(driver, "http://10.100.100.141/jwglxt/xtgl/login_slogin.html")

    while True:
        current_url = driver.current_url
        parsed_url = urlparse(current_url)
        current_domain = parsed_url.netloc  # 获取域名部分
        
        if current_domain in ["portal.nxist.com", "10.100.100.141","cas.nist.edu.cn"]:
            update_status_in_browser(driver, f"已进入指定域名: {current_domain}")
            break  # 如果是指定域名，退出循环
        else:
            update_status_in_browser(driver, f"当前域名 ({current_domain}) 非预期，正在跳转...")
            navigate_with_retry(driver, "http://10.100.100.141/jwglxt/xtgl/login_slogin.html") # 跳转到指定页面


        time.sleep(1)  # 每秒检查一次
    update_status_in_browser(driver, f"强制登录成功！你可以操作了！当前页面: {driver.current_url}")


# 检查浏览器进程是否仍在运行
def is_browser_running(driver):
    try:
        # 获取浏览器的进程 ID
        browser_pid = driver.service.process.pid
        for proc in psutil.process_iter(['pid', 'name']):
            if proc.info['pid'] == browser_pid and 'msedge' in proc.info['name'].lower():
                return True
    except Exception as e:
        print(f"错误: {e}")
    return False

# 检查浏览器是否关闭
def check_browser_closed(driver):
    if not is_browser_running(driver):
        update_status_in_browser(driver, "浏览器已关闭，程序退出。")
        driver.quit()  # 关闭浏览器
        sys.exit(0)  # 退出程序

#QQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQ
# 主程序执行流程
def main():
    driver = start_browser_initial_page()#打开浏览器并初始化页面

    check_and_navigate_to_correct_domain(driver)#打开登录界面
    wait_for_login(driver)#等待人工登录
    check_route_cookie(driver)#检查cookie是否有效
    while True:
        if check_route_cookie(driver)==0:#如果cookie无效
            modify_cookie_and_navigate(driver)#修改cookie并跳转登录页
            wait_for_login(driver)#等待人工登录
            check_route_cookie(driver)#检查cookie是否有效
        else:#如果cookie有效
            cookies = get_cookies(driver)#获取cookie
            for cook in cookies:#修改cookie生效于10.100.100.141
                if 'domain' in cook:
                    cook['domain'] = '10.100.100.141'

            update_status_in_browser(driver, "登录内网。。请确保已连接校园网！！！")
            navigate_with_retry(driver, "http://10.100.100.141")
            driver.delete_cookie(cook['name'])#删除旧cookie
            driver.add_cookie(cook) #添加新cookie
            new_cookie(driver)
            navigate_with_retry(driver, "http://10.100.100.141/jwglxt/xtgl/login_slogin.html")
            update_status_in_browser(driver, "test")  # 显示 
            break

    #new_cookie(driver)
    #navigate_with_retry(driver, "http://10.100.100.141/jwglxt/xtgl/login_slogin.html")
        #new_cookie(driver)#给当前界面创建新cookie
        #new_cookie1(driver)

    
    #wait_for_login(driver)

    
    #cookies = get_cookies(driver)
    #time.sleep(1)
    #modify_route_cookie(cookies, driver)
    #refresh_and_get_cookies(driver)
    #cookies = get_cookies(driver)
    # 修改 cookies 的 Domain 值
    #for cook in cookies:
     #   if 'domain' in cook:
      #      cook['domain'] = '10.100.100.141'

   # update_status_in_browser(driver, "登录内网。。请确保已连接校园网！！！")
    #navigate_with_retry(driver, "http://10.100.100.141")

     # 将 JSON 字符串解析为字典
    #cook = json.loads(cook)
 
    # 将旧 cookie 和新创建的 route cookie 一起添加到浏览器 
    #for cookie in cook: 
        #driver.delete_cookie(cookie['name'])  # 删除旧的 cookie（确保不会重复） 
        #driver.add_cookie(cookie)  # 重新添加原有 cookie 
    
    # 添加新创建的 route cookie 
   # driver.delete_cookie(cook['name'])
   # driver.add_cookie(cook) 
    #navigate_with_retry(driver, "http://10.100.100.141/jwglxt/xtgl/login_slogin.html")
    #update_status_in_browser(driver, "test")  # 显示 

    #set_cookies_in_browser(driver, cook)
   # while True:
        #current_url = driver.current_url
        #parsed_url = urlparse(current_url)
        #current_domain = parsed_url.netloc  # 获取域名部分
        
        #if current_domain in ["portal.nxist.com", "10.100.100.141","cas.nist.edu.cn"]:
           # update_status_in_browser(driver, f"已进入指定域名: {current_domain}")
           # break  # 如果是指定域名，退出循环
        #else:
            #update_status_in_browser(driver, f"当前域名 ({current_domain}) 非预期，正在跳转...")
           # navigate_with_retry(driver, "http://10.100.100.141/jwglxt/xtgl/login_slogin.html")
            


        #time.sleep(1)  # 每秒检查一次


    # 将修改后的 cookies 写回浏览器
    #set_cookies_in_browser(driver, cook)

    
    #open_target_page(driver)


    update_status_in_browser(driver, "你可以操作了！感谢使用小易教务快速登录系统！")

    # 检查浏览器是否仍在运行，直到浏览器关闭后退出脚本
    #while is_browser_running(driver):
    time.sleep(86400)  # 每秒检查一次浏览器进程
    
   # print("浏览器已关闭，脚本退出。")
    #driver.quit()  # 关闭浏览器

if __name__ == "__main__":
    main()
