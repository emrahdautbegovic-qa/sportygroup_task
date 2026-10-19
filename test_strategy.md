# Test Strategy

## Single Bet Placement scope

The feature covers single bets on upcoming football/soccer matches in the desktop web application. Live betting, accumulators/multi-bets, other sports, and mobile-specific UX are out of scope. Use EUR, dedicated test users, and controllable match fixtures wherever possible.

## API tests

- **Unit tests:** Test isolated rules for football and pre-match eligibility, valid single selections (`HOME`, `DRAW`, `AWAY`), stake and odds bounds, two-decimal precision, payout calculation and currency rounding, and balance deductions. Cover stake boundaries (€1.00 minimum and €100.00 maximum), missing/nonnumeric/negative stakes, insufficient balance, invalid selection, and odds boundaries (1.01–1000.00). Mock persistence and external services.
- **Integration tests:** Exercise API handlers with persistence and dependent services. Verify `x-user-id` authentication, request parsing and validation, endpoint methods, response schemas, error mapping (400, 401, 405, 409, 422, and 500), and persisted state consistency. Cover:
  - `GET /api/matches`: response shape, football-only upcoming matches, valid dates, team names, and three odds.
  - `GET /api/balance`: EUR balance response and user isolation.
  - `POST /api/place-bet`: accepted bet response, selected odds and payout, exactly-once balance deduction, insufficient balance, invalid or unknown match, and same-user in-progress conflict.
  - `POST /api/reset-balance`: reset response agrees with the persisted balance on a subsequent read.
  - API documentation endpoints `/api/docs` and `/api/docs?format=json` return usable Swagger UI and OpenAPI documentation.
- **End-to-end tests:** Send requests through the deployed API in a development or QA environment using a dedicated test account. Verify complete match retrieval, balance read, valid single-bet placement, and post-placement balance; also exercise representative validation failures, stale/ineligible matches, and balance reset. Verify response data and persisted state agree.

The specification conflicts on the minimum stake: business rules and minimum UI copy say €1.00, while the validation table says €1.01. Confirm the intended boundary before making the minimum-stake assertion a release gate.

## UI regression tests

Automate the critical user-visible flows on desktop:

- Verify the match list contains upcoming football matches only and each card shows home/away teams, kickoff date/time, and selectable `1`, `X`, and `2` odds.
- Select an outcome, verify the single-selection bet slip, then select a different outcome and confirm it replaces the previous one.
- Verify the fixed bet slip shows the selection, stake, available balance, total stake, and potential payout; cover per-selection remove and Remove All.
- Validate stake input and feedback for missing, nonnumeric, invalid precision, below/above limits, and insufficient balance.
- Verify date single-day/range filters and inclusive boundaries; verify odds min/max filters are inclusive and invalid ranges show clear feedback.
- Place a valid bet: verify the loading label (`Placing...`), one final success state, stake deduction, and receipt fields (bet ID, match, selection, accepted odds, stake, payout, timestamp).
- Close the success receipt and verify the main flow returns with no active selection.
- Simulate placement failure: verify the error modal title/message, Rebet retries placement, and Close or top-right X dismisses it and clears selection/stake.
- Verify available balance and displayed match, date, and odds data against API responses.

## Execution schedule

- Run all API unit and integration tests on every pull request.
- Run API end-to-end tests and UI tests as regression suites before each release.
- Keep tests that mutate account state on dedicated test accounts and reset test data before use.

## API performance and load testing

Run performance tests against a non-production environment with production-like data and configuration. Exercise representative API traffic, including match retrieval, balance reads, bet placement, and balance reset. Use ramp-up, steady-state, and short peak-load scenarios to identify throughput limits, latency degradation, and error rates. Monitor application and datastore resource usage, and agree on explicit latency and error-rate targets with the service owners before making performance results a release gate. Keep load tests separate from functional CI runs to avoid resource contention.
