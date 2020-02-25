from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, WebDriverException
from selenium.common.exceptions import TimeoutException, ElementNotInteractableException, JavascriptException

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import sys
import time
import random
import threading

sem = threading.Semaphore(3)

from modules.proxychilli import ProxyChilli

from modules.get_channel_videos import GetChannelVideos
from modules.watch_videos import WatchVideos


class YTBot:
    def __init__(channel_name,keyword, threads=2, watch_method=4):
        get_channel = GetChannelVideos(channel_name,keyword)
        video_list = get_channel.get_channel_videos()
        watch_vidz = WatchVideos(channel_name, video_list,keyword, threads,watch_method)
        watch_vidz.choose_method()
     
    
         
if __name__ == '__main__':
    pass
        
        
        
               
