# tests/test_auth_register.py
import pytest
import allure
import time
from pages.auth_page import AuthPage
from utils.generators import generate_unique_user
@pytest.mark.ui
@pytest.mark.auth
@pytest.mark.regression
@allure.feature("Auth")
@allure.story("Register")

def test_register_valid(page):
    auth = AuthPage(page)

    username, email = generate_unique_user(prefix="ThanhQA")

    with allure.step("Đi tới trang đăng ký"):
        auth.goto_register()

    with allure.step("Điền form và submit"):
        auth.register(username=username, email=email, password="123456", confirm_pass="123456")

    with allure.step("Xác thực đăng ký thành công (đúng nội dung thông báo)"):
        auth.verify_register_success(success_text="Đăng ký thành công!")



