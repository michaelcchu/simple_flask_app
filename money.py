import matplotlib.pyplot as plt

import math
import os
import datetime

HANDSIZE = 5

## Deck -> PieChart
## Calculates the probability of getting every possible amount of money from a draw.
## Generates a pie chart to visualize the probabilities. 
## Saves the chart in the images folder. 
## Returns the probabilities for each money amount, as well as the filename of the pie chart image.
def main(deck,app):
  # If deck has 5 or fewer cards, there is only one possible hand.
  if nCards(deck) <= 5:
      hands = [deck]
      probs = [1]
  else:
    hands = generateHands(deck)
    probs = calcHandProbs(hands,deck)
  money = evaluateHands(hands)
  [condensedMoney,condensedProbs] = condense(money,probs) 
  filePath = generatePieChart(deck,hands,condensedProbs,condensedMoney,app)
  return [condensedMoney,condensedProbs,filePath]

## Deck -> HandList
## Generates a list of all possible hands that could be drawn from the deck.
def generateHands(deck,base={}):
  # Makes copies so as to not disturb the originals
  d = deck.copy()
  b = base.copy()

  # If the deck is empty, return base (as long at it is a valid hand)
  if len(d)==0:
      spots = spotsLeft(b)
      if spots > 0:
          return []
      elif spots == 0:
          return [b]
      else:
          return ["INVALID HAND"]

  # Otherwise... Pick a card type from the deck 
  cardType = list(d)[0]
  amount = d[cardType]
  
  # Update the deck
  del d[cardType]

  # Figure out how many spots in the hand are left
  spots = spotsLeft(b)

  # Generate hands with i of the card type
  handList = []
  for i in range(0,min(spots,amount)+1):
      b[cardType] = i
      handList += generateHands(d,b)

  return handList

# Returns the number of spots left in the hand we're trying to build (given a certain base b)
def spotsLeft(b):
    spots = HANDSIZE
    for n in b.values():
        spots = spots - n
    return spots

# HandList, Deck -> Probability
## Calculates the probability of drawing each possible hand.
def calcHandProbs(hands, deck):
  probList = []
  for hand in hands:
    successes = 1
    for card,amount in hand.items():    
        successes = successes*nCr(deck[card],amount)
    possible = nCr(nCards(deck),5)

    prob = successes/possible
    probList.append(prob)
  return probList

# Calculates n choose r
def nCr(n,r):
  f = math.factorial
  return f(n)/(f(r)*f(n-r))

# Calculates the number of cards in deck d
def nCards(d):
  count = 0
  for n in d.values():
      count += n
  return count

## Hand -> Amount of Money
## Determines how much money one can extract from a certain hand.
def evaluateHands(hands):
  moneyList = []
  for hand in hands:
    sum = 0
    if 'copper' in hand:
      sum += 1*hand['copper']
    if 'silver' in hand:
      sum += 2*hand['silver']
    if 'gold' in hand:
      sum += 3*hand['gold']
    if 'moneylender' in hand and 'copper' in hand:
      if hand['moneylender']>0:
        sum += 2
    elif 'militia' in hand:
      if hand['militia']>0:
        sum += 2
    moneyList.append(sum)
  return moneyList

## Money, Probs -> Money, Probs
## Combines and sorts money categories with the same value 
def condense(money,probs):
  updatedMoney = []
  updatedProbs = []
  for i in range(len(money)):
    if money[i] in updatedMoney:
      updateIndex = updatedMoney.index(money[i])
      updatedProbs[updateIndex] += probs[i]
    else:
      j=0
      while j in range(len(updatedMoney)) and updatedMoney[j]<money[i]:
        j+=1
      updatedMoney.insert(j,money[i])
      updatedProbs.insert(j,probs[i])
  return [updatedMoney,updatedProbs]

## Hand -> PieChart
## Produces a pie chart 
def generatePieChart(deck,hands,probs,money,app):
  plt.pie(probs, labels=money, autopct='%1.1f%%')
  plt.suptitle("Deck: "+str(deck)+"\nHow much money will I obtain from my next draw?")

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

#main({"silver":1,"gold":3,"estate":4})