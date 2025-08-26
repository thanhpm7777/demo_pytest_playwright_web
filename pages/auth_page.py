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

    RG_username = "Tên đăng nhập viết liền không dấu"
    RG_email = "Email của bạn"
    RG_password = "password"
    RG_confirm_password = "Xác nhận mật khẩu"
    BTN_register = "ĐĂNG KÝ"
    link_register ="Đăng ký tài khoản"

    @allure.step("Goto Login")
    def goto_login(self):
        self.open()
        self.click_nav(self.SIGN_IN_LINK)
        return self

    @allure.step("Goto Register")
    def goto_register(self):
        self.open()
        self.click_nav(self.SIGN_IN_LINK)
        self.click_link_or_button(name=self.link_register)
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

    @allure.step("Register user")
    def register(self, username: str, email: str, password: str, confirm_pass: str):
        self.fill_by_placeholder(self.RG_username, username)
        self.fill_by_placeholder(self.RG_email, email)
        self.fill_by_name(self.RG_password, password)
        self.fill_by_placeholder(self.RG_confirm_password, confirm_pass)
        self.click_button(self.BTN_register)
        return self
