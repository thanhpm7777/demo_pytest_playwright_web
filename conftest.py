import json
import os
from pathlib import Path
import pytest
import allure
from playwright.sync_api import Playwright, sync_playwright
from configs.settings import settings
import pytest
from configs.db import get_mysql_engine

# ----- Test data -----
@pytest.fixture(scope="session")
def test_users():
    with open("data/users.json", encoding="utf-8") as f:
        return json.load(f)

@pytest.fixture(scope="session")
def test_posts():
    with open("data/posts.json", encoding="utf-8") as f:
        return json.load(f)

# ----- Playwright core -----
@pytest.fixture(scope="session")
def pw() -> Playwright:
    with sync_playwright() as p:
        yield p

@pytest.fixture(scope="session")
def browser_type(pw):
    return getattr(pw, settings.PW_BROWSER.lower())  # chromium/firefox/webkit

Path("videos").mkdir(exist_ok=True)
Path("artifacts").mkdir(exist_ok=True)

@pytest.fixture
def browser(browser_type):
    browser = browser_type.launch(headless=settings.PW_HEADLESS)
    yield browser
    browser.close()

@pytest.fixture
def context(browser):
    ctx = browser.new_context(
        base_url=settings.BASE_URL,
        record_video_dir="videos" if settings.RECORD_VIDEO else None,
    )
    ctx.set_default_timeout(settings.PW_TIMEOUT)
    yield ctx
    ctx.close()


@pytest.fixture
def page(context, request):
    page = context.new_page()
    yield page

    # attach khi fail
    failed = hasattr(request.node, "rep_call") and request.node.rep_call.failed
    if failed:
        png_path = f"artifacts/{request.node.name}.png"
        page.screenshot(path=png_path, full_page=True)
        allure.attach.file(png_path, name="screenshot", attachment_type=allure.attachment_type.PNG)
        allure.attach(page.content(), name="page_source", attachment_type=allure.attachment_type.HTML)
        if settings.RECORD_VIDEO and page.video:
            try:
                allure.attach.file(page.video.path(), name="video", attachment_type=allure.attachment_type.MP4)
            except Exception:
                pass


# hook để biết phase fail/pass (dùng ở fixture page)
@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)

# ---- optional: tạo storage_state sau khi login một lần cho suite ----
@pytest.fixture(scope="session")
def session_storage(pw, test_users):
    from pages.auth_page import AuthPage
    browser = getattr(pw, settings.PW_BROWSER).launch(headless=settings.PW_HEADLESS)
    ctx = browser.new_context(base_url=settings.BASE_URL)
    page = ctx.new_page()
    AuthPage(page).goto_login().login(test_users["editor"]["email"], test_users["editor"]["password"]).expect_dashboard()
    ctx.storage_state(path="artifacts/storage_state.json")
    ctx.close()
    browser.close()
    return "artifacts/storage_state.json"

@pytest.fixture
def context_with_auth(browser, session_storage):
    ctx = browser.new_context(
        base_url=settings.BASE_URL,
        storage_state=session_storage,
        record_video_dir="videos" if settings.RECORD_VIDEO else None,
    )
    ctx.set_default_timeout(settings.PW_TIMEOUT)
    yield ctx
    ctx.close()




@pytest.fixture(scope="session")
def db_engine():
    """MySQL Engine dùng chung cho toàn bộ test session."""
    return get_mysql_engine()
