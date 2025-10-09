import pytest
import allure
from pages.post_page import PostPage
from pages.auth_page import AuthPage

@allure.feature("Post")
class TestPost:
    @pytest.mark.ui
    @pytest.mark.post
    @pytest.mark.smoke
    @allure.story("Create")
    def test_create_post_valid(self, page, test_users, test_posts):
        AuthPage(page).goto_login().login(
            email=test_users["editor"]["email"],
            password=test_users["editor"]["password"],
        )
        post = PostPage(page)
        post.goto_new_post()
        post.create_post(
            title=test_posts["valid"]["title"],
            the_loai=test_posts["valid"]["the_loai"],
            content=test_posts["valid"]["content"],
            pdf_driver=test_posts["valid"]["pdf_driver"],
            path_file=test_posts["valid"]["path_file"],
            tag=test_posts["valid"]["tag"],
            is_active=False,
            is_active_tap_chi=True,
        )
        with allure.step("Verify post vừa tạo đã thành công"):
            # đặt tên hàm assert cho rõ nghĩa (ví dụ verify_create_success)
            post.verify_create_success("Đã thêm bài viết thành công")

    # @pytest.mark.ui
    # @pytest.mark.post
    # @pytest.mark.regression
    # @allure.story("Update")
    # def test_update_post_title(self, test_posts, test_users, page):
    #     AuthPage(page).goto_login().login(
    #         test_users["editor"]["email"],
    #         test_users["editor"]["password"])
    #
    #     edit_post = PostPage(page)
    #     edit_post.open_latest_post()
    #     edit_post.update_post(title=test_posts["update"]["new_title"])


    # @pytest.mark.ui
    # @pytest.mark.post
    # @allure.story("Delete")
    # def test_delete_post(self,page, test_users):
    #     AuthPage(page).goto_login().login(
    #         test_users["editor"]["email"],
    #         test_users["editor"]["password"])
    #
    #     delete_post = PostPage(page)
    #     delete_post.open_latest_post()
    #     delete_post.delete_first_post()
    #     #PostPage(page).toast_should_appear("Deleted successfully")
