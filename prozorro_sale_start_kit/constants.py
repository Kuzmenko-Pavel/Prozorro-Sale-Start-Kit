import pathlib

__all__ = [
    'TEMPLATE_DIR',
    'EXTENSIONS'
]

TEMPLATE_NAME = 'template_project'
TEMPLATE_DIR = pathlib.Path(__file__).parent / TEMPLATE_NAME

EXTENSIONS = {
    'swagger_yaml': {
        'TEMPLATE_DIRS': ['swagger'],
        'TEMPLATE_FILES': []
    },
    'databridge': {
        'TEMPLATE_DIRS': [
            'src/prozorro_sale/{{cookiecutter.underscore_project_name}}/databridge'
        ],
        'TEMPLATE_FILES': [
            'test/integration/test_databridge.py'
        ]
    },
    'chronograph': {
        'TEMPLATE_DIRS': [
            'src/prozorro_sale/{{cookiecutter.underscore_project_name}}/chronograph'
        ],
        'TEMPLATE_FILES': [
        ]
    },
    'setup_py': {
        'TEMPLATE_DIRS': [
        ],
        'TEMPLATE_FILES': [
            'setup.py'
        ]
    }
}
