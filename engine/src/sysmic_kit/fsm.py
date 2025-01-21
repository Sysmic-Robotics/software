class State():
    def __init__(self, name):
        self.name = name
    
    def loop(self):
        pass
    
    def get_name(self):
        return self.name


class FiniteStateMachine():
    def __init__(self):
        self.states = {}
        self.state : State = None
        self.debug = False
        
    def loop(self, delta = 0):
        if self.state == None:
            print("No state")
            return
        self.state.loop()
        new_state = self.get_transition(self.state.get_name())
        if new_state != None:
            self._set_state( new_state )
        
    def _set_state(self, new_state : State):
        if self.debug == True:
            print("Transition to: ", new_state.get_name())
        self.enter_state(self.state, new_state)
        self.state = new_state
           
    def get_transition(self, state_name):
        """ Overrides with custom transitions """
        pass
    
    def enter_state(self, from_state, to_state):
        """ Overrides with custom state enter"""
        pass