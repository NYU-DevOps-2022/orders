
<pre>
  _____             _   _                  _______
 |  __ \           | | (_)                |__   __|
 | |__) |   _ _ __ | |_ _ _ __ ___   ___     | | ___ _ __ _ __ ___  _ __
 |  _  / | | | '_ \| __| | '_ ` _ \ / _ \    | |/ _ \ '__| '__/ _ \| '__|
 | | \ \ |_| | | | | |_| | | | | | |  __/    | |  __/ |  | | | (_) | |
 |_|  \_\__,_|_| |_|\__|_|_| |_| |_|\___|    |_|\___|_|  |_|  \___/|_|

</pre>

[![Build Status](https://github.com/NYU-DevOps-2022/orders/actions/workflows/tdd.yml/badge.svg)](https://github.com/NYU-DevOps-2022/orders/actions)

[![codecov](https://codecov.io/gh/NYU-DevOps-2022/orders/branch/main/graph/badge.svg?token=PTK7NZM3ZT)](https://codecov.io/gh/NYU-DevOps-2022/orders)

## Tests

First run `honcho run`

Then in a new terminal window run `nosetests` for unit tests or `behave` for Behave test.


## Cloud URLs:
* [Dev - Frontend](https://devops-orders.us-south.cf.appdomain.cloud)
* [Dev - Swagger Doc](https://devops-orders.us-south.cf.appdomain.cloud/apidocs)
* [Prod - Frontend](https://prod-orders.us-south.cf.appdomain.cloud)
* [Prod - Swagger Doc](https://prod-orders.us-south.cf.appdomain.cloud/apidocs)

## IBM Cloud Commands

```
ibmcloud login --apikey @~/.bluemix/apikey.json -r us-south
ibmcloud target -o {org_name} -s {environment}
ibmcloud cf logs {app_name} --recent
ibmcloud cf apps
ibmcloud cf services

```