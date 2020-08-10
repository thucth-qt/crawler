from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager #for install chrome driver
from pyvirtualdisplay import Display  #for use virtual view windows
import time




def intialize_crawler(isDisplay, targetUrl):

    chrome_options = Options()
    chrome_options.add_argument("--incognito")
    chrome_options.add_argument("--window-size=1920x1080")

    # start chrome

    display = Display(visible=isDisplay, size=(800, 600))
    display.start()
    driver = webdriver.Chrome(
        chrome_options=chrome_options, executable_path=ChromeDriverManager().install()
    )

    # retrieve url
    driver.get(targetUrl)
    time.sleep(2)
    return display, driver

def login_with_GAcount(driver):
    signin = driver.find_element_by_link_text("Sign In")
    signin.click()
    time.sleep(2)

    # click sign in with google
    signinGoogle = driver.find_element_by_id("g-signin2-signin")
    signinGoogle.click()
    time.sleep(2)

    # the new window created
    window_after = driver.window_handles[1]

    driver.switch_to_window(window_after)
    # enter credentials
    credentials = open("./.pw.txt", "r")

    input = driver.find_element_by_id("identifierId")
    username = credentials.readline().strip()
    input.send_keys(username)
    next = driver.find_element_by_css_selector("div.VfPpkd-RLmnJb")
    next.click()
    time.sleep(3)

    # pwInput = driver.find_element_by_xpath('//*[@id="password"]/div[1]/div/div[1]/input')
    pwInput = driver.find_element_by_name('password')
    pw = credentials.readline().strip()
    pwInput.send_keys(pw)
    send = driver.find_element_by_xpath('//*[@id="passwordNext"]/div/button')
    send.click()
    time.sleep(5)
def show_info(job):
    jd = job.find_element_by_css_selector('div.job__description')
    detail = jd.find_element_by_css_selector('div.job__body').find_element_by_css_selector('div.details')
    title= detail.find_element_by_class_name('title').find_element_by_css_selector('a').text
    salary=detail.find_element_by_class_name('salary').find_element_by_css_selector('span.salary-text').text
    jd_detail = detail.find_element_by_class_name('description').text
    addr=job.find_element_by_class_name('city_and_posted_date').find_element_by_class_name('address')
    city= addr.find_element_by_class_name('text').text 
    district = addr.find_element_by_class_name('other-address').text
    location = city +", "+ district
    return [title, salary, location, jd_detail]

def crawl(job, area, result, driver):
    time.sleep(3)
    
    # import csv
    options = driver.find_element_by_xpath('//*[@id="search_form"]/div[2]/div/div[2]')
    options.click()
    time.sleep(1) 
    ul = driver.find_element_by_xpath('/html/body/div[1]/div[1]/div[2]/form/div[2]/div/div[2]/div/div/ul') 
    areas = ul.find_elements_by_class_name('active-result')
    for li in areas:
        if li.text == area:
            li.click()
            time.sleep(1)

    keyword = driver.find_element_by_xpath('//*[@id="search_form"]/div[1]/div/div[2]/ul/li/input')
    keyword.send_keys(job+'\n')

    #show all jd
    time.sleep(2)
    try:
        more_jobs = driver.find_element_by_xpath('//*[@id="show_more"]/a')
        while more_jobs:
            more_jobs.click()   
            time.sleep(2)
            more_jobs = driver.find_element_by_xpath('//*[@id="show_more"]/a')

    except:
        pass

    jobs = driver.find_elements_by_class_name('job')

    hot_jobs = [job  for job in jobs if ('super-hot-job' in job.get_attribute("class"))]

    normal_jobs = list(set(jobs).difference(set(hot_jobs)))
    
    #write csv
    import csv
    f = open(result, 'w')
    with f:
        writer = csv.writer(f)
        writer.writerow(["Hot Job?", "Job", "Salary", "Location", "Details"])

        print('hot jobs: amount:', len(hot_jobs))
        for job in hot_jobs:
            try:
                info = ["hot job"]+show_info(job)
                writer.writerow(info)
            except:
                pass
        print('normal jobs: amount: ',len(normal_jobs))
        for job in normal_jobs:
            try:
                info = ["normal job"] + show_info(job)
                writer.writerow(info)
            except:
                pass


if __name__ == "__main__":
    #enter informations for crawling data
    targetUrl="https://itviec.com/"
    isDisplay=False
    job ="golang"
    locations = {0:"All Cities", 1:"Ha Noi", 2:"Ho Chi Minh", 3:"Da Nang", 4:"Others"}
    city = locations[0]
    destination ="./results.csv"

    
    display, driver = intialize_crawler(isDisplay, targetUrl)
    window_before = driver.window_handles[0]

    #login with your google account located in "./pw.txt"
    login_with_GAcount(driver)
    
    driver.switch_to_window(window_before)

    crawl(job, city, destination, driver)

    time.sleep(1)
    driver.close()
    driver.quit()
    if isDisplay: display.stop()

