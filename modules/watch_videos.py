import threading, random
from modules.youtube_viewer import YoutubeViewer
from modules.proxychilli import ProxyChilli

class WatchVideos:      
    def __init__(self, channel_name, video_list,keyword, threads=2, watch_method=1, debug=False):
        """
        @summary - Start watching YT videos
        @video_list - List of videos to watch
        @threads = Number of concurrent videos
        @debug - Show whats happening under the hood
        """
        self.watch_method = watch_method
        self.thread_list = []
        self.video_list = video_list
        self.thread_count = threads
        self.debug = debug
        proxies = ProxyChilli(10)
        self.proxy_list = proxies.get_proxy_list()
             
    def choose_method(self):
        """
        @summary - Choose which method to take
        """
        if self.method == 1:
            self.one_proxy_to_many_videos()
        elif self.method == 2:
            self.one_proxy_one_video_seq()
        elif self.choose_method == 3:
            self.one_proxy_one_video_random()
        elif self.choose_method == 4:
            self.one_proxy_to_many_videos()
    
    # Watch video method 1: 1 proxy for many videos
    def one_proxy_to_many_videos(self):
        """
        @summary - Given a proxy watch all videos on the list, move to next proxy and repeat
        """
        
        
        for proxy in self.proxy_list:
            for video in self.video_list:
                self.start_video_thread(video, proxy)
                self.wait_for_threads()
        
    # Watch video mathod #2: 1 Proxy One video(Sequentially)
    def one_proxy_one_video_seq(self):
        """
        @summary - Each proxy is used to watch one video sequentially
        """
        index = 0
        for video in self.video_list:
            try:
                self.start_video_thread(video, self.proxy_list[index])
                self.wait_for_threads()
                index += 1
            except IndexError:
                break
            
    # Watch video mathod #3: One Random Proxy One video(Randomly)
    def one_proxy_one_video_random(self):
        """
        @summary - Each random proxy is used to watch one  video randomly
        
        ABout combinations:
        Every proxy u use is paired with a video(that it watches). We dont want to repeat
        combinations, uniqueness is key....
        """
        combinations = {}
        
        for video in self.video_list:
            select_proxy = random.choice(self.proxy_list)
            
            try:
                
                try:
                    if combinations[select_proxy] == video:
                        continue
                except IndexError:
                    pass
                
                self.start_video_thread(video, select_proxy)
                self.wait_for_threads()
                
                combinations[select_proxy] = video
            except IndexError:
                break
            
    # Watch video mathod #4: One Proxy For Random video(Randomly)
    def one_proxy_one_video(self):
        """
        @summary - Each random proxy is used to watch one  video randomly
        
        ABout combinations:
        Every proxy u use is paired with a video(that it watches). We dont want to repeat
        combinations, uniqueness is key....
        """
        combinations = {}

        for proxy in self.proxy_list:
            select_vid = random.choice(self.video_list)
            
            try:
                
                try:
                    if combinations[proxy] == select_vid:
                        continue
                except IndexError:
                    pass
                
                self.start_video_thread(select_vid, proxy)
                self.wait_for_threads()
                
                combinations[select_vid] = proxy
            except IndexError:
                break
            
    def start_video_thread(self,video, proxy=None):
        """
        @summary - start a video watching thread
        @video - The video to watch
        """
        
        t = threading.Thread(target=YoutubeViewer, args=(video, 
                                                         self.channel_name, 
                                                         self.video_url, 
                                                         self.keyword, 
                                                         proxy, 
                                                         self.debug,))
        t.start()
        self.thread_list.append(t)
        
    def wait_for_threads(self):
        """
        @summary - Wait for threads to finish and remove dead threads from list
        @threads - The thread list
        """
        
        # Wait for thread to exit
        if len(self.thread_list) == self.total_threads:
            for t in self.thread_list:
                t.join()
                self.thread_list.remove(t)
        
        # Remove finished threads
        for t in self.thread_list:
            if not t.isAlive():
                self.thread_list.remove(t)
       