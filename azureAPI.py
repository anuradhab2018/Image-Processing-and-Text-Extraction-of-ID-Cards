import os
import json
import requests


API_KEY = '078706da7479441fb6337355c3b91741'
ENDPOINT = 'https://ar2020.cognitiveservices.azure.com/vision/v1.0/ocr'
DIR = 'C://Users//DELL//Desktop//Maveai//NewImages/'

def handler():

    for filename in sorted(os.listdir(DIR)):
        if filename.endswith(".jpeg"):
            output_file_name = os.path.splitext(filename)[0]
            pathToImage = '{0}/{1}'.format(DIR, filename)
            print(pathToImage)
            results = get_text(pathToImage)
            text = parse_text(results)
            
            #open('exceloutput.xls', 'w+',encoding="utf-8-sig").write(text)
            #open(output_file_name+'.csv', 'w',encoding="utf-8-sig").write(text)
            with open(output_file_name+'.csv', 'w',encoding="utf-8-sig") as fd:
                fd.write(text)
                fd.close()


def parse_text(results):
    text = ''
    for region in results['regions']:
        for line in region['lines']:
            print(line)
            for word in line['words']:
                print(word)
                text += word['text'] + ' '
            text += '\n'
    #text_encoded = text.encode(encoding = "utf-8-sig")
    #return text_encoded
    return text

def get_text(pathToImage):
    print('Processing: ' + pathToImage)
    headers  = {
        'Ocp-Apim-Subscription-Key': API_KEY,
        'Content-Type': 'application/octet-stream'
    }
    params   = {
        'language': 'ar',
        'detectOrientation ': 'true'
    }
    payload = open(pathToImage, 'rb').read()
    response = requests.post(ENDPOINT, headers=headers, params=params, data=payload)
    results = json.loads(response.content)
    #print(type(results))
    return results

if __name__ == '__main__':
    handler()
