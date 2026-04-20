# 🎭 UI Test Automation Framework
### Python · Pytest · Playwright · Allure · Docker

> **Mô tả:** Framework kiểm thử UI tự động hóa theo mô hình **Page Object Model (POM)** cho ứng dụng web, tích hợp Allure Report, xDist parallel execution và Docker CI-ready.

---

## 📋 Mục lục

- [Tổng quan](#-tổng-quan)
- [Công nghệ sử dụng](#-công-nghệ-sử-dụng)
- [Kiến trúc dự án](#-kiến-trúc-dự-án)
- [Cài đặt môi trường](#-cài-đặt-môi-trường)
- [Cấu hình](#-cấu-hình)
- [Chạy test](#-chạy-test)
- [Allure Report](#-allure-report)
- [Docker](#-docker)
- [Test Coverage](#-test-coverage)
- [Contributing](#-contributing)

---

## 🔍 Tổng quan

Framework này được xây dựng để kiểm thử UI tự động hóa cho ứng dụng web, bao gồm các module chính:

| Module | Chức năng |
|---|---|
| **Auth** | Đăng nhập, Đăng ký |
| **Post** | Tạo bài viết mới |
| **Social** | Like bài viết, Chia sẻ bài viết |
| **Comment** | Thêm bình luận |

**Điểm nổi bật:**
- ✅ Mô hình **Page Object Model (POM)** — tách biệt logic UI với test logic
- ✅ **Session-based authentication** — đăng nhập 1 lần, dùng lại `storage_state` cho toàn suite
- ✅ **Tự động chụp screenshot + ghi video** khi test fail, đính kèm vào Allure Report
- ✅ **Parallel execution** với `pytest-xdist`
- ✅ **MySQL integration** — verify dữ liệu trực tiếp xuống database
- ✅ **Docker CI-ready** — chạy toàn bộ suite trong container

---

## 🛠 Công nghệ sử dụng

| Thư viện | Phiên bản | Mục đích |
|---|---|---|
| `pytest` | 8.3.2 | Test runner chính |
| `playwright` | ≥ 1.46 | Trình điều khiển browser (Chromium/Firefox/WebKit) |
| `allure-pytest` | 2.13.5 | Sinh báo cáo HTML đẹp |
| `pytest-xdist` | 3.6.1 | Chạy test song song |
| `pydantic-settings` | 2.3.4 | Quản lý cấu hình qua `.env` |
| `python-dotenv` | 1.0.1 | Load biến môi trường |
| `sqlalchemy` | latest | ORM kết nối MySQL |
| `pymysql` | latest | MySQL driver |
| `cryptography` | latest | Hỗ trợ mã hóa kết nối DB |

---

## 📁 Kiến trúc dự án

```
demo_pytest_playwright_web/
│
├── 📂 tests/                    # Tất cả test cases
│   ├── 📂 auth/
│   │   ├── test_login.py        # TC: Đăng nhập hợp lệ / sai mật khẩu
│   │   └── test_register.py     # TC: Đăng ký hợp lệ / trùng username
│   ├── 📂 post/
│   │   └── test_post.py         # TC: Tạo bài viết mới
│   ├── 📂 social/
│   │   ├── test_like_post.py    # TC: Like bài viết
│   │   └── test_share_post.py   # TC: Chia sẻ bài viết
│   ├── 📂 comment/
│   │   └── test_comment_add.py  # TC: Thêm bình luận
│   └── 📂 resources/            # File/dữ liệu hỗ trợ test
│
├── 📂 pages/                    # Page Object Model
│   ├── base_page.py             # BasePage: toàn bộ helper method (click, fill, wait…)
│   ├── auth_page.py             # AuthPage: login, register, assert
│   ├── post_page.py             # PostPage: create, update, delete post
│   ├── social_page.py           # SocialPage: like, share
│   └── comment_page.py          # CommentPage: add comment
│
├── 📂 configs/                  # Cấu hình dự án
│   ├── settings.py              # Pydantic Settings — load từ .env
│   └── db.py                    # MySQL engine & query helper
│
├── 📂 data/                     # Test data (fixtures)
│   ├── users.json               # Tài khoản test (editor, admin…)
│   └── posts.json               # Payload để tạo bài viết
│
├── 📂 utils/                    # Tiện ích chung
│   └── generators.py            # Sinh username/email/title ngẫu nhiên
│
├── 📂 artifacts/                # Screenshot & storage_state khi fail
├── 📂 videos/                   # Video ghi lại khi fail (nếu bật)
├── 📂 allure-results/           # Dữ liệu thô của Allure
│
├── conftest.py                  # Fixtures: browser, context, page, db_engine…
├── pytest.ini                   # Cấu hình pytest & markers
├── requirements.txt             # Danh sách dependencies
├── Dockerfile                   # Docker image build
├── docker-compose.yml           # Orchestrate tests + MySQL service
└── .env                         # Biến môi trường (không commit lên git)
```

---

## ⚙️ Cài đặt môi trường

### Yêu cầu
- Python **3.10+**
- pip

### Bước 1 — Tạo virtual environment

```bash
# Tạo venv
python -m venv .venv

# Kích hoạt (Windows)
.venv\Scripts\activate

# Kích hoạt (Linux/macOS)
source .venv/bin/activate
```

### Bước 2 — Cài dependencies

```bash
pip install -r requirements.txt
```

### Bước 3 — Cài Playwright browsers

```bash
python -m playwright install --with-deps chromium
```

> 💡 Thay `chromium` bằng `firefox` hoặc `webkit` nếu cần test đa trình duyệt.

---

## 🔧 Cấu hình

Tạo file `.env` ở thư mục gốc (có thể copy từ `.env.example`):

```dotenv
# ── Application URL ──────────────────────────
BASE_URL=https://your-app-url.com/
USER_EMAIL=editor@example.com
USER_PASSWORD=P@ssw0rd

# ── Playwright ───────────────────────────────
PW_BROWSER=chromium        # chromium | firefox | webkit
PW_HEADLESS=True           # True = chạy ẩn | False = mở giao diện
PW_TIMEOUT=10000           # Timeout mặc định (ms)
RECORD_VIDEO=false         # true = ghi video mỗi test

# ── MySQL Database ────────────────────────────
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=your_password
MYSQL_DB=your_database
```

### Markers có sẵn

| Marker | Mô tả |
|---|---|
| `smoke` | Bộ test critical path — chạy nhanh |
| `regression` | Toàn bộ regression suite |
| `ui` | Tất cả UI test (Playwright) |
| `auth` | Module Authentication |
| `post` | Module Post |
| `social` | Module Like / Share |

---

## ▶️ Chạy test

### Chạy theo marker

```bash
# Smoke tests (nhanh, critical path)
pytest -m "smoke and ui"

# Regression đầy đủ
pytest -m "regression and ui"

# Chỉ module auth
pytest -m "auth"

# Chỉ module post
pytest -m "post"
```

### Chạy song song (xDist)

```bash
# Tự động phát hiện số CPU core
pytest -m "regression and ui" -n auto

# Giới hạn số worker
pytest -m "regression and ui" -n 4
```

### Chạy file / test cụ thể

```bash
# Cả file
pytest tests/auth/test_login.py -vv

# Một test cụ thể
pytest tests/auth/test_login.py::TestLogin::test_login_valid -vv

# Tìm theo tên
pytest -k "test_login_valid" -q
```

### Tùy chọn hữu ích

```bash
# Verbose + hiện stdout
pytest -vv -s

# Tắt header ngắn gọn
pytest -q

# Dừng ở lần fail đầu tiên
pytest -x

# Retry khi fail (cần pytest-rerunfailures)
pytest --reruns 2 --reruns-delay 1
```

---

## 📊 Allure Report

### Cài Allure CLI

```bash
# macOS (Homebrew)
brew install allure

# Windows (Scoop)
scoop install allure

# Windows (Chocolatey)
choco install allure
```

### Sinh và xem báo cáo

```bash
# Chạy test trước (kết quả lưu vào ./allure-results)
pytest -m "regression"

# Xem báo cáo trực tiếp (tự động mở browser)
allure serve ./allure-results

# Hoặc: export ra thư mục tĩnh
allure generate ./allure-results -o ./allure-report --clean
```

### Xem báo cáo đã export

```bash
# Mở thư mục chứa allure-report rồi chạy:
python -m http.server 8000
# Truy cập: http://localhost:8000
```

---

## 🐳 Docker

### Build image

```bash
docker build -t ui-tests:local .
```

### Chạy toàn bộ test (regression)

```bash
docker run --rm \
  -e BASE_URL="https://your-app-url.com/" \
  -e USER_EMAIL="editor@example.com" \
  -e USER_PASSWORD="P@ssw0rd" \
  -e MYSQL_HOST="host.docker.internal" \
  -e MYSQL_PORT="3306" \
  -e MYSQL_USER="root" \
  -e MYSQL_PASSWORD="your_password" \
  -e MYSQL_DB="your_database" \
  -v "$PWD/allure-results:/app/allure-results" \
  -v "$PWD/screenshots:/app/screenshots" \
  -v "$PWD/videos:/app/videos" \
  ui-tests:local
```

### Chạy theo marker cụ thể

```bash
docker run --rm \
  -e BASE_URL="https://your-app-url.com/" \
  -e USER_EMAIL="editor@example.com" \
  -e USER_PASSWORD="P@ssw0rd" \
  -v "$PWD/allure-results:/app/allure-results" \
  ui-tests:local \
  pytest -m "smoke" --alluredir=allure-results --tb=short -v
```

### Docker Compose (kèm MySQL service)

```bash
# Khởi động MySQL
docker compose up -d mysql

# Chạy toàn bộ suite với MySQL
docker compose up --build tests

# Dọn dẹp
docker compose down -v
```

---

## ✅ Test Coverage

| Module | Test File | Scenarios |
|---|---|---|
| **Auth — Login** | `tests/auth/test_login.py` | ✔ Đăng nhập hợp lệ · ✔ Sai mật khẩu |
| **Auth — Register** | `tests/auth/test_register.py` | ✔ Đăng ký hợp lệ · ✔ Username đã tồn tại |
| **Post** | `tests/post/test_post.py` | ✔ Tạo bài viết mới |
| **Social — Like** | `tests/social/test_like_post.py` | ✔ Like bài viết |
| **Social — Share** | `tests/social/test_share_post.py` | ✔ Chia sẻ bài viết |
| **Comment** | `tests/comment/test_comment_add.py` | ✔ Thêm bình luận |

---

## 🤝 Contributing

1. Fork repository
2. Tạo branch mới: `git checkout -b feature/ten-tinh-nang`
3. Commit thay đổi: `git commit -m "feat: mô tả ngắn gọn"`
4. Push và tạo Pull Request

### Convention đặt tên test

```
test_<module>_<action>_<expected_result>
# Ví dụ:
test_login_valid_user_success
test_register_duplicate_username_fail
test_post_create_with_attachment_success
```

---

<div align="center">
  <sub>Built with ❤️ using Python · Playwright · Pytest · Allure</sub>
</div>