class Favorite(object):
    id = 0
    uid = 0
    ctime = ''
    title = ''
    description = ""
    picUrl = ""
    url = ""
        
    def __init__(self, id=0, uid=0, ctime="", title="", description="", picUrl="", url=""):
        self.id = id
        self.uid = uid
        self.ctime = ctime
        self.title = title
        self.description = description
        self.picUrl = picUrl
        self.url = url