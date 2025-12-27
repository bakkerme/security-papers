from datetime import datetime, timezone

from security_papers.state import load_last_run, save_last_run


def test_state_round_trip(tmp_path):
    state_file = tmp_path / "state.txt"
    timestamp = datetime(2024, 5, 1, 12, 30, tzinfo=timezone.utc)

    save_last_run(str(state_file), timestamp)
    loaded = load_last_run(str(state_file))

    assert loaded == timestamp
