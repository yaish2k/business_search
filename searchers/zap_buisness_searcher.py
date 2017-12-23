from searchers.base_business_searcher import BaseBusinessSearcher
import time


class ZapBuisnessSearcher(BaseBusinessSearcher):
    searcher_url_key = 'ZAP_URL'

    def __init__(self, search_term, locations, dal):
        super(ZapBuisnessSearcher, self).__init__(search_term, locations, dal)

    def extract_elements(self):
        data_to_save = []
        for location in self.locations[:5]:
            self.driver.get(self.url.format(city=location['name'], business=self.search_term))
            time.sleep(1)
            div_elements = self.driver.find_elements_by_class_name('result-box')
            for div_element in div_elements:
                try:
                    name_content_element = div_element.find_element_by_class_name('result-content-container')
                    name_content_element = name_content_element.find_element_by_tag_name('h3')
                    name_content_element = name_content_element.find_element_by_tag_name('a')
                    business_name_element = name_content_element.find_element_by_tag_name('span')
                    address_and_phone_content_element = div_element.find_element_by_class_name('grid-location')
                    phone_element = address_and_phone_content_element.find_element_by_class_name('number')
                    address_element = address_and_phone_content_element.find_element_by_class_name(
                        'result-contact-address')
                    entity = self.create_entity_as_dict(business_name_element=business_name_element.text,
                                                        phone_element=phone_element.get_attribute('innerHTML'),
                                                        address_element=address_element.text)
                    data_to_save.append(entity)
                except Exception as e:
                    print str(e)
        return data_to_save
