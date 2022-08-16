import click
from utils import price_option, Option


@click.command()
@click.option('--option-type', 'o', help='Option type.', required=True, type=click.Choice(['PUT', 'CALL'], case_sensitive=False))
@click.option('--price', 'p', help='Price of the underlying stock.', type=float)
@click.option('--volatility', 'v', help='Stock price volatility.', type=float)
@click.option('--rate', 'r', help='Risk free rate.', type=float)
@click.option('--yield', 'y', help='Divident yield rate.', type=float)
@click.option('--time', 't', help='Time to expiration.', type=float)
@click.option('--strike-price', 'k', help='Exercise price.', type=float)
@click.option('--steps', 'n', help='Number of steps.', type=int)
def calculate(o: Option, p: float, v: float, r: float, y: float, t: float, k: float, n: int):
    price = price_option(o, p, v, r, y, t, k, n)
    click.echo(price)
    
if __name__ == '__main__':
    calculate()