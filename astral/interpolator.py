def state_diff(d1,d2,tolerance=.01):
    """Returns variables that have changed between d1 and d2.
    Only handles basic types (no lists or dictionaries)
    For floats, consider tolerance
    Can only add keys, not delete them
    To apply a diff, just do dict.update(nd)"""
    nd = {}
    for k in d2:
        if k not in d1:
            nd[k] = d2[k]
        elif type(d1[k])!=type(d2[k]):
            nd[k] = d2[k]
        elif type(d1[k])==type(0.1) and abs(d1[k]-d2[k])>tolerance:
            nd[k] = d2[k]
        elif d1[k]!=d2[k]:
            nd[k] = d2[k]
    return nd
            
#~ 0 0 0 ball red v=0 v=0              0 0 0 ball red v=0 v=0
#~ 1 0 0 ball red v=1 v=0              1 - -  --- --- v=1 ---
assert state_diff({"x":0,"y":0,"v":0},{"x":1,"y":0,"v":1}) == {"x":1,"v":1}
#~ 2 0 0 ball red v=1 v=0              2 - - --- ---  --- ---
assert state_diff({"x":1,"y":0,"v":1},{"x":2,"y":0,"v":1}) == {"x":2}
#~ 3 0 0 ball red v=1 v=0              3 - - --- ---  --- ---
assert state_diff({"x":2,"y":0,"v":1},{"x":3,"y":0,"v":1}) == {"x":3}
#~ 4 0 0 ball red v=0 v=1              4 - - --- ---  v=0 v=1
assert state_diff({"x":3,"y":0,"v":1},{"x":4,"y":0,"v":0,"v2":1}) == {"x":4,"v":0,"v2":1}
#~ 4 1 0 ball green v=0 v=0           - 1 - --- green  --- v=0
assert state_diff({"x":4,"y":0,"v":0,"v2":1},{"x":4,"y":1,"v":0,"v2":0}) == {"y":1,"v2":0}
#~ 4 1 0 ball green v=0 v=0           - - - --- --- --- ---
assert state_diff({"x":4,"y":1,"v":0,"v2":0},{"x":4,"y":1,"v":0,"v2":0}) == {}
#~ 4 1 0 ball green v=0 v=0           - - - --- --- --- ---

def interpolate(state1,state2,t,method={}):
    """Interpolate between to states. Method is a
    dictionary mapping keys to the interpolation method.
    Example: {'pos_x':'linear','health':zero}
    Methods available are:
    
    one: value equal to state1 from t=0 to t=1, then set to state2
    zero: value equal to state2 from t=0 to t=1
    linear: value equal to between state1 and state 2 based on t
    
    integers, strings, cases where state1 has no value, all default to 'one'
    floats default to 'linear'
    all other cases default to 'zero'
    """
    nd = {}
    for k in state2:
        
        m = method.get(k,None)
        
        if m=="linear" or not m:
            if k not in state1:
                m = "one"
            elif type(state1[k])!=type(state2[k]):
                m = "one"
            elif type(state1[k])==type(""):
                m = "one"
        if not m:
            if type(state1[k])!=type(state2[k]):
                m = "one"
            elif type(state1[k])==type(""):
                m = "one"
            if type(state1[k])==type(1):
                m = "one"
            elif type(state1[k])==type(1.0):
                m = "linear"
            else:
                m = "zero"

        if m=="linear":
            nd[k] = state1[k]+(state2[k]-state1[k])*t
        elif m=="one":
            if t>=1:
                nd[k] = state2[k]
        elif m=="zero":
            nd[k] = state2[k]
    return nd