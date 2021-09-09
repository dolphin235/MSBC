#!/usr/bin/python3

import os
import site_list
from bs4 import BeautifulSoup
import urllib.request
import re


g_data_dir_name = 'dataset'
g_categories = ['governance', 'threat_intelligence', 'security_operation', 'security_architecture', 'major_area']
g_dict_list = {
    'governance' : site_list.governance_urls,
    'threat_intelligence': site_list.threat_intelligence_urls,
    'security_operation': site_list.security_operation_urls,
    'security_architecture': site_list.security_architecture_urls,
    'major_area': site_list.major_area_urls
}



def request_url(url):
    headers = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'}
    req = urllib.request.Request(url, headers=headers)
    response = urllib.request.urlopen(req, timeout=20)

    if response.status == 200:
        return response
    else:
        print(f"[ERROR] Get url fail response: [{response.status_code}] - [{url}]")


def remove_in_bracket(text):
    fcnt = 0
    res = ''
    for c in text:
        if c == '<':
            fcnt = fcnt + 1
            continue

        if c == '>':
            if fcnt == 0:
                print("[ERROR]: flag count error !!")
                print(text)
                exit()
            else:
                fcnt = fcnt - 1
                continue
                
        if fcnt > 0:
            continue
        res = res + c

    return res


def get_content(url):
    print("[INFO] url: ["+url+"]")
    content = ""
    response = request_url(url)
    html = response.read()
    soup = BeautifulSoup(html, 'html.parser')

    tag = soup.findAll('div', attrs={'class':'entry-content'})
    content = remove_in_bracket(str(tag))

    return content

def save_text(text, dir_path, file_path):
    path = g_data_dir_name+"/"+dir_path+"/"+file_path
    print("[INFO] save file ["+path+"]")
    f = open(path, 'w')
    f.write(text)
    f.close()


def make_directory(dir_name):
    os.makedirs(dir_name)
    for cate in g_categories:
        os.makedirs(dir_name+'/'+cate)


def main():
    try:
        if not os.path.exists(g_data_dir_name):
            make_directory(g_data_dir_name)
        else:
            print("data dir already exist")
            exit()
    except Exception as e:
        print("[ERROR]: " + e)
    

    for cate in g_categories:
        num = 0
        for url in g_dict_list[cate]:
            num = num + 1
            save_text(get_content(url), cate, cate+'_'+str(num))


if __name__=="__main__":
        main()
