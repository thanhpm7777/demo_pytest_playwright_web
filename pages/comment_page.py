import allure
from .base_page import BasePage

class CommentPage(BasePage):
    @allure.step("Add comment: {text}")
    def add_comment(self, text: str):
        self.page.locator("textarea[name='comment']").fill(text)
        self.page.get_by_role("button", name="Comment").click()
        return self

    @allure.step("Delete first comment")
    def delete_first_comment(self):
        self.page.locator(".comment .btn-delete").first.click()
        self.page.get_by_role("button", name="Confirm").click()
        return self
