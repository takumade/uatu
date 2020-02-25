import random, time

class BeforeVideoHook:
    """
    @summary - Decides how reach a given video URL
    """
    
    def __init__(self, channel_name, video_url, keyword, browser):
        self.channel_name = channel_name
        self.video_url = video_url
        self.browser = browser
        self.keyword = keyword
        self.route_taken= 0
        
        self.decide_action()
    
    def decide_action(self, route=1):
        """
        @summary - Decides which route to take
        
        1. Random(choose random route)
        2. Choose First route(Start from Youtube)
        3. Choose Second Route(Start from Google)
        4. Choose Third route(Do nothing)
        5. Choose Fourth route(Start from duck duck go)
        """
        routes = [2,3,4]
        
        if route == 1:
            route = random.choice(routes)
        
        if route == 2:
            self.start_from_youtube()
        elif route == 3:
            self.start_from_google()
        elif route == 4:
            self.just_jump_to_video()
        elif route == 5:
            self.start_from_duck_go()
    
    def start_from_youtube(self):
        pass
    
    def start_from_google(self):
        pass
    
    def just_jump_to_video(self):
        pass
    
    def start_from_duck_go(self):
        """
        """
        
        self.route_taken = 5
        
        self.browser.get("https://duckduckgo.com/")
        time.sleep(3)
        
        search_f = self.browser_find_element_by_id("search_form_input_homepage")
        search_text  = "%s %s" % (self.channel_name, self.keyword)
        search_f.send_keys(search_text)
        
        self.browser.execute_script("""
            document.getElementById('search_button_homepage').click()
        """)
        time.click()
        
        
        self.browser.execute_script("""
            document.getElementsByClassName('js-zci-link--videos')[0].click()
        """)
        time.click()
        
        self.browser.execute_script("""
            var tlink = %s
            var ytlinks = document.getElementsByClassName('tile__title')
            var clink
            for (var r = 0; r < ytlinks.length; r++ ){
                
                if (ytlinks[r].firstElementChild.href == tlink){
                    clink = ytlinks[r].firstElementChild
                    break
                }
            }
            clink.click()
            """)
        
        
        
    