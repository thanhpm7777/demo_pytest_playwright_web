import pytest
import allure
from pages.post_page import PostPage

@pytest.mark.ui
@pytest.mark.post
@allure.feature("Post")
@allure.story("Create")
def test_create_post_valid(context_with_auth, test_posts):
    page = context_with_auth.new_page()
    post = PostPage(page)
    post.visit("/")
    post.goto_new_post().create_post(
        title=test_posts["valid"]["title"],
        content=test_posts["valid"]["content"]
    )
    post.toast_should_appear("Created successfully")
    post.open_latest_post()
    # Assert title hiển thị (chỉnh selector)
    # expect(page.locator("h1.post-title")).to_have_text(test_posts["valid"]["title"])
