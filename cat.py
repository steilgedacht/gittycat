from datetime import datetime, timezone
import json
import os


class Cat:
    def __init__(self, name: str,
                 max_food=100.0,
                 food_gain_modifier=10.0,
                 food_drain_modifier=100.0,
                 max_energy=100.0,
                 energy_gain_modifier=100.0,
                 energy_drain_modifier=5.0,
                 max_excitement=100.0,
                 excitement_gain_modifier=5.0,
                 excitement_drain_modifier=100.0,
                 evolution_thresholds=None,
                 look='cat1'
                 ):
        """
        :param name: Name of the cat. Purely cosmetic
        :param max_food: Maximum value of the food meter
        :param food_gain_modifier: Food gained per commit
        :param food_drain_modifier: Food lost per day
        :param max_energy: Maximum value of the energy meter
        :param energy_gain_modifier: Energy gained per day
        :param energy_drain_modifier: Energy lost per file touched
        :param max_excitement: Maximum value of the excitement meter
        :param excitement_gain_modifier: Excitement gained per line added
        :param excitement_drain_modifier: Excitement lost per day
        :param evolution_thresholds: List of thresholds for the cat to evolve. If None, the cat will always stay at evolution stage 0
        """
        self.name = name
        self.look = look

        self.max_food = max_food
        self.food_gain_modifier = food_gain_modifier
        self.food_drain_modifier = food_drain_modifier
        self.food = self.max_food

        self.max_energy = max_energy
        self.energy_gain_modifier = energy_gain_modifier
        self.energy_drain_modifier = energy_drain_modifier
        self.energy = self.max_energy

        self.max_excitement = max_excitement
        self.excitement_gain_modifier = excitement_gain_modifier
        self.excitement_drain_modifier = excitement_drain_modifier
        self.excitement = self.max_excitement

        self.evolution_thresholds = evolution_thresholds if evolution_thresholds is not None else []
        self.evolution = 0.0

        self.last_update = datetime.now(timezone.utc)

    def pet(self):
        """A manual way to increase cat excitement. Besides, who doesn't like petting cats?"""
        self.excitement = min(self.excitement + self.excitement_gain_modifier, self.max_excitement)

    def nap(self):
        """A manual way to increase cat energy"""
        self.energy = min(self.energy + self.energy_gain_modifier, self.max_energy)

    def update_by_time_passed(self, days: float) -> bool:
        """
        Updates the cat needs by the given amount of days.
        :param days: a float representing the amount of days that passed since the last update
        :return: True if cat reached new evolution stage, False otherwise
        """
        self.hunger(days)
        self.bore(days)
        self.recharge(days)
        prev_stage = self.get_evolution_stage()
        self.evolve(days)
        new_stage = self.get_evolution_stage()
        return prev_stage != new_stage

    def feed(self, amount: float):
        self.food = min(self.food + amount * self.food_gain_modifier, self.max_food)

    def hunger(self, days: float):
        self.food = max(0.0, self.food - days * self.food_drain_modifier)

    def recharge(self, days: float):
        self.energy = min(self.energy + days * self.energy_gain_modifier, self.max_energy)

    def exhaust(self, amount: float):
        self.energy = max(0.0, self.energy - amount * self.energy_drain_modifier)

    def excite(self, amount: float):
        self.excitement = min(self.excitement + amount + self.excitement_gain_modifier, self.max_excitement)

    def bore(self, days: float):
        self.excitement = max(0.0, self.excitement - days * self.excitement_drain_modifier)

    def evolve(self, days: float):
        self.evolution += days

    def get_evolution_stage(self):
        stage = 0
        for threshold in self.evolution_thresholds:
            if self.evolution >= threshold:
                stage += 1
            else:
                break
        return stage

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
                cat.food_gain_modifier = data['food_gain_modifier']
                cat.food_drain_modifier = data['food_drain_modifier']
                cat.food = data['food']

                cat.max_energy = data['max_energy']
                cat.energy_gain_modifier = data['energy_gain_modifier']
                cat.energy_drain_modifier = data['energy_drain_modifier']
                cat.energy = data['energy']

                cat.max_excitement = data['max_excitement']
                cat.excitement_gain_modifier = data['excitement_gain_modifier']
                cat.excitement_drain_modifier = data['excitement_drain_modifier']
                cat.excitement = data['excitement']

                cat.evolution_thresholds = data['evolution_thresholds']
                cat.evolution = data['evolution']

                cat.last_update = datetime.fromtimestamp(data['last_update'], timezone.utc)
                return cat
        except FileNotFoundError:
            raise FileNotFoundError(f'No cat with name {name} found!')

    @staticmethod
    def create_with_personality(name: str, personality: str):
        """Intializes a new cat with the given name and personality"""
        if not os.path.isdir(os.path.join('.gittycat', 'cats')):
            raise FileNotFoundError('.gittycat folder missing or corrupted!')
        dirname = os.path.dirname(__file__)
        # personality is saved in a json file relative to the gittycat installation
        with open(os.path.join(dirname, 'personalities', f'{personality}.json'), 'r') as infile:
            data = json.load(infile)
            cat = Cat(name)
            cat.look = data['look']

            cat.max_food = data['max_food']
            cat.food_gain_modifier = data['food_gain_modifier']
            cat.food_drain_modifier = data['food_drain_modifier']
            cat.food = cat.max_food

            cat.max_energy = data['max_energy']
            cat.energy_gain_modifier = data['energy_gain_modifier']
            cat.energy_drain_modifier = data['energy_drain_modifier']
            cat.energy = cat.max_energy

            cat.max_excitement = data['max_excitement']
            cat.excitement_gain_modifier = data['excitement_gain_modifier']
            cat.excitement_drain_modifier = data['excitement_drain_modifier']
            cat.excitement = cat.max_excitement

            cat.evolution_thresholds = data['evolution_thresholds']
            cat.evolution = 0.0
            return cat

    def save(self):
        """Saves the cat into the corresponding json file"""
        if not os.path.isdir(os.path.join('.gittycat', 'cats')):
            raise FileNotFoundError('.gittycat folder missing or corrupted!')
        with open(os.path.join('.gittycat', 'cats', f'{self.name}.json'), 'w') as outfile:
            data = {
                'name': self.name,
                'look': self.look,

                'max_food': self.max_food,
                'food_gain_modifier': self.food_gain_modifier,
                'food_drain_modifier': self.food_drain_modifier,
                'food': self.food,

                'max_energy': self.max_energy,
                'energy_gain_modifier': self.energy_gain_modifier,
                'energy_drain_modifier': self.energy_drain_modifier,
                'energy': self.energy,

                'max_excitement': self.max_excitement,
                'excitement_gain_modifier': self.excitement_gain_modifier,
                'excitement_drain_modifier': self.excitement_drain_modifier,
                'excitement': self.excitement,

                'evolution_thresholds': self.evolution_thresholds,
                'evolution': self.evolution,

                'last_update': self.last_update.timestamp()
            }
            json.dump(data, outfile, indent=2)
    
    def ascii_plot(self, state):
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ascii", self.look, "0", state + ".txt")

        with open(path, 'r') as file:
            content = file.read()
            print(content)
        