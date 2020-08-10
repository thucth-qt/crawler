from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager #for install chrome driver
from pyvirtualdisplay import Display  #for use virtual view windows
thuc

    #login with your google account located in "./pw.txt"
    login_with_GAcount(driver)
    
    driver.switch_to_window(window_before)

    crawl(job, city, destination, driver)

    time.sleep(1)
    driver.close()
    driver.quit()
    if isDisplay: display.stop()

