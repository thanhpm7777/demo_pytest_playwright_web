import pytest
import allure
from pages.auth_page import AuthPage

@pytest.mark.ui
@pytest.mark.auth
@pytest.mark.smoke
@allure.feature("Auth")
@allure.story("Login")
def test_login_valid(page, test_users):
    AuthPage(page).goto_login().login(
        email=test_users["editor"]["email"],
        password=test_users["editor"]["password"]
    ).assert_logged_in("test1111")
