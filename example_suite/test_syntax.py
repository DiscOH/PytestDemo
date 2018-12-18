# minimum test syntax
# file name starts with "test"
# function name starts with "test"
def test_asdf():
    pass

# function name does not start with test
# Pytest does not recognize function as a test
def not_at_test():
    assert True

