import random
from enum import Enum
from typing import List, Dict, Optional

class Type(Enum):
    NORMAL = "Normal"
    FIRE = "Fire"
    WATER = "Water"
    GRASS = "Grass"
    ELECTRIC = "Electric"
    ICE = "Ice"
    FIGHTING = "Fighting"
    POISON = "Poison"
    GROUND = "Ground"
    FLYING = "Flying"
    PSYCHIC = "Psychic"
    BUG = "Bug"
    ROCK = "Rock"
    GHOST = "Ghost"
    DRAGON = "Dragon"
    DARK = "Dark"
    STEEL = "Steel"
    FAIRY = "Fairy"

class Status(Enum):
    NONE = "None"
    PARALYZED = "Paralyzed"
    BURNED = "Burned"
    POISONED = "Poisoned"
    ASLEEP = "Asleep"
    FROZEN = "Frozen"

class Weather(Enum):
    CLEAR = "Clear"
    RAIN = "Rain"
    SUN = "Sun"
    HAIL = "Hail"
    SANDSTORM = "Sandstorm"

class Move:
    def __init__(self, name: str, type: Type, power: int, accuracy: int, pp: int, 
                 is_physical: bool, status_effect: Optional[Status] = None):
        self.name = name
        self.type = type
        self.power = power
        self.accuracy = accuracy
        self.pp = pp
        self.max_pp = pp
        self.is_physical = is_physical
        self.status_effect = status_effect

class Pokemon:
    def __init__(self, name: str, level: int, types: List[Type], 
                 base_stats: Dict[str, int], moves: List[Move]):
        self.name = name
        self.level = level
        self.types = types
        self.base_stats = base_stats
        self.moves = moves
        self.current_hp = self.calculate_hp()
        self.max_hp = self.current_hp
        self.status = Status.NONE
        self.stat_modifiers = {
            "Attack": 0, "Defense": 0, "SpAttack": 0, "SpDefense": 0, "Speed": 0
        }

    def calculate_hp(self) -> int:
        return int((2 * self.base_stats["HP"] * self.level) / 100) + self.level + 10

    def calculate_stat(self, stat_name: str) -> int:
        base = self.base_stats[stat_name]
        modifier = self.stat_modifiers[stat_name]
        return int((2 * base * self.level) / 100 + 5) * (2 if modifier > 0 else 0.5)

class Battle:
    def __init__(self, player1: str, player2: str):
        self.player1 = player1
        self.player2 = player2
        self.weather = Weather.CLEAR
        self.turn_count = 0
        self.active_pokemon = {player1: None, player2: None}
        self.teams = {player1: [], player2: []}

    def initialize_teams(self, player1_team: List[Pokemon], player2_team: List[Pokemon]):
        self.teams[self.player1] = player1_team
        self.teams[self.player2] = player2_team
        self.active_pokemon[self.player1] = player1_team[0]
        self.active_pokemon[self.player2] = player2_team[0]

    def calculate_damage(self, attacker: Pokemon, defender: Pokemon, move: Move) -> int:
        # Base damage calculation
        level = attacker.level
        power = move.power
        attack = attacker.calculate_stat("Attack" if move.is_physical else "SpAttack")
        defense = defender.calculate_stat("Defense" if move.is_physical else "SpDefense")
        
        base_damage = ((2 * level / 5 + 2) * power * attack / defense) / 50 + 2

        # STAB (Same Type Attack Bonus)
        stab = 1.5 if move.type in attacker.types else 1.0

        # Type effectiveness (simplified for now)
        effectiveness = 1.0  # TODO: Implement type chart

        # Random factor (85-100%)
        random_factor = random.uniform(0.85, 1.0)

        # Weather effects
        weather_multiplier = 1.0
        if self.weather == Weather.SUN and move.type == Type.FIRE:
            weather_multiplier = 1.5
        elif self.weather == Weather.RAIN and move.type == Type.WATER:
            weather_multiplier = 1.5

        final_damage = int(base_damage * stab * effectiveness * random_factor * weather_multiplier)
        return max(1, final_damage)

    def apply_status_effect(self, pokemon: Pokemon, status: Status):
        if pokemon.status == Status.NONE:
            pokemon.status = status
            return True
        return False

    def apply_weather_damage(self, pokemon: Pokemon) -> int:
        if self.weather == Weather.HAIL and Type.ICE not in pokemon.types:
            return int(pokemon.max_hp * 0.0625)
        elif self.weather == Weather.SANDSTORM and not any(t in [Type.ROCK, Type.GROUND, Type.STEEL] for t in pokemon.types):
            return int(pokemon.max_hp * 0.0625)
        return 0

    def switch_pokemon(self, player: str, new_pokemon_index: int) -> bool:
        if 0 <= new_pokemon_index < len(self.teams[player]):
            new_pokemon = self.teams[player][new_pokemon_index]
            if new_pokemon.current_hp > 0:
                self.active_pokemon[player] = new_pokemon
                return True
        return False

    def is_battle_over(self) -> bool:
        for player in [self.player1, self.player2]:
            if all(p.current_hp <= 0 for p in self.teams[player]):
                return True
        return False

    def get_winner(self) -> Optional[str]:
        if all(p.current_hp <= 0 for p in self.teams[self.player1]):
            return self.player2
        elif all(p.current_hp <= 0 for p in self.teams[self.player2]):
            return self.player1
        return None 