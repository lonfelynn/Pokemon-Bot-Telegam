import datetime
from random import randint
import requests

class Pokemon:
    pokemons = {}
    # Инициализация объекта (конструктор)
    def __init__(self, pokemon_trainer):

        self.pokemon_trainer = pokemon_trainer   

        self.pokemon_number = randint(1,1000)
        self.level = randint(1, 50)
        self.hp = randint(1, 50)
        self.power = randint(1, 50)

        self.types = self.get_types()
        self.img = self.get_img()
        self.name = self.get_name()

        Pokemon.pokemons[pokemon_trainer] = self

    # Метод для получения картинки покемона через API

    def attack(self, enemy):
        if isinstance(enemy, Wizard): # Проверка на то, что enemy является типом данных Wizard (является экземпляром класса Волшебник)
            chance = randint(1,5)
            if chance == 1:
                return "Покемон-волшебник применил щит в сражении"
        if enemy.hp > self.power:
            enemy.hp -= self.power
            return f"Сражение @{self.pokemon_trainer} с @{enemy.pokemon_trainer}"
        else:
            enemy.hp = 0
            self.hp += 3
            self.power += 3
            return f"Победа @{self.pokemon_trainer} над @{enemy.pokemon_trainer}!"
            

    def get_img(self):
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return (data['sprites']['other']['official-artwork']['front_default'])
        else:
            return "Pikachu"
    
    # Метод для получения имени покемона через API
    def get_name(self):
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return (data['forms'][0]['name'])
        else:
            return "Pikachu"
        
    def get_types(self):
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            types_list = []
            for t in data['types']:
                types_list.append(t['type']['name'])
            return types_list


    # Метод класса для получения информации
    def info(self):
        return (
            f"📛 Имя покемона: {self.name}\n"
            f"📊 Уровень: {self.level}\n"
            f"🔥 Тип: {self.get_types()}\n"
            f"❤️ Здоровье: {self.hp}\n"
            f"💪 Сила: {self.power}\n"
        )

    # Метод класса для получения картинки покемона
    def show_img(self):
        return self.img
    
    def heal(self):
        heal_points = randint(10, 30)
        self.hp += heal_points
        return f"{self.name} восстановил {heal_points} HP. Теперь у него {self.hp} HP!"
    

    def feed(self, feed_interval = 20, hp_increase = 10 ):
        current_time = datetime.now()  
        delta_time = datetime.timedelta(hours=feed_interval)  
        if (current_time - self.last_feed_time) > delta_time:
            self.hp += hp_increase
            self.last_feed_time = current_time
            return f"Здоровье покемона увеличено. Текущее здоровье: {self.hp}"
        else:
            return f"Следующее время кормления покемона: {self.last_feed_time + delta_time}"
    

class Wizard(Pokemon):

    hp = randint(35, 80)
    power = randint(1, 15)
    last_feed_time = datetime.now() - datetime.timedelta(hours=21)

    def attack(self, enemy):
        return super().attack(enemy)
    
    def info(self):
        return ("У тебя покемон-волшебник\n" + super().info())
    
    def feed(self, feed_interval = 20, hp_increase = 20 ):
        current_time = datetime.now()  
        delta_time = datetime.timedelta(hours=feed_interval)  
        if (current_time - self.last_feed_time) > delta_time:
            self.hp += hp_increase
            self.last_feed_time = current_time
            return f"Здоровье покемона увеличено. Текущее здоровье: {self.hp}"
        else:
            return f"Следующее время кормления покемона: {self.last_feed_time + delta_time}"

    

class Fighter(Pokemon):

    hp = randint(1, 40)
    power = randint(15, 35)
    last_feed_time = datetime.now() - datetime.timedelta(hours=21)

    def attack(self, enemy):
        self.superpower = randint(5,15)
        self.power += self.superpower
        result = super().attack(enemy)
        self.power -= self.superpower
        return result + f"\nБоец применил супер-атаку силой:{self.superpower} "
    
    def info(self):
        return ("У тебя покемон-боец\n" + super().info())
    
    def feed(self, feed_interval = 20, hp_increase = 10 ):
        current_time = datetime.now()  
        delta_time = datetime.timedelta(hours=feed_interval)  
        if (current_time - self.last_feed_time) > delta_time:
            self.hp += hp_increase
            self.last_feed_time = current_time
            return f"Здоровье покемона увеличено. Текущее здоровье: {self.hp}"
        else:
            return f"Следующее время кормления покемона: {self.last_feed_time + delta_time}"

        




