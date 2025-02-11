import math

class Trajectory1D:
    def __init__(self, a_max : float, v_max : float, v0 : float, wf : float):
        # Check for valid inputs
        if a_max <= 0:
            raise ValueError("Max acceleration cant be 0")
        if v_max <= 0:
            raise ValueError("Max velocity cant be 0")
        
        if wf == 0:
            self.states = [State(v0, 0, 0, 0)]
            return
        
        # Normalize
        wf_sign = -1 if wf < 0 else 1
        wf = wf_sign*wf
        v0 = wf_sign*v0

        state_0 = State(v0, 0, 0, 0)
        c = Constraints(a_max, v_max)
        states : list[type[State]] = [state_0]
        
        # Check which case is applicable

        # Case 1
        if v0 < 0:
            states.append(Cases.case_1(state_0, c))
        # Case 2.1
        elif wf > ( v0**2 )/(2*a_max) and v_max > v0 and v0 >= 0:
            states.append(Cases.case_2_1(state_0, c, wf))
        # Case 2.2
        elif wf > (v0**2)/(2*a_max) and abs(v_max - v0) <= 0.002:
            states.append( Cases.case_2_2(state_0, c, wf) )
        # Case 2.3
        elif wf <= (v0**2)/(2*a_max) and 0 < v0  and v0 <= v_max:
            states.append(Cases.case_2_3(state_0, c))
        # Case 3
        elif v0 > v_max:
            states.append( Cases.case_3(state_0, c))

        # Normalize
        if wf_sign == -1:
            for s in states:
                s.v = -s.v
        self.states = states

    def tf(self) -> float:
        return self.states[-1].t

    def get_solution(self) -> tuple[float, float]:
        return self.states[-1].t , self.states[-1].v

class Constraints:
    def __init__(self, a_max, v_max):
        self.a_max = a_max # <- constant
        self.v_max = v_max
    def __repr__(self):
        return f" a_max:{self.a_max} v_max:{self.v_max}"


class State:
    def __init__(self, v, t, a, d):
        self.v = v # final velocity
        self.t = t # final time
        self.a = a # acceleration applied from last state to this state
        self.d = d # distance traveled from last state and this state
    def __repr__(self):
        return "(vf: {0}, t: {1}, a: {2}, d: {3})".format(self.v, self.t, self.a, self.d)


class Cases:
    # The initial velocity is negative; the vehicle has to accelerate 
    # with maximal control effort until it reaches v = 0
    def case_1(last_state : State, constraints : Constraints):
        t = -(last_state.v/constraints.a_max)
        d = -(last_state.v**2)/(2*constraints.a_max)
        new_state = State(0, t, constraints.a_max, d)
        return new_state

    # The vehicle has to accelerate, either because 
    # the destination is far away or the initial velocity is small.
    def case_2_1(last_state : State, c : Constraints, wf : float):
        tI = (c.v_max - last_state.v)/c.a_max
        v1 = math.sqrt(wf*c.a_max + (last_state.v**2)/2)
        tII = (v1 - last_state.v)/c.a_max
        # Subcase 1: The vehicle reach the max velocity
        if tI < tII:
            d = (c.v_max**2 - last_state.v**2)/(2*c.a_max)
            return State(c.v_max, tI, c.a_max, d)
        # Subcase 2: The vehicle accelerate until it has to desaccelerate
        else:
            d = wf/2 + (last_state.v**2)/(2*c.a_max)
            return State(v1, tII, c.a_max, d)

    # The vehicle is cruising at 
    # maximum velocity until it has to decelerate.
    def case_2_2(last_state : State, c : Constraints, wf : float): # Same velocity
        t = (wf/c.v_max) - (c.v_max/(2*c.a_max))
        d = wf - ( ( last_state.v**2 )/( 2*c.a_max ) )
        return State(c.v_max, t, 0, d)
    # The vehicle has to decelerate 
    # until it reaches zero final velocity.
    def case_2_3(last_state : State, c : Constraints):
        t = last_state.v/c.a_max
        d = (last_state.v**2)/(2*c.a_max)
        return State(0, t, -c.a_max, d)

    # The vehicle moves faster 
    # than the allowed maximum velocity.
    def case_3(last_state : State, c : Constraints):
        t = (last_state.v - c.v_max)/c.a_max
        d = ( 1/(2*c.a_max) )*(last_state.v**2 - c.v_max**2)
        return State(c.v_max, t, -c.a_max, d)