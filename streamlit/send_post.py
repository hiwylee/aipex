import requests
import json

API_HOST = "https://cexcieoazb3u2spa76p7z5xyn4.apigateway.ap-seoul-1.oci.customer-oci.com"
#API_HOST = "http://146.56.164.72:8000"
# path=/aipex/summarize

def do_post(path, body):
    url = API_HOST + path
    #url = "http://146.56.164.72:8000/api/v1/summarize"
    headers = {'Content-Type': 'application/json', 'charset': 'UTF-8', 'Accept': '*/*'}
    
    try:
        # response = requests.post(url, headers=headers, data=json.dumps(body, ensure_ascii=False, indent="\t"))
        response = requests.post(url, headers=headers, data=json.dumps(body))
        print(f"type={type(response.text)}")
        print("response status %r" % response.status_code)
        print("response text %r" %  json.loads(response.text))
      
        return response
    except Exception as ex:
        print(ex)
