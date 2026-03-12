from driver_interactions.ElementInteractions import ElementInteractions
from driver_interactions.InitWebDriver import InitWebDriver
from driver_interactions.HTMLCleaner import HTMLCleaner
from driver_interactions.AIAgentLogic import GetResponseIA
import utilities.Logger as Logger
from pages.HomePage import HomePage
from pages.ProductListPage import ProductListPage
from pages.LoginPage import LoginPage
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

    def first_test_ia(self):
        self.web_driver = InitWebDriver().init_web_driver()
        self.interactions_object = ElementInteractions(self.web_driver)
        self.interactions_object.launch_web_page(Configs.website)
        login_page = LoginPage(self.web_driver)
        self.actions_ai_object = GetResponseIA(self.web_driver)
        html_cleaner = HTMLCleaner

        page = login_page.validate_login_page()
        page_cleaned = html_cleaner.limpiar_html_para_ia(page)
        self.actions_ai_object.get_action_ai(page_cleaned, "Escribe 'standard_user' en el campo de nombre de usuario.")
        self.actions_ai_object.get_action_ai(page_cleaned, "Escribe 'secret_sauce' en el campo de contraseña.")
        self.actions_ai_object.get_action_ai(page_cleaned, "Haz clic en el botón para iniciar sesión.")
        self.actions_ai_object.get_action_ai(page_cleaned, "Haz clic en el primer producto que dice 'Sauce Labs Backpack'")
        self.actions_ai_object.get_action_ai(page_cleaned, "Haz clic en el botón Add to cart para agregar el producto.")
        self.actions_ai_object.get_action_ai(page_cleaned, "Verifica que el texto del botón haya cambiado a Remove.")


if __name__ == '__main__':
    DebugScenarios().first_test_ia()
