import allure
from playwright.sync_api import expect
from .base_page import BasePage

class PostPage(BasePage):
    # Gợi ý selector bền: data-testid ở app
    LINK_POSTS = ("role=link[name='Posts']")
    LINK_NEW_POST = ("role=link[name='New Post']")
    INPUT_TITLE = ("placeholder=Title")
    TEXTAREA_CONTENT = ("css=textarea[name='content']")  # chỉnh theo UI
    BTN_PUBLISH = ("role=button[name='Publish']")
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
        self.page.get_by_role("link", name="New Post", exact=True).click()
        expect(self.page).to_have_url("**/posts/new")
        return self

    @allure.step("Create post: {title}")
    def create_post(self, title: str, content: str):
        self.page.get_by_placeholder("Title").fill(title)
        self.page.locator("textarea[name='content']").fill(content)
        self.page.get_by_role("button", name="Publish").click()
        return self

    @allure.step("Open latest post")
    def open_latest_post(self):
        self.page.get_by_role("link", name="Posts", exact=True).click()
        self.page.locator("article.post-card").first.get_by_role("link").click()
        expect(self.page).to_have_url("**/posts/*")
        return self

    @allure.step("Update post")
    def update_post(self, new_title: str | None = None, new_content: str | None = None):
        self.page.get_by_role("button", name="Edit").click()
        if new_title:
            self.page.get_by_placeholder("Title").fill(new_title)
        if new_content:
            self.page.locator("textarea[name='content']").fill(new_content)
        self.page.get_by_role("button", name="Save").click()
        return self

    @allure.step("Delete post")
    def delete_post(self):
        self.page.get_by_role("button", name="Delete").click()
        self.page.get_by_role("button", name="Confirm").click()
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
