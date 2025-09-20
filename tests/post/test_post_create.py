import time

import pytest
import allure
from pages.post_page import PostPage
from pages.auth_page import AuthPage
from configs.db import run_query, execute
@pytest.mark.ui
@pytest.mark.post
@allure.feature("Post")
@allure.story("Create")
def test_create_post_valid(page, test_users, test_posts):

    AuthPage(page).goto_login().login(
        test_users["editor"]["email"],
        test_users["editor"]["password"])
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
        is_active_tap_chi=True
    )
    with allure.step("Verify post vừa tạo đã thành công"):
        post.verify_register_success(success_text="Đã thêm bài viết thành công")


