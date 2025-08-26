# Automation POM – Python + Playwright + Allure

## 1) Setup
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/Mac:
. .venv/bin/activate

pip install -r requirements.txt
python -m playwright install --with-deps chromium
cp .env.example .env  # sửa BASE_URL, USER_*

## 2) Chạy smoke / regression
pytest -m "smoke and ui"
pytest -m "regression and ui" -n auto  # parallel

## 3) Allure report
# Cài allure commandline: (Mac brew / Win scoop / choco)
allure serve ./allure-results

## 4) Lưu session (tùy chọn)
# Khi cần tạo storage_state:
pytest -k test_login_valid -q

# cach mo file report download ve
1.Mở PowerShell, chạy:
cd "D:\Automation 2025\allure-report-html (3)"
python -m http.server 8000
http://localhost:8000