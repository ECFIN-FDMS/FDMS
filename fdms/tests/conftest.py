def pytest_addoption(parser):
    parser.addoption("--country", action="store", default="default country")


def pytest_generate_tests(metafunc):
    # This is called for every test. Only get/set command line arguments
    # if the argument is specified in the list of test "fixturecountrys".
    option_value = metafunc.config.option.country
    if 'country' in metafunc.fixturecountrys and option_value is not None:
        metafunc.parametrize("country", [option_value])