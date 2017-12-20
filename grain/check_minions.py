def _check_grain_minions(self, expr, delimiter, greedy):
    '''
    Return the minions found by looking via grains
    '''
    return self._check_cache_minions(expr, delimiter, greedy, 'grains')