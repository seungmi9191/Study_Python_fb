import json
import re
from konlpy.tag import Twitter
from collections import Counter

#json 파일명, 추출할 데이터의 key값을 주면 문자열을 리턴한다.
def json_to_str(filename, key) :
   jsonfile = open(filename, 'r', encoding='utf-8') #(파일이름, 모드(읽기모드), 인코딩)
   json_string = jsonfile.read() #json_string가 실제 문자열 #문자열 하나
   jsondata = json.loads(json_string) #리스트로 담겨있음

   # print(type(json_string))
   # print(json_string)
   #
   # print(type(jsondata))
   # print(jsondata)

   data = ''
   for item in jsondata :
       value = item.get(key) #get은 딕셔너리에서 key값이면 value값 가져오는 함수!

       if value is None : #value값이 없으면 for문으로 돌아가라.
           continue

       data += re.sub(r'[^\w]', '', value) #한글만 계속 붙여나간다. 정규식을 통해 공백을 지워라
   return data


#명사를 추출해서 빈도수를 알려줌
def count_wordfreq(data) :
    twitter = Twitter()
    nouns = twitter.nouns(data)
    #print(nouns)

    count = Counter(nouns)
    #print(count)

    return count

dataString=json_to_str("/Users/WOOSEUNGMI/Desktop/2018/javaStudy/facebook/jtbcnews.json", "message_str") #파일경로+경로명, key값(dic의)
#print(dataString)
count_wordfreq(dataString)


