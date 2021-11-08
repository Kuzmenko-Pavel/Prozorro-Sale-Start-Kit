{%- if cookiecutter.use_dotenv == 'y' %}
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv('py.env'), override=False)
{%- endif %}
