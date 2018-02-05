
# Development Notes

## Requirements and Dependencies

Development of Tarski currently happens under Python 3.

## Code Style

We aim at following the [PEP 8 Python Style Guide](https://www.python.org/dev/peps/pep-0008/).
Many Python IDEs support on-the-fly PEP 8 style checks, and there are also external tools
to help the code comply with the style guidelines, such as [Google's YAPF](https://github.com/google/yapf).
We might consider using one of these down the road.


## Project Structure
We follow a [`src`-based](https://blog.ionelmc.ro/2014/05/25/python-packaging/) project structure.

## Testing
Tests are written using `pytest` and can be run by issuing `pytest` on the project root directory,
provided that the `pytest` module has been installed.


### Running the test from a virtual environment
We can run the tests from a virtual environment where the necessary dependencies have been
installed first:

```
virtualenv -p python3 venv
source venv/bin/activate
pip install pytest scipy tox detox
```

Once this has been done, running `pytest` will work the same, but we avoid the need for
doing a system-wide installation of all the project dependencies. This can be automated by using
[tox](https://tox.readthedocs.io/en/latest/) & [detox](https://pypi.python.org/pypi/detox): if you have it installed, you can run all tests by simply
running `detox` on the project root directory