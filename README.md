
<pre>
  _____             _   _                  _______
 |  __ \           | | (_)                |__   __|
 | |__) |   _ _ __ | |_ _ _ __ ___   ___     | | ___ _ __ _ __ ___  _ __
 |  _  / | | | '_ \| __| | '_ ` _ \ / _ \    | |/ _ \ '__| '__/ _ \| '__|
 | | \ \ |_| | | | | |_| | | | | | |  __/    | |  __/ |  | | | (_) | |
 |_|  \_\__,_|_| |_|\__|_|_| |_| |_|\___|    |_|\___|_|  |_|  \___/|_|

</pre>

[![Build Status](https://github.com/NYU-DevOps-2022/orders/actions/workflows/tdd.yml/badge.svg)](https://github.com/NYU-DevOps-2022/orders/actions)


## Contents

The project contains the following:

```text
.coveragerc         - settings file for code coverage options
.devcontainers      - support for VSCode Remote Containers
.gitignore          - this will ignore vagrant and other metadata files
dot-env-example     - copy to .env to use environment variables
requirements.txt    - list if Python libraries required by your code
config.py           - configuration parameters

service/                - service python package
├── __init__.py         - package initializer
├── error_handlers.py   - HTTP error handling code
├── models.py           - module with business models
├── routes.py           - module with service routes
└── status.py           - HTTP status constants

tests/              - test cases package
├── __init__.py     - package initializer
├── test_models.py  - test suite for busines models
└── test_routes.py  - test suite for service routes

Vagrantfile         - sample Vagrant file that installs Python 3 and PostgreSQL
```

This repository is part of the NYU class **CSCI-GA.2810-001: DevOps and Agile Methodologies** taught by John Rofrano, Adjunct Instructor, NYU Courant Institute, Graduate Division, Computer Science.
