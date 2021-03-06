# -*- coding: utf-8 -*-
try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

setup(
    name='tagger',
    version='0.1',
    description='A personal website and blog management system',
    author='Lorenzo Pierfederici',
    author_email='lpierfederici@gmail.com',
    url='http://lorenzopierfederici.net/software/tagger',
    install_requires=[
        "TurboGears2 >= 2.1b2",
        "Babel >=0.9.4",
        "zope.sqlalchemy >= 0.4 ",
        "repoze.tm2 >= 1.0a4",
        "sqlalchemy >= 0.6.0",        
        "repoze.what-quickstart >= 1.0",
        "tw.dynforms",
        "docutils",
        "MySQL-python",
                ],
    setup_requires=["PasteScript >= 1.7"],
    paster_plugins=['PasteScript', 'Pylons', 'TurboGears2', 'tg.devtools'],
    packages=find_packages(exclude=['ez_setup']),
    include_package_data=True,
    test_suite='nose.collector',
    tests_require=['WebTest', 'BeautifulSoup'],
    package_data={'tagger': ['i18n/*/LC_MESSAGES/*.mo',
                                 'templates/*/*',
                                 'public/*/*']},
    message_extractors={'tagger': [
            ('**.py', 'python', None),
            ('templates/**.mak', 'mako', None),
            ('templates/**.html', 'genshi', None),
            ('public/**', 'ignore', None)]},

    entry_points="""
    [paste.app_factory]
    main = tagger.config.middleware:make_app

    [paste.app_install]
    main = pylons.util:PylonsInstaller
    """,
)
