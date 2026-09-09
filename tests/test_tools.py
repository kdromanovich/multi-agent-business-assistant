from app.tools import build_action_plan, calculate_roi, extract_numbers


def test_roi():
    result = calculate_roi(1000, 500, 500)
    assert result["roi_percent"] == 200


def test_numbers():
    assert extract_numbers("revenue 100.5 cost 20") == [100.5, 20.0]


def test_action_plan_has_approval():
    assert any("approval" in step.lower() for step in build_action_plan("send report"))
