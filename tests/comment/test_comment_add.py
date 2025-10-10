import pytest
import allure
from pages.comment_page import CommentPage
from pages.auth_page import AuthPage
from configs.db import run_query
@allure.feature("Post")
class TestComment:
    @pytest.mark.ui
    @pytest.mark.post
    @pytest.mark.smoke
    @pytest.mark.regression
    @allure.story("Create")
    def test_add_comment(self, page, test_users):
        AuthPage(page).goto_login().login(
            email=test_users["editor"]["email"],
            password=test_users["editor"]["password"],
        )
        comment = CommentPage(page)
        comment.goto_post()
        comment_text = "abc"
        comment.add_comment(comment_text=comment_text)

        with allure.step("Verify comment được lưu trong database"):
            query = "SELECT * FROM blog_comment WHERE text = :comment_text"
            result = run_query(query, {"comment_text": comment_text})
            assert result, f"Không tìm thấy comment '{comment_text}' trong database!"
            db_comment = result[0]
            assert db_comment["text"].strip() == comment_text, (
                f"Nội dung comment trong DB khác với mong đợi: {db_comment['content']}"
            )


