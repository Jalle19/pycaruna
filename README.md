﻿# pycaruna

Basic Python implementation for interfacing with Caruna's API. It supports only basic methods, 
but enough to extract electricity usage data for further processing.

Supported features:

* Get user profile information
* Get metering points
* Get consumption data (daily/hourly, optioanlly divided by tariffs)

## Usage

```python
import json
from datetime import date, datetime
from pycaruna import Caruna, Resolution

if __name__ == '__main__':
    caruna = Caruna('you@example.com', 'password')
    caruna.login()

    customer = caruna.get_user_profile()
    metering_points = caruna.get_metering_points(customer['username'])

    end_time = datetime.combine(date.today(), datetime.min.time()).astimezone().isoformat()
    start_time = datetime.combine(date.today().replace(day=1), datetime.min.time()).astimezone().isoformat()
    metering_point = metering_points[0]['meteringPoint']['meteringPointNumber']

    consumption = caruna.get_consumption(customer['username'],
                                         metering_points[0]['meteringPoint']['meteringPointNumber'],
                                         Resolution.DAYS, True,
                                         start_time, end_time)
    print(json.dumps(consumption))
```

The resources directory has examples of API response structures

## Credits

https://github.com/kimmolinna/pycaruna

## License

TODO
