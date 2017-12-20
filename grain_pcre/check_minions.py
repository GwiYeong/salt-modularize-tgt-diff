    def _check_grain_pcre_minions(self, expr, delimiter, greedy):
        '''
        Return the minions found by looking via grains with PCRE
        '''
        return self._check_cache_minions(expr,
                                         delimiter,
                                         greedy,
                                         'grains',
                                         regex_match=True)

