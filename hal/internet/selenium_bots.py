# -*- coding: utf-8 -*-

""" Some utils methods for a selenium web-driver """


class SeleniumForm:
    """Great and simple static methods to deal with selenium web-drivers"""

    def __init__(self, browser):
        self.browser = browser

    @staticmethod
    def fill_form_field(browser, field_name, field_value):
        """
        :param browser: web
        :param Browser: to use to submit form
        :param field_name: string
        :param Name: of field to fill
        :param field_value: string
        :param Value: with which to fill field
          Fill given field with given value.
        """
        browser.execute_script(
            "document.getElementsByName(\"" + str(
                field_name) + "\")[0].value = \"" + str(field_value) + "\"")

    @staticmethod
    def fill_login_form(browser, username, username_field, user_password,
                        user_password_field):
        """
        :param browser: web
        :param Browser: to use to submit form
        :param username: string
        :param Username: of user to login
        :param username_field: string
        :param Name: of field to fill with username
        :param user_password: string
        :param Password: of user to login
        :param user_password_field: string
        :param Name: of field to fill with user password
          Form filled with given information
        """
        SeleniumForm.fill_form_field(browser, username_field,
                                     username)  # set username
        SeleniumForm.fill_form_field(browser, user_password_field,
                                     user_password)  # set password

    @staticmethod
    def submit_form(browser, button_name):
        """
        :param browser: web
        :param Browser: to use to submit form
        :param button_name: string
        :param Name: of button to press to submit form
          Submit form.
        """
        browser.execute_script(
            "document.getElementsByName(\"" + button_name + "\")[0].click()"
        )  # click button
