from collect import crawler as cr
from analysis import analizer as an

pagename = "jtbcnews"
from_date = "2018-05-01"
to_date = "2018-05-15"

if __name__ == "__main__" :

    #수집
    # postList = cr.fb_get_post_list(pagename, from_date, to_date)
    # print(postList)

    #분석
    dataString = an.json_to_str("/Users/WOOSEUNGMI/Desktop/2018/javaStudy/facebook/jtbcnews.json", "message_str")  # 파일경로+경로명, key값(dic의)
    count_data = an.an.count_wordfreq(dataString)
    print(count_data)
