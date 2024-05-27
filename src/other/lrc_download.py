import syncedlyrics
import os

def download_lrc(artist):
    directory_path = "../../data/"+artist
    file_path = directory_path+"/"
    lrcs_less_path = directory_path + "_plain_texts/"
    if not os.path.exists(lrcs_less_path):
        os.makedirs(lrcs_less_path)
    pairless_list = open(file_path+".pairless", 'w')

    for song in os.listdir(directory_path):

        if (song.endswith(".mp3") or song.endswith(".wav")) and not song.startswith(artist):
            print("\n>>>", song) # " - ", song.startswith(artist)
            new_name = artist + " - " + song.lstrip("0123456789. - ")
            try:
                lrc_path = file_path+new_name[0:-4]+".lrc"
                syncedlyrics.search(new_name[0:-4], save_path=lrc_path)
                if os.path.isfile(lrc_path):
                    print("\t\t - done -")
                    os.rename(file_path + song, file_path + new_name)
                else:
                    print("\t\t - lrc not found")
                    txt_path = lrcs_less_path+new_name[0:-4]+".lrc"
                    syncedlyrics.search(new_name[0:-4], save_path=txt_path)
                    if os.path.isfile(txt_path):
                        print("\t\t - text found")
                        os.replace(song, lrcs_less_path+new_name[0:-4]+".mp3")
                    else:
                        pairless_list.write(song+"\n")
                    
            except Exception as e:
                print("\t\t - \"", e, "\" occured, skipping track -")
                
    pairless_list.close()

artist = input("write down artist name >> ")
download_lrc(artist)
