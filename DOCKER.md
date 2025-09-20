# Docker Setup for Pytest Playwright Automation

## Quick Start

1. **Build and run tests:**
   ```bash
   docker-compose up --build
   ```

2. **Run specific test markers:**
   ```bash
   docker-compose run tests PYTEST_MARKS="smoke and ui"
   ```

3. **Run with custom environment:**
   ```bash
   docker-compose --env-file docker.env up
   ```

## Configuration

### Environment Variables

The Docker setup uses the following environment variables (defined in `docker-compose.yml`):

- **Application Settings:**
  - `BASE_URL`: Your application URL
  - `USER_EMAIL`: Test user email
  - `USER_PASSWORD`: Test user password

- **Playwright Settings:**
  - `PW_HEADLESS`: Run browser in headless mode (true/false)
  - `PW_BROWSER`: Browser type (chromium/firefox/webkit)
  - `PW_TIMEOUT`: Default timeout in milliseconds
  - `RECORD_VIDEO`: Record test videos (true/false)

- **Database Settings:**
  - `MYSQL_HOST`: Database host (use "db" for Docker)
  - `MYSQL_PORT`: Database port
  - `MYSQL_USER`: Database username
  - `MYSQL_PASSWORD`: Database password
  - `MYSQL_DB`: Database name

- **Test Settings:**
  - `PYTEST_MARKS`: Pytest markers to run (e.g., "smoke", "regression")

### Custom Configuration

1. **Using docker.env file:**
   ```bash
   # Edit docker.env with your settings
   docker-compose --env-file docker.env up
   ```

2. **Override specific variables:**
   ```bash
   docker-compose run -e BASE_URL=https://myapp.com -e PYTEST_MARKS=regression tests
   ```

## Services

### Database Service (`db`)
- **Image:** MySQL 8.0
- **Port:** 3306
- **Health Check:** Automatic database readiness check
- **Persistent Storage:** MySQL data is persisted in Docker volume

### Tests Service (`tests`)
- **Build:** Custom image with Playwright and Python dependencies
- **Dependencies:** Waits for database to be healthy
- **Volumes:** Mounts test results and artifacts to host

## Output Directories

The following directories are mounted from the container to your host:

- `./allure-results/` - Allure test results
- `./allure-report/` - Generated Allure HTML report
- `./artifacts/` - Screenshots and other test artifacts
- `./videos/` - Test execution videos (if enabled)

## Common Commands

```bash
# Run smoke tests
docker-compose run tests PYTEST_MARKS=smoke

# Run regression tests
docker-compose run tests PYTEST_MARKS=regression

# Run with video recording
docker-compose run -e RECORD_VIDEO=true tests

# Run in non-headless mode (for debugging)
docker-compose run -e PW_HEADLESS=false tests

# Clean up containers and volumes
docker-compose down -v

# View logs
docker-compose logs tests
```

## Troubleshooting

1. **Database connection issues:**
   - Ensure the database service is healthy before tests run
   - Check MySQL credentials in environment variables

2. **Test failures:**
   - Check the BASE_URL is accessible from the container
   - Verify test data in `data/` directory
   - Review logs: `docker-compose logs tests`

3. **Permission issues:**
   - Ensure output directories are writable
   - On Windows, check Docker Desktop file sharing settings

## Development

To modify the Docker setup:

1. **Dockerfile:** Update Python dependencies or system packages
2. **docker-compose.yml:** Modify services, environment variables, or volumes
3. **entrypoint.sh:** Change test execution logic or pre-test setup
