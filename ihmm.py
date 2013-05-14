from collections import defaultdict
from __future__ import division
import math
import numpy

__author__ = 'jpaton'

def dirties_trans_count(fn):
    def g(self, *args, **kwargs):
        self._transition_count = None
        return fn(*args, **kwargs)
    return g

def dirties_emission_count(fn):
    def g(self, *args, **kwargs):
        self._emission_count = None
        return fn(*args, **kwargs)
    return g

class State(defaultdict):
    """A state is a mapping from EmissionSymbols to emission counts"""
    def __init__(self):
        super(State, self).__init__(lambda: 0)
        self.is_oracle = False

    @property
    def total_emissions(self):
        # TODO: memoize this
        return numpy.sum(self.values())

    def generate_emission(self):
        # TODO: implement categorical sampling: http://en.wikipedia.org/wiki/Categorical_distribution#Sampling
        raise NotImplementedError()

class EmissionSymbol(str):
    pass

class Emission(object):
    def __init__(self, symbol):
        self.symbol = symbol

class HMM(defaultdict):
    def __init__(self):
        # self.trans: transmission counts
        super(HMM, self).__init__(lambda: defaultdict(0))
        self.start_state = State()
        self._transition_count = None
        self._emission_count = None

    def __str__(self):
        for state in self.keys():
            print ',\t'.join([count for count in self[state].values()])

    @property
    def total_transmissions(self):
        if self._transition_count == None:
            # recompute transition count
            self._transition_count = 0
            for state_i in self:
                for state_j in self:
                    if state_i == state_j:
                        continue
                    self._transition_count += self[state_i][state_j]
        return self._transition_count

    @property
    def total_emissions(self):
        if self._emission_count == None:
            # recompute emission count
            self._emission_count = 0
            for state in self:
                for symbol, count in state.iteritems():
                    self._emission_count += count
        return self._emission_count

    def logprob_states(self, states):
        """
        states: a sequence of states, the first state being the start state
        """
        logprob = 0
        for i in range(len(states) - 1):
            state_i, state_j = states[i], states[i + 1]
            logprob += math.log(self[state_i][state_j] / self.total_transitions)
        return logprob

    def logprob_emissions(self, emissions):
        raise NotImplementedError()

    def logprob_both(self, states, emissions):
        return self.logprob_states(states) + self.logprob_emissions(emissions)

    def logprob(self, states = None, emissions = None):
        if states != None and emissions == None:
            return self.logprob_states(states)
        elif states == None and emissions != None:
            return self.logprob_emissions(emissions)
        else:
            return self.logprob_both(states, emissions)

    def generate_states(self, n):
        """
        Returns a state sequence of length n
        """
        raise NotImplementedError()

    def generate_emissions(self, n, states = None):
        """
        Returns an emission sequence of length n
        """
        if states == None:
            states = self.generate_states(n)
        emissions = EmissionSequence()
        emissions.append(self.start_state)
        for state in states[1:]:    # omit start state
            emissions.append(state.generate_emission())
        return emissions

class EmissionSequence(list):
    def __init__(self, hmm):
        self.hmm = hmm

class StateSequence(list):
    def __init__(self, hmm):
        self.hmm = hmm

    @property
    def transition_counts(self):
        counts = defaultdict(lambda: defaultdict(lambda: 0))
        for i in self[:-1]:
            state_i, state_j = self[i], self[i + 1]
            counts[state_i][state_j] += 1
        return counts

def main():
    pass

if __name__ == '__main__':
    main()