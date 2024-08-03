import requests
from bs4 import BeautifulSoup
import json
from urllib.parse import urljoin

def image_text_get(url,file_get):
    response = requests.get(url)
    html_content = response.content

    soup = BeautifulSoup(html_content, 'html.parser')

    articles = soup.find_all("li", class_="clearfix")
    
    data = []
    
    for article in articles:
        image_url = urljoin(url, article.find('img')['data-original'])
        title = article.find('h3')
        if title:
            title = title.text.strip()
        else:
            title = ''
            
        brand = article.find('a', href='/company/12632')
        if brand:
            brand = brand.text.strip()
        else:
            brand = ''
            
        author = article.find('a', href='/company/12122')
        if author:
            author = author.text.strip()
        else:
            author = ''
            
        date = article.find('label')
        if date:
            date = date.text.strip()
        else:
            date = ''
            
        rating = article.find('em', class_='v_m')
        if rating:
            rating = rating.text.strip()
        else:
            rating = ''
            
        favorites = article.find_all('em', class_='v_m')
        if len(favorites) > 1:
            favorites = favorites[1].text.strip()
        else:
            favorites = ''
            
        comments = article.find_all('em', class_='v_m')
        if len(comments) > 2:
            comments = comments[2].text.strip()
        else:
            comments = ''
            
        article_url = article.find('a')['href']
        context_response= requests.get(article_url)
        context_html_content = context_response.content
        context_soup = BeautifulSoup(context_html_content, 'html.parser')
        
        article_con = context_soup.find("div", {"class": "article_con"})
        content_list = []
        current_text = ""
        article_children=article_con.children
        for element in article_children:
            tt=element.get_text().strip()
            if tt:
                for element_children in element.children:
                    if element_children.name == "p":
                        if element_children.children:
                            ii=element_children.find("img")
                            if ii:
                                try:
                                    img_src = element_children.find("img")["data-original"]
                                    content_list.append({"image": img_src})
                                except KeyError:
                                    break
                            text = element_children.get_text().strip()
                            if text:
                                content_list.append({"text": text})
                        else:
                            text = element_children.get_text().strip()
                            if text:
                                content_list.append({"text": text})
                    elif element_children.name == "h4":
                        text = element_children.get_text().strip()
                        content_list.append({"text": text})
    

        item = {
            'image_url': image_url,
            'title': title,
            'article_url': article_url,
            'context' : content_list
        }
        
        data.append(item)
    
    with open(file_get, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    
    print('数据已保存到文件中')