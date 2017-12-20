def _check_pcre_minions(self, expr, greedy):  # pylint: disable=unused-argument
    '''
    Return the minions found by looking via regular expressions
    '''
    reg = re.compile(expr)
    return {'minions': [m for m in self._pki_minions() if reg.match(m)],
            'missing': []}
