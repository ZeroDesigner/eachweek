# coding=utf-8

'''
Author: sujiaqi
Date: 2021-08-17 17:56:17
LastEditTime: 2021-12-11 14:54:29
Description: get week paper
FilePath: /Users/sujiaqi/Desktop/周刊/eachweek.py
'''

from googletrans import Translator


def geogle_translate(input_str):
    translator = Translator()
    translations = translator.translate([input_str], dest='zh-cn',src='en')
    return translations[0].text

from Bio import Entrez
from Bio import Medline
import numpy as np

def get_abstract(pmid,Eemail):
    Entrez.email = Eemail
    handle = Entrez.efetch(db="pubmed", id=pmid,rettype="medline")
    records = Medline.parse(handle)
    records = list(records)
    for index in np.arange(len(records)):
        abstract = records[index].get("AB", "?")
    return abstract

def search_in_pmd(key_words,Eemail):
    # 输入你的entrez账号
    Entrez.email = Eemail
    handle = Entrez.esearch(db="pubmed", term=key_words)
    record = Entrez.read(handle)
    return record['IdList']

def get_summary(pmid,Eemail):
    Entrez.email = Eemail
    handle = Entrez.esummary(db="pubmed",id=pmid)
    return Entrez.read(handle)[0]

def into_md(basic_info):
    paper_block = '''
+ 标题：str1

+ 杂志：str2

+ 发表日期：str3

+ 作者：str4

+ PMID：str5

+ 摘要：

>str6

+ Abstract：

>str7

'''
    paper_block1=paper_block.replace('str1',basic_info['Title'])
    paper_block1=paper_block1.replace('str2',basic_info['Source'])
    paper_block1=paper_block1.replace('str3',basic_info['PubDate'])
    paper_block1=paper_block1.replace('str4',basic_info['LastAuthor'])
    paper_block1=paper_block1.replace('str5',basic_info['Id'])
    paper_block1=paper_block1.replace('str6',basic_info['abstract_zh'])
    paper_block1=paper_block1.replace('str7',basic_info['abstract_en'])
    #printstar_str=str(basic_info['star']*3)
    #print(basic_info['star'])
#    paper_block1=paper_block1.replace('star',basic_info['star']*':star:')
    return paper_block1

def judge_time(t):
    from dateutil.parser import parse
    from datetime import  datetime, timedelta
    nt = datetime.now()
    # 在这里输入你的时间节点
    nt_7 = datetime.now() - timedelta(days=15)
    pubdata = parse(t)
    if nt_7<pubdata<nt:
        return 1
    else:
        return 0

def judge_paper(journal):
    import os
    cmd_str = 'impact_factor search \"tmp\"'
    try:
        cmd_str = cmd_str.replace('tmp',journal)
        text = os.popen(cmd_str).read()
        factor = text.split('\"factor\": ')[1].split(',')[0]
        return float(factor)
    except:
        #print('None',journal)

        return 0

def star_paper(factor):
    if factor >= 9:
        return 5
    elif 3 <= factor < 5:
        return 3
    elif 5 <= factor < 9:
        return 4
    elif factor < 3:
        return 0

def md_special(key_words,Eemail):
    pmid_list = search_in_pmd(key_words,Eemail)
    pmid_dict = []
    header = '<header-box>str0</header-box>\n'
    md_text = '# tmp\n\n'
    md_text = md_text.replace('tmp',key_words)
    count = 0
    for i in pmid_list:
        #print(i)
        summary = get_summary(i,Eemail)
        if judge_time(summary['History']['pubmed'][0]) == 1 and judge_paper(summary['Source']) > 3  :
            #abstract = get_abstract(i)
            basic_info = {}
            basic_info['If'] = judge_paper(summary['Source'])
            basic_info['Id'] =summary['Id']
            basic_info['PubDate']=summary['History']['pubmed'][0]
            basic_info['Title'] =summary['Title']
            basic_info['Source']=summary['Source']
            basic_info['LastAuthor']=summary['LastAuthor']
            abstract = get_abstract(i,Eemail).replace( "'", "\'" )
            basic_info['abstract_zh']=geogle_translate(abstract)
            basic_info['abstract_en']=abstract
            basic_info['star']= star_paper(float(basic_info['If']))
            print(basic_info['star'])
            print(float(basic_info['If']))
            #print(basic_info['abstract'])
            #input_str=input_str.replae( "'", "" )
            #print(sumary)
            print(basic_info['Title'],basic_info['Id'],basic_info['PubDate'],basic_info['If'],basic_info['star'])
            count = count + 1 
            header_t  = header.replace('str0',str(count))
            md_text = md_text + header_t + into_md(basic_info) 
        else:
            True 
    return md_text

#coding: utf-8

if __name__ == '__main__':
    import  datetime
    nt = datetime.datetime.today()
    import json
    
    with open("./keywords.json",'r') as keyw:
        All_words = json.load(keyw)
    # entrez账号
    Eemail=All_words['entrez']
    # 在这里输入你的检索的关键词
    kword_list = All_words['kword_list'].split(",")
    this_week = ''
    for w in kword_list:
        this_week = this_week + md_special(w,Eemail)
    title = '半月刊 '+str(nt.year)+'-'+str(nt.month)+'_'+str(nt.day)
    md_filename = '/data/Eachweek/source/_posts/nots'+title
    with open(md_filename,'w+') as mdf:
        mdf.write(this_week)