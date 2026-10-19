from datetime import date

from helpers.api_helper import get_matches

# This test validates there are no past matches returned by the API. 
#It is a critical test because the presence of past matches in the API response would indicate 
#a serious issue with the backend data or logic, 
#which could lead to incorrect information being displayed to users 
#and potentially allow betting on already completed matches.


def test_matches_api_returns_only_matches_with_non_past_dates(user_id):
    # get_matches calls raise_for_status(), so any non-2xx response fails here.
    matches = get_matches(user_id)

    past_matches = [
        match
        for match in matches
        if date.fromisoformat(match["kickoffDate"]) < date.today()
    ]
    assert not past_matches, (
        "Matches API returned matches with past kickoff dates: "
        f"{[match['id'] for match in past_matches]}"
    )