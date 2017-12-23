# -*- encoding: utf-8 -*-
import os
import requests
import json
from models.dal import Dal
from searchers.bezeq_business_searcher import BezeqBuisnessSearcher
from searchers.zap_buisness_searcher import ZapBuisnessSearcher


def main():
    list_of_locations = json.loads(requests.get(url=os.environ['LOCATIONS_URL']).content)
    search_term = u'מאפיות'
    dal = Dal()
    dal.connect()
    searchers = [
        BezeqBuisnessSearcher(search_term=search_term, locations=list_of_locations, dal=dal),
        ZapBuisnessSearcher(search_term=search_term, locations=list_of_locations, dal=dal)
    ]

    for searcher in searchers:
        searcher.search()


if __name__ == '__main__':
    main()
