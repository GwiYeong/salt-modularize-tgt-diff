def _check_pillar_pcre_minions(self, expr, delimiter, greedy):
    '''
    Return the minions found by looking via pillar with PCRE
    '''
    return self._check_cache_minions(expr,
                                     delimiter,
                                     greedy,
                                     'pillar',
                                     regex_match=True)

