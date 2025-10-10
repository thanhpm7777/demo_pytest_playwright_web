import time

import allure
from .base_page import BasePage

class SocialPage(BasePage):
    LINK_POST = "a[href='/tap-chi/truyen-ngan-cai-nhin-khac-khoai-tu-khac-khoai-than-phan-den-ngoi-sang-nghia-tinh-song-nuoc-mien-tay/']"
    id_message="message"
    btn_like = "like-btn"
    btn_share = "share-btn"
    @allure.step("go to post")
    def goto_post(self):

        post_locator = self.get_by_css(self.LINK_POST)
        post_locator.wait_for(state="visible")
        post_locator.scroll_into_view_if_needed()
        post_locator.click()

        return self


    @allure.step("like post")
    def like_post(self):
        like = self.get_by_id(self.btn_like)
        like.wait_for(state="visible")
        like.scroll_into_view_if_needed()
        like.click()
        allure.attach(self.page.screenshot(), "after_like", allure.attachment_type.PNG)
        return self

    @allure.step("like post")
    def share_post(self):
        share = self.get_by_id(self.btn_share)
        share.wait_for(state="visible")
        share.scroll_into_view_if_needed()
        share.click()
        return self
