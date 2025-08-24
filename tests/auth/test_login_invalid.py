import pytest
import allure
from pages.auth_page import AuthPage


@pytest.mark.ui
@pytest.mark.auth
@pytest.mark.regression
@allure.feature("Auth")
@allure.story("Login")

@allure.story("Login không thành công")
def test_login_invalid(page, test_users):

    lg = AuthPage(page)
    lg.goto_login().login(test_users["editor"]["email"], "wrong-password")
    lg.assert_login_fail("Thông tin tài khoản hoặc mật khẩu không đúng.")