def scale(value, min_val, max_val):
    """
    Scale a value, given min-max range, to the
    min=0, max=1 range. Negative and >1 values allowed.
    """
    return (value - min_val) / (max_val - min_val)
    
def flatscale(value, min_val, max_val):
    """
    Like scale(), except negative values are flattened
    to 0 and >1 values are flattened to 1.
    """
    result = scale(value, min_val, max_val)
    if result < 0:
        result = 0
    elif result > 1:
        result = 1
    return result
