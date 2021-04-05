# -*- coding: utf-8 -*-
# @Time : 2021/3/1 20:29
# @Author : luff543@gmail.com
# @Email : luff543@gmail.com
# @File : query_elasticsearch_qa.py
# @Software: PyCharm

from elasticsearch import Elasticsearch
import json

def query(query):
    es = Elasticsearch()

    index_name = 'bbc_news'
    type = 'fb_post'

    search_params = {
        "query": {
            "match": {"contents": query}
        },
        "size": 5
    }
    result = es.search(index=index_name, doc_type=type, body=search_params)
    result = result['hits']['hits'][0]

    result = json.dumps(result, indent=2)
    print(result)

query_input = input('What do you want to query?')
query('query_input')
