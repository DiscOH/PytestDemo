

class TestBrowserExamples(object):
    # open browser
    # navigate to google
    def test_google(self, chrome_session):
        chrome_session.navigate('https://www.google.com/')
        assert chrome_session.element_should_exist('//*[@name="q"]')
        assert chrome_session.get_title() == 'Google'

    # navigate to bing
    def test_bing(self, chrome_session):
        chrome_session.navigate('https://www.bing.com/')
        assert chrome_session.get_title() == 'Bing'
        chrome_session.input_text('//*[@id="sb_form_q"]', 'woof doggo')
        chrome_session.click_element('//*[@id="sb_form_go"]')
        assert chrome_session.get_title() == 'woof doggo - Bing'

    # close browser
