import json
import requests

request_template = (
    "POST /Wxamp/Parent_Message/addMsg HTTP/1.1\n"
    "Host: app.gzhtedu.cn\n"
    "Connection: keep-alive\n"
    "Content-Length: {}\n"
    "Accept: */*\n"
    "Sec-Fetch-Site: cross-site\n"
    "Sec-Fetch-Mode: cors\n"
)

def extract_and_send_titles():
    # 
    with open('1.json', 'r', encoding='utf-8') as f:
        data = json.load(f)


    all_titles = []


    for item in data['data']['list']:
        feed_content = item.get('feedContent', {})

        
        if 'news' in feed_content:
            news_list = feed_content['news']
            for news in news_list:
                title = news.get('title')
                if title:  
                    all_titles.append(title)


        if 'sourceRankItem' in feed_content:
            source_rank_item = feed_content['sourceRankItem']
            if 'sourceRankRecordItems' in source_rank_item:
                source_rank_list = source_rank_item['sourceRankRecordItems']
                for record_item in source_rank_list:
                    title = record_item.get('title')
                    if title:  #
                        all_titles.append(title)


 
    selected_titles = all_titles[0:20] + all_titles[30:40]
    
    return selected_titles


def send_titles(selected_titles):
    request_template = (
        "POST /Wxamp/Parent_Message/addMsg HTTP/1.1\n"
        "Connection: keep-alive\n"
        "Content-Length: {}\n"
    )

    url = "https://app.gz.cn/ydzt/"
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': ' AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    }

    for title in selected_titles:
        
        chunks = [title[i:i+200] for i in range(0, len(title), 200)]
        
        for i, chunk in enumerate(chunks):
            # 构造请求数据
            request_data = request_template.format(chunk)
            content_length = len(request_data)
            request_data = request_data.replace('Content-Length: {}', f'Content-Length: {content_length}')
            
            
            print(f" {i+1} ：{chunk}")
            response = requests.post(url, data=request_data, headers=headers)
            
            
            print(f"：{response.status_code}, ：{response.text}")


fetch_json()
titles = extract_and_send_titles()
send_titles(titles)
