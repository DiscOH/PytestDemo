import pytest


def test_idk():
    assert False


def test_also_a_test():
    assert 1 == 2//2


# classes with constructors cant be used as test containers
class TestWithConstructor(object):
    def __init__(self):
        pass

    def test_wont_work(self):
        assert False


class TestClassExample(object):
    dog = 'dog'
    backwardsdog = ''.join(['g', 'o', 'd'][::-1])

    def is_it_dog(self, animal):
        return animal == self.dog

    def test_dog(self):
        assert self.is_it_dog(self.backwardsdog)


def test_with_parameters(param_example):
    assert type(param_example) == int


