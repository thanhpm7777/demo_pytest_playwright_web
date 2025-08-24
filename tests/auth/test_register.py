import pytest
import allure
from pages.auth_page import AuthPage

@pytest.mark.ui
@pytest.mark.auth
@pytest.mark.regression
@allure.feature("Auth")
@allure.story("Register")
def test_register_valid(page):
    auth = AuthPage(page).goto_register()
    auth.register(name="Thanh QA", email="newuser@example.com", password="P@ssw0rd!")
    # tuỳ UI: toast hoặc redirect
    auth.toast_should_appear("Registration successful")
