import random

import pandas as pd
import pytest

from air_handling_unit.faults import FaultConditionOne

'''
to see print statements in pytest run with
$ pytest tests/unit/test_ahu_fc2.py -rP

random seed set every time random.random()
is called so the results to be exact same
every time for the flag mean col output.

Future compare to ML FDD Vs rule based FDD
'''

TEST_DUCT_STATIC_COL = "duct_static"
TEST_DUCT_STATIC_SETPOINT_COL = "duct_static_setpoint"
TEST_SUPPLY_VFD_SPEED_COL = "supply_vfd_speed"
TEST_VFD_ERR_THRESHOLD = 0.05
TEST_VFD_SPEED_MAX = 0.7
TEST_DUCT_STATIC_ERR_THRESHOLD = 0.1


def fail_row() -> dict:
    data = {
        TEST_DUCT_STATIC_COL: .8,
        TEST_DUCT_STATIC_SETPOINT_COL: 1.1,
        TEST_SUPPLY_VFD_SPEED_COL: 0.99,
    }
    return data


def pass_row() -> dict:
    data = {
        TEST_DUCT_STATIC_COL: 1.5,
        TEST_DUCT_STATIC_SETPOINT_COL: 1.0,
        TEST_SUPPLY_VFD_SPEED_COL: 0.80,
    }
    return data


def generate_data(fail_portion: float, samples: int) -> pd.DataFrame:
    data = []
    for _ in range(samples):
        random.seed(_)
        if random.random() < fail_portion:
            data.append(fail_row())
        else:
            data.append(pass_row())
    return pd.DataFrame(data)


@pytest.fixture
def failing_df() -> pd.DataFrame:
    return generate_data(0.9, 100)


@pytest.fixture
def passing_df() -> pd.DataFrame:
    return generate_data(0.1, 100)


def test_failing(failing_df):
    fc1 = FaultConditionOne(
        TEST_VFD_ERR_THRESHOLD,
        TEST_VFD_SPEED_MAX,
        TEST_DUCT_STATIC_ERR_THRESHOLD,
        TEST_DUCT_STATIC_COL,
        TEST_SUPPLY_VFD_SPEED_COL,
        TEST_DUCT_STATIC_SETPOINT_COL,
    )

    results = fc1.apply(failing_df)
    actual = results["fc1_flag"].mean()
    expected = 0.89
    message = f"FC1 FAIL actual is {actual} and expected is {expected}"
    assert actual == pytest.approx(expected), message


def test_passing(passing_df):
    fc1 = FaultConditionOne(
        TEST_VFD_ERR_THRESHOLD,
        TEST_VFD_SPEED_MAX,
        TEST_DUCT_STATIC_ERR_THRESHOLD,
        TEST_DUCT_STATIC_COL,
        TEST_SUPPLY_VFD_SPEED_COL,
        TEST_DUCT_STATIC_SETPOINT_COL,
    )

    results = fc1.apply(passing_df)
    actual = results["fc1_flag"].mean()
    expected = 0.11
    message = f"FC1 PASS actual is {actual} and expected is {expected}"
    assert actual == pytest.approx(expected), message
