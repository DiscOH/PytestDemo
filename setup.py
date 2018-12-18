from setuptools import setup

setup(name='pytest-demo',
      version='0.1',
      description='sample pytest tests and syntax',
      install_requires=[
          'allure-pytest',
          'paramiko',
          'paramiko-expect',
          'pytest',
          'requests',
          'selenium',
      ],
      zip_safe=False)
