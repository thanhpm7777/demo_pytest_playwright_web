# import pytest
# import allure
# from pages.post_page import PostPage
# from pages.auth_page import AuthPage
# @pytest.mark.ui
# @pytest.mark.post
# @pytest.mark.regression
# @allure.feature("Post")
# @allure.story("Delete")
# def test_delete_post(page, test_users):
#     AuthPage(page).goto_login().login(
#         test_users["editor"]["email"],
#         test_users["editor"]["password"])
#
#     post = PostPage(page)
#     post.open_latest_post()
#     post.delete_post()
#     #PostPage(page).toast_should_appear("Deleted successfully")
