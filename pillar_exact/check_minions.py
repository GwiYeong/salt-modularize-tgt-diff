def _check_pillar_exact_minions(self, expr, delimiter, greedy):
    '''
    Return the minions found by looking via pillar
    '''
    return self._check_cache_minions(expr,
                                     delimiter,
                                     greedy,
                                     'pillar',
                                     exact_match=True)

