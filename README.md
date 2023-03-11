# pycaruna

Basic Python implementation for interfacing with Caruna Plus (sometimes called _Caruna+_). It supports only basic 
methods, but enough to extract electricity usage data for further processing.

Supported features:

* Get user profile information
* Get metering points ("assets")
* Get consumption data (daily/hourly)

## Usage

> TODO: Publish to PyPI

You can use this package by adding the following to your `requirements.txt` (verify that the commit is pointing at a 
fresh revision, the example here may not be up-to-date):

```
git+https://github.com/Jalle19/pycaruna.git@51d3ee12429d68592640cb146ead71541bf14944#egg=pycaruna==1.0.0
```

The `examples/` directory has example Python programs illustrating how to use the library.

The `resources/` directory has examples of API response structures.

Please note that the authentication procedure requires a lot of HTTP requests to be sent back and forth, so the 
script is relatively slow. It's best to store the token produced by it and reusing that instead of doing the 
authentication process all over again.

## Credits

https://github.com/kimmolinna/pycaruna

## License

MIT
