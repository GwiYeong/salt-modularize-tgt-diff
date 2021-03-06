def check_minions(expr, delimiter, greedy):
    '''
    Return the minions found by looking via compound matcher
    Disable pillar glob matching
    '''
    return salt.tgt.check_compound_minions(__opts__, expr, delimiter, greedy, pillar_exact=True)
