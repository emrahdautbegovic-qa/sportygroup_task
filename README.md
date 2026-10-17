# Sports Betting UI Tests

## Run the tests

Activate the project virtual environment, then run pytest with the required user ID:

```bash
source venv/bin/activate
pytest -v --user-id "YOUR_USER_ID"
```

Pytest writes Allure test results to `allure-results/` and clears that directory
at the start of each test run.

## Generate a standalone Allure report

After running the tests, generate a single-page report with:

```bash
bash scripts/generate_allure_report.sh
```

The script uses a checksum-verified, project-local Allure CLI 2.46.1, so it does
not depend on the system or Homebrew Allure installation. On the first run it
downloads the CLI into the ignored `.tools/` directory. The standalone report
is written to `allure-report/index.html`.
