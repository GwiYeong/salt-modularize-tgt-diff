def check_minions(expr, delimiter, greedy):
    '''
    Return the minions found by looking via grains
    '''
    return salt.tgt.check_cache_minions(__opts__, expr, delimiter, greedy, 'grains')
