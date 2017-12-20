def _check_list_minions(self, expr, greedy):  # pylint: disable=unused-argument
    '''
    Return the minions found by looking via a list
    '''
    if isinstance(expr, six.string_types):
        expr = [m for m in expr.split(',') if m]
    minions = self._pki_minions()
    return {'minions': [x for x in expr if x in minions],
            'missing': [x for x in expr if x not in minions]}