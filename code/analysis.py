import json
import requests
import time
def save_in_file(filename,data):
    with open(filename,encoding="utf-8",mode="a") as f:
        for line in data :
            f.write(line+'\n')

def translate(text):
    data = {
        'doctype': 'json',
        'type': 'AUTO',
        'i':text
    }
    url = "http://fanyi.youdao.com/translate"
    r = requests.get(url,params=data)
    results = r.json()
    #print(results)
    return [result[0]['tgt'] for result in results['translateResult']]
    
def write_log(data):
    with open("log.txt",encoding="utf-8" ,mode="w") as f:
        for d in data:
            f.write(d)




with open("data.json","r") as f:
    data = json.load(f)  
filename = "titles_zh.txt"
count = 50
trans = []
index = 0
titles = [issue['title'] for issue in data]
arr = titles[index:index+count]
times = 0
while arr:
    times += 1
    text = '\n'.join(arr)
    # print(text)
    results = translate(text)
    save_in_file(filename,results)
    index += count
    arr = titles[index:index+count]
    time.sleep(1)
    if times % 10 == 0:
        print("current index : {}".format(index))
        write_log(results)

