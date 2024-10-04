import requests
import json

# Step 1
url = "https://api.ihome.com/api/home/getfeeds?"
headers = {
    "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 12; ASUS_I003DD Build/PI)",  
    "Authorization": "gzip"  
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    with open('1.json', 'w', encoding='utf-8') as f:
        json.dump(response.json(), f, ensure_ascii=False, indent=4)
else:
    raise Exception(f"请求失败，状态码: {response.status_code}")

# Step 2
with open('1.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 展平 JSON 数据
def flatten_json(y):
    out = {}

    def flatten(x, name=''):
        if isinstance(x, dict):
            for a in x:
                flatten(x[a], name + a + '.')
        elif isinstance(x, list):
            for i, a in enumerate(x):
                flatten(a, name + str(i) + '.')
        else:
            out[name[:-1]] = x

    flatten(y)
    return out

# 
flat_data = flatten_json(data)

# Step 3
target_ranges = [(50, 95), (167, 212), (307, 352)]
titles = []

for key, value in flat_data.items():
    if 'title' in key and isinstance(value, str) and all('\u4e00' <= char <= '\u9fff' for char in value):
        key_parts = key.split('.')
        if len(key_parts) >= 2 and key_parts[-2].isdigit():
            line_number = int(key_parts[-2])
            for start, end in target_ranges:
                if start <= line_number <= end:
                    titles.append(value)

# Step 4
output_titles = [f"{idx + 1}. {title}" for idx, title in enumerate(titles)]

# print(output_titles)
for line in output_titles:
    print(line)
