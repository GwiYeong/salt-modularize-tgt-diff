def _check_pillar_minions(self, expr, delimiter, greedy):
    '''
    Return the minions found by looking via pillar
    '''
    return self._check_cache_minions(expr, delimiter, greedy, 'pillar')
