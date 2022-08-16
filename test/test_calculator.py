import pytest

from price_calculator.utils import price_option, Option

@pytest.mark.parametrize(
    "price,volatility,rate,dividend,time,strike,periods,expected_call,expected_put", 
    [
        (50, .3, .05, 0., 2., 52, 2, 9.194, 7.428),
        (50, .3, .05, 0., 2., 52, 5, 10.033, 7.581),
        (50, .3, .05, 0., 2., 52, 500, 9.705, 7.47),
    ]
    )
def test_price_calculator(price, volatility, rate, dividend, time, strike, periods, expected_call, expected_put):
    result_call = price_option(Option.CALL, price, volatility, rate, dividend, time, strike, periods)
    result_put = price_option(Option.PUT, price, volatility, rate, dividend, time, strike, periods)

    assert result_call == pytest.approx(expected_call, rel=1e-4)
    assert result_put == pytest.approx(expected_put, rel=1e-4)
