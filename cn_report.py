#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib2
import lxml
import lxml.html
import os
import hashlib
import jieba
from gensim.models import Word2Vec
import content_extract as ce
import text_util

def cache_dir():
    work_dir = os.path.dirname(os.path.realpath(__file__)) + "/.cache"
    if not os.path.isdir(work_dir):
        os.makedirs(work_dir)
    return work_dir

def get(url, enc='utf-8', cache=True):
    if cache:
        md5 = hashlib.md5(url).hexdigest()
        f = "%s/%s" % (cache_dir(), md5)
        if os.path.isfile(f):
            return open(f).read().decode(enc, 'ignore')
    req = urllib2.Request(url)
    req.add_header('User-Agent','Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3 QQDownload/1.7')
    req.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
    req.add_header('Accept-Language', 'zh-cn,zh;q=0.5')
    try:
        response = urllib2.urlopen(req)
        content = response.read()
        if cache:
            out = open(f, "w")
            out.write(content)
            out.close()
        content = content.decode(enc, 'ignore')
        return content
    except:
        return None
   
def crawl_report_list():
    '''
    抓取政府工作报告列表
    http://www.gov.cn/guoqing/2006-02/16/content_2616810.htm
    '''
    content = get("http://www.gov.cn/guoqing/2006-02/16/content_2616810.htm")
    if content is None: return []
    doc = lxml.html.document_fromstring(content)
    return doc.xpath("*//td//a/@href")

def build_model(cache=True):
    if cache:
        f = "%s/word2vec.model" % cache_dir()
        if os.path.isfile(f):
            return Word2Vec.load(f)
    texts = []
    for url in crawl_report_list():
        html = get(url)
        enc, time, title, text = ce.parse(url, html)
        sentences = text_util.get_sentences(text)
        for s in sentences:
            texts.append([w for w in jieba.cut(s)])
    b = Word2Vec(texts)
    if cache:
        b.save(f)
    return b

if __name__ == "__main__":
    model = build_model()
    ret = model.most_similar(u'税收', topn=50)
    for i in ret:
        print i[0],i[1]
     
