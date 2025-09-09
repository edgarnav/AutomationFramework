from driver_interactions.ElementInteractions import ElementInteractions


class HomePage(ElementInteractions):

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    id_search_bar = ":R37d9d9utsq:-input"
    xpath_category_btn = "//*[@data-testid='blt26617d4f2e17657d-header-button-category']"
    xpath_categories = "//*[@data-testid='blt26617d4f2e17657d-header-menu-categories-menu-category-item--label']"
    link_text_perfume_man = "Perfumes Hombre"

    def validate_home_page(self):
        if not self.is_element_displayed(self.id_search_bar, "id"):
            assert False

    def input_search_term(self, search_term):
        self.send_text(search_term, self.id_search_bar, "id")

    def perform_search(self):
        self.perform_enter()

    def press_category_button(self):
        self.press_element(self.xpath_category_btn, "xpath")

    def hover_category(self, category):
        categories = self.get_all_elements(self.xpath_categories, "xpath")
        for index, category_element in enumerate(categories):
            if category_element.text == category:
                self.hover_element(category_element)
                break
            elif index + 1 == len(categories):
                self.take_screenshot("Category not found")
                self.log.info("Category not found")
                assert False

    def press_subcategory(self, subcategory):
        self.press_element(self.link_text_perfume_man, "link")
