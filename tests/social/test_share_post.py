import pytest
import allure
from pages.social_page import SocialPage
from pages.auth_page import AuthPage
from configs.db import run_query
@allure.feature("Post")
class TestSharePost:
    @pytest.mark.ui
    @pytest.mark.post
    @pytest.mark.smoke
    @pytest.mark.regression
    @allure.story("Create")
    def test_share_post(self, page, test_users):
        AuthPage(page).goto_login().login(
            email=test_users["editor"]["email"],
            password=test_users["editor"]["password"],
        )
        share = SocialPage(page)
        share.goto_post()
        share.share_post()
