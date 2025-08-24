import allure
from playwright.sync_api import expect
from .base_page import BasePage

class AuthPage(BasePage):
    # NOTE: chỉnh locator theo UI thực tế của bạn

    SIGN_IN_LINK = "Đăng nhập"  # text của link
    BTN_SIGN_IN = "ĐĂNG NHẬP"

    PH_EMAIL = "Tên đăng nhập hoặc email"
    PH_PASSWORD = "Mật khẩu"

    lbl_username = "username"
    lbl_messages = "div[role='alert']"

    @allure.step("Goto Login")
    def goto_login(self):
        self.open()
        self.click_nav(self.SIGN_IN_LINK)
        return self

    @allure.step("Goto Register")
    def goto_register(self):
        self.open()
        self.page.get_by_role("link", name="Register", exact=True).click()
        expect(self.page).to_have_url("**/register")
        return self

    def login(self, email: str, password: str):
        with allure.step("Nhập thông tin đăng nhập"):
            self.fill_by_placeholder(self.PH_EMAIL, email)
            self.fill_by_placeholder(self.PH_PASSWORD, password)
        with allure.step("Đăng nhập"):
            self.click_button(self.BTN_SIGN_IN)
        return self

    # @allure.step("Expect dashboard after login")
    # def expect_dashboard(self):
    #     expect(self.page).to_have_url("https://hocvancokimngan.com/")
    #     return self

    def assert_logged_in(self, username):
        with allure.step("Xác minh đã đăng nhập thành công"):
            expect(self.get_by_class(self.lbl_username)).to_have_text(username)

    def assert_login_fail(self, username):
        with allure.step("đăng nhập không thành công"):
            expect(self.get_by_css(self.lbl_messages)).to_contain_text(username)

    @allure.step("Register user {email}")
    def register(self, name: str, email: str, password: str):
        self.page.get_by_placeholder("Name").fill(name)
        self.page.get_by_placeholder("Email").fill(email)
        self.page.get_by_placeholder("Password").fill(password)
        self.page.get_by_role("button", name="Sign up").click()
        return self
