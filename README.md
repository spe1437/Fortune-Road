# Fortune-Road
Fortune Road is a terminal-based Monopoly-inspired board game written in Python.  Players move around a board, buy properties, pay rent, upgrade lands, trigger chance card events, and compete to become the wealthiest player.

## Features

- Multiple player support
- Fixed-round mode
- Endless game mode
- Random board generation
- File-based custom board loading
- Input validation for menu choices
- Property purchasing system
- Property upgrade system
- Property trading system
- Debt and bankruptcy system
- Chance card events
- Dynamic board display
- Cash summary system
- Start tile reward system

## How to Run

Run the following command in the terminal:

```bash
python3 main.py
```
## File Structure

main.py              Main program entry point  
game.py              Core gameplay logic  
board.py             Board generation and display system  
player.py            Player class and player-related operations  
property.py          Property system and upgrade mechanics  
chance.py            Chance card event system  
menu.py              Menu interface system  
rules.py             Rule display system  

data/  
│── board.txt              Custom board layout  
│── chance_cards.txt       Chance card data  
│── rules.txt              Game rules

## Game Rules

- Players take turns rolling a dice to move around the board.
- Passing the Start tile rewards the player with $1000.
- Landing exactly on the Start tile does not provide money.
- Players may purchase unowned properties.
- Landing on another player's property requires rent payment.
- Players may upgrade their own properties to increase rent value.
- Chance tiles trigger random events.
- Players with negative money enter debt status and must sell properties or declare bankruptcy.
- When landing on another player's property, players may offer to purchase the property from the owner.
- The game ends when:
  - all rounds are completed in fixed-round mode,
  - all players agree to end the game, or
  - only one player remains active.

## Future Improvements

Possible future improvements include:

- Computer-controlled players
- Save and load game system
- More advanced chance card events
- Property auction system
- Graphical user interface (GUI)
- Online multiplayer support
