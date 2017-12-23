from searchers.base_business_searcher import BaseBusinessSearcher
import time


class BezeqBuisnessSearcher(BaseBusinessSearcher):
    searcher_url_key = 'BEZEQ_URL'

    def __init__(self, search_term, locations, dal):
        super(BezeqBuisnessSearcher, self).__init__(search_term, locations, dal)

    def extract_elements(self):
        data_to_save = []
        for location in self.locations[:5]:
            self.driver.get(self.url.format(city=location['name'], business=self.search_term))
            time.sleep(1)
            li_elements = self.driver.find_elements_by_class_name('extra-promoted-b-card')
            for li in li_elements:
                try:
                    business_name_element = li.find_element_by_tag_name('h3')
                    phone_element = li.find_element_by_class_name('extra-card-phone')
                    address_element = li.find_element_by_class_name('extra-card-location')
                    entity = self.create_entity_as_dict(business_name_element=business_name_element.text,
                                                        phone_element=phone_element.text,
                                                        address_element=address_element.text)
                    data_to_save.append(entity)
                except Exception as e:
                    print str(e)
        return data_to_save
