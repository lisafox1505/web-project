import requests

def add_numbers(a, b):
    if not (isinstance(a, (int, float)) and isinstance(b, (int, float))):
        raise TypeError("Тільки числа!")
    return a + b

def wether_request(city):
  data = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid=e90fab7014064d2c88795d9fd95afa6f")
  data_json = data.json()
  if not city:
      raise ValueError("Введіть назву міста!")
  elif not isinstance(city, str):
      raise TypeError("Місто не знайдено!")
  return data_json
