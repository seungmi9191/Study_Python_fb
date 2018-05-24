import matplotlib.pyplot as plt
from matplotlib import font_manager
import pytagcloud
import webbrowser

#matplotlib 그래프
def show_graph_bar(dictWords, pagename) : #그래프 이미지로 저장

    #한글처리
    font_filename = '/Users/WOOSEUNGMI/Library/Fonts/YDIYGO110.otf'
    font_name = font_manager.FontProperties(fname=font_filename).get_name()
    print(font_name)

    plt.rc('font', family=font_name) #rc=리소스

    #라벨처리
    plt.xlabel("주요단어")
    plt.ylabel("빈도수")
    plt.grid(True)

    #데이터 대입
    dict_keys = dictWords.keys() #dictWords의 단어(명사들)
    dict_values = dictWords.values() #dictWords의 값

    plt.bar(range(len(dictWords)), dict_values, align='center') #단어갯수만큼 범위 지정
    plt.xticks(range(len(dictWords)), list(dict_keys), rotation=70)

    #파일 저장
    save_filename = "/Users/WOOSEUNGMI/Desktop/2018/javaStudy/facebook/%s_bar_graph.png" % pagename
    plt.savefig(save_filename, dpi=300, bbox_inches='tight')

    plt.show()

#워드 클라우드
def wordcloud(dictWords, pagename) :
    taglist = pytagcloud.make_tags(dictWords.items(), maxsize=80)
    save_filename = "/Users/WOOSEUNGMI/Desktop/2018/javaStudy/facebook/%s_wordcloud.jpg" % pagename

    pytagcloud.create_tag_image(
        taglist,
        save_filename,
        size=(800, 600),
        fontname = 'korean',
        rectangular=False
    )

    webbrowser.open(save_filename)