import pytest
import allure
from pages.auth_page import AuthPage
# DB helpers
from configs.db import run_query, execute

@pytest.mark.ui
@pytest.mark.auth
@pytest.mark.regression
@allure.feature("Auth")
@allure.story("Register")
def test_register_valid(page):
    auth = AuthPage(page).goto_register()
    username ="ThanhQA"
    email = "newuser@example.com"
    auth.register(username="ThanhQA", email=email, password="123456", confirm_pass="123456")
    with allure.step("Verify user vừa đăng ký đã tồn tại trong MySQL"):
        rows = run_query(
            "SELECT email FROM user_profile_user WHERE email = :email",
            {"email": email})
        assert rows, f"Không tìm thấy user email={email} trong DB"
        assert rows[0]["email"] == email

        # --- Cleanup để test chạy lặp không bị trùng dữ liệu ---
    # with allure.step("Cleanup: xóa user test trong MySQL"):
    #     execute("DELETE FROM user_profile_user WHERE email = :email", {"email": email})




