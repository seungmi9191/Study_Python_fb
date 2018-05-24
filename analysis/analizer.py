import json

#json 파일명, 추출할 데이터의 key값을 주면 문자열을 리턴한다.
def json_to_str(filename, key) :
   jsonfile = open(filename, 'r', encoding='utf-8') #(파일이름, 모드(읽기모드), 인코딩)
   json_string = jsonfile.read() #json_string가 실제 문자열 #문자열 하나
   jsondata = json.loads(json_string) #리스트로 담겨있음

   print(type(json_string))
   print(json_string)

   print(type(jsondata))
   print(jsondata)

json_to_str("/Users/WOOSEUNGMI/Desktop/2018/javaStudy/facebook/jtbcnews.json", "message_str") #파일경로+경로명, key값(dic의)

