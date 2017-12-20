def _check_nodegroup_minions(self, expr, greedy):  # pylint: disable=unused-argument
    '''
    Return minions found by looking at nodegroups
    '''
    return self._check_compound_minions(nodegroup_comp(expr, self.opts['nodegroups']),
        DEFAULT_TARGET_DELIM,
        greedy)

