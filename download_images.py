import os
import requests
import json
from urllib.request import urlretrieve


def images_download(input_file,output_file):
    # 读取 JSON 文件
    data_processed=[]
    with open(input_file, 'r') as f:
        data = json.load(f)
        
    img_dir_context='images_context'
    img_dir_cover='images_cover'
    # 创建用于存储图片的文件夹
    if not os.path.exists(img_dir_cover):
        os.makedirs(img_dir_cover)
    
    if not os.path.exists(img_dir_context):
        os.makedirs(img_dir_context)
    
    # 遍历 JSON 数据并下载图片
    for item in data:
        image_url = item['image_url']
        image_filename = os.path.basename(image_url)
        image_path = os.path.join(img_dir_cover, image_filename)
    
        # 下载图片并保存到本地
        response = requests.get(image_url)
        with open(image_path, 'wb') as f:
            f.write(response.content)
    
        # 替换图片网址为本地路径
        item['image_url'] = image_path
    
        for context in item['context']:
            if 'image' in context:
                image_url_context = context['image']
                image_filename = os.path.join(img_dir_context, os.path.basename(image_url_context))
                urlretrieve(image_url_context, image_filename)
                context['image'] = image_filename

        item_processed={
                        'image_cover': image_path,
                        'title': item['title'],
                        'article_url': item['article_url'],
                        'context' : item['context']
        }
        data_processed.append(item_processed)
    
    # 将更新后的数据保存到新的 JSON 文件
    with open(output_file, 'w') as f:
        json.dump(data_processed, f, indent=2)
    
    print('数据已保存到文件中')