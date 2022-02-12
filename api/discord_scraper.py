import requests
import re

def scrape_messages(token, channel_id):
        
    url = 'https://discord.com/api/v8/channels/{}/messages'.format(channel_id)
    header = {"authorization": token}

    r = requests.get(url, headers=header)
    print(r.status_code)
    data = r.json()

    content = []
    usernames = []
    timestamps = []

    for j in data:
        
        msgcontent = j['content']
        msgcontent = re.sub(r'[\d\.]', '', re.sub(r'<@.+>', '', msgcontent))
        msgcontent = re.sub(r"[+/-/']", '', msgcontent)
        #Removes all mentions, then removes all non alphanumberic, then removes all numbers
        
        RE_EMOJI = re.compile('[\U00010000-\U0010ffff]', flags=re.UNICODE) #removes all emojis
        msgcontent = RE_EMOJI.sub(r'', msgcontent)
       

        msgusername = j['author']['username']
        turnintodate = lambda date: date[:date.find('.')].replace('T', ' ')
        timestamp = turnintodate(j['timestamp'])
        
        msgcontent = re.sub(' +', ' ', msgcontent).lower() #removes extra spaces
        
        if len(j['attachments']) == 0: #filters out messages with attachments
                    
            content.append(msgcontent)
            usernames.append(msgusername)
            timestamps.append(timestamp)
        
    content, usernames, timestamps = content[::-1], usernames[::-1], timestamps[::-1]

    return content, usernames, timestamps
