from ability import Ability
from bolt import Bolt


def new_bolt_ability(inventory):

    return Bolt(inventory)


ability_dict = {
    'bolt': new_bolt_ability
}


def new_ability(ability_id, inventory):

    if ability_dict.get(ability_id) is not None:
        return ability_dict[ability_id](inventory)

    return Ability(ability_id, inventory)
