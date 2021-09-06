from prozorro_sale.tools.environment import Environment

__all__ = ['environment']

spec = {
    'HOST': str,
    'PORT': int
}
default = {
    'HOST': 'localhost',
    'PORT': 8080
}

environment = Environment(spec=spec, default=default)
