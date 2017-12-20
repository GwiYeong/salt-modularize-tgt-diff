def _check_glob_minions(self, expr, greedy):  # pylint: disable=unused-argument
    '''
    Return the minions found by looking via globs
    '''
    return {'minions': fnmatch.filter(self._pki_minions(), expr),
                'missing': []}

