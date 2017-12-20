def _match_check(regex, fun):
    '''
    Validate a single regex to function comparison, the function argument
    can be a list of functions. It is all or nothing for a list of
    functions
    '''
    vals = []
    if isinstance(fun, six.string_types):
        fun = [fun]
    for func in fun:
        try:
            if re.match(regex, func):
                vals.append(True)
            else:
                vals.append(False)
        except Exception:
            log.error('Invalid regular expression: {0}'.format(regex))
    return vals and all(vals)

