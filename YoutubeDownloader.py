import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains   
#test    
def HandlePopUp(driver):
    mainWinHandle = driver.window_handles[0]
    driver.switch_to_window(driver.window_handles[1])
    driver.close()
    driver.switch_to_window(mainWinHandle)
    
def FindDownloadButton (potentialDownloadButtons):
    for potentialDownloadButton in potentialDownloadButtons:
        if (potentialDownloadButton.is_displayed()):
            return potentialDownloadButton
        
    return None
        
videoListURL = raw_input('Enter full youtube list URL: ')
youtubeToMp3 = "http://www.youtube-mp3.org/"
    
driver = webdriver.Chrome("chromedriver.exe")

driver.get(videoListURL)
 
allVideos = driver.find_elements_by_xpath('//*[@id="pl-load-more-destination"]/tr')
videoList = []

for video in allVideos:
    videoId = video.get_attribute("data-video-id")    
    print(videoId)    
    videoList.append(videoId)

for videoId in videoList:
    actions = ActionChains(driver)
    driver.get(youtubeToMp3)
    linkBar = driver.find_element_by_id("youtube-url")
    linkBar.clear()
    linkBar.send_keys("http://www.youtube.com/watch?v="+videoId)
    submitLink = driver.find_element_by_id("submit")
    submitLink.click()
    time.sleep(0.5)
    HandlePopUp(driver)
    time.sleep(5)
    potentialDownloadButtons = driver.find_elements_by_xpath('//*[@id="dl_link"]/a')    
    downloadButton = FindDownloadButton(potentialDownloadButtons)
    if (downloadButton != None):        
        downloadButton.click()
    else:
        if (driver.find_element_by_xpath('//*[@id="error_text"]/b').text.startswith('There was an Error')):
            print("There was an error downloading a youtube video due to copyright issues or the length of the video. Youtube Id - "+videoId)
        else:
            print(videoId + " could not be downloaded due to an unknown error. Please try again later.")
        
print("Please allow time for all files to download to disk.")

                 
