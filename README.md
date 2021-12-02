# Blackjack
 
## Requirements
- Python 3
- Pygame 2.0.1

## Controls
|Function|Button|
|--|--|
|Hit|H|
|Stand|S|
|New Round|N|
|Card Counting|P|

(Please note card counting is only avalable when in a game and new round button only functions once a round is completed)

## Features
- Ajustment of hit/stand threshold for cpu and dealer
- Card counting and probability statistics
- Satsfying card dealing animations
- Hit Stand and Bust indicators
- Betting functionality (If you get blackjack player triples their money all other wins are double)


## Compile

### Install pyInstaller:
	pip install pyinstaller

### Windows:

    pyinstaller --onefile --windowed main.py game.py cards.py text.py --add-data "font;font" --add-data "Cards;Cards" --icon "blackjack.icns" --name "Blackjack"


### Mac/Linux:

    pyinstaller --onefile --windowed main.py game.py cards.py text.py --add-data "font:font" --add-data "Cards:Cards" --icon "blackjack.icns" --name "Blackjack"
	
