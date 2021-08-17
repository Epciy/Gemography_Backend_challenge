'''fetching number  and list of repos for each language '''
from flask import Flask, jsonify 
import requests
import pandas as pd
from datetime import datetime, timedelta


today = datetime.now()
last_thirty_days = (today - timedelta(days=30)).strftime("%Y-%m-%d")

api = 'https://api.github.com/search/repositories?q=created:>{0}&sort=stars&order=desc&page=1&per_page=100'.format(last_thirty_days)


response =requests.get(api)
response.status_code
repos=response.json()
data=repos['items']
df = pd.DataFrame(data)
lang=df.groupby(['language']).groups
#print(lang)




trending_repos = []

app = Flask(__name__)


@app.route("/", methods=['GET'])
def langage_of_trending_repo():
    for l, k in lang.items():
        repos=[]
        for i in k:
            repos.append({
                'name':df.loc[i]['name'],
                'url':df.loc[i]['url'] 

            })
            
        each_lang={
            'language':l, 
              'number_of_repos':len(k),
              'list_of_repos':repos

        }
        trending_repos.append(each_lang )
    return jsonify (trending_repos) 
  
    

if __name__=='__main__':
    app.run(debug=True,port=5000,host='localhost')