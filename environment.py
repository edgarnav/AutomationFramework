from driver_interactions.ElementInteractions import ElementInteractions
from driver_interactions.InitWebDriver import InitWebDriver
import configurations.ConfigFile as Configs
import utilities.Logger as Logger

log = Logger.func_logger()


def before_all(context):
    log.info("Test started")


def before_scenario(context, scenario):
    context.web_driver = InitWebDriver().init_web_driver()
    context.interactions_object = ElementInteractions(context.web_driver)
    context.interactions_object.launch_web_page(Configs.website)


def after_scenario(context, scenario):
    context.web_driver.quit()


def after_all(context):
    log.info("Test ended")


"""def before_feature(context):

def before_step(context):"""
