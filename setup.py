"""
GitHub release signing tool
"""
from setuptools import find_packages, setup

dependencies = ['click', 'python-gnupg', 'github3.py', 'six']

setup(
    name='ballsy',
    version='0.1.0',
    url='https://github.com/satta/ballsy',
    license='BSD',
    author='Sascha Steinbiss',
    author_email='sascha@steinbiss.name',
    description='GitHub release signing tool',
    long_description=__doc__,
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    install_requires=dependencies,
    entry_points="""
        [console_scripts]
        ballsy=ballsy.cli:main
    """,
    classifiers=[
        'Development Status :: 4 - Beta',
        # 'Development Status :: 5 - Production/Stable',
        # 'Development Status :: 6 - Mature',
        # 'Development Status :: 7 - Inactive',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX',
        'Operating System :: MacOS',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
    ]
)
