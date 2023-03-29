Daniele Andrean PhD student @DEI 
supervisor: prof. Morten Gram Pedersen

Run the main.py file to test the program.

The game engine is a Finite State Machine, the entry state is the character creation in which the user is asked to provide its name
and select a starter pokemon.
Once the pokemon trainer is created, the FSM passes to the main menu (Story) state from which all the available operations are accessible.

Every user input is checked for expected format and value, in case the input is wrong the user is asked to try and insert again the 
correct value. 