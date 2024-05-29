from datetime import datetime
import syncedlyrics

class Processing:
    def __init__(self):
        self.song = None
        self.song_path = None

        self.lyrics_path = None
        self.lyrics = None
    
        self.result = None
        self.request_time = None

    def process(self, ):
        # NOW IT IS JUST LOADING LRC FROM INTERNET. LATER, IT'LL USE MODEL 
        # LATER HERE MUST BE MODEL, WHICH WILL PROCESS FILES THROUGH
        try:
            self.request_time = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
            self.result = syncedlyrics.search(self.song_path[0:-4])
        except Exception as e:
            print(e, "\" occured, skipping track -")
        