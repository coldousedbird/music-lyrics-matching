import os
from RequestHistoryDB import RequestHistoryDB 

if __name__ == "__main__":
    # init
    tested_db = RequestHistoryDB()
    # creating new
    tested_db.create_new("tested_db.db")
    tested_db.create_new("rubbish.db")
    # activating existing db
    tested_db.set_name("tested_db.db")

    # read
    print("created:\n", tested_db.read())
    
    # add & read
    requests = [
        ["25.05.24 18:00:00", "кровосток - гантеля", "",                "[00:00] кровяка кишки распидорасило",                      "йе йе"],
        ["25.05.24 18:01:00", "убийцы - реку перейти", "",              "[00:51] адвокат авокату брат, брат брату адвокат",         "нам бы только реку перейти"],
        ["25.05.24 18:02:00", "hanae - kamisama hajimemashita", "",     "[00:07] o na no ko hajimemashita",                         "na no ko hajime bus stoppu"],
        ["25.05.24 18:03:00", "kana hanazawa - ren'ai circulation","",  "[00:00] Se no Demo sonnan ja dame",                        "nya"],
        ["25.05.24 18:04:00", "shellac - tattos", "",                   "[03:02] we'll tattoo the names of the dead on your ass",   "rest in peace"]
    ]
    for request in requests:
        tested_db.add(*request)
    print("\nfilled")
    for request in tested_db.read():
        print(request)

    # remove & read
    tested_db.remove(requests[1][0])
    tested_db.remove(requests[3][0])
    print("\nsecond and fourth items removed")
    for request in tested_db.read():
        print(request)

    os.remove("rubbish.db")
    os.remove("tested_db.db")
