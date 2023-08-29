from selenium import webdriver
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
@pytest.fixture(autouse=True)
def testing():
   pytest.driver = webdriver.Firefox()
   pytest.driver.get('http://petfriends.skillfactory.ru/login')
   yield pytest.driver
   pytest.driver.quit()

def test_show_my_pets(testing):
   # Установка явного ожидания
   element = WebDriverWait(pytest.driver, 10).until(
      EC.presence_of_element_located((By.ID, "email"))
   )
   # Вводим email
   pytest.driver.find_element(By.ID, "email").send_keys('aelita-yunusova@yandex.ru')
   # Установка явного ожидания
   element = WebDriverWait(pytest.driver, 10).until(
      EC.presence_of_element_located((By.ID, "pass"))
   )
   # Вводим пароль
   pytest.driver.find_element(By.ID, "pass").send_keys('Tel9031042154')
   # Установка явного ожидания, что кнопка входа в аккаунт кликабельна
   element = WebDriverWait(pytest.driver, 10).until(
      EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
   )
   # Нажимаем на кнопку входа в аккаунт
   pytest.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
   # Установка неявного ожидания
   myDynamicElement = pytest.driver.find_element(By.TAG_NAME, "h1").text == "PetFriends"
   # Проверяем, что мы оказались на главной странице
   assert pytest.driver.find_element(By.TAG_NAME, 'h1').text == "PetFriends"
   # Установка явного ожидания, что кнопка Мои питомцы кликабельна
   WebDriverWait(pytest.driver, 10).until(
      EC.element_to_be_clickable((By.CSS_SELECTOR, "#navbarNav > ul > li:nth-child(1) > a"))
   )
   # Нажимаем на кнопку мои питомцы
   pytest.driver.find_element(By.CSS_SELECTOR, "#navbarNav > ul > li:nth-child(1) > a").click()
   # список img элементов
   images = pytest.driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr/th')
   # список имен питомцев
   names = pytest.driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr/td[1]')
   animal_types = pytest.driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr/td[2]')
   ages = pytest.driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr/td[3]')
   # список всех объектов животных
   all_pets = pytest.driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr/td')


   for i in range(len(names)):
      assert names[i].text != ''
      assert animal_types[i].text != ''
      assert ages[i].text != ''
      assert all_pets[i] != ''

   # Проверяем, что присутствуют все питомцы
   count = pytest.driver.find_element(By.CLASS_NAME, "task3").text.split("\n")[1].split(" ")[-1]
   assert int(count) == len(names)

   # Проверяем, что хотя бы у половины питомцев есть фото.
   fotos = 0
   for i in range(len(images)):
      if images[i].get_attribute('scr') != '':
         fotos += 1
   assert fotos >= int(count)//2

   # Проверяем, что у всех питомцев разные имена
   n = 0
   for i in range(len(names)):
      if names.count(names[i]) > 1:
         n += 1
   assert n == 0

   # Проверяем, что у всех питомцев есть имя, возраст и порода
   assert len(names) == len(ages) == len(animal_types)

   # Проверяем, что в списке нет повторяющихся питомцев
   k = 0
   for i in range(len(all_pets)):
      if all_pets.count(all_pets[i]) > 1:
         k += 1
   assert k == 0









