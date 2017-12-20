def _check_compound_pillar_exact_minions(self, expr, delimiter, greedy):
    '''
    Return the minions found by looking via compound matcher

    Disable pillar glob matching
    '''
    return self._check_compound_minions(expr,
                                        delimiter,
                                        greedy,
                                        pillar_exact=True)

