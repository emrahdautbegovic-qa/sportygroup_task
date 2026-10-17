# Single Bet Placement — Prioritized Test Scenarios

## Scope and test data

These scenarios cover match availability and filtering, single-bet placement, stake limits, retry behavior, and the transition of an event from upcoming to live. The user configured on the current test environment has 125EUR balance which is more then maximum bet of 100EUR so it makes not sense to test if user is able to bet with money they don't have available on their balance. We would need to reconfigure the balance for this case so it is not added to the list.

## SBP-001 — Show only eligible matches with visible date, time, and odds

- **Priority:** Critical
- **Risk Rationale:** Missing or incorrect kickoff information prevents users from judging event eligibility. Offering live or past events can allow bets after an event has started or its result is known.
- **Steps:**
  1. Open the match list without applying filters.
  2. Inspect every listed event, including its displayed date, kickoff time, timezone (if shown), and odds.
  3. Compare each kickoff time with the current time and check the fixture data/status for live and past events.
- **Expected Result:**
  - Every listed event displays a clear, valid date and kickoff time, and visible odds for its available outcomes; each odds value is valid and within the configured product range.
  - Only upcoming events with kickoff times strictly in the future are listed.
  - Live, in-progress, and past events are not listed or available for selection.

## SBP-002 — Ensure filters cannot expose live or past matches

- **Priority:** Critical
- **Risk Rationale:** Filtering must preserve the match eligibility rules; otherwise a filter could expose an event that is unavailable in the unfiltered list.
- **Steps:**
  1. Attempt to select date in the past
  2. Attempt to select date range with dates in the past
  3. Attempt to select today's date
- **Expected Result:**
  - No individual filter, filter combination, or past-date query exposes a live, in-progress, or past event.
  - A past date is either unavailable for selection or returns no ineligible events.
  - today's date gives only eligible matches that are playing today (not the one that already started, or already finished today)

## SBP-003 — Place a valid single bet and verify receipt and persistent balance

- **Priority:** Critical
- **Risk Rationale:** A successful bet must be recorded once, confirmed clearly, and debited consistently in both the current view and persisted account state.
- **Steps:**
  1. Note the user's available balance.
  2. Select an outcome for an upcoming event and enter a valid stake of €10.00.
  3. Place the bet once and inspect the success receipt and displayed balance.
  4. Refresh the page, return to the account or bet history if needed, and inspect the balance and placed bet.
- **Expected Result:**
  - Exactly one bet is accepted for the selected event and outcome.
  - The receipt includes a bet ID, event, outcome, stake (€10.00), accepted odds, potential payout, and placement timestamp.
  - The available balance decreases by exactly €10.00.
  - After refresh, the reduced balance and the placed bet remain recorded; the stake is not deducted again on refresh.

## SBP-004 — Reject stakes below the minimum and above the maximum

- **Priority:** Critical
- **Risk Rationale:** Accepting a stake outside configured limits can create unintended financial exposure; inconsistent validation may also mislead users.
- **Steps:**
  1. With a valid upcoming selection, attempt to place a bet with a stake below €1.00 (for example, €0.99 or €-1.00).
  2. Repeat with a stake above €100.00 (for example, €100.01 or €-100.00).
- **Expected Result:**
  - Both attempts are rejected with clear validation feedback identifying the €1.00–€100.00 stake range.
  - Neither attempt creates a bet or changes the user's balance.

## SBP-005 — Verify potential payout from stake multiplied by odds

- **Priority:** Critical
- **Risk Rationale:** An incorrect payout calculation can misrepresent the return a customer may receive and undermine confidence in the bet receipt.
- **Steps:**
  1. Select an upcoming event outcome with known displayed odds.
  2. Enter a valid stake and note the displayed potential payout before placement.
  3. Place the bet and compare the receipt's accepted stake, odds, and potential payout with the calculation.
- **Expected Result:**
  - Potential payout (gross return) equals the accepted stake multiplied by the accepted decimal odds, rounded according to the product's currency rules; 
  - User's balance is decreased for the stake amount
  - Closing the modal doesn't place another bet 

## SBP-006 — Reject placement when a selected upcoming event becomes live

- **Priority:** Critical
- **Risk Rationale:** An event may start after a user selects an outcome but before bet placement. The server must revalidate eligibility at placement time rather than accepting a stale selection.
- **Steps:**
  1. Select an outcome for an event that is upcoming (close to current time like in 1 min, or configure 1 of the events in test environment if possible for this scenario) and confirm it appears in the bet slip.
  2. Wait 1 min until the event started
  3. Attempt to place a valid-stake bet using the selection made before kickoff.
- **Expected Result:**
  - Placement is rejected because the event is live or has started; a stale selection cannot be used to place the bet.
  - The user receives clear feedback that the event is no longer available, and the selection/odds are disabled or removed.
  - No bet is created and the user's balance remains unchanged.
