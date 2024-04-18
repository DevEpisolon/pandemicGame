import random

class Navi:
    def __init__(self,age, lifespan, health, gender=None):
        self.age = age
        #to vary the lifespan of the navi
        multiplier = random.choice([0.10, 0.20, 0.30, 0.40,.50])
        lifespan = round(multiplier * random.randint(1, 40) + random.randint(1, 40))
        self.health = 100
        self.gender = gender if gender is not None else random.choice(["Male", "Female"])

    def set_age(self, age):
        self.age = age

    def get_age(self):
        return self.age

    def simulate_death(self, death_chance):
        if random.random() < death_chance:
            return True
        else:
            return False


