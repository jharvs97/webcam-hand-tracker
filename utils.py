def remap(val, lower, upper, new_lower, new_upper):
    return ( new_lower + (val - lower) * ((new_upper - new_lower) / (upper - lower)) )
