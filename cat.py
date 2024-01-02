from datetime import datetime, timezone
import json
import os


class Cat:
    def __init__(self, name: str, max_food=100.0, max_energy=100.0, max_excitement=100.0):
        self.name = name
        self.max_food = max_food
        self.max_energy = max_energy
        self.max_excitement = max_excitement

        self.food = self.max_food
        self.energy = self.max_energy
        self.excitement = self.max_excitement

        self.last_update = datetime.now(timezone.utc)

    def pet(self):
        # TODO
        pass

    def feed(self, amount: float):
        self.food = min(self.food + amount, self.max_food)

    def hunger(self, amount: float):
        self.food = max(0.0, self.food - amount)

    def recharge(self, amount: float):
        self.energy = min(self.energy + amount, self.max_energy)

    def exhaust(self, amount: float):
        self.energy = max(0.0, self.energy - amount)

    def excite(self, amount: float):
        self.excitement = min(self.excitement + amount, self.max_excitement)

    def bore(self, amount: float):
        self.excitement = max(0.0, self.excitement - amount)

    @staticmethod
    def load(name: str) -> 'Cat':
        if not os.path.isdir(os.path.join('.gittycat', 'cats')):
            raise FileNotFoundError('.gittycat folder missing or corrupted!')

        try:
            with open(os.path.join('.gittycat', 'cats', f'{name}.json'), 'r') as infile:
                data = json.load(infile)
                cat = Cat(name)
                cat.name = data['name']
                cat.max_food = data['max_food']
                cat.max_energy = data['max_energy']
                cat.max_excitement = data['max_excitement']

                cat.food = data['food']
                cat.energy = data['energy']
                cat.excitement = data['excitement']
                cat.last_update = datetime.fromtimestamp(data['last_update'], timezone.utc)
                return cat
        except FileNotFoundError:
            raise FileNotFoundError(f'No cat with name {name} found!')

    def save(self):
        """Saves the cat into the corresponding json file"""
        if not os.path.isdir(os.path.join('.gittycat', 'cats')):
            raise FileNotFoundError('.gittycat folder missing or corrupted!')
        with open(os.path.join('.gittycat', 'cats', f'{self.name}.json'), 'w') as outfile:
            data = {
                'name': self.name,
                'max_food': self.max_food,
                'max_energy': self.max_energy,
                'max_excitement': self.max_excitement,
                'food': self.food,
                'energy': self.energy,
                'excitement': self.excitement,
                'last_update': self.last_update.timestamp()
            }
            json.dump(data, outfile, indent=2)
