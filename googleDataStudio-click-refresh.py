import time
from selenium import webdriver
from depot.manager import DepotManager
from seleniumrequests import Chrome
from selenium.webdriver.common.keys import Keys

SITE = "https://datastudio.google.com/YourURLHere/page/SomeUUIDHere/edit"
username = 'yourusername@domain.com'
password = '32CharPassword'

depot = DepotManager.get()
driver = webdriver.PhantomJS()
driver.set_window_size(1024, 768) # set the window size that you need
driver.get(SITE)
driver.save_screenshot('1.png')

# Enter the username
time.sleep(5)
usr = driver.find_element_by_id('identifierId')
usr.send_keys(username)
userBtn = driver.find_element_by_xpath('//*[@id="identifierNext"]/content')
userBtn.click()
print('Entered username. Sleeping for password input \n')
time.sleep(3)
driver.save_screenshot('2.png')

# Enter the password
passw = driver.find_element_by_xpath('//*[@id="password"]/div[1]/div/div[1]/input')
passw.send_keys(password)
passBtn = driver.find_element_by_id('passwordNext')
driver.execute_script("arguments[0].click();", passBtn)
print('Just signed in. Sleeping 10 seconds \n')
time.sleep(10)
driver.save_screenshot('3.png')

# Click the data refresh button
refreshBtn = driver.find_element_by_xpath('//*[@id="reporting-app-header"]/md-toolbar/div/div[2]/div[4]/div')
refreshBtn.click()
print('Clicked the refresh button. Sleeping till then screenshot and exit. \n')
time.sleep(3)
driver.save_screenshot('refresh.png')
driver.close()

# https://stackoverflow.com/questions/33045183/firefox-phantomjs-login-to-website-not-working
# https://www.softwaretestingmaterial.com/dynamic-xpath-in-selenium/
# https://www.periscopix.co.uk/blog/how-to-get-real-time-reports-in-data-studio/

