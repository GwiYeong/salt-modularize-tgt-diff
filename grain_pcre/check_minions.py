def check_minions(expr, delimiter, greedy):
    '''
    Return the minions found by looking via grains with PCRE
    '''
    return salt.tgt.check_cache_minions(__opts__, expr, delimiter, greedy, 'grains', regex_match=True)
