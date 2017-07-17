from ability import Ability
from bolt import Bolt
from block import Block
from bind import Bind
from imbue import Imbue
from invoke import Invoke
from ray import Ray
from shatter import Shatter
from summon import Summon


def new_block_ability(inventory):

    return Block(inventory)


def new_bolt_ability(inventory):

    return Bolt(inventory)


def new_bind_ability(inventory):

    return Bind(inventory)


def new_imbue_ability(inventory):

    return Imbue(inventory)


def new_invoke_ability(inventory):

    return Invoke(inventory)


def new_ray_ability(inventory):

    return Ray(inventory)


def new_shatter_ability(inventory):

    return Shatter(inventory)


def new_summon_ability(inventory):

    return Summon(inventory)


ability_dict = {
    'bolt': new_bolt_ability,
    'block': new_block_ability,
    'bind': new_bind_ability,
    'imbue': new_imbue_ability,
    'invoke': new_invoke_ability,
    'ray': new_ray_ability,
    'summon': new_summon_ability,
    'shatter': new_shatter_ability
}


def new_ability(ability_id, inventory):

    if ability_dict.get(ability_id) is not None:
        return ability_dict[ability_id](inventory)

    return Ability(ability_id, inventory)
