# pycaruna

Basic Python implementation for interfacing with Caruna Plus (sometimes called _Caruna+_). It supports only basic 
methods, but enough to extract electricity usage data for further processing.

Supported features:

* Get user profile information
* Get metering points ("assets")
* Get consumption data (daily/hourly)

## Usage

> TODO: Publish to PyPI

You can use this package by adding the following to your `requirements.txt`:

```
pycaruna @ git+https://github.com/Jalle19/pycaruna
```

The `examples/` directory has example Python programs illustrating how to use the library.

The `resources/` directory has examples of API response structures.

## Caveats

* During daylight savings time changes, the API may return a duplicate datapoint (same timestamp in two consecutive 
  data points). See https://github.com/Jalle19/pycaruna/issues/7 for more details.
* The authentication procedure requires a lot of HTTP requests to be sent back and forth, so the process is 
  relatively slow. It's best to store and reuse the token produced by it instead of doing the authentication 
  process all over again all the time.

## Related projects

* [caruna-influxdb](https://github.com/Jalle19/caruna-influxdb) - a collection of scripts for ingesting your Caruna data 
into InfluxDB

## Credits

https://github.com/kimmolinna/pycaruna

## License

MIT
