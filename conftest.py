# the highest level conftest file in a project determines the starting point of your pytest suite
# all fixtures are visible to all lower level test files
# multiple conftest files can exist in a directory.
# lower level conftest files are applied after higher level ones

import pytest


@pytest.fixture()
def teardown_example():
    a = 1
    yield a
    print(a)


# scope:
# session = entire pytest run
# module = 1 pytest file
# function = as name implies.  1 function
# class = as name implies.  1 class
#autouse:
# every test in the session will call the fixture automatically
@pytest.fixture(scope='session', autouse=False)
def fixture_example():
    print('this is only called once per run because its scope is "session"')


# any test that invokes this fixture will be run 5 times.  The tests will be reported with the names, "apple", "ball", "car", "dice", "elephant"
@pytest.fixture(params=[1, 2, 3, 4, 5], ids=['apple', 'ball', 'car', 'dice', 'elephant'])
def param_example(request):
    return request.param


