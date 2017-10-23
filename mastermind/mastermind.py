#!/usr/bin/python

import random
import timeit

class Choice:
    ALL_COLORS = frozenset({"RED", "BLUE", "GREEN", "YELLOW", "BLACK", "BROWN"})
    NUM_COLORS = 4

    def __init__(self, colors):
        if (len(colors) != Choice.NUM_COLORS):
            raise "Bad number of colors"
        for c in colors:
            if c not in Choice.ALL_COLORS:
                raise "Bad color: %s" % c
        self._colors = colors

    def __str__(self):
        return str(self._colors)

    @staticmethod
    def All(prefix = []):
        for c in Choice.ALL_COLORS:
            next_prefix = prefix + [c]
            if (len(next_prefix) == Choice.NUM_COLORS):
                yield Choice(next_prefix)
            else:
                for c in Choice.All(next_prefix):
                    yield c

class Board:
    GUESS_COUNT = 10
    
    @staticmethod
    def ScoreChoice(hidden, guess):
        black_pegs = 0
        white_pegs = 0

        colors = {c:0 for c in Choice.ALL_COLORS} 
        for i in xrange(0, Choice.NUM_COLORS):
            hidden_color = hidden._colors[i]
            if (hidden_color == guess._colors[i]):
                black_pegs = black_pegs + 1
            colors[hidden_color] = colors[hidden_color] + 1

        for guess_color in guess._colors:
            if colors[guess_color] > 0:
                white_pegs = white_pegs + 1
                colors[guess_color] = colors[guess_color] - 1

        white_pegs = white_pegs - black_pegs

        return (black_pegs, white_pegs)

class Strategy:
    def NextGuess(self):
        raise "Abstract method Strategy.NextGuess called"

    def Reset(self):
        raise "Abstract method Strategy.Reset called"
    
    def AddEvaluation(self, guess, evaluation):
        raise "Abstract method Strategy.AddEvaluation called"

    
class RandomStrategy(Strategy):
    def __init__(self):
        self._all_choices = list(Choice.All())

    def NextGuess(self):
        return random.choice(self._all_choices)

    def Reset(self):
        pass
    
    def AddEvaluation(self, guess, evaluation):
        pass

class RandomAllowedStrategy(Strategy):
    def __init__(self):
        self.Reset()

    def Reset(self):
        self._valid_choices = list(Choice.All())
        
    def NextGuess(self):
        return random.choice(self._valid_choices)

    def AddEvaluation(self, guess, evaluation):
        new_valid_choices = []
        for potential_hidden in self._valid_choices:
            if Board.ScoreChoice(potential_hidden, guess) == evaluation:
                new_valid_choices = new_valid_choices + [potential_hidden]
        self._valid_choices = new_valid_choices
        

def EvaluateStrategy(strategy):
    guess_counts = {i:0 for i in xrange(-1,Board.GUESS_COUNT + 1)}
    for hidden in Choice.All():
        guess_count = -1
        strategy.Reset()
        for x in xrange(0, Board.GUESS_COUNT):
            guess = strategy.NextGuess()
            evaluation = Board.ScoreChoice(hidden, guess)
            strategy.AddEvaluation(guess, evaluation)
            if evaluation[0] == Choice.NUM_COLORS:
                guess_count = x
                break
        guess_counts[guess_count] = guess_counts[guess_count] + 1
    return guess_counts
    

def TestScoreChoice():
    for i in xrange(0, 10):
        hidden = random.choice(all_choices)
        guess = random.choice(all_choices)

        score = Board.ScoreChoice(hidden, guess)

        print "h:%s g:%s -> %s" % (hidden, guess, score)
    
def main():
    print "RandomStrategy: %s" % EvaluateStrategy(RandomStrategy())
    print "RandomAllowedStrategy: %s" % EvaluateStrategy(RandomAllowedStrategy())

if __name__ == "__main__":
    main()
