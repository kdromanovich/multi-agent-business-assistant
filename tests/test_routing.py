from app.graph import _heuristic_route


def test_action_route():
    assert _heuristic_route("send the report") == "action"


def test_data_route():
    assert _heuristic_route("calculate ROI") == "data"
