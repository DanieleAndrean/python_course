from engine.state_machine import *
from pokemon.trainer import Trainer


class CreateCharacter(State):

    def run(self, *args):
        #trainer = Trainer('', [])
        trainer = args[0]
        # name
        print('create your pokemon trainer')
        nickname = input()
        trainer.addName(nickname)
        print('Welcome ' + trainer.name)

        options = ['Bulbasaur', 'Charmender', 'Squirtle']
        print('Chooose one Pokemon among:')
        for i, opt in enumerate(options):
            print(i, ':', opt)
        choice = int(input('Choose option:'))

        pokemon = options[choice]
        trainer.addPokemon(pokemon)

        ## aggiungere items:
        trainer.addFullItems()
        print('added 10 potions and 10 pokeballs!')

    def update(self):
        pass

    def __str__(self):
        return '[State: ' + self.name + ']'

    def __repr__(self):
        return str(self)

# methods

cc = CreateCharacter('Create Character')
