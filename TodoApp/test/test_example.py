import pytest

def test_equal_or_not_equal():
    assert 3 == 3
    assert 3 != 1

def test_is_instance():
    # isinstance checks whether an obj or item is of a class
    assert isinstance('this is a string', str)
    assert not isinstance('10', int)

def test_boolean():
    validated = True 
    assert validated is True
    assert ('hello' == 'world') is False

def test_type():
    assert type('hello' is str)
    assert type('world' is not int)

def test_greater_and_less_than():
    assert 7 >  3
    assert 4 < 10

def test_list():
    num_list = [1,2,3,4,5]
    any_list = [False, False]

    assert 1 in num_list
    assert 7 not in num_list
    assert all(num_list)
    assert not any(any_list)


# old way is to instantiate an object new way is to use fixtures
class Student:
    def __init__(self, first_name: str, last_name: str, major: str, years: int):
        self.first_name = first_name
        self.last_name = last_name
        self.major = major
        self.years = years

# using fixtures
@pytest.fixture
def defualt_employee():
    return Student('John', 'Doe', 'Computer Science', 3)
    
def test_person_initlization(defualt_employee):
    # p = Student('John', 'Doe', 'Computer Science', 3)
    assert defualt_employee.first_name == 'John', 'First name should be John'
    assert defualt_employee.last_name == 'Doe', 'Last name should be Doe'
    assert defualt_employee.major == 'Computer Science'
    assert defualt_employee.years == 3


