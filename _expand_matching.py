def _expand_matching(opts, auth_entry):
    ref = {'G': 'grain',
           'P': 'grain_pcre',
           'I': 'pillar',
           'J': 'pillar_pcre',
           'L': 'list',
           'S': 'ipcidr',
           'E': 'pcre',
           'N': 'node',
           None: 'glob'}

    target_info = parse_target(auth_entry)
    if not target_info:
        log.error('Failed to parse valid target "{0}"'.format(auth_entry))

    v_matcher = ref.get(target_info['engine'])
    v_expr = target_info['pattern']

    _res = check_minions(opts, v_expr, v_matcher)
    return set(_res['minions'])

