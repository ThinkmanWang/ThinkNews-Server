class Favorite(object):
    uid = 0
    ctime = ''
    title = ''
    description = ""
    picUrl = ""
    url = ""
        
    def __init__(self, uid=0, ctime="", title="", description="", picUrl="", url=""):
        self.uid = uid
        self.ctime = ctime
        self.title = title
        self.description = description
        self.picUrl = picUrl
        self.url = url