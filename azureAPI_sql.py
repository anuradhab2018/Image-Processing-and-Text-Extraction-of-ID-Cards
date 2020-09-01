# Link to source: https://docs.microsoft.com/en-us/azure/mysql/connect-python

import os
import json
import requests
import mysql.connector
from mysql.connector import errorcode

API_KEY = '078706da7479441fb6337355c3b91741'
ENDPOINT = 'https://ar2020.cognitiveservices.azure.com/vision/v1.0/ocr'
DIR = 'C://Users//DELL//Desktop//Maveai//NewImages/'

#-------------------------------------------------------------------
# Obtain connection string information from the portal
config = {
  'host':'<mydemoserver>.mysql.database.azure.com',
  'user':'<myadmin>@<mydemoserver>',
  'password':'<mypassword>',
  'database':'<mydatabase>'
}
#-------------------------------------------------------------------

def handler():
    text = ''
    for filename in sorted(os.listdir(DIR)):
        if filename.endswith(".jpeg"):
            output_file_name = os.path.splitext(filename)[0]
            pathToImage = '{0}/{1}'.format(DIR, filename)
            results = get_text(pathToImage)
            text += parse_text(results)
            #open('exceloutput.xls', 'w+',encoding="utf-8-sig").write(text)
            open(output_file_name+'.csv', 'w').write(text)
#-------------------------------------------------------------------
            # Insert some data into table
            cursor.execute("INSERT INTO inventory (name, quantity) VALUES (%s, %s);", ("banana", 150))
            print("Inserted",cursor.rowcount,"row(s) of data.")
#-------------------------------------------------------------------
def parse_text(results):
    text = ''
    for region in results['regions']:
        for line in region['lines']:
            for word in line['words']:
                text += word['text'] + ' '
            text += '\n'
    text_encoded = text.encode(encoding = "utf-8")
    return text_encoded

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
    return results

if __name__ == '__main__':
#-------------------------------------------------------------------
    #Construct connection string
    try:
       conn = mysql.connector.connect(**config)
       print("Connection established")
    except mysql.connector.Error as err:
      if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with the user name or password")
      elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
      else:
        print(err)
    else:
      cursor = conn.cursor()
    
    # Drop previous table of same name if one exists
    cursor.execute("DROP TABLE IF EXISTS inventory;")
    print("Finished dropping table (if existed).")

    # Create table
    cursor.execute("CREATE TABLE inventory (name VARCHAR(50) PRIMARY KEY;")
    print("Finished creating table.")
#-------------------------------------------------------------------
    handler()
#-------------------------------------------------------------------
    # Cleanup
    conn.commit()
    cursor.close()
    conn.close()
    print("Done.")
#-------------------------------------------------------------------