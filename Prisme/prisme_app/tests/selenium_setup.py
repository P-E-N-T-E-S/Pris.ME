from selenium import webdriver

driver = None

def setup_selenium():
    global driver
    if driver is None:
        driver = webdriver.Chrome()
    return driver

def finalizar_selenim():
    global driver
    if driver:
        driver.quit()
        driver = None

    return driver