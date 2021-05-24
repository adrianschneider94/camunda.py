from setuptools import find_packages, setup

setup(
    name='camunda',
    version='0.0.1',
    packages=find_packages("src"),
    package_dir={
        'camunda': "./src/camunda",
    },
    url='',
    license='',
    author='Adrian Schneider',
    author_email='adrian.schneider@sangl.com',
    description='',
    install_requires=['requests', 'pydantic'],
    extras_require={
        'dev': [
            'jsonpatch',
            'datamodel-code-generator',
            'lxml'
        ]
    }

)
