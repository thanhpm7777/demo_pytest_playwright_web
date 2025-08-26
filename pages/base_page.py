# core/base_page.py
from __future__ import annotations

import re
import time
from typing import Optional, Union

from playwright.sync_api import Page, Locator, expect
from configs.settings import settings


class BasePage:

    def __init__(self, page: Page):
        self.page: Page = page
        self.page.set_default_timeout(settings.PW_TIMEOUT)

    # =========================

    def expect_url(self, pattern: str):
        expect(self.page).to_have_url(pattern)

    def toast_should_appear(self, text: str):
        expect(self.page.get_by_text(text)).to_be_visible()
    # =========================

    def open(self, path: str = "", wait_until: str = "domcontentloaded"):

        base = settings.BASE_URL
        if path:
            if base.endswith("/") and path.startswith("/"):
                url = base[:-1] + path
            else:
                url = base + path
        else:
            url = base

        self.page.goto(url, wait_until=wait_until)
        return self

    def assert_url_contains(self, fragment: str):
        expect(self.page).to_have_url(lambda u: fragment in u)

    def assert_url_is(self, url: str):
        expect(self.page).to_have_url(re.compile(re.escape(url)))

    # =========================
    # Low-level Locator getters
    # =========================
    def get_by_css(self, selector: str) -> Locator:
        return self.page.locator(selector)

    def get_by_id(self, element_id: str) -> Locator:
        return self.page.locator(f"#{element_id}")

    def get_by_class(self, class_name: str) -> Locator:
        return self.page.locator(f".{class_name}")

    def get_by_text(self, text: str, exact: bool = True) -> Locator:
        return self.page.get_by_text(text, exact=exact)

    def get_by_name(self, name: str) -> Locator:
        return self.page.locator(f"[name='{name}']")

    def get_by_placeholder(self, placeholder: str) -> Locator:
        return self.page.get_by_placeholder(placeholder)

    def get_by_label(self, label: str, exact: bool = True) -> Locator:
        return self.page.get_by_label(label=label, exact=exact)

    def get_by_testid(self, testid: str) -> Locator:
        # Quy ước data-testid chuẩn công ty
        return self.page.get_by_test_id(testid)

    def get_by_xpath(self, xpath: str) -> Locator:
        return self.page.locator(f"xpath={xpath}")

    def get_by_role(self, role: str, name: Union[str, re.Pattern], exact: bool = True) -> Locator:
        # name có thể là str hoặc regex pattern
        kwargs = {"name": name, "exact": exact} if isinstance(name, str) else {"name": name}
        return self.page.get_by_role(role=role, **kwargs)

    # =========================
    # Robust click / fill APIs
    # =========================
    def click_nav(self, text: str, exact: bool = True, expect_nav: bool = False):
        """
        Click một item menu/link theo text (ưu tiên role=link).
        - exact: khớp chính xác text
        - expect_nav: true nếu dự kiến điều hướng (bọc expect_navigation)
        """
        # 1) Ưu tiên link theo role
        locator = self.get_by_role("link", text, exact=exact)

        # 2) Fallback button
        if locator.count() == 0:
            locator = self.get_by_role("button", text, exact=exact)

        # 3) Fallback theo CSS + text (chống trường hợp icon + text)
        if locator.count() == 0:
            locator = self.page.locator(f"a:has-text('{text}'), button:has-text('{text}')")

        self._click(locator.first, expect_nav=expect_nav)

    def click_button(self, name: str, exact: bool = True, expect_nav: bool = False):
        locator = self.get_by_role("button", name, exact=exact)
        if locator.count() == 0:
            locator = self.page.locator(f"button:has-text('{name}')")
        self._click(locator.first, expect_nav=expect_nav)

    def click_link_or_button(self, name: str, exact: bool = True, expect_nav: bool = False):
        """
        Click theo text "thông minh": thử link -> button -> css fallback.
        """
        loc = self.get_by_role("link", name, exact=exact)
        if loc.count() == 0:
            loc = self.get_by_role("button", name, exact=exact)
        if loc.count() == 0:
            loc = self.page.locator(f"a:has-text('{name}'), button:has-text('{name}')")
        self._click(loc.first, expect_nav=expect_nav)

    def click_css(self, selector: str, expect_nav: bool = False):
        self._click(self.get_by_css(selector), expect_nav=expect_nav)

    def _click(self, locator: Locator, expect_nav: bool = False, retries: int = 2):
        """
        Click có:
        - Đợi visible + enabled
        - Scroll vào view
        - Retry nhẹ khi bị overlay/animation
        - Option expect_navigation
        """
        self._wait_visible(locator)
        for attempt in range(retries + 1):
            try:
                locator.scroll_into_view_if_needed()
                if expect_nav:
                    with self.page.expect_navigation():
                        locator.click()
                else:
                    locator.click()
                return
            except Exception:
                # Thử một nhịp nhỏ để tránh animation/overlay
                time.sleep(0.2)
                if attempt == retries:
                    raise

    # =========================
    # Filling / typing / select
    # =========================
    def fill_by_placeholder(self, placeholder: str, value: str, clear: bool = True):
        field = self.get_by_placeholder(placeholder)
        self._wait_visible(field)
        if clear:
            field.fill(value)
        else:
            field.type(value)

    def fill_by_name(self, name: str, value: str, clear: bool = True):
        field = self.get_by_name(name)
        self._wait_visible(field)
        if clear:
            field.fill(value)
        else:
            field.type(value)

    def fill_by_label(self, label: str, value: str, exact: bool = True, clear: bool = True):
        field = self.get_by_label(label, exact=exact)
        self._wait_visible(field)
        if clear:
            field.fill(value)
        else:
            field.type(value)

    def type_text(self, locator: Locator, text: str, delay_ms: int = 0):
        self._wait_visible(locator)
        locator.type(text, delay=delay_ms)

    def select_by_label(self, select_locator: Union[str, Locator], label: str):
        loc = self.get_by_css(select_locator) if isinstance(select_locator, str) else select_locator
        self._wait_visible(loc)
        loc.select_option(label=label)

    def select_by_value(self, select_locator: Union[str, Locator], value: str):
        loc = self.get_by_css(select_locator) if isinstance(select_locator, str) else select_locator
        self._wait_visible(loc)
        loc.select_option(value=value)

    # =========================
    # Keyboard / mouse utils
    # =========================
    def press(self, locator: Union[str, Locator], key: str):
        loc = self.get_by_css(locator) if isinstance(locator, str) else locator
        self._wait_visible(loc)
        loc.press(key)

    def hover(self, locator: Union[str, Locator]):
        loc = self.get_by_css(locator) if isinstance(locator, str) else locator
        self._wait_visible(loc)
        loc.hover()

    def scroll_into_view(self, locator: Union[str, Locator]):
        loc = self.get_by_css(locator) if isinstance(locator, str) else locator
        loc.scroll_into_view_if_needed()

    def upload_file(self, input_locator: Union[str, Locator], file_path: str):
        loc = self.get_by_css(input_locator) if isinstance(input_locator, str) else input_locator
        self._wait_visible(loc)
        loc.set_input_files(file_path)

    # =========================
    # Wait helpers
    # =========================
    def _wait_visible(self, locator: Locator, timeout: Optional[int] = None):
        expect(locator).to_be_visible(timeout=timeout or settings.PW_TIMEOUT)

    def wait_hidden(self, locator: Union[str, Locator], timeout: Optional[int] = None):
        loc = self.get_by_css(locator) if isinstance(locator, str) else locator
        expect(loc).to_be_hidden(timeout=timeout or settings.PW_TIMEOUT)

    def wait_enabled(self, locator: Union[str, Locator], timeout: Optional[int] = None):
        loc = self.get_by_css(locator) if isinstance(locator, str) else locator
        expect(loc).to_be_enabled(timeout=timeout or settings.PW_TIMEOUT)

    def wait_for_toast(self, text: str, exact: bool = False, timeout: Optional[int] = None):
        """
        Chờ toast/banner/thông báo có text (ví dụ div[role='alert']).
        Tùy dự án có thể sửa selector gốc.
        """
        candidate = self.page.locator("div[role='alert'], .toast, .notification")
        locator = candidate.get_by_text(text, exact=exact)
        expect(locator.first).to_be_visible(timeout=timeout or settings.PW_TIMEOUT)

    # =========================
    # Convenience shortcuts
    # =========================
    def click_by_text(self, text: str, exact: bool = True, expect_nav: bool = False):
        loc = self.get_by_text(text, exact=exact)
        self._click(loc.first, expect_nav=expect_nav)

    def click_testid(self, testid: str, expect_nav: bool = False):
        loc = self.get_by_testid(testid)
        self._click(loc.first, expect_nav=expect_nav)
