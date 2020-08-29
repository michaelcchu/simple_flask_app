import matplotlib.pyplot as plt

import math
import os
import datetime
import random

HANDSIZE = 5
NUM_SIM = 10000

## Deck -> PieChart
## Calculates the probability of getting every possible amount of money from a draw.
## Generates a pie chart to visualize the probabilities. 
## Saves the chart in the images folder. 
## Returns the probabilities for each money amount, as well as the filename of the pie chart image.
def main(deckInput,deckDictionary,app):
  moneyDictionary = {}
  for i in range(NUM_SIM):
    deck = deckInput.copy()
    hand = []
    discard = []
    actions = 1
    buys = 1
    money = 0

    # Shuffle the deck
    deck = shuffleDeck(deck)

    # Draw
    [deck,hand,discard] = draw(deck,hand,discard,5)
    
    # Actions
    while "village" in hand and actions > 0:
      hand.remove("village")
      actions -= 1
      [deck,hand,discard] = draw(deck,hand,discard,len(hand)+1)
      actions += 2

    while "festival" in hand and actions > 0:  
      hand.remove("festival")
      actions -= 1
      actions += 2
      buys += 1
      money += 2

    while "market" in hand and actions > 0:
      hand.remove("market")
      actions -= 1
      [deck,hand,discard] = draw(deck,hand,discard,len(hand)+1)
      actions += 1
      buys += 1
      money += 1

    while "smithy" in hand and actions > 0:
      hand.remove("smithy")
      actions -= 1
      [deck,hand,discard] = draw(deck,hand,discard,len(hand)+3)
    
    for card in hand:
      if card == "gold":
        money += 3
      elif card == "silver":
        money += 2
      elif card == "copper":
        money += 1
    
    if money in moneyDictionary:
        moneyDictionary[money] += 1
    else:
        moneyDictionary[money] = 1

  moneyList = []
  probList = []

  # Fills moneyList and probList in a sorted manner
  for key,value in moneyDictionary.items():
    j=0
    while j in range(len(moneyList)) and moneyList[j]<key:
      j+=1
    moneyList.insert(j,key)
    probList.insert(j,value/NUM_SIM)

  filePath = generatePieChart(deckDictionary,probList,moneyList,app)
  return [moneyList,probList,filePath]

# The following code is from Raymond:
# draws a specified number of cards to the hand
# Note: numCardsWanted is the desired total hand size
def draw(deck,hand,discard,numCardsWanted):
  # how many cards have been drawn
  numDrawn = len(hand)

  # run this if there are not enough cards in the deck
  if(len(deck) < numCardsWanted-numDrawn):
    # put the cards in the deck right now in the hand
    hand.extend(deck.copy())
    numDrawn += len(hand)

    # shuffle the discard pile and make it the new deck
    deck = discard.copy()
    discard = []
    deck = shuffleDeck(deck)

  # add cards from the deck until the right number of cards have been drawn
  while(numDrawn < numCardsWanted):
    try:
      hand.append(deck.pop(0))
    except IndexError:
      pass
    numDrawn += 1
  
  return [deck,hand,discard]

def shuffleDeck(deck):
  # just shuffles the deck
  deckCopy = deck.copy()
  random.shuffle(deckCopy)
  return deckCopy

## Probs, Money -> PieChart
## Produces a pie chart 
def generatePieChart(deckDictionary,probs,money,app):
  # Add dollar signs to the money
  moneyWithDollars = []
  for element in money:
    moneyWithDollars.append("$"+str(element))

  plt.pie(probs, labels=moneyWithDollars, autopct='%1.1f%%')
  plt.suptitle("Deck: "+str(deckDictionary)+"\nHow much money will I obtain from my next draw?")

  timeString = str(datetime.datetime.now())
  timeString = timeString.replace(':','.')
  newFilename = 'pie_chart'+timeString+'.png'

  # Removes all previous pie_chart images from the static folder 
  for filename in os.listdir(os.path.join(app.root_path,'static/')):
    if filename.startswith('pie_chart'):  # not to remove other images
      os.remove(os.path.join(app.root_path,'static/'+filename))

  plt.savefig(os.path.join(app.root_path,'static/'+newFilename))
  plt.clf()
  return newFilename