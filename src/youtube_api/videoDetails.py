from googleapiclient.discovery import build

class ytube_api:
    def __init__(self,link: str,apikey: str):
        self.video_id = None
        self.video_link = link
        self.details = []
        self.apiKey = apikey
        
    def extractVideoId(self):
        _id = self.video_link.split("=")
        self.video_id = _id[1]
        return self.video_id
    
    def getvideocomments(self):
        _youtube = build('youtube', 'v3', developerKey=self.apiKey)
        getResult = _youtube.commentThreads().list(
            part = 'snippet',videoId = self.extractVideoId(),maxResults = 100, textFormat = "plainText"
        ).execute()
        return getResult
        
    def extractfromresponses(self):
        for detail in self.getvideocomments()["items"]:
            authorname = detail["snippet"]['topLevelComment']['snippet']['authorDisplayName']
            comment = detail["snippet"]['topLevelComment']["snippet"]["textDisplay"]
            likes = detail["snippet"]['topLevelComment']["snippet"]['likeCount']
            replies = detail["snippet"]['totalReplyCount']
            details_dict = {'authorname':authorname,'comment':comment,'likes':likes,'replies':replies}
            self.details.append(details_dict)
        return self.details
            
        
    