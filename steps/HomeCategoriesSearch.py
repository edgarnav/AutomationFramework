from behave import given, when, then
from pages.HomePage import HomePage
from pages.ProductListPage import ProductListPage


class SearchBarSteps:

    @given("Go to liverpool.com")
    def go_to_website(context):
        context.home_page_object = HomePage(context.web_driver)
        context.product_list_page = ProductListPage(context.web_driver)

    @when("Validate Home Page is showing")
    def validate_home_page(context):
        context.home_page_object.validate_home_page()

    @then("Input a {search_term} and press return or search button")
    def input_sear_term_and_press_return(context, search_term):
        context.home_page_object.input_search_term(search_term)
        context.home_page_object.perform_search()

    @then("Validate that the results shown make sense with {search_term}")
    def validate_results(context, search_term):
        context.product_list_page.validate_product_list_page()
        context.product_list_page.validate_results(search_term)

    @when("Filter the results by size: {size_filter}, brand: {brand_filter}")
    def select_filters(context, size_filter, brand_filter):
        context.product_list_page.press_brand_filter(brand_filter)
        context.product_list_page.press_size_filter(size_filter)

    @then("Validate the results count")
    def validate_number_results(context):
        context.product_list_page.get_results()

    @then("Open category menu")
    def open_category_menu(context):
        context.home_page_object.press_category_button()

    @when("Select the {category} option and press {subcategory} subcategory")
    def select_category_subcategory(context, category, subcategory):
        context.home_page_object.hover_category(category)
        context.home_page_object.press_subcategory(subcategory)

    @then("Filter results by brand: {brand}")
    def select_brand_filter(context, brand):
        context.product_list_page.press_brand_filter(brand)
