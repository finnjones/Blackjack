
# dar = {
#     "AS" : 1, "2S" : 2, "3S" : 3, "4S" : 4, "5S" : 5, "6S" : 6, "7S" : 7, "8S" : 8, "9S" : 9, "10S" : 10, "JS" : 10, "QS" : 10, "KS" : 10,
#     "AH" : 1, "2H" : 2, "3H" : 3, "4H" : 4, "5H" : 5, "6H" : 6, "7H" : 7, "8H" : 8, "9H" : 9, "10H" : 10, "JH" : 10, "QH" : 10, "KH" : 10,
#     "AD" : 1, "2D" : 2, "3D" : 3, "4D" : 4, "5D" : 5, "6D" : 6, "7D" : 7, "8D" : 8, "9D" : 9, "10D" : 10, "JD" : 10, "QD" : 10, "KD" : 10,
#     "AC" : 1, "2C" : 2, "3C" : 3, "4C" : 4, "5C" : 5, "6C" : 6, "7C" : 7, "8C" : 8, "9C" : 9, "10C" : 10, "JC" : 10, "QC" : 10, "KC" : 10,
# }
# dar = "123"
def deals():
    global cardSelector
    cardSelector += 1
    cards(screenSize[0]/2, 0, (screenSize[0]/2 - 20, 760))
    cardSelector += 1
    cards(screenSize[0]/2, 0, (screenSize[0]/2 + 20, 780))
    cardSelector += 1
    cards(screenSize[0]/2, 0, (screenSize[0]/4 - 20, 760))
    cardSelector += 1
    cards(screenSize[0]/2, 0, (screenSize[0]/4 + 20, 780))
    cardSelector += 1
    cards(screenSize[0]/2, 0, (screenSize[0] * 0.75 - 20, 760))
    cardSelector += 1
    cards(screenSize[0]/2, 0, (screenSize[0] * 0.75 + 20, 780))
