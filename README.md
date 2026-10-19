# Sports Betting UI Tests

## Run the tests

Activate the project virtual environment, then run pytest with the required user ID:

```bash
source venv/bin/activate
python -m pip install -r requirements.txt
pytest -v --user-id "YOUR_USER_ID"
```

Pytest writes Allure test results to `allure-results/` and clears that directory
at the start of each test run.

## Generate a standalone Allure report

After running the tests, generate a single-page report with:

```bash
npm install --global allure-commandline
allure generate --single-file allure-results --clean --report-dir allure-report
```

The standalone report is written to `allure-report/index.html`. Allure CLI
requires Node.js/npm and Java; GitHub Actions installs Java and Allure CLI before
running tests.

## GitHub Actions

The Chrome tests run on each push and can also be started manually from the
Actions tab. Add a repository secret named `USER-ID`; the workflow passes it to
pytest as `--user-id`, runs Chrome headlessly, and uploads the standalone
`index.html` report as the `allure-single-file-report` artifact.
