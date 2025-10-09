import time

import allure
from playwright.sync_api import expect
from .base_page import BasePage

class PostPage(BasePage):
    # Gợi ý selector bền: data-testid ở app
    LINK_NEW_ARTICLE = "user-avatar"
    lbl_setting = "Cài đặt thông tin"
    lbl_dangbai = "Đăng bài"
    lbl_myblog="Blog của tôi"

    btn_delete ="Xóa"
    PH_TITLE = "title"
    PH_category = "#category_id"
    PH_BODY = "presentation"
    PH_TAGS = "Enter tags"

    LINK_POSTS = ("lbl_dangbai")
    click_avata = "username"

    lbl_notification = ".alert.alert-success"

    INPUT_TITLE = "Tiêu đề bài viết"

    select_the_loai = "#category_id"
    CKEDITOR_IFRAME = "iframe.cke_wysiwyg_frame"
    INPUT_BANNER = "#banner_id"  # input file
    input_pdf_driver = "ID PDF Driver"
    TEXTAREA_TAGS = "#tags_id"
    CHECKBOX_IS_ACTIVE = "#id_is_active"
    checkbox_tap_chi_van_hoc="#id_tap_chi_van_hoc"
    BTN_PUBLISH = "Đăng bài"
    BTN_UPDATE = "Cập nhật"
    TEXTAREA_CONTENT = ("css=textarea[name='content']")  # chỉnh theo UI

    BTN_SAVE = ("role=button[name='Save']")
    BTN_EDIT = ("role=button[name='Edit']")
    BTN_DELETE = ("role=button[name='Delete']")
    BTN_CONFIRM = ("role=button[name='Confirm']")
    BTN_LIKE = ("role=button[name='Like']")
    LIKE_COUNT = ("css=[data-testid='like-count']")
    BTN_SHARE = ("role=button[name='Share']")
    INPUT_SHARE_LINK = ("css=input.share-link")         # chỉnh theo UI
    CARD_POST = ("css=article.post-card")

    @allure.step("Open New Post form")
    def goto_new_post(self):
        self.get_by_class(self.LINK_NEW_ARTICLE).click()
        self.click_nav(self.lbl_setting)
        self.click_nav(self.lbl_dangbai, expect_nav=True)
        return self

    @allure.step("delete post")
    def goto_delete_post(self):
        self.get_by_class(self.LINK_NEW_ARTICLE).click()
        self.click_nav(self.lbl_setting)
        return self

    @allure.step("Create post: {title}")
    def create_post(self, title: str, the_loai: str, content: str, pdf_driver, path_file, tag, is_active: bool=True, is_active_tap_chi: bool= False):
        self.fill_by_label(self.INPUT_TITLE, title)
        self.select_by_label(self.select_the_loai, the_loai)
        self.fill_ckeditor_iframe(self.CKEDITOR_IFRAME, content)
        self.upload_file(self.INPUT_BANNER, path_file)
        self.fill_by_label(self.input_pdf_driver, pdf_driver)
        self.fill_textarea(self.TEXTAREA_TAGS, tag)
        self.set_checkbox(self.CHECKBOX_IS_ACTIVE, is_active)
        self.set_checkbox(self.checkbox_tap_chi_van_hoc, is_active_tap_chi)
        self.click_button(self.BTN_PUBLISH)
        return self

    @allure.step("Open latest post")
    def open_latest_post(self):
        self.get_by_class(self.LINK_NEW_ARTICLE).click()
        self.click_nav(self.lbl_setting)
        self.click_nav(self.lbl_myblog)

        return self

    @allure.step("Update post")
    def update_post(self, title):
        self.click_link_or_button("Sửa")
        self.fill_by_label(self.INPUT_TITLE, title)
        self.click_link_or_button(self.BTN_UPDATE)
        return self

    @allure.step("Delete post")
    def delete_post(self):
        loc = self.page.get_by_role("link", name="Xóa").first
        self._click(loc, expect_nav=True)  # expect_nav=True nếu click dẫn tới điều hướng
        return self

    @allure.step("Toggle like")
    def like_toggle(self):
        self.page.get_by_role("button", name="Like").click()
        return self

    @allure.step("Read share link")
    def share_get_link(self) -> str:
        self.page.get_by_role("button", name="Share").click()
        # C1: có input hiển thị link
        if self.page.locator("input.share-link").count() > 0:
            return self.page.locator("input.share-link").input_value()
        # C2: app copy vào clipboard -> lấy từ navigator (nếu app hỗ trợ)
        return self.page.evaluate("navigator.clipboard.readText && navigator.clipboard.readText()") or ""

    def verify_create_success(self, success_text: str):

        self.expect_text(self.lbl_notification, success_text)
        return self