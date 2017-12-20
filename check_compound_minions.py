def _check_compound_minions(self,
                            expr,
                            delimiter,
                            greedy,
                            pillar_exact=False):  # pylint: disable=unused-argument
    '''
    Return the minions found by looking via compound matcher
    '''
    if not isinstance(expr, six.string_types) and not isinstance(expr, (list, tuple)):
        log.error('Compound target that is neither string, list nor tuple')
        return {'minions': [], 'missing': []}
    minions = set(self._pki_minions())
    log.debug('minions: {0}'.format(minions))

    if self.opts.get('minion_data_cache', False):
        ref = {'G': self._check_grain_minions,
               'P': self._check_grain_pcre_minions,
               'I': self._check_pillar_minions,
               'J': self._check_pillar_pcre_minions,
               'L': self._check_list_minions,
               'N': None,    # nodegroups should already be expanded
               'S': self._check_ipcidr_minions,
               'E': self._check_pcre_minions,
               'R': self._all_minions}
        if pillar_exact:
            ref['I'] = self._check_pillar_exact_minions
            ref['J'] = self._check_pillar_exact_minions

        results = []
        unmatched = []
        opers = ['and', 'or', 'not', '(', ')']
        missing = []

        if isinstance(expr, six.string_types):
            words = expr.split()
        else:
            words = expr

        for word in words:
            target_info = parse_target(word)

            # Easy check first
            if word in opers:
                if results:
                    if results[-1] == '(' and word in ('and', 'or'):
                        log.error('Invalid beginning operator after "(": {0}'.format(word))
                        return {'minions': [], 'missing': []}
                    if word == 'not':
                        if not results[-1] in ('&', '|', '('):
                            results.append('&')
                        results.append('(')
                        results.append(str(set(minions)))
                        results.append('-')
                        unmatched.append('-')
                    elif word == 'and':
                        results.append('&')
                    elif word == 'or':
                        results.append('|')
                    elif word == '(':
                        results.append(word)
                        unmatched.append(word)
                    elif word == ')':
                        if not unmatched or unmatched[-1] != '(':
                            log.error('Invalid compound expr (unexpected '
                                      'right parenthesis): {0}'
                                      .format(expr))
                            return {'minions': [], 'missing': []}
                        results.append(word)
                        unmatched.pop()
                        if unmatched and unmatched[-1] == '-':
                            results.append(')')
                            unmatched.pop()
                    else:  # Won't get here, unless oper is added
                        log.error('Unhandled oper in compound expr: {0}'
                                  .format(expr))
                        return {'minions': [], 'missing': []}
                else:
                    # seq start with oper, fail
                    if word == 'not':
                        results.append('(')
                        results.append(str(set(minions)))
                        results.append('-')
                        unmatched.append('-')
                    elif word == '(':
                        results.append(word)
                        unmatched.append(word)
                    else:
                        log.error(
                            'Expression may begin with'
                            ' binary operator: {0}'.format(word)
                        )
                        return {'minions': [], 'missing': []}

            elif target_info and target_info['engine']:
                if 'N' == target_info['engine']:
                    # Nodegroups should already be expanded/resolved to other engines
                    log.error('Detected nodegroup expansion failure of "{0}"'.format(word))
                    return {'minions': [], 'missing': []}
                engine = ref.get(target_info['engine'])
                if not engine:
                    # If an unknown engine is called at any time, fail out
                    log.error(
                        'Unrecognized target engine "{0}" for'
                        ' target expression "{1}"'.format(
                            target_info['engine'],
                            word,
                        )
                    )
                    return {'minions': [], 'missing': []}

                engine_args = [target_info['pattern']]
                if target_info['engine'] in ('G', 'P', 'I', 'J'):
                    engine_args.append(target_info['delimiter'] or ':')
                engine_args.append(greedy)

                _results = engine(*engine_args)
                results.append(str(set(_results['minions'])))
                missing.extend(_results['missing'])
                if unmatched and unmatched[-1] == '-':
                    results.append(')')
                    unmatched.pop()

            else:
                # The match is not explicitly defined, evaluate as a glob
                _results = self._check_glob_minions(word, True)
                results.append(str(set(_results['minions'])))
                if unmatched and unmatched[-1] == '-':
                    results.append(')')
                    unmatched.pop()

        # Add a closing ')' for each item left in unmatched
        results.extend([')' for item in unmatched])

        results = ' '.join(results)
        log.debug('Evaluating final compound matching expr: {0}'
                  .format(results))
        try:
            minions = list(eval(results))  # pylint: disable=W0123
            return {'minions': minions, 'missing': missing}
        except Exception:
            log.error('Invalid compound target: {0}'.format(expr))
            return {'minions': [], 'missing': []}

    return {'minions': list(minions),
            'missing': []}

