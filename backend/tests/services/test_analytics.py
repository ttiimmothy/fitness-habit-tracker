import pytest
from datetime import date, timedelta
from unittest.mock import Mock

from app.services.analytics import build_week_overview
from app.models.habit_log import HabitLog


class TestAnalyticsService:
  """Test analytics service functions"""

  def test_build_week_overview_with_logs(self):
    """Test building week overview with habit logs"""
    today = date.today()

    # Create mock logs for different days
    logs = [
        Mock(spec=HabitLog, date=today),
        Mock(spec=HabitLog, date=today),
        Mock(spec=HabitLog, date=today - timedelta(days=1)),
        Mock(spec=HabitLog, date=today - timedelta(days=3)),
        Mock(spec=HabitLog, date=today - timedelta(days=7)),  # Outside range
    ]

    result = build_week_overview(logs)

    assert "labels" in result
    assert "datasets" in result
    assert len(result["labels"]) == 7  # 7 days
    assert len(result["datasets"]) == 1
    assert result["datasets"][0]["label"] == "Logs"
    assert len(result["datasets"][0]["data"]) == 7

    # Check that today has 2 logs
    today_index = 6  # Last day in the week
    assert result["datasets"][0]["data"][today_index] == 2

    # Check that yesterday has 1 log
    yesterday_index = 5
    assert result["datasets"][0]["data"][yesterday_index] == 1

    # Check that day 3 has 1 log
    day3_index = 3
    assert result["datasets"][0]["data"][day3_index] == 1

  def test_build_week_overview_empty_logs(self):
    """Test building week overview with no logs"""
    logs = []

    result = build_week_overview(logs)

    assert "labels" in result
    assert "datasets" in result
    assert len(result["labels"]) == 7
    assert len(result["datasets"]) == 1
    assert result["datasets"][0]["label"] == "Logs"
    assert all(count == 0 for count in result["datasets"][0]["data"])

  def test_build_week_overview_outside_range(self):
    """Test building week overview with logs outside date range"""
    today = date.today()

    # Create logs outside the 7-day range
    logs = [
        Mock(spec=HabitLog, date=today - timedelta(days=8)),
        Mock(spec=HabitLog, date=today - timedelta(days=10)),
        Mock(spec=HabitLog, date=today + timedelta(days=1)),  # Future date
    ]

    result = build_week_overview(logs)

    assert "labels" in result
    assert "datasets" in result
    assert len(result["labels"]) == 7
    assert all(count == 0 for count in result["datasets"][0]["data"])

  def test_build_week_overview_labels_format(self):
    """Test that labels are formatted correctly"""
    today = date.today()
    logs = [Mock(spec=HabitLog, date=today)]

    result = build_week_overview(logs)

    assert "labels" in result
    assert len(result["labels"]) == 7

    # Check that labels are day abbreviations
    for label in result["labels"]:
      assert len(label) == 3  # "Mon", "Tue", etc.
      assert label.isalpha()

  def test_build_week_overview_week_boundaries(self):
    """Test that week overview covers exactly 7 days"""
    today = date.today()
    start = today - timedelta(days=6)

    # Create logs for the exact boundaries
    logs = [
        Mock(spec=HabitLog, date=start),  # First day
        Mock(spec=HabitLog, date=today),  # Last day
    ]

    result = build_week_overview(logs)

    assert len(result["labels"]) == 7
    assert len(result["datasets"][0]["data"]) == 7

    # First and last days should have logs
    assert result["datasets"][0]["data"][0] == 1  # First day
    assert result["datasets"][0]["data"][6] == 1  # Last day

  def test_build_week_overview_multiple_logs_same_day(self):
    """Test building week overview with multiple logs on same day"""
    today = date.today()

    # Create multiple logs for the same day
    logs = [
        Mock(spec=HabitLog, date=today),
        Mock(spec=HabitLog, date=today),
        Mock(spec=HabitLog, date=today),
    ]

    result = build_week_overview(logs)

    # Today should have 3 logs
    today_index = 6
    assert result["datasets"][0]["data"][today_index] == 3

  def test_build_week_overview_data_structure(self):
    """Test that the returned data structure is correct"""
    today = date.today()
    logs = [Mock(spec=HabitLog, date=today)]

    result = build_week_overview(logs)

    # Check top-level structure
    assert isinstance(result, dict)
    assert "labels" in result
    assert "datasets" in result

    # Check labels structure
    assert isinstance(result["labels"], list)
    assert len(result["labels"]) == 7

    # Check datasets structure
    assert isinstance(result["datasets"], list)
    assert len(result["datasets"]) == 1

    dataset = result["datasets"][0]
    assert isinstance(dataset, dict)
    assert "label" in dataset
    assert "data" in dataset
    assert dataset["label"] == "Logs"
    assert isinstance(dataset["data"], list)
    assert len(dataset["data"]) == 7
