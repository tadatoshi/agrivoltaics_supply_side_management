"""
Based on second equation from https://handbook-5-1.cochrane.org/chapter_7
/7_7_3_2_obtaining_standard_deviations_from_standard_errors_and.htm
"""

import math

def standard_deviation_from_confidence_interval(sample_size,
        confidence_interval_upper_limit, confidence_interval_lower_limit):
    return math.sqrt(sample_size) * (
        confidence_interval_upper_limit - confidence_interval_lower_limit
        ) / 3.92