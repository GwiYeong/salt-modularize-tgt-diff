def nodegroup_comp(nodegroup, nodegroups, skip=None, first_call=True):
    '''
    Recursively expand ``nodegroup`` from ``nodegroups``; ignore nodegroups in ``skip``

    If a top-level (non-recursive) call finds no nodegroups, return the original
    nodegroup definition (for backwards compatibility). Keep track of recursive
    calls via `first_call` argument
    '''
    expanded_nodegroup = False
    if skip is None:
        skip = set()
    elif nodegroup in skip:
        log.error('Failed nodegroup expansion: illegal nested nodegroup "{0}"'.format(nodegroup))
        return ''

    if nodegroup not in nodegroups:
        log.error('Failed nodegroup expansion: unknown nodegroup "{0}"'.format(nodegroup))
        return ''

    nglookup = nodegroups[nodegroup]
    if isinstance(nglookup, six.string_types):
        words = nglookup.split()
    elif isinstance(nglookup, (list, tuple)):
        words = nglookup
    else:
        log.error('Nodegroup \'%s\' (%s) is neither a string, list nor tuple',
                  nodegroup, nglookup)
        return ''

    skip.add(nodegroup)
    ret = []
    opers = ['and', 'or', 'not', '(', ')']
    for word in words:
        if not isinstance(word, six.string_types):
            word = str(word)
        if word in opers:
            ret.append(word)
        elif len(word) >= 3 and word.startswith('N@'):
            expanded_nodegroup = True
            ret.extend(nodegroup_comp(word[2:], nodegroups, skip=skip, first_call=False))
        else:
            ret.append(word)

    if ret:
        ret.insert(0, '(')
        ret.append(')')

    skip.remove(nodegroup)

    log.debug('nodegroup_comp({0}) => {1}'.format(nodegroup, ret))
    # Only return list form if a nodegroup was expanded. Otherwise return
    # the original string to conserve backwards compat
    if expanded_nodegroup or not first_call:
        return ret
    else:
        opers_set = set(opers)
        ret = words
        if (set(ret) - opers_set) == set(ret):
            # No compound operators found in nodegroup definition. Check for
            # group type specifiers
            group_type_re = re.compile('^[A-Z]@')
            if not [x for x in ret if '*' in x or group_type_re.match(x)]:
                # No group type specifiers and no wildcards. Treat this as a
                # list of nodenames.
                joined = 'L@' + ','.join(ret)
                log.debug(
                    'Nodegroup \'%s\' (%s) detected as list of nodenames. '
                    'Assuming compound matching syntax of \'%s\'',
                    nodegroup, ret, joined
                )
                # Return data must be a list of compound matching components
                # to be fed into compound matcher. Enclose return data in list.
                return [joined]

        log.debug(
            'No nested nodegroups detected. Using original nodegroup '
            'definition: %s', nodegroups[nodegroup]
        )
        return ret


'''
Used to check what minions should respond from a target

Note: This is a best-effort set of the minions that would match a target.
Depending on master configuration (grains caching, etc.) and topology (syndics)
the list may be a subset-- but we err on the side of too-many minions in this
'''

