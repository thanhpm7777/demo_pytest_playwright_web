import pytest
import allure
from pages.post_page import PostPage

@pytest.mark.ui
@pytest.mark.post
@pytest.mark.regression
@allure.feature("Post")
@allure.story("Delete")
def test_delete_post(context_with_auth):
    page = context_with_auth.new_page()
    PostPage(page).open_latest_post().delete_post()
    PostPage(page).toast_should_appear("Deleted successfully")
