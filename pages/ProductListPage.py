import time
from driver_interactions.ElementInteractions import ElementInteractions


class ProductListPage(ElementInteractions):

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    class_product_card_name = "a-card-brand"
    class_product_card_description = "a-card-description"
    id_search_brand_text = "searchBrand"
    id_see_more_size_filter = "Tamao"
    id_filter_brand = "brand-"
    id_filter_size = "variants.normalizedSize-"
    id_filter_price = "variants.prices.sortPrice-"
    class_filter_applied = "newChipContainer"
    class_results_lbl = "a-plp-results-title"

    def validate_product_list_page(self):
        self.is_element_displayed(self.class_product_card_name, "class")

    def press_brand_filter(self, brand):
        self.scroll_to_element(self.id_search_brand_text, "id")
        self.send_text(brand, self.id_search_brand_text, "id")
        self.scroll_to_element(self.id_filter_brand + brand, "id")
        self.press_element(self.id_filter_brand + brand, "id")
        self.validate_filter_applied(brand)

    def press_size_filter(self, size):
        self.scroll_to_element(self.id_filter_size + size, "id")
        self.press_element(self.id_filter_size + size, "id")
        self.validate_filter_applied("55 pulgadas")

    def press_price_filter(self, price):
        self.scroll_to_element(self.id_filter_price + price, "id")
        self.press_element(self.id_filter_price + price, "id")
        self.validate_filter_applied("Mas de $10000.0")

    def validate_results(self, search_term):
        products = self.get_all_elements(self.class_product_card_description, "class")
        for index, product in enumerate(products):
            if search_term in product.text.lower():
                break
            elif index + 1 == len(products):
                self.take_screenshot("Results do not match the search term")
                self.log.info("Results do not match the search term")
                assert False

    def validate_filter_applied(self, filter_name):
        filters = self.get_all_elements(self.class_filter_applied, "class")
        for index, filter in enumerate(filters):
            if filter_name.lower() in filter.text.lower() and index + 1 <= len(filters):
                self.log.info("Filter applied")
                time.sleep(1)
                break
            elif index + 1 > len(filters):
                self.take_screenshot("Filter not applied")
                self.log.info("Filter not applied")
                assert False

    def get_results(self):
        time.sleep(1)
        results = self.get_text(self.class_results_lbl, "class")
        self.take_screenshot("The number of products is: " + results)
