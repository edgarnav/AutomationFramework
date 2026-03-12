from driver_interactions.ElementInteractions import ElementInteractions


class LoginPage(ElementInteractions):

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    def validate_login_page(self):
        if not self.is_element_displayed("login-button", "id"):
            assert False
        return self.get_html()
