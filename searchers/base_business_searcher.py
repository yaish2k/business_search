from models.business_model import Business
import os
from selenium import webdriver
import json
import hashlib


class BaseBusinessSearcher(object):
    def __init__(self, search_term, locations, dal):
        self.search_term = search_term
        self.locations = locations
        self.dal = dal
        self.driver = None
        self.url = unicode(os.environ[self.searcher_url_key])

    def create_driver(self):
        self.driver = webdriver.Chrome(os.environ['DRIVER_LINK'])

    def create_entity_as_dict(self, business_name_element, phone_element, address_element):
        entity = {
            'name': business_name_element,
            'phone': phone_element,
            'address': address_element
        }
        entity.update({'id': hashlib.sha256(json.dumps(entity)).hexdigest()})
        return entity

    def extract_elements(self):
        raise NotImplementedError

    def save_entities_on_db(self, entities):
        existing_entities_ids = []
        for id in self.dal.query(Business.id):
            existing_entities_ids.append(id)
        entities = [Business(**e) for e in entities if e['id'] not in existing_entities_ids]
        self.dal.add_all(entities)

    def search(self):
        self.create_driver()
        data_to_save = self.extract_elements()
        self.save_entities_on_db(data_to_save)
