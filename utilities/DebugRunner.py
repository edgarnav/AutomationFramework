from driver_interactions.ElementInteractions import ElementInteractions
from driver_interactions.InitWebDriver import InitWebDriver
import utilities.Logger as Logger
from pages.HomePage import HomePage
from pages.ProductListPage import ProductListPage
import configurations.ConfigFile as Configs


log = Logger.func_logger()


class DebugScenarios():


    def debug_category(self):
        self.web_driver = InitWebDriver().init_web_driver()
        self.interactions_object = ElementInteractions(self.web_driver)
        self.interactions_object.launch_web_page(Configs.website)
        self.home_page_object = HomePage(self.web_driver)
        self.product_list_page = ProductListPage(self.web_driver)

        self.home_page_object.validate_home_page()
        self.home_page_object.press_category_button()
        self.home_page_object.hover_category("Belleza")
        self.home_page_object.press_subcategory("Perfumes Hombre")
        self.product_list_page.validate_product_list_page()
        self.product_list_page.validate_results("parfum")
        self.product_list_page.press_brand_filter("DIOR")
    
    def debug_filter(self):
        self.web_driver = InitWebDriver().init_web_driver()
        self.interactions_object = ElementInteractions(self.web_driver)
        self.interactions_object.launch_web_page(Configs.website)
        self.home_page_object = HomePage(self.web_driver)
        self.product_list_page = ProductListPage(self.web_driver)

        self.home_page_object.validate_home_page()
        self.home_page_object.input_search_term("smart tv")
        self.home_page_object.perform_search()
        self.product_list_page.validate_product_list_page()
        self.product_list_page.validate_results("smart tv")
        self.product_list_page.press_brand_filter("SONY")
        self.product_list_page.press_size_filter("55 pulgadas")
        self.product_list_page.press_price_filter("10000-700000")
        self.product_list_page.get_results()
        

if __name__ == '__main__':
    DebugScenarios().debug_filter()
