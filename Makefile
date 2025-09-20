	cat > Makefile <<'EOF'
IMAGE=ui-tests:local

.PHONY: build run run-mark compose up down allure clean

build:
	\tdocker build -t $(IMAGE) .

run:
	\tmkdir -p allure-results test-results screenshots videos
	\tdocker run --rm \\
	\t  -e BASE_URL="$(BASE_URL)" \\
	\t  -e USER_EMAIL="$(USER_EMAIL)" \\
	\t  -e USER_PASSWORD="$(USER_PASSWORD)" \\
	\t  -e MYSQL_HOST="$(MYSQL_HOST)" -e MYSQL_PORT="$(MYSQL_PORT)" \\
	\t  -e MYSQL_USER="$(MYSQL_USER)" -e MYSQL_PASSWORD="$(MYSQL_PASSWORD)" -e MYSQL_DB="$(MYSQL_DB)" \\
	\t  -v "$$PWD/allure-results:/app/allure-results" \\
	\t  -v "$$PWD/test-results:/app/test-results" \\
	\t  -v "$$PWD/screenshots:/app/screenshots" \\
	\t  -v "$$PWD/videos:/app/videos" \\
	\t  $(IMAGE)

run-mark:
	\t# Ví dụ: make run-mark MARK="smoke or regression"
	\tmkdir -p allure-results
	\tdocker run --rm \\
	\t  -e BASE_URL="$(BASE_URL)" \\
	\t  -e USER_EMAIL="$(USER_EMAIL)" \\
	\t  -e USER_PASSWORD="$(USER_PASSWORD)" \\
	\t  -v "$$PWD/allure-results:/app/allure-results" \\
	\t  $(IMAGE) \\
	\t  pytest -m "$(MARK)" --alluredir=allure-results --tb=short -v

compose:
	\tdocker compose up --build tests

up:
	\tdocker compose up -d mysql

down:
	\tdocker compose down -v

allure:
	\t# Tạo HTML report từ allure-results -> allure-report
	\tmkdir -p allure-report
	\tdocker run --rm \\
	\t  -v "$$PWD/allure-results:/results" \\
	\t  -v "$$PWD/allure-report:/report" \\
	\t  frankescobar/allure-docker-service \\
	\t  /bin/sh -c "allure generate /results -o /report --clean"

clean:
	\trm -rf allure-results allure-report test-results screenshots videos || true
	\tdocker image prune -f
	EOF
