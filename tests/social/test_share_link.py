import pytest
import allure
from playwright.sync_api import expect
from pages.post_page import PostPage

@pytest.mark.ui
@pytest.mark.social
@allure.feature("Social")
@allure.story("Like & Share")
def test_like_toggle_and_share_link(context_with_auth):
    page = context_with_auth.new_page()
    post = PostPage(page).open_latest_post()

    # like toggle
    before = int(page.locator("[data-testid='like-count']").inner_text())
    post.like_toggle()
    after = int(page.locator("[data-testid='like-count']").inner_text())
    assert after in (before + 1, before - 1)  # tuỳ trạng thái ban đầu

    # share link
    link = post.share_get_link()
    assert isinstance(link, str) and link.startswith("http")
