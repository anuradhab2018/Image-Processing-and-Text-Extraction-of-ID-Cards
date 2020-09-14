import os
import json
import requests
import re
from PIL import Image
import numpy as np
import pymongo


API_KEY = '078706da7479441fb6337355c3b91741'
ENDPOINT = '$$$$$$$$$$$$$$$$$$$$$$$$$$$/vision/v1.0/ocr'
DIR = 'C://Users//DELL//Desktop//Maveai//Images//Residentcard//Preprocessed//combined'
output_dir = 'C://Users//DELL//Desktop//Maveai//Images//Residentcard//outputresident'
#Mongodb
client = pymongo.MongoClient('mongodb://localhost:27017/')
mydb = client['Residentcard']
ArabicResidentcardinfo = mydb.ArabicResidentcardinformation

def handler():

    for filename in sorted(os.listdir(DIR)):
        if filename.endswith(".jpeg") or filename.endswith(".jpg") or filename.endswith(".png"):
            output_file_name = os.path.splitext(filename)[0]
            pathToImage = '{0}/{1}'.format(DIR, filename)
            results = get_text(pathToImage)
            text = parse_text(results)

def parse_text(results):

                text = ''
                for region in results['regions']:
                    for line in region['lines']:
                        print(line)
                        for word in line['words']:
                            print(word)
                            text += word['text'] + ' '
                        text += '\n'

                # Country information parsing
                test = results['regions'][7]
                test1 = test['lines'][0]
                test2 = test1['words'][0]
                test3 = test1['words'][1]
                test4 = test1['words'][2]
                test5 = test1['words'][3]
                dict1 = test2['text']
                dict2 = test3['text']
                dict3 = test4['text']
                dict4 = test5['text']
                Arabic_Country = dict1 + dict2 + dict3 + dict4

                # Sex information parsing
                test = results['regions'][0]
                test1 = test['lines'][0]
                test2 = test1['words'][1]
                Sex = (test2['text'])

                # ArabicSex_Key
                test = results['regions'][0]
                test1 = test['lines'][0]
                test2 = test1['words'][3]
                ArabicSex_Key = (test2['text'])

                # ArabicSex_Value
                test = results['regions'][0]
                test1 = test['lines'][0]
                test2 = test1['words'][2]
                ArabicSex_Value = (test2['text'])

                # Date of Birth parsing
                test = results['regions'][1]
                test1 = test['lines'][0]
                test2 = test1['words'][3]
                Dateofbirth = (test2['text'])

                # Arabic_DOB_Key parsing
                test = results['regions'][1]
                test1 = test['lines'][0]
                test2 = test1['words'][4]
                Arabic_DOB_Key = (test2['text'])

                # Arabic_DOB_Value parsing
                test = results['regions'][1]
                test1 = test['lines'][0]
                test2 = test1['words'][5]
                Arabic_DOB_Value = (test2['text'])

                # Signature_Key parsing
                test = results['regions'][2]
                test1 = test['lines'][0]
                test2 = test1['words'][1]
                Signature_Key = (test2['text'])

                #Expiry Date parsing
                test = results['regions'][2]
                test1 = test['lines'][2]
                test2 = test1['words'][0]
                Expirydate = (test2['text'])

                # Arabic_Expiry_Date_Key parsing
                test = results['regions'][2]
                test1 = test['lines'][0]
                test2 = test1['words'][4]
                Arabic_Expiry_Date_Key = (test2['text'])

                # Arabic_Expiry_Date_Value parsing
                test = results['regions'][2]
                test1 = test['lines'][0]
                test2 = test1['words'][5]
                Arabic_Expiry_Date_Value = (test2['text'])

                # CardNumber parsing
                test = results['regions'][2]
                test1 = test['lines'][1]
                test2 = test1['words'][0]
                CardNumber = (test2['text'])

                # Arabic_CardNumber_Key parsing
                test = results['regions'][2]
                test1 = test['lines'][0]
                test2 = test1['words'][8]
                test3 = test1['words'][9]
                dict1 = test2['text']
                dict2 = test3['text']
                Arabic_CardNumber_Key = dict1 + dict2

                # Arabic_CardNumber_Value parsing
                test = results['regions'][2]
                test1 = test['lines'][0]
                test2 = test1['words'][10]
                Arabic_CardNumber_Value = (test2['text'])

                # ArabicIDnumber_Key
                test = results['regions'][8]
                test1 = test['lines'][0]
                test2 = test1['words'][3]
                test3 = test1['words'][4]
                dict1 = test2['text']
                dict2 = test3['text']
                Arabic_IDnumber_Key = dict1 + dict2

                #IDcardnumber
                test = results['regions'][8]
                test1 = test['lines'][1]
                test2 = test1['words'][0]
                IDnumber = (test2['text'])

                # ArabicName Key
                test = results['regions'][8]
                test1 = test['lines'][2]
                test2 = test1['words'][5]
                Arabic_name_Key = test2['text']

                #Nationality
                test = results['regions'][8]
                test1 = test['lines'][6]
                test2 = test1['words'][1]
                Nationality = (test2['text'])

                # ArabicNationality_Key
                test = results['regions'][8]
                test1 = test['lines'][5]
                test2 = test1['words'][1]
                Arabic_Nationality_Key = (test2['text'])

                # ArabicNationality_Value
                test = results['regions'][8]
                test1 = test['lines'][5]
                test2 = test1['words'][0]
                Arabic_Nationality_Value = (test2['text'])

                    # EnglishName Value
                name_build =""
                test = results['regions'][8]
                test1 = test['lines'][3]
                name = test1['words']
                for items in range(len(name)):
                    if items > 0:
                        name_temp = name[items]
                        name_build = name_build + name_temp['text']

                print(name_build)
                print("44444444444444444444444444444444444444444")

                name_build1 = ""
                test = results['regions'][8]
                test1 = test['lines'][4]
                name = test1['words']
                for items in name:
                    if str.isalpha(items['text']):
                        name_build1 = name_build1 + items['text']

                print(name_build1)
                print("44444444444444444444444444444444444444444")
                Name= (name_build+name_build1)

                #Name = EnglishName1 + EnglishName2

                # Information Extraction
                text_ocr = {}

                Country = re.search(r"\bUnited.*Emirates\b", text).group()

                # ID card varies as  Resident Identity Card or Identity Card both is the same
                if re.search(r"\bResident.*Card\b", text) is not None:
                    Type_Of_Document = re.search(r"\bResident.*Card\b", text).group()

                elif re.search(r"\bIdentity.*Card\b", text) is not None:
                    Type_Of_Document = re.search(r"\bIdentity*Card\b", text).group()

                # Store the results in the dict
                text_ocr['Country'] = Country
                text_ocr['Arabic_Country'] = Arabic_Country
                text_ocr['Type_Of_Document'] = Type_Of_Document
                #text_ocr['Arabic_Type_Of_Document'] = Arabic_Type_Of_Document
                text_ocr['Dateofbirth'] = Dateofbirth
                text_ocr['Arabic_DOB_Key'] = Arabic_DOB_Key
                text_ocr['Arabic_DOB_Value'] = Arabic_DOB_Value
                text_ocr['Signature_Key'] = Signature_Key
                text_ocr['Sex'] = Sex
                text_ocr['ArabicSex_Key'] = ArabicSex_Key
                text_ocr['ArabicSex_Value'] = ArabicSex_Value
                text_ocr['Expirydate'] = Expirydate
                text_ocr['Arabic_Expiry_Date_Key'] = Arabic_Expiry_Date_Key
                text_ocr['Arabic_Expiry_Date_Value'] = Arabic_Expiry_Date_Value
                text_ocr['CardNumber'] = CardNumber
                text_ocr['Arabic_CardNumber_Key'] = Arabic_CardNumber_Key
                text_ocr['Arabic_CardNumber_Value'] = Arabic_CardNumber_Value
                text_ocr['Arabic_IDnumber_Key'] = Arabic_IDnumber_Key
                text_ocr['IDnumber'] = IDnumber
                text_ocr['Arabic_name_Key'] = Arabic_name_Key
                text_ocr['Name'] = Name
                text_ocr['Arabic_Nationality_Key'] = Arabic_Nationality_Key
                text_ocr['Arabic_Nationality_Value'] = Arabic_Nationality_Value
                text_ocr['Nationality'] = Nationality


                print(text_ocr)
                ArabicResidentcardinfo.insert_one(text_ocr)
                return text

def get_text(pathToImage):
                print('Processing: ' + pathToImage)
                headers = {
                    'Ocp-Apim-Subscription-Key': API_KEY,
                    'Content-Type': 'application/octet-stream'
                }
                params = {
                    'language': 'ar',
                    'detectOrientation ': 'true'
                }
                payload = open(pathToImage, 'rb').read()
                response = requests.post(ENDPOINT, headers=headers, params=params, data=payload)
                results = json.loads(response.content)
                print(results)
                return results

if __name__ == '__main__':
    handler()
