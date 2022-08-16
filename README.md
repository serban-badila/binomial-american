![PyTests](https://github.com/serban-badila/binomial-american/actions/workflows/pytest.yml/badge.svg)

# binomial-american
Price calculator for american options using binomial trees

# CLI Usage
In a virtual env with all the dependencies installed ( `pip install -r requirements.txt` from the `$PWD` ) run

```python price_calculator/cli.py --option-type put --price 50 --volatility .3 --rate .05 --yield .0 --time 2 --strike-price 52 --steps 1000```
