from collections import defaultdict
import math

__author__ = 'jpaton'

class HMM(defaultdict):
    """
    An HMM is a two-dimensional dictionary mapping ordered pairs of States
    to transition probabilities.
    """
    def __init__(self):
        # self.trans: transmission counts
        super(HMM, self).__init__(lambda: defaultdict(0))
        # self.start_state = State()
        self._transition_count = None
        self._emission_count = None

    def __repr__(self):
        for state in self.keys():
            print ',\t'.join([count for count in self[state].values()])

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