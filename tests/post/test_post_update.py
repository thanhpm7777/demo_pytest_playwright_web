# import pytest
# import allure
# from pages.post_page import PostPage
#
# @pytest.mark.ui
# @pytest.mark.post
# @pytest.mark.regression
# @allure.feature("Post")
# @allure.story("Update")
# def test_update_post_title(context_with_auth, test_posts):
#     page = context_with_auth.new_page()
#     PostPage(page).open_latest_post().update_post(
#         new_title=test_posts["update"]["new_title"]
#     )
#     # Assert title đổi
#     # expect(page.locator("h1.post-title")).to_have_text(test_posts["update"]["new_title"])
