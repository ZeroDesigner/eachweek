# Python与PubMed

#### 简介


这期是和半月刊一起在出，我本来的想法是，使用Python构建一个可以自动整理文献的工具

+ 来源：PubMed
+ IF影响因子: >3
+ 只是截取一些较为关键的信息：标题，杂志，发表日期，作者，PMID，摘要
+ 为了方便，摘要自动翻译为中文
+ 每周以邮件的形式发送到邮箱中，格式为MarkDown
+ 使用关键词检索，可以自己定义任意关键词
+ 可以自定义文献的时间段，例如前10天，20天等等

So，这就是半月刊的原型，后期通过人力矫正，我们进行整理规划。

所以，我是因为懒惰才创建的eachweek。

#### 主要使用流程

```
conda env create -f  eachweek.yml
conda activate eachweek
python eachweek.py
```
#### 需要修改的参数

1. 需要安装conda
2. 需要一个entra的email的账号
3. 需要获取邮箱的license，我是用的是qq邮箱
4. 可以自己定义关键词
5. 可以自己定义检索时间段，从当前开始往前推

#### 需要注意的事项

1. **不要滥用**
2. **不要滥用**
3. **不要滥用**

#### License

** GPL V3 **

#### conda环境

```yaml
name: eachweek
channels:
  - defaults
dependencies:
  - _libgcc_mutex=0.1=main
  - _openmp_mutex=4.5=1_gnu
  - backcall=0.2.0=pyhd3eb1b0_0
  - biopython=1.78=py37h7b6447c_0
  - blas=1.0=mkl
  - ca-certificates=2021.7.5=h06a4308_1
  - certifi=2021.5.30=py37h06a4308_0
  - decorator=5.0.9=pyhd3eb1b0_0
  - intel-openmp=2021.3.0=h06a4308_3350
  - ipython=7.26.0=py37hb070fc8_0
  - ipython_genutils=0.2.0=pyhd3eb1b0_1
  - jedi=0.18.0=py37h06a4308_1
  - libedit=3.1.20210216=h27cfd23_1
  - libffi=3.2.1=hf484d3e_1007
  - libgcc-ng=9.3.0=h5101ec6_17
  - libgomp=9.3.0=h5101ec6_17
  - libstdcxx-ng=9.3.0=hd4cf53a_17
  - matplotlib-inline=0.1.2=pyhd3eb1b0_2
  - mkl=2021.3.0=h06a4308_520
  - mkl-service=2.4.0=py37h7f8727e_0
  - mkl_fft=1.3.0=py37h42c9631_2
  - mkl_random=1.2.2=py37h51133e4_0
  - ncurses=6.2=he6710b0_1
  - numpy=1.20.3=py37hf144106_0
  - numpy-base=1.20.3=py37h74d4b33_0
  - openssl=1.0.2u=h7b6447c_0
  - parso=0.8.2=pyhd3eb1b0_0
  - pexpect=4.8.0=pyhd3eb1b0_3
  - pickleshare=0.7.5=pyhd3eb1b0_1003
  - pip=21.2.2=py37h06a4308_0
  - prompt-toolkit=3.0.17=pyh06a4308_0
  - ptyprocess=0.7.0=pyhd3eb1b0_2
  - pygments=2.9.0=pyhd3eb1b0_0
  - python=3.7.0=h6e4f718_3
  - readline=7.0=h7b6447c_5
  - setuptools=52.0.0=py37h06a4308_0
  - six=1.16.0=pyhd3eb1b0_0
  - sqlite=3.33.0=h62c20be_0
  - tk=8.6.10=hbc83047_0
  - traitlets=5.0.5=pyhd3eb1b0_0
  - wcwidth=0.2.5=py_0
  - wheel=0.37.0=pyhd3eb1b0_0
  - xz=5.2.5=h7b6447c_0
  - zlib=1.2.11=h7b6447c_3
  - pip:
    - beautifulsoup4==4.9.3
    - bs4==0.0.1
    - chardet==3.0.4
    - charset-normalizer==2.0.4
    - click==8.0.1
    - coloredlogs==15.0.1
    - googletrans==3.1.0a0
    - greenlet==1.1.1
    - h11==0.9.0
    - h2==3.2.0
    - hpack==3.0.0
    - hstspreload==2021.8.1
    - httpcore==0.9.1
    - httpx==0.13.3
    - humanfriendly==9.2
    - hyperframe==5.2.0
    - idna==2.10
    - impact-factor==1.0.8
    - importlib-metadata==4.6.4
    - interval==1.0.0
    - pandas==1.1.5
    - pyside6==6.1.2
    - python-dateutil==2.8.2
    - pytz==2021.1
    - requests==2.26.0
    - rfc3986==1.5.0
    - shiboken6==6.1.2
    - simple-loggers==1.0.4
    - sniffio==1.2.0
    - soupsieve==2.2.1
    - sqlalchemy==1.4.22
    - typing-extensions==3.10.0.0
    - urllib3==1.26.6
    - webrequests==1.0.4
    - zipp==3.5.0
prefix: /home/user/miniconda3/envs/eachweek
```



