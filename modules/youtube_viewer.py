import time, random, sys
from threading import Semaphore
from selenium import webdriver
from selenium.common.exceptions import *
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from modules.before_video_watch_hook import BeforeVideoHook

class YoutubeViewer:
    sem = Semaphore(3)
    def __init__(self, video, proxy_use=None, debug=False):
        """
        @summary - Watch a YT video
        @proxy_use - proxy to use
        @debug - Set headless mode(show or hide browsers)
        """
        
        
        self.chrome_options = webdriver.ChromeOptions()
        if proxy_use != None:
            self.chrome_options.add_argument('--proxy-server=%s' % proxy_use)
               
        chromedriver_path = self.get_chromedriver_path()
        
        if debug == False:
            self.chrome_options.add_argument("--headless")
            
        self.browser = webdriver.Chrome(chromedriver_path, chrome_options=self.chrome_options)
        self.went_to_channel = False
        self.opened_random_video = False
        self.channel_name = None
        self.video_url = None
        self.keyword = None
        
        call_vid_hook = BeforeVideoHook(self.channel_name,self.video_url, self.keyword)
        
        #Deal with routes taken
        if call_vid_hook.route_taken == 5:
            self.get_video_time_n_sleep()
        
        
    def get_chromedriver_path(self):
        """
        @summary - Get chromedriver path
        @returns - chromedriver path
        """
        
        if sys.platform == "darwin":
            chrome_driver = "chromedriver_mac"
        elif sys.platform == "linux":
            chrome_driver = "chromedriver_linux"
        else:
            chrome_driver = "chromedriver_win"
            
        return "./chromedrivers/"+chrome_driver
    
    
    def find_and_close_popups(self):
        """@summary - Find and close random youtube popups"""
        try:
            self.browser.execute_script("document.getElementsByClassName('style-scope ytd-mealbar-promo-renderer')[7].click()")
            sem.acquire()
            print("[+] Review popup found and closed!")
            sem.release()
        except JavascriptException:
            sem.acquire()
            print("[-] Didnt detect any Review popup")
            sem.release()
        
    def skip_add(self):
        """@summary - Skip youtube ads if found"""
        time.sleep(6)
        try:
            self.browser.execute_script("document.getElementsByClassName('ytp-ad-skip-button')[0].click()")
            sem.acquire()
            print("[+] Ad found and closed")
            sem.release()
        except JavascriptException:
            sem.acquire()
            print("[-] Didnt detect any ad")
            sem.release()
    
    def find_video(self, video_link):
        """
        @summary - Find a particular video
        @video_link - The video to find"""
        if video_link != None and "watch" in video_link:
            self.browser.get(video_link)
        elif video_link == None:
            pass
        else:
            video_link.click()
        
        self.wait = WebDriverWait(self.browser, 10)
        
        try:
            play_el = self.wait.until(EC.presence_of_element_located((By.XPATH, '//button[@title="Play (k)"]')))
            play_el.click()
            #  self.browser.execute_script("document.getElementsByClassName('ytp-play-button')[0].click()")
        except (ElementClickInterceptedException, TimeoutException):
            self.find_and_close_popups()
            self.browser.execute_script("document.getElementsByClassName('ytp-play-button')[0].click()")
        except ElementNotInteractableException: 
            pass
        
        self.skip_add()
        
        self.get_video_time_n_sleep()
        
        self.find_and_close_popups()    
        # Random Actions
        # 1. Go channel and watch a random video
        # 2. Click a random video from the page
        # 3. Exit
        
        if self.went_to_channel or self.opened_random_video:
            sem.acquire()
            print("[-] Exiting")
            sem.release()
            self.browser.quit()
            return
            
        choice2 =  random.choice([1,2,3])
        # choice2 =  2
        
        if choice2 == 1:
            self.go_to_channel()
        if choice2 == 2:
            self.pick_a_random_video()
        if choice2 == 3:
            sem.acquire()
            print("[-] Exiting")
            sem.release()
            self.browser.quit()
            return
    
    def go_to_channel(self, go_to_channel=True):
        """
        @summary - Go to a user channel
        @go_to_channel - If set to True go to channel
        """
        sem.acquire()
        print("[+] Going to channel!")
        sem.release()
        proc_links = []
        
        if go_to_channel == True:
            # self.browser.execute_script("document.getElementById('channel-name').click()")
            # channel_name = self.browser.find_element_by_xpath('//ytd-channel-name[@id="channel-name"]')
            # channel_name.click()
            
            self.browser.execute_script("""
                var links = document.getElementsByTagName('a');
                var links_filtered = [];
                for (var i = 0; i < links.length; i++){
                    if (links[i].href.includes('channel')){
                        links_filtered.push(links[i])
                    }
                }
                
                click_link = links_filtered[1]
                click_link.click()
                """)
            self.went_to_channel = True
            sem.acquire()
            print("[+] Now in channel")
            sem.release()
        else:
            self.opened_random_video = True
            
            
        if self.went_to_channel == True:
            sem.acquire()
            print("[+] Selecting a random video")
            sem.release()
            try:
                time.sleep(random.randint(3,5))
                self.browser.execute_script("document.getElementsByClassName('tab-content')[1].click()")
                time.sleep(random.randint(3,5))
                self.browser.execute_script("""
                        
                        var links = document.getElementsByTagName('a');
                        var links_filtered = [];
                        for (var i = 0; i < links.length; i++){
                            if (links[i].href.includes('watch')){
                                links_filtered.push(links[i])
                            }
                        }
                        
                        click_link = links_filtered[Math.floor(Math.random() * links_filtered.length)]
                        click_link.click()
                        """)
            except JavascriptException:
                sem.acquire()
                print('[-] line 174 javascript error...')
                sem.release()
                
        if self.opened_random_video == True:
            sem.acquire()
            print("[+] Selecting a random video")
            sem.release()
            time.sleep(random.randint(3,5))
            
            self.browser.execute_script("""
                        
                        var links = document.getElementsByTagName('a');
                        var links_filtered = [];
                        for (var i = 0; i < links.length; i++){
                            if (links[i].href.includes('watch')){
                                links_filtered.push(links[i])
                            }
                        }
                        
                        click_link = links_filtered[Math.floor(Math.random() * links_filtered.length)]
                        click_link.click()
                        """)
            
        # links = self.wait.until(EC.presence_of_all_elements_located((By.XPATH, '//span[@id="video-title"]')))
         
        
        #  links = self.browser.find_elements_by_xpath('//a[@href]')
         
        # for link in links:
            # if "watch" in link.get_attrubute("href"):
            # proc_links.append(link)
        
        self.find_video(None) 
        
    def pick_a_random_video(self):
        """
        @summary - Pick a random video and watch it!
        """
        sem.acquire()
        print("[+] Picking a random video")
        sem.release()
        self.go_to_channel(False)
 
    def get_video_time_n_sleep(self, qafterwards=False):
        time_duration = self.browser.find_element_by_xpath('//span[@class="ytp-time-duration"]')
        time_duration = time_duration.text
        sem.acquire()
        print('[+] Time duratiion; '+time_duration)
        sem.release()
        
        # time_secs = (int(time_duration.split(":")[0]) * 60) + int(time_duration.split(":")[1]) - 10 -5
        time_secs = 30
        sem.acquire()
        print("Time seconds: "+str(time_secs))
        sem.release()
        
        # Part or full video 
        choice = random.choice([1, 2])
        
        if choice == 1:
            time.sleep(time_secs)
        else:
            # find a random start time 
            if self.opened_random_video:
                end = int((5/100) * (time_secs-1))
                time.sleep(random.randint(0, end))
            else:    
                start = int((25/100) * (time_secs-1))
                time.sleep(random.randint(start,time_secs))
        
        if qafterwards == True:
            self.browser.quit()