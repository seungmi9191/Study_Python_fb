
import requests
import json
from datetime import datetime, timedelta

#변수선언
BASE_URL_FB_API = "https://graph.facebook.com/v3.0"
ACCESS_TOKEN = "EAACEdEose0cBAODyZAlf91w85ZCk5ZAcTZBRCZCFSgh4Ef8SHKbLZAv2KVq8sFdn9z2sLGRy9NXcdpZBXHSz0NZAnOJDujnmZCoQgIgyAyN85VS23cE8DP9TTjBYZAtY0bDKzCYtZBtb0Obtw4OOS9cNNHVZCVqoQqaYYxqTK8XfJpC60Jk2zIMQD53AT2ugncZBq1a0elpDGw9CFDLm5nhvokw1v984jWaetnuQZD"
LIMIT_REQUEST = 20
pagename = "jtbcnews"
from_date = "2017-01-01"
to_date = "2017-02-01"

#얘는 url 던져주면 json으로 데이터를 받아오는 애(리턴해주는 애)
def get_json_result(url) :
    try :
        # get방식으로 url을 요청, 요청하면 응답와야함
        response = requests.get(url)

        # 주소가 없을 시 오류 방지 , statue_code로 정상적인지 판단
        if response.status_code == 200 :  # 성공인 경우 200
            return response.json()

    except Exception as e :
        #아예 인터넷이 안될때, 통신상 오
        return "%s : Error for request [%s]" % (datetime.now(), url)



#얘는 url 던져주면 id값 받아오는 애
#페이스북 페이지네임을 주면 페이지 id값을 리턴해준다.
#뒤에 받아낼 값의 jtbcnews를 숫자값으로 받아와야함
#https://graph.facebook.com/v3.0/12345(이건 jtbcnews)/?access_token=32j23l2da 이런식으로 물어봐야 key값을 알려줌
def fb_name_to_id(pagename) :

    base = BASE_URL_FB_API
    node = "/%s" % pagename #%s = string형으로 치환
    params = "/?access_token=%s" %ACCESS_TOKEN
    url = base + node + params

    json_result = get_json_result(url) #딕셔너리로 리턴된다.
    # print(json_result)

    #id만 리턴하게 만들어줌 - 특정값만 뽑아쓸 때 ; key값 던져주면 value값만 뽑아옴
    return json_result["id"]


#페이스북 페이지네임, 시작날짜, 끝날짜를 주면 json형태로 데이터를 리턴해준다. --> 이제 json 형태가 아니라 리스트 형태로 데이터를 리턴해
#실제로는 https://graph.facebook.com/v3.0/[Node, Edge]/?parameters 이런 형식의 주소임
#v3.0 뒤부터는 jtbcnews/posts 형식으로 와야함 -> 숫자/posts

#fields = 데이터 달라고 정의, limit(0)이면 값주지마, summary(true)는 요약본(count만 옴, 글이 전체  개)
#포스트 정보를 딕셔너리 형태로 리턴한다. (data, paging)
def fb_get_post_list(pagename, from_date, to_date) :
    #id값 받아오기
    page_id = fb_name_to_id(pagename)

    base = BASE_URL_FB_API
    node = '/%s/posts' % page_id
    fields = '/?fields=id,message,link,name,type,shares,'+\
             'created_time,comments.limit(0).summary(true),'+\
             'reactions.limit(0).summary(true)'
    duration = '&since=%s&until=%s' % (from_date, to_date)
    parameters = '&limit=%s&access_token=%s' % (LIMIT_REQUEST, ACCESS_TOKEN)

    url = base + node + fields + duration + parameters

    #next를 계속 받아오기 위해 반복문 사용

    postList=[]
    isNext = True
    while isNext :
        #우리가 만든 주소로 데이터를 요청하면 받아옴
        temPostList = get_json_result(url)
        for post in temPostList["data"] : #20개짜리(data) 하나씩 꺼내서 post에 담을예정
            # message_str = post["message"] #메세지를 받아와서 찍어
            # print(message_str)

            postVo = preprocess_post(post)
            postList.append(postVo)

        paging = temPostList.get("paging").get("next") #받은 데이터안에 paging안에 next를 담아왕
        #paging = temPostList["paging"]["next"]
        if paging != None : #이 주소가 아직 있으면
            url = paging #url에 넣어줘 (여기 url은 내가 처음 사용한게 아니라 json으로 다시 준거임,계속 바뀜)
        else :
            isNext = False #없으면 for문 나가버림

    # save results to file - postList를 던져주면 json으로 바꿔줌 -> d:/저장경
    with open("/Users/WOOSEUNGMI/Desktop/2018/javaStudy/facebook/" + pagename + ".json", 'w', encoding='utf-8') as outfile:
        json_string = json.dumps(postList, indent=4, sort_keys=True, ensure_ascii=False)
        outfile.write(json_string)

    return postList


    # return jsonPosts

#json데이터를 주면 내가 원하는 5개만 뽑아내는 함수
def preprocess_post(post) :

    #작성일 +9시간 해줘야함(표준시간으로)
    created_time = post["created_time"]
    created_time = datetime.strptime(created_time, '%Y-%m-%dT%H:%M:%S+0000')
    created_time = created_time + timedelta(hours=+9)
    created_time = created_time.strftime('%Y-%m-%d %H:%M:%S')


    #공유 수
    if "shares" not in post :
        shares_count = 0
    else :
        shares_count = post["shares"]["count"] #있으면 가져온 실제 숫자를 넣음

    #리액션 수
    if "reactions" not in post :
        reactions_count = 0
    else :
        reactions_count = post["reactions"]["summary"]["total_count"]

    # 댓글 수
    if "comments" not in post:
        comments_count = 0
    else:
        comments_count = post["comments"]["summary"]["total_count"]

    # 메세지 수
    if "message" not in post:
        message_str = ""
    else:
        message_str = post["message"]

    postVo = {
                "created_time":created_time,
                "shares_count": shares_count,
                "reactions_count": reactions_count,
                "comments_count": comments_count,
                "message_str": message_str
             }

    return postVo



#무조건 순차적!!!!
jsonData = fb_get_post_list(pagename, from_date, to_date)
print(jsonData)

# #실제 함수 불러와서 실행
# result = fb_name_to_id("jtbcnews")
# print(result)


#------------------------테스트-----------------------------
# url = "http://192.168.1.14:8088/mysite4/api/gb/list2/"
#실제 실행
# result = get_json_result(url)
# print(result)

