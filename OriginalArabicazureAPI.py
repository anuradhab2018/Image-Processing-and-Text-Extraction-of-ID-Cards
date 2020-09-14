import os
import json
import requests
import re
from PIL import Image
import numpy as np
import pymongo


API_KEY = '############################'
ENDPOINT = '#################################/v1.0/ocr'
DIR = 'C://Users//DELL//Desktop//Maveai//Images//Residentcard//Preprocessed//combined'
output_dir = 'C://Users//DELL//Desktop//Maveai//Images//Residentcard//outputresident'
#Mongodb
client = pymongo.MongoClient('mongodb://localhost:27017/')
mydb = client['Residentcard']
NewResidentcardinfo = mydb.NewResidentcardinformation

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




                 # EnglishName Value
                name_build =""
                test = results['regions'][8]
                test1 = test['lines'][3]
                name = test1['words']
                for items in range(len(name)):
                    if items > 0:
                        name_temp = name[items]
                        name_build = name_build + " " + name_temp['text']

                name_build1 = ""
                test = results['regions'][8]
                test1 = test['lines'][4]
                name = test1['words']
                for items in name:
                    if str.isalpha(items['text']):
                        name_build1 = name_build1 + " " + items['text']


                Name = name_build + name_build1

                whole_json_1 = results['regions']
                for items_1 in whole_json_1:
                        whole_json_2 = items_1['lines']
                        for items_2 in whole_json_2:
                            whole_json_3 = items_2['words']
                            if whole_json_3[0]['text'] == "Sex":
                                value_of_sex = whole_json_3[1]['text']
                                value_of_sex_value_ar = whole_json_3[2]['text']
                                value_of_sex_key_ar = whole_json_3[3]['text']
                            if whole_json_3[0]['text'] == "Date":
                                value_of_dob = whole_json_3[3]['text']
                                value_of_dob_key_ar = whole_json_3[4]['text']
                                value_of_dob_value_ar = whole_json_3[5]['text']

                            if whole_json_3[0]['text'] == "United":
                                value_of_country ="United Arab Emirates"
                            if whole_json_3[0]['text'] == "Resident" or "Identity":
                                value_of_typeofdocument = "Resident Identity Card"

                for items_1 in whole_json_1:
                    whole_json_2 = items_1['lines']
                    if whole_json_2[0]['words'][0]['text'] == "ID":
                        valueof_IDcardnumber = whole_json_2[1]['words'][0]['text']
                        valueof_IDcardnumber_key_ar = whole_json_2[0]['words'][3]['text']
                        valueof_IDcardnumber_value_ar = whole_json_2[0]['words'][4]['text']
                        nationality_value = whole_json_2[6]['words'][1]['text']
                        nationality_key_ar = whole_json_2[5]['words'][1]['text']
                        nationality_value_ar = whole_json_2[5]['words'][0]['text']

                for items_1 in whole_json_1:
                    whole_json_2 = items_1['lines']
                    valueof_country_ar = whole_json_2[0]['words'][0]['text']

                for items_1 in whole_json_1:
                    whole_json_2 = items_1['lines']
                    if whole_json_2[0]['words'][0]['text'] == "Signature":
                        value_of_signature_key = whole_json_2[0]['words'][1]['text']
                        valueof_expirydate = whole_json_2[2]['words'][0]['text']
                        valueof_cardnumber = whole_json_2[1]['words'][0]['text']
                        value_of_expirydate_key_ar = whole_json_2[0]['words'][4]['text']
                        value_of_expirydate_value_ar = whole_json_2[0]['words'][5]['text']
                        value_of_cardnumber_key_ar = whole_json_2[0]['words'][9]['text']
                        value_of_cardnumber_value_ar = whole_json_2[0]['words'][10]['text']

                 # Information Extraction
                text_ocr = {}

                # Store the results in the dict
                text_ocr['Country'] = value_of_country
                text_ocr['Arabic_Country'] = value_of_country_ar

                text_ocr['Type_Of_Document'] = value_of_typeofdocument
                #text_ocr['Arabic_Type_Of_Document'] = Arabic_Type_Of_Document

                text_ocr['Expirydate'] = valueof_expirydate
                text_ocr['Arabic_Expiry_Date_Key'] = value_of_expirydate_key_ar
                text_ocr['Arabic_Expiry_Date_Value'] = value_of_expirydate_value_ar

                text_ocr['Dateofbirth'] = value_of_dob
                text_ocr['Arabic_DOB_Key'] = value_of_dob_key_ar
                text_ocr['Arabic_DOB_Value'] = value_of_dob_value_ar

                text_ocr['Signature_Key'] = value_of_signature_key

                text_ocr['Sex'] = value_of_sex
                text_ocr['ArabicSex_Key'] = value_of_sex_key_ar
                text_ocr['ArabicSex_Value'] = value_of_sex_value_ar

                text_ocr['CardNumber'] = valueof_cardnumber
                text_ocr['Arabic_CardNumber_Key'] = value_of_cardnumber_key_ar
                text_ocr['Arabic_CardNumber_Value'] = value_of_cardnumber_value_ar

                text_ocr['IDnumber'] = valueof_IDcardnumber
                text_ocr['Arabic_IDnumber_Key'] = valueof_IDcardnumber_key_ar
                text_ocr['Arabic_IDnumber_Value'] = valueof_IDcardnumber_value_ar

                text_ocr['Name'] = Name
                #text_ocr['Arabic_name_Key'] = Arabic_name_Key

                text_ocr['Nationality'] = nationality_value
                text_ocr['Arabic_Nationality_Key'] = nationality_key_ar
                text_ocr['Arabic_Nationality_Value'] = nationality_value_ar

                print(text_ocr)
                NewResidentcardinfo.insert_one(text_ocr)
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
