import pytest


def pytest_addoption(parser):
    parser.addoption("--country", action="store", default="BE")


@pytest.fixture(scope='class')
def country(request):
    import code;code.interact(local=locals())
    request.cls.country = request.config.getoption("--country")
