import pytest
from add_number import add_numbers, wether_request

def test_add_numbers():
    assert add_numbers(3, 5) == 8
    assert add_numbers(-2, -3) == -5
    assert add_numbers(5, -3) == 2
    assert add_numbers(0, 7) == 7
    assert add_numbers(10, 0) == 10

def test_add_numbers_just_num():
    with pytest.raises(TypeError):
        assert add_numbers("g", 0)
    with pytest.raises(TypeError):
        assert add_numbers(12, "d")
    with pytest.raises(TypeError):
        assert add_numbers("g", "k")

if __name__ == "__main__":
    test_add_numbers()
    test_add_numbers_just_num()
    print("Всі тести пройдено успішно!")


def test_wether_request():
    assert wether_request("lviv")
    assert wether_request("odesa")
def test_wether_request_not_city():
    with pytest.raises(ValueError):
        assert wether_request("")
def test_wether_request_not_correct_city():
    with pytest.raises(TypeError):
        assert wether_request(586)

if __name__ == "__main__":
    test_wether_request()
    test_wether_request_not_city()
    test_wether_request_not_correct_city()
    print("Всі тести пройдено успішно!")
