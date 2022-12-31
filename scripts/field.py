class Field:
    def __init__(self, possibleStates):
        self.isCollapsed = False
        self.possibleStates = possibleStates

    def __copy__(self):
        return type(self)(self.possibleStates)

    def number_of_states(self):
        return len(self.possibleStates)

    def collapse(self, state):
        self.possibleStates = []
        self.possibleStates.append(state)
    
    def get_id(self):
        #print(self.possibleStates)
        
        return self.possibleStates[0][0]
    
    def get_rotation(self):
        return self.possibleStates[0][1]
    
    def set_states(self, states):
        self.possibleStates = []
        #print("set states: {0}".format(len(states)))
        for state in states:
            self.possibleStates.append(state)