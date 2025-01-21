class State():
    def __init__(self, name, id):
        self.name = name
        self.id = 0
    
    def loop(self, delta = 0):
        pass
    
    def get_name(self):
        return self.name
    
    def get_id(self):
        return self.id


class FiniteStateMachine():
    def __init__(self):
        self.states_id = {}
        self.state : State = None
        
    def loop(self, delta = 0):
        if self.state == None:
            print("No state")
            return
        self.state.loop()
        new_state = self.get_transition()
        if new_state != None:
            self._set_state( self, new_state.get_name() )
        
    def _set_state(self, new_state : State):
        self.enter_state(self.state, new_state)
        self.state = new_state
           
    def get_transition(self, state_name):
        """ Overrides with custom transitions """
        pass
    
    def enter_state(self, from_state, to_state):
        """ Overrides with custom state enter"""
        pass