import os

def check_pairless_songs(artist):
    directory_path = "../../data/"+artist
    file_path = directory_path+"/"
    pairless_list = open(file_path+".pairless", 'w')
    for song in os.listdir(directory_path):
        if (song.endswith(".mp3") or song.endswith(".wav")):
            lrc = song[0:-4]+".lrc"
            if not os.path.isfile(file_path+lrc):
                pairless_list.write(lrc+"\n")     
    pairless_list = open(file_path+".pairless", 'r')
    print(pairless_list.read())
    pairless_list.close()

artist = input("write down artist name >> ")
check_pairless_songs(artist)
