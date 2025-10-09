import pytest
import allure
from pages.auth_page import AuthPage


@allure.feature("Auth")
class TestLogin:
    @pytest.mark.ui
    @pytest.mark.auth
    @pytest.mark.smoke
    @allure.story("Login")
    def test_login_valid(self, page, test_users):
        AuthPage(page).goto_login().login(
            email=test_users["editor"]["email"],
            password=test_users["editor"]["password"]
        ).assert_logged_in("test1111")

    @pytest.mark.ui
    @pytest.mark.auth
    @pytest.mark.regression
    @allure.story("Login không thành công")
    def test_login_invalid(self, page, test_users):
        lg = AuthPage(page)
        lg.goto_login().login(
            email=test_users["editor"]["email"],
            password="wrong-password"
        )
        lg.assert_login_fail("Thông tin tài khoản hoặc mật khẩu không đúng.")
