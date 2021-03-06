# Blackjack
 
## Requirements
- Python 3
- Pygame 2.1.0

## Controls
|Function|Button|
|--|--|
|Hit|H|
|Stand|S|
|New Round|N or use GUI button|
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
	
### Navigate to Blackjack directory using cd

### Windows:

    pyinstaller --onefile --windowed main.py game.py cards.py text.py --add-data "font;font" --add-data "Cards;Cards" --icon "blackjack.ico" --name "Blackjack"


### Mac/Linux:

    pyinstaller --onefile --windowed main.py game.py cards.py text.py --add-data "font:font" --add-data "Cards:Cards" --icon "blackjack.icns" --name "Blackjack"
	
## OR
Use precompiled program in the folder "Standalone Programs"

## Theory Work

https://soft-felidae-860.notion.site/Blackjack-Game-Theory-9b09830b6372453b9a73084a040f4969
