__all__ = [
    'EXTENSIONS'
]

EXTENSIONS = {
    'mongo': {
        'TEMPLATE_DIRS': [],
        'TEMPLATE_FILES': []
    },
    'redis': {
        'TEMPLATE_DIRS': [],
        'TEMPLATE_FILES': []
    },
    'swagger': {
        'TEMPLATE_DIRS': [],
        'TEMPLATE_FILES': []
    },
    'swagger_yaml': {
        'TEMPLATE_DIRS': ['swagger'],
        'TEMPLATE_FILES': []
    },
    'api': {
        'TEMPLATE_DIRS': [
            'src/prozorro_sale/{underscore_project_name}/api'
        ],
        'TEMPLATE_FILES': [
            'test/integration/test_api.py',
            'helm/{project_name}/templates/api.yaml'
        ]
    },
    'databridge': {
        'TEMPLATE_DIRS': [
            'src/prozorro_sale/{underscore_project_name}/databridge'
        ],
        'TEMPLATE_FILES': [
            'test/integration/test_databridge.py',
            'helm/{project_name}/templates/api.yaml'
        ]
    },
    'chronograph': {
        'TEMPLATE_DIRS': [
            'src/prozorro_sale/{underscore_project_name}/chronograph'
        ],
        'TEMPLATE_FILES': [
            'test/integration/test_chronograph.py',
            'helm/{project_name}/templates/chronograph.yaml'
        ]
    },
    'prozorro_tools': {
        'TEMPLATE_DIRS': [
            'config'
        ],
        'TEMPLATE_FILES': [
            'src/prozorro_sale/{underscore_project_name}/environment.py'
            'test/unit/test_environment.py'
        ]
    },
    'schematics': {
        'TEMPLATE_DIRS': [],
        'TEMPLATE_FILES': []
    },
    'prozorro_auth': {
        'TEMPLATE_DIRS': [],
        'TEMPLATE_FILES': []
    },
    'prozorro_procedure': {
        'TEMPLATE_DIRS': [],
        'TEMPLATE_FILES': []
    },
    'prozorro_mirror': {
        'TEMPLATE_DIRS': [],
        'TEMPLATE_FILES': []
    },
    'prozorro_metrics': {
        'TEMPLATE_DIRS': [],
        'TEMPLATE_FILES': []
    },
    'uvloop': {
        'TEMPLATE_DIRS': [],
        'TEMPLATE_FILES': []
    },
    'yaml': {
        'TEMPLATE_DIRS': [],
        'TEMPLATE_FILES': []
    },
    'orjson': {
        'TEMPLATE_DIRS': [],
        'TEMPLATE_FILES': []
    },
    'ujson': {
        'TEMPLATE_DIRS': [],
        'TEMPLATE_FILES': []
    },
    'python_box': {
        'TEMPLATE_DIRS': [],
        'TEMPLATE_FILES': []
    },
    'trafaret': {
        'TEMPLATE_DIRS': [],
        'TEMPLATE_FILES': []
    },
    'requests': {
        'TEMPLATE_DIRS': [],
        'TEMPLATE_FILES': []
    },
    'aiohttp_jinja2': {
        'TEMPLATE_DIRS': [
            'src/prozorro_sale/{underscore_project_name}/api/static',
            'src/prozorro_sale/{underscore_project_name}/api/templates'
        ],
        'TEMPLATE_FILES': []
    },
    'setup_py': {
        'TEMPLATE_DIRS': [
        ],
        'TEMPLATE_FILES': [
            'setup.py'
        ]
    },
    'gitlab_ci': {
        'TEMPLATE_DIRS': [
        ],
        'TEMPLATE_FILES': [
            '.gitlab-ci.yml'
        ]
    },
    'docker': {
        'TEMPLATE_DIRS': [
        ],
        'TEMPLATE_FILES': [
            'Dockerfile',
            'docker-compose.yml',
            '.dockerignore'
        ]
    },
    'helm': {
        'TEMPLATE_DIRS': [
            'helm'
        ],
        'TEMPLATE_FILES': [
        ]
    },
    'helm_demo': {
        'TEMPLATE_DIRS': [
        ],
        'TEMPLATE_FILES': [
            'demo-k8s.yaml'
        ]
    },
    'sphinx': {
        'TEMPLATE_DIRS': [
            'docs'
        ],
        'TEMPLATE_FILES': [
            'requirements/documentation.txt'
        ]
    }
}
