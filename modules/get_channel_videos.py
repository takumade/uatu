class GetChannelVideos:
    """
    @summary - Given a channel name it will all get videos
    """
    
    def __init__(self, channel_name, channel_url=None):
        self.channel_name = channel_name
        self.channel_url = channel_url
        self.channel_videos = []
        
    def search_channel(self):
        self.get_channel_videos()
        
    def get_channel_videos(self):
        pass
    
    def get_video_list(self):
        return self.channel_videos
    