import enum
import attr
from excelcy.registry import Registry, field
from tests.test_base import BaseTestCase


@attr.s()
class Params1(Registry):
    f1: int = field()


class Params2(Registry):
    f1: int = field(0)


@attr.s()
class Params3(Registry):
    f1: int = field(0)


def validate_f3(instance, attribute, value):
    if value is None:
        raise ValueError('None is not accepted')


@attr.s()
class Params4(Registry):
    class TestState(enum.Enum):
        S1 = 's1'
        S2 = 's2'

    f1: int = field(validator=[attr.validators.instance_of(int)])
    f2 = field(validator=[attr.validators.in_(TestState)])
    f3 = field(validator=[validate_f3])


@attr.s()
class Params6(Registry):
    f1: int = field(0)


class RegistryTestCase(BaseTestCase):
    def test_create_params(self):
        # test required fields
        self.assertRaises(TypeError, Params1)
        # test missing attr.s
        self.assertRaises(TypeError, Params2)
        # test field assignment and remove all non field attr
        items = {'f1': 1}
        params = Params3()
        params.f1 = 1
        params.f2 = 2
        self.assertDictEqual(params.items(), items)
        # test init
        params = Params3(f1=1)
        self.assertDictEqual(params.items(), items)
        # test init 2
        params = Params3(**items)
        self.assertDictEqual(params.items(), items)
        # test extends
        params = Params3()
        params.extend(items)
        self.assertDictEqual(params.items(), items)

    def test_validator_params(self):
        # test basic validator
        items = {'f1': 1, 'f2': Params4.TestState.S1, 'f3': 'A'}
        params = Params4(**items)
        params.f1 = 'a'
        self.assertRaises(TypeError, params.validate)
        # test enum validator
        params = Params4(**items)
        params.f2 = 'S3'
        self.assertRaises(ValueError, params.validate)
        # test fn validator
        params = Params4(**items)
        params.f3 = None
        self.assertRaises(ValueError, params.validate)

    def test_exception(self):
        def test5a():
            TestParams5a = attr.make_class('TestParams5a', {'f1': field(0), 'f2': field()})
            return TestParams5a

        def test5b():
            @attr.s()
            class TestParams5b(Registry):
                f1: int = field(0)
                # this is not allowed
                f2: int = field()

            return TestParams5b

        # test required param after default param
        self.assertRaises(ValueError, test5a)
        self.assertRaises(ValueError, test5b)