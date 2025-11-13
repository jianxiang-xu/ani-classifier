

import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time
import re

def download_images_from_url(base_url, save_folder, max_images=8000, max_pages=5000):
    """
    从指定URL下载图片到本地文件夹（支持自动翻页）
    
    参数:
        base_url (str): 要爬取的网页URL（可以包含页码占位符{page}）
        save_folder (str): 保存图片的文件夹
        max_images (int): 最大下载图片数量
        max_pages (int): 最大爬取页数
    """
    # 创建保存图片的文件夹
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    downloaded_count = 0
    page = 0
    

    
    while downloaded_count < max_images and page <= max_pages:
        try:
            # 处理分页URL（支持{page}占位符或原始URL）
            if '{page}' in base_url:
                url = base_url.format(page=page)
            else:
                url = f"{base_url}&page={page}" if page > 1 else base_url
            
            print(f"\n正在爬取第 {page} 页: {url}")
            
            # 获取网页内容
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            # 解析HTML内容
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 查找所有图片标签
            img_tags = soup.find_all('img')
            
            for img in img_tags:
                if downloaded_count >= max_images:
                    break
                
                try:
                    # 获取图片URL
                    img_url = img.get('src') or img.get('data-src')
                    if not img_url:
                        continue
                    
                    # 处理相对URL

                    img_url = urljoin(url, img_url)
                    
                    # # 过滤非图片URL
                    # if not re.search(r'\.(jpg)$', img_url, re.I):
                    #     continue
                    
                    # 获取图片文件名
                    img_name = os.path.basename(urlparse(img_url).path)
                    if not img_name:
                        img_name = f"image_{int(time.time())}.jpg"
                    elif '?' in img_name:  # 去除URL参数
                        img_name = img_name.split('?')[0]
                    
                    # 检查文件是否已存在
                    save_path = os.path.join(save_folder, img_name)
                    if os.path.exists(save_path):
                        continue
                    
                    # 下载图片
                    img_data = requests.get(img_url, headers=headers, timeout=10).content
                    
                    # 保存图片
                    with open(save_path, 'wb') as f:
                        f.write(img_data)
                    
                    downloaded_count += 1
                    print(f"已下载[{downloaded_count}/{max_images}]: {img_name}")
                    
                except Exception as e:
                    print(f"下载图片时出错: {e}")
                    continue
            
            # 尝试查找下一页链接（备用方法）
            next_page_link = None
            for a_tag in soup.find_all('a', href=True):
                if 'next' in a_tag.text.lower() or '下一页' in a_tag.text:
                    next_page_link = urljoin(url, a_tag['href'])
                    break
            
            if next_page_link and next_page_link != url:  # 防止无限循环
                base_url = next_page_link.split('&page=')[0] if '&page=' in next_page_link else next_page_link
                page += 1
            else:
                page += 1  # 简单递增页码
            
            
        except Exception as e:
            print(f"爬取第 {page} 页时出错: {e}")
            break
    
    print(f"\n完成! 共下载 {downloaded_count} 张图片到 '{save_folder}' 文件夹")

if __name__ == "__main__":
    # 使用示例
    print("网页图片爬虫（支持自动翻页）")
    print("=" * 50)
    
    target_url ='https://bgm.tv/character?orderby=comment' 
    save_dir = input("请输入保存图片的文件夹名称: ").strip(

    ) or 'charactor'
    max_img = input("请输入最大下载图片数量(默认为500): ").strip()
    max_img = int(max_img) if max_img.isdigit() else 500
    max_pg = input("请输入最大爬取页数(默认为50): ").strip()
    max_pg = int(max_pg) if max_pg.isdigit() else 50
    
    download_images_from_url(target_url, save_dir, max_img, max_pg)
