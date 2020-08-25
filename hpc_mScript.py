import matplotlib.pyplot as plt

import math
import os
import datetime

HANDSIZE = 5

## Deck -> Hands and Probs
## Calculates the probability of getting every possible hand from a draw.
## Returns the probabilities for each hand.
def main(deck,app):
  # If deck has 5 or fewer cards, there is only one possible hand.
  if nCards(deck) <= 5:
      hands = [deck]
      probs = [1]
  else:
    hands = generateHands(deck)
    probs = calcHandProbs(hands,deck)
  return [hands,probs]

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