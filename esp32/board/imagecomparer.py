



class ImageComparer():


    def __init__(self):
        self.reset()
        

    def reset(self):
        self.hash = None

    def checksum(self,msg):
        v = 21
        for c in msg:
            v ^= c
        return v


    def check(self,msg):
        hash = self.checksum(msg)
        result = (self.hash == hash)
        self.hash = hash
        return result