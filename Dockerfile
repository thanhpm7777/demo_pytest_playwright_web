# Base Playwright Python
FROM mcr.microsoft.com/playwright/python:v1.48.0-jammy

WORKDIR /app

# MySQL client (giống CI)
RUN apt-get update && apt-get install -y mysql-client && rm -rf /var/lib/apt/lists/*

# ---- Thêm system deps cần thiết để cài cryptography (và build packages nếu cần) ----
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libssl-dev \
    libffi-dev \
    python3-dev \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Nếu bạn thấy cryptography vẫn bị build error, uncomment dòng cargo:
# RUN apt-get update && apt-get install -y cargo && rm -rf /var/lib/apt/lists/*

# Cài libs Python trước để tận dụng cache
COPY requirements.txt .
RUN python -m pip install --upgrade pip setuptools wheel && pip install -r requirements.txt

# 🔧 CÀI BROWSER CHO PLAYWRIGHT (bắt buộc)
RUN python -m playwright install --with-deps chromium

# Copy source code
COPY . .

# (tuỳ chọn) thư mục artifacts
RUN mkdir -p allure-results test-results screenshots videos

# Lệnh mặc định (có thể override khi run)
CMD ["pytest", "-m", "smoke", "--alluredir=allure-results", "--tb=short", "-v"]
