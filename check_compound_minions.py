def check_compound_minions(opts,
                           expr,
                           delimiter,
                           greedy,
                           pillar_exact=False):
    '''
    Return the minions found by looking via compound matcher
    '''
    tgts = salt.loader.tgt(opts)
    if not isinstance(expr, six.string_types) and not isinstance(expr, (list, tuple)):
        log.error('Compound target that is neither string, list nor tuple')
        return {'minions': [], 'missing': []}
    minions = set(pki_minions(opts))
    log.debug('minions: {0}'.format(minions))

    def all_minions():
        '''
        Return a list of all minions that have auth'd
        '''
        mlist = pki_dir_minions(opts)
        return {'minions': mlist, 'missing': []}

    if opts.get('minion_data_cache', False):
        ref = {'G': tgts.grain.check_minions,
               'P': tgts.grain_pcre.check_minions,
               'I': tgts.pillar.check_minions,
               'J': tgts.pillar_pcre.check_minions,
               'L': tgts.list.check_minions,
               'N': None,    # nodegroups should already be expanded
               'S': tgts.ipcidr.check_minions,
               'E': tgts.pcre.check_minions,
               'R': all_minions}
        if pillar_exact:
            ref['I'] = tgts.pillar_exact.check_minions
            ref['J'] = tgts.pillar_exact.check_minions

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
                if target_info['engine'] == 'N':
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

                try:
                    fcall = salt.utils.args.format_call(engine,
                                                        {'expr': target_info['pattern'],
                                                         'delimiter': target_info['delimiter'] or delimiter,
                                                         'greedy': greedy})
                    _results = engine(*fcall['args'], **fcall.get('kwargs', {}))
                except:
                    log.error(('Failed to match available minions with engine: {0} pattern: {1}'
                               .format(target_info['engine'], expr)))
                    return {'minions': [], 'missing':[]}
                results.append(str(set(_results['minions'])))
                missing.extend(_results['missing'])
                if unmatched and unmatched[-1] == '-':
                    results.append(')')
                    unmatched.pop()

            else:
                # The match is not explicitly defined, evaluate as a glob
                _results = tgts.glob.check_minions(word)
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


