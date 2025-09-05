import webbrowser, os
## DIRECTORY = "C:/Users/light/OneDrive/Desktop/Dinosaur Venture/"
DIRECTORY = ""
DIRECTORY = "D:/Dinosaur Venture/"

## Opens the google folder
if input(" Enter in [NOTHING] to skip opening Google Drive. ") != "":
    webbrowser.open('https://drive.google.com/drive/u/0/folders/1CCQYurvVd9AIWouTiDW5TqwF6KfhXeBO')

## Opens all files, in order
webbrowser.open(DIRECTORY + 'dinosaurVenture.py')
webbrowser.open(DIRECTORY + 'clearing.py')
webbrowser.open(DIRECTORY + 'entity.py')
webbrowser.open(DIRECTORY + 'enemyCards.py')
webbrowser.open(DIRECTORY + 'helper.py')
webbrowser.open(DIRECTORY + 'dinoCards.py')
webbrowser.open(DIRECTORY + 'card.py')
webbrowser.open(DIRECTORY + 'cardFunctions.py')
webbrowser.open(DIRECTORY + 'mainVisuals.py')
# webbrowser.open(DIRECTORY + 'simulatePulls.py')
webbrowser.open(DIRECTORY + 'cardTokens.py')
webbrowser.open(DIRECTORY + 'react.py')
webbrowser.open(DIRECTORY + 'simulateCards.py')

## Opens 'dinosaurVenture.py' again so that document will be focused
webbrowser.open(DIRECTORY + 'dinosaurVenture.py')