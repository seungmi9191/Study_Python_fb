from collect import crawler as cr
from analysis import analizer as an
from visualize import visualizer as vi
import simplejson

pagename = "jtbcnews"
from_date = "2018-05-01"
to_date = "2018-05-15"

if __name__ == "__main__" :

    #수집
    # postList = cr.fb_get_post_list(pagename, from_date, to_date)
    # print(postList)

    #분석
    dataString = an.json_to_str("/Users/WOOSEUNGMI/Desktop/2018/javaStudy/facebook/jtbcnews.json", "message_str")  # 파일경로+경로명, key값(dic의)
    count_data = an.count_wordfreq(dataString)
    print(count_data) #어떤 단어를 몇번 이용했는지 출력
    #리스트를 딕셔너리 형태로 변경
    dictWord = dict(count_data.most_common(20)) #단어 상위 몇개만 지정

    #그래프
    vi.show_graph_bar(dictWord, pagename) #폰트네임알아내기

    # 워드크라우드
    vi.wordcloud(dictWord, pagename)
