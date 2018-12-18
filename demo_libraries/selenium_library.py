from selenium.common.exceptions import NoSuchElementException, ElementNotVisibleException
from selenium.webdriver.remote.webelement import WebElement
from time import time


class Session(object):
    def __init__(self, driver, request, timeout=15, url=None):
        self.driver = driver
        self.default_timeout = timeout
        self.driver.implicitly_wait(self.default_timeout)
        if url:
            self.navigate(url)
        self.request = request

    def quit(self):
        self.driver.quit()

    def navigate(self, url):
        self.driver.get(url)

    def set_size(self, width, height):
        self.driver.set_window_size(width, height)

    def get_size(self):
        return self.driver.get_window_size()

    def get_title(self, timeout=None):
        if timeout:
            timeout = time() + timeout
        else:
            timeout = time() + self.default_timeout
        while True:
            if self.driver.title is not '' or time() > timeout:
                return self.driver.title

    def find_element(self, locator, element_property=None):

        if element_property:
            element_property = element_property.lower()

        try:
            if not element_property or property is 'xpath':
                return self.driver.find_element_by_xpath(locator)
            elif element_property is 'name':
                return self.driver.find_element_by_name(locator)
            elif element_property is 'id':
                return self.driver.find_element_by_id(locator)
            elif element_property is 'class':
                return self.driver.find_element_by_class_name(locator)
            elif element_property is 'css':
                return self.driver.find_element_by_css(locator)
            elif element_property is 'link':
                return self.driver.find_element_by_link_text(locator)
        except NoSuchElementException as e:
            assert False, str(e)

    def find_elements(self, locator, element_property=None):

        if element_property:
            element_property = element_property.lower()

        if not element_property or property is 'xpath':
            return self.driver.find_elements_by_xpath(locator)
        elif element_property is 'name':
            return self.driver.find_elements_by_name(locator)
        elif element_property is 'id':
            return self.driver.find_elements_by_id(locator)
        elif element_property is 'class':
            return self.driver.find_elements_by_class_name(locator)
        elif element_property is 'css':
            return self.driver.find_elements_by_css(locator)
        elif element_property is 'link':
            return self.driver.find_elements_by_link_text(locator)

    def does_element_exist(self, locator, element_property=None):

        count = len(self.find_elements(locator, element_property))
        if count > 0:
            return True
        return False

    def element_should_exist(self, locator, timeout=None):
        if timeout:
            self.driver.implicitly_wait(timeout)

        self.find_element(locator)

        if timeout:
            self.driver.implicitly_wait(self.default_timeout)

    def element_should_not_exist(self, locator, timeout=None):
        self.driver.implicitly_wait(0)

        if not timeout:
            timeout = time() + self.default_timeout
        else:
            timeout = time() + timeout
        while True:
            if len(self.find_elements(locator)) == 0:
                results = True
                break
            if time() > timeout:
                results = False
                break

        self.driver.implicitly_wait(self.default_timeout)

        assert results, 'locator should not have been found'

    def extract_element(self, locator):
        if isinstance(locator, WebElement):
            return locator
        return self.find_element(locator)

    def is_element_visible(self, locator, timeout=None):
        if not timeout:
            timeout = self.default_timeout
        element = self.extract_element(locator)
        timeout = time() + timeout
        while True:
            if element.is_displayed():
                width = self.driver.execute_script('return arguments[0].offsetWidth', element)
                height = self.driver.execute_script('return arguments[0].offsetHeight', element)
                rectangles = self.driver.execute_script('return arguments[0].getClientRects()', element)
                if width and height and rectangles:
                    return True
            if time() > timeout:
                return False

    def replace_element_text(self, locator, text):
        element = self.extract_element(locator)
        self.driver.execute_script('arguments[0].textContent =%s' % text, element)

    def replace_text_with_placeholder(self, asset):
        element = self.extract_element(asset)
        self.replace_element_text(element, 'loRem ipSum')

    def get_element_coordinates(self, asset):
        element = self.extract_element(asset)

        x_min = element.location['x']
        x_max = element.location['x'] + element.size['height']

        y_min = element.location['y']
        y_max = element.location['y'] + element.size['width']

        return x_min, x_max, y_min, y_max

    def get_viewport_coordinates(self):
        height = self.driver.execute_script('return window.innerHeight')
        width = self.driver.execute_script('return window.innerWidth')

        x_min = self.driver.execute_script('return window.pageXOffset')
        x_max = x_min + width

        y_min = self.driver.execute_script('return window.pageYOffset')
        y_max = y_min + height

        return x_min, x_max, y_min, y_max

    def is_overlap_between_elements(self, asset1, asset2):
        x_min_1, x_max_1, y_min_1, y_max_1 = self.get_element_coordinates(asset1)
        x_min_2, x_max_2, y_min_2, y_max_2 = self.get_element_coordinates(asset2)

        if (x_min_1 > x_max_2 or x_max_1 > x_min_2) or (y_min_1 > y_max_2 or y_max_1 > y_min_2):
            return False
        return True

    def scroll_to_element(self, asset):
        element = self.extract_element(asset)
        self.driver.execute_script('arguments[0].scrollIntoView(true);', element)

    def click_element(self, asset):
        element = self.extract_element(asset)
        try:
            self.scroll_to_element(element)
            element.click()
        except (ElementNotVisibleException, NoSuchElementException) as e:
            assert False, str(e)

    def input_text(self, locator, text):
        element = self.extract_element(locator)
        self.scroll_to_element(element)
        element.send_keys(text)

    def refresh(self):
        self.driver.refresh()

    def highlight_element(self, asset):
        element = self.extract_element(asset)
        self.driver.execute_script('arguments[0].style.outline = "#f00 solid 2px";', element)

    def url_should_contain(self, url, timeout=None):
        current_url = None
        if not timeout:
            timeout = self.default_timeout
        timeout = time() + timeout
        while timeout > time():
            current_url = self.driver.current_url
            if url in current_url:
                return
        assert False, 'current url is %s, should have contained %s but did not' % (current_url, url)

    def validate_asset(self, asset):

        self.element_should_exist(asset)
        print('%s exists' % asset.name)

        assert self.is_element_visible(asset), '%s was not visible' % asset.name
        print('%s is visible' % asset.name)
