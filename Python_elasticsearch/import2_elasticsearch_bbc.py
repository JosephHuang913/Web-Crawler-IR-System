# -*- coding: utf-8 -*-
# @Time : 2021/3/1 18:06
# @Author : luff543@gmail.com
# @Email : luff543@gmail.com
# @File : import2_elasticsearch_qa.py
# @Software: PyCharm

from elasticsearch import Elasticsearch, helpers
import json

bbc_news_mapping = {
    "properties": {
        "contents": {
            "type": "text",
            #"analyzer":"ik_smart"
            "analyzer":"standard"
        },
        "postimes": {
            "type": "text"
        },
        "likes": {
            "type": "integer"
        },
        "comments": {
            "type": "integer"
        },
        "shares": {
            "type": "integer"            
        }
    }
}

renames_key = {
    'contents': 'contents',
    'postimes': 'postimes',
    'likes': 'likes',
    'comments': 'comments',
    'shares': 'shares'
}

def read_data():
    with open('bbcnews.json', 'r') as f:
        for row in f:
            d = eval(row.strip())
            d = json.dumps(d)
            row = json.loads(d)

            for k, v in renames_key.items():
                for old_name in row:
                    if k == old_name:
                        row[v] = row.pop(old_name)
            yield row


def load2_elasticsearch():
    index_name = 'bbc_news'
    type = 'fb_post'
    es = Elasticsearch()

    if not es.indices.exists(index=index_name):
        es.indices.create(index=index_name)
    print('Index created!')

    if not es.indices.exists_type(index=index_name, doc_type=type):
        es.indices.put_mapping(
            index=index_name, doc_type=type, body=bbc_news_mapping, include_type_name=True)
    print('Mappings created!')

    success, _ = helpers.bulk(
        client=es, actions=read_data(), index=index_name, doc_type=type, ignore=400)
    print('success: ', success)

load2_elasticsearch()
