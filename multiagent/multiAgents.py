# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        if action == 'Stop':
            return -10000
        #get closest food
        closestFood = None
        closestFoodDistance = float('inf')
        for food in newFood.asList():
            distanceToFood = manhattanDistance(food, newPos)
            if distanceToFood < closestFoodDistance:
                closestFood = food
                closestFoodDistance = distanceToFood

        total = 0
        if closestFood:
            mDistance = manhattanDistance(newPos, closestFood)
            total -= mDistance * .25

        # ghost positions
        ghostPositions = []
        for ghostState in newGhostStates:
            ghost = ghostState.configuration.pos
            ghostPositions.append(ghost)

        closestGhost = None
        closestGhostDistance = float('inf')
        for ghost in ghostPositions:
            distance = manhattanDistance(newPos, ghost)
            if distance < closestGhostDistance:
                closestGhostDistance = distance
                closestGhost = ghost
        if closestGhostDistance <= 3:
            total -= (3 - closestGhostDistance) * 1000

        total += successorGameState.data.score

        if newPos == currentGameState.getPacmanPosition():
            total -= 1
        return total

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def maxNode(self, gameState, numGhosts, plyCounter):
        if gameState.isWin() or gameState.isLose() or plyCounter == 0:
            return self.evaluationFunction(gameState)

        evaluations = []
        legalActions = gameState.getLegalActions()

        for action in legalActions:
            evaluations.append(self.minNode(gameState.generateSuccessor(self.index, action), numGhosts, plyCounter))

        return max(evaluations)

    def minNode(self, gameState, numGhosts, plyCounter):
        if gameState.isWin() or gameState.isLose() or plyCounter == 0:
            return self.evaluationFunction(gameState)

        evaluations = []

        totalNumGhosts = gameState.getNumAgents() - 1
        currentGhostIndex = totalNumGhosts - numGhosts + 1
        legalActions = gameState.getLegalActions(currentGhostIndex)
        if numGhosts > 1:
            for action in legalActions:
                evaluations.append(self.minNode(gameState.generateSuccessor(currentGhostIndex, action), numGhosts - 1, plyCounter))
        else:
            for action in legalActions:
                evaluations.append(self.maxNode(gameState.generateSuccessor(currentGhostIndex, action), totalNumGhosts, plyCounter - 1))

        return min(evaluations)

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game

          gameState.isWin():
            Returns whether or not the game state is a winning state

          gameState.isLose():
            Returns whether or not the game state is a losing state
        """
        actions = []
        evaluations = []

        # import pdb; pdb.set_trace()
        for action in gameState.getLegalActions():
            actions.append(action)
            numGhosts = gameState.getNumAgents() - 1
            evaluations.append(self.minNode(gameState.generateSuccessor(self.index, action), numGhosts, self.depth))

        print("\n")
        print(gameState)
        maxEvaluationIndex = evaluations.index(max(evaluations))
        return actions[maxEvaluationIndex]
        #need to return an action not a value
        # return self.maxNode(gameState, self.depth, gameState.getNumAgents() - 1)
        #use recursive helper function to make the best choice
        #every time everyone has taken an action, it's depth 1
        #return one of the legal actions

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def maxNode(self, gameState, numGhosts, plyCounter, alpha, beta):
        if gameState.isWin() or gameState.isLose() or plyCounter == 0:
            return self.evaluationFunction(gameState)

        legalActions = gameState.getLegalActions()
        v = - float('inf')
        for action in legalActions:
            successorState = gameState.generateSuccessor(self.index, action)
            v = max(v, self.minNode(successorState, numGhosts, plyCounter, alpha, beta))
            if v > beta:
                return v
            alpha = max(alpha, v)
        return v

    def minNode(self, gameState, numGhosts, plyCounter, alpha, beta):
        if gameState.isWin() or gameState.isLose() or plyCounter == 0:
            return self.evaluationFunction(gameState)

        totalNumGhosts = gameState.getNumAgents() - 1
        currentGhostIndex = totalNumGhosts - numGhosts + 1
        legalActions = gameState.getLegalActions(currentGhostIndex)
        v = float('inf')
        if numGhosts > 1:
            for action in legalActions:
                successorState = gameState.generateSuccessor(currentGhostIndex, action)
                v = min(v, self.minNode(successorState, numGhosts - 1, plyCounter, alpha, beta))
                if v < alpha:
                    return v
                beta = min(beta, v)
        else:
            for action in legalActions:
                successorState = gameState.generateSuccessor(currentGhostIndex, action)
                v = min(v, self.maxNode(successorState, totalNumGhosts, plyCounter - 1, alpha, beta))
                if v < alpha:
                    return v
                beta = min(beta, v)
        return v

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        actions = []
        evaluations = []

        alpha = - float('inf')
        beta = float('inf')
        v = - float('inf')
        for action in gameState.getLegalActions():
            actions.append(action)
            numGhosts = gameState.getNumAgents() - 1
            successorState = gameState.generateSuccessor(self.index, action)
            v = max(v, self.minNode(successorState, numGhosts, self.depth, alpha, beta))
            if v > beta:
                return v
            alpha = max(alpha, v)

            evaluations.append(v)

        maxEvaluationIndex = evaluations.index(max(evaluations))
        return actions[maxEvaluationIndex]

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def maxNode(self, gameState, numGhosts, plyCounter):
        if gameState.isWin() or gameState.isLose() or plyCounter == 0:
            return self.evaluationFunction(gameState)

        evaluations = []
        legalActions = gameState.getLegalActions()

        for action in legalActions:
            evaluations.append(self.minNode(gameState.generateSuccessor(self.index, action), numGhosts, plyCounter))

        return max(evaluations)

    def minNode(self, gameState, numGhosts, plyCounter):
        if gameState.isWin() or gameState.isLose() or plyCounter == 0:
            return self.evaluationFunction(gameState)

        totalNumGhosts = gameState.getNumAgents() - 1
        currentGhostIndex = totalNumGhosts - numGhosts + 1
        legalActions = gameState.getLegalActions(currentGhostIndex)
        sum = 0.0
        if numGhosts > 1:
            for action in legalActions:
                sum += float(self.minNode(gameState.generateSuccessor(currentGhostIndex, action), numGhosts - 1, plyCounter))
        else:
            for action in legalActions:
                sum += float(self.maxNode(gameState.generateSuccessor(currentGhostIndex, action), totalNumGhosts, plyCounter - 1))
        # print("min eval:")
        # print(evaluations)
        return sum / (len(legalActions))

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        actions = []
        evaluations = []

        for action in gameState.getLegalActions():
            actions.append(action)
            numGhosts = gameState.getNumAgents() - 1
            evaluations.append(self.minNode(gameState.generateSuccessor(self.index, action), numGhosts, self.depth))

        maxEvaluationIndex = evaluations.index(max(evaluations))
        return actions[maxEvaluationIndex]

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: chase after ghost if the manhattan distance to it is < 10
                    and the ghost is scared.
                    go towards closest foods.
                    run away from ghosts <= 3 distance away
    """
    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()
    newGhostStates = currentGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

    closestFood = None
    closestFoodDistance = float('inf')
    for food in newFood.asList():
        distanceToFood = manhattanDistance(food, newPos)
        if distanceToFood < closestFoodDistance:
            closestFood = food
            closestFoodDistance = distanceToFood

    total = 0
    if closestFood:
        mDistance = manhattanDistance(newPos, closestFood)
        total -= mDistance * .25

    # ghost positions
    ghostPositions = []
    for ghostState in newGhostStates:
        ghost = ghostState.configuration.pos
        ghostPositions.append(ghost)

    scaredGhostIndex = newScaredTimes.index(max(newScaredTimes))
    ghostScared = newScaredTimes[scaredGhostIndex]
    closestGhostDistance = float('inf')
    for ghost in ghostPositions:
        distance = manhattanDistance(newPos, ghost)
        if distance < closestGhostDistance:
            closestGhostDistance = distance
    if not ghostScared and closestGhostDistance <= 3:
        total -= (3 - closestGhostDistance) * 1000
    else:
        for time in newScaredTimes:
            scaredGhostPosition = newGhostStates[newScaredTimes.index(time)].configuration.pos
            distanceToScaredGhost = manhattanDistance(newPos, scaredGhostPosition)
            if time > 0 and distanceToScaredGhost < 10:
                total += distanceToScaredGhost

    total += currentGameState.data.score

    if newPos == currentGameState.getPacmanPosition():
        total -= 1

    return total
# Abbreviation
better = betterEvaluationFunction