#### 源码

```python
# !/home/spuser/miniconda3/envs/eachweek/bin/python
# coding=utf-8

'''
Author: sujiaqi
Date: 2021-08-17 17:56:17
LastEditTime: 2021-08-22 13:34:30
Description: get week paper
FilePath: /Users/sujiaqi/Desktop/周刊/eachweek.py
'''

def geogle_translate(input_str):
    from googletrans import Translator
    translator = Translator()
    translations = translator.translate([input_str], dest='zh-cn',src='en')
    return translations[0].text
    
def get_abstract(pmid):
    from Bio import Entrez
    from Bio import Medline
    import numpy as np
    # 注册好的entrez的账号
    Entrez.email = "12223334@outlook.com"
    handle = Entrez.efetch(db="pubmed", id=pmid,rettype="medline")
    records = Medline.parse(handle)
    records = list(records)
    for index in np.arange(len(records)):
        abstract = records[index].get("AB", "?")
    return abstract

def search_in_pmd(key_words):
    from Bio import Entrez
    # 注册好的entrez的账号
    Entrez.email = "12223334@outlook.com"
    handle = Entrez.esearch(db="pubmed", term=key_words)
    record = Entrez.read(handle)
    return record['IdList']

def get_summary(pmid):
    from Bio import Entrez
    Entrez.email = "luskyqi@outlook.com"
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
    # 判断时间段，间隔时间为天
    nt_7 = datetime.now() - timedelta(days=15)
    pubdata = parse(t)
    if nt_7<pubdata<nt:
        return 1
    else:
        return 0
#def judge_paper(journal):
#    import pickle
#    f=open ("id.txt", 'rb')
#    if_dict=pickle.load(f)
#    print(journal,if_dict[journal])
#    try:
#        if if_dict[journal] != 'Not Available' and if_dict[journal] > 3 :
#            return 1
#        else:
#            return 0
#    except:
#        return 0
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

def md_special(key_words):
    pmid_list = search_in_pmd(key_words)
    pmid_dict = []
    header = '<header-box>str0</header-box>\n'
    md_text = '# tmp\n\n'
    md_text = md_text.replace('tmp',key_words)
    count = 0
    for i in pmid_list:
        #print(i)
        summary = get_summary(i)
        if judge_time(summary['History']['pubmed'][0]) == 1 and judge_paper(summary['Source']) > 3  :
            #abstract = get_abstract(i)
            basic_info = {}
            basic_info['If'] = judge_paper(summary['Source'])
            basic_info['Id'] =summary['Id']
            basic_info['PubDate']=summary['History']['pubmed'][0]
            basic_info['Title'] =summary['Title']
            basic_info['Source']=summary['Source']
            basic_info['LastAuthor']=summary['LastAuthor']
            abstract = get_abstract(i).replace( "'", "\'" )
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
def auto_report(receiver,sender,mail_license,smtpserver,mail_body,mail_title):
    import smtplib
    from email.mime.text import MIMEText
    from email.header import Header
    message = MIMEText( mail_body, 'plain', 'utf-8' )
    message ['From'] = sender                                              
    message['To'] = receiver                                              
    message['Subject'] = Header( mail_title, 'utf-8' )  
    smtp = smtplib.SMTP()                                               
    smtp.connect( smtpserver )                                        
    smtp.login( sender, mail_license )                               
    smtp.sendmail( sender, receiver, message.as_string() )     
    smtp.quit()
    return

if __name__ == '__main__':
    import  datetime
    nt = datetime.datetime.today()
    #for i in  range(len(10)):
    # 在这里输入你的检索的关键词
    kword_list = ['Peptide','Virus','CADD','DOCK','Molecular Dynamics','SARS-COV-2','COVID-19''Drug','AI']
    this_week = ''
    for w in kword_list:
        this_week = this_week + md_special(w)
    # you need to get these informations below
    # 接受邮箱
    receiver = 'pubmed@outlook.com'
    # 发送邮箱
    sender = '12345678@qq.com'
    # 邮箱的license
    mail_license = '1a2b3c4d5e6f7g8h9j0k'
    smtpserver = 'smtp.qq.com'
    mail_body = this_week
    mail_title = '半月刊 '+str(nt.year)+'-'+str(nt.month)+'_'+str(nt.day)
    auto_report(receiver,sender,mail_license,smtpserver,mail_body,mail_title)

```

