# Copilot Prompts

The following is a chronological record of the prompts used during this work. IDE selection metadata and timestamps are omitted.

1. Create session level fixture that reads user-id from cmd parameters
2. Add another session level fixture that returns url:
   `https://qae-assignment-tau.vercel.app/?user-id=<user-id>`
3. what the urlencode does?
4. does it have any security advances
5. add a comment
6. now create another fixture that is selenium webdriver that runs on chrome
7. create a new UI test that just navigates to the url using the driver.
   The test should be in ui_tests/test_sports_betting.py
8. run the test
9. how should I install selenium
10. I need driver to wait for page to load
11. it didn't work

    can you do 2 commands:
    - source ./venv/bin/activate
    - pytest ui_tests  --user-id candidate-R7PrnqPEdCPa
12. it is installed, I want to see terminal while you are runnning these commands 1 by
13. so why the test passed when url wasn't opened at all
14. add some assert that confirms page title is Sports Betting QA
15. run it no
16. Make a fixture that does api request to https://qae-assignment-tau.vercel.app/api/matches
    saves received matches into an array and returns the array.
    This fixture should have a function scope (so it is executed only if passed as test parameter)
17. update test so it writes all received matches to terminal
18. add header item x-user-id
19. add page object that has the following elements:
    header_title (ID: header-title)
    header_balance_container (ID: header-balance)
    header_balance = header_balance_container/span(contains text Balance)
    match_list_title (ID: match-list-title)
    match_list_count (ID:match-list-count)
    date_filter (ID:date-filter)
    odds_filter (ID: odds-filter)
    match_list (ID: match-list)
    match_card = match_list/div with class=card matchCard
    match_meta (match_card/div with class matchMeta)
    match_teams (match_card/div with class teams)
    odds_grid = match_card/div class odds grid
20. add function to upen page using url passed as parameter
21. use match_list_page to open url
    and assert page is loaded
22. can you turn this into a class SportsBettingTests so pages are initialized in constructor and reused accross tests
23. why did you use regular python constructor?
24. shouldn't you use __init__
25. add function called wait_page_loaded
    that waits for each page element to load
26. reuse existing elements instead of writing locators from scratch
27. run test
28. figure that out on your own.
    also update the page so it opens browser in full screen
29. create helpers/api_helper.py
    and simplify def matches logic by reusing api_helper
30. rerun test
31. add more tests with proper assertion:
32. test number of shown matches equals number of matches received from api
33. test date in the match card matches the date retrieved from api
34. assert past matches are not displayed
35. test all matches dates are displayed in format Wed 28 Oct and the date matches the one retrieved from the api
36. make a logic that excepts today and tomorrow matches
37. add comment for that logic
38. add comment with format explanation
39. what does the !r mean: {count_text!r}
40. add comment
41. explain the line
42. what does the group(1) mean
43. it should be date now (not 00:00 today)
44. The API provides only `kickoffDate` (no kickoff time), so the test can compare dates but can’t distinguish a match earlier today from one later today.
    add this as a comment
45. is this checking there are no past matches in match_ids?
46. install ruff and fix all code to follow ruff rules
47. https://qae-assignment-tau.vercel.app/api/balance

    add function to get balance and then update balance test to also validate correct balance is displayed
48. run tests
49. use base_api_url
50. update all screenshot paths to use them from screenshots folder
51. update .gitignore to ignore redundant files like pycache
52. can you put the logic to the page object and reuse
53. do the same everywhere it is applicable
54. install allure-pytest and update tests to have screenshot if test failed and proper allure annotations so I get a single page html report in the end and nice test description in html format and useful logs
55. I can see full allure-report. It should be only index.html inside if you used --single-page parameter
56. I need this conversation saved into copilot_prompts.md
    So whoever review the code can see all my prompts I used
