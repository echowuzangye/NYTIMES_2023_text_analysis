import json
import pandas as pd
import requests
import time

# Cannot import requests on python 3.10. 
# https://github.com/psf/requests/issues/5901
# need to update urllib3 to a newer version (>1.23 at the minimum)
# requests 2.28.1 requires urllib3<1.27,>=1.21.1
# I use python -m pip install urllib3==1.23

key='OWXgX1QxIO17AtYGKqz2AQjaXox6lXG9'
secret='qqdi2aRv5TfR8qOo'

NY_archive_ENDPOINT = 'https://api.nytimes.com/svc/archive/v1/2023/'


# get ALL NYTIMES archived article in 2023
for i in range(1,13):
    list = []
    response = requests.get(NY_archive_ENDPOINT + str(i) + '.json?api-key=' + key)
    data = response.json()['response']['docs']
    for file in data:
        news_dict = {'abstract': file['abstract'],
                    #  'keywords' : file['keywords'],
                     'pub_date' : file['pub_date'],
                     'document_type' : file['document_type'],
                     'news_desk' : file['news_desk'],
                     'section_name' : file['section_name'],
                     'type_of_material': file['type_of_material']          
        }

        keyword_list = []
        if len(file['keywords']) == 0:
            pass
        else:
            for word in file['keywords']:
                value = word['value'].upper()
                keyword_list.append(value)

        news_dict['keywords'] = keyword_list

        list.append(news_dict)
    
    # there are two rate limits per API: 500 requests per day and 5 requests per minute. 
    time.sleep(12)
    
    #save data into a csv file
    df = pd.DataFrame(list)
    df.to_csv(f'extra_data/2023-{i}.csv')

