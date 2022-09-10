import pytest
from agrivoltaics_supply_side_management.util.statistics_conversion\
    import standard_deviation_from_confidence_interval


@pytest.mark.parametrize(
    "sample_size, confidence_interval_upper_limit, " +\
    " confidence_interval_lower_limit",
    [
        (1200, 0.0, -0.4)
    ]
)
def test_standard_deviation_from_confidence_interval(sample_size,
        confidence_interval_upper_limit, confidence_interval_lower_limit):

    standard_deviation = standard_deviation_from_confidence_interval(
        sample_size,
        confidence_interval_upper_limit,
        confidence_interval_lower_limit
    )

    assert standard_deviation == 3.5347975664670974