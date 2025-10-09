import time

import allure
from .base_page import BasePage

class CommentPage(BasePage):
    LINK_POST = "a[href='/tap-chi/truyen-ngan-cai-nhin-khac-khoai-tu-khac-khoai-than-phan-den-ngoi-sang-nghia-tinh-song-nuoc-mien-tay/']"
    id_message="message"
    btn_message="Gửi bình luận"
    @allure.step("go to post")
    def goto_post(self):

        post_locator = self.get_by_css(self.LINK_POST)
        post_locator.wait_for(state="visible")
        post_locator.scroll_into_view_if_needed()
        post_locator.click()

        return self


    @allure.step("Add comment: {comment_text}")
    def add_comment(self, comment_text: str):
        comment_box = self.get_by_id(self.id_message)
        comment_box.wait_for(state="visible")
        comment_box.scroll_into_view_if_needed()
        comment_box.fill(comment_text)
        self.click_button(self.btn_message)
        return self


    # @allure.step("Delete first comment")
    # def delete_first_comment(self):
    #     self.page.locator(".comment .btn-delete").first.click()
    #     self.page.get_by_role("button", name="Confirm").click()
    #     return self
