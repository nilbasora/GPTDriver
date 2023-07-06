from setuptools import find_packages, setup

setup(
    name='GPTDriver',
    packages=find_packages(include=['GPTDriver']),
    version='0.1.0',
    description='Selenium Driver to Control ChatGPT from Command Lines',
    author='Nil Basora',
    author_email="nilbasora@gmail.com",
    url="https://github.com/nilbasora/GPTDriver",
    keywords=['GPT', 'OpenAI', 'ChatGPT', 'Selenium', 'Driver'],
    license='MIT',
    install_requires=['undetected-chromedriver==3.5.0',
                      'selenium==4.10.0'],
    classifiers=[
        'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Intended Audience :: Developers',      # Define that your audience are developers
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',   # Again, pick a license
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11'
  ],
    setup_requires=['pytest-runner'],
    tests_require=['pytest==7.4.0'],
    test_suite='tests',
)
