def parse_target(target_expression):
    '''Parse `target_expressing` splitting it into `engine`, `delimiter`,
     `pattern` - returns a dict'''

    match = TARGET_REX.match(target_expression)
    if not match:
        log.warning('Unable to parse target "{0}"'.format(target_expression))
        ret = {
            'engine': None,
            'delimiter': None,
            'pattern': target_expression,
        }
    else:
        ret = match.groupdict()
    return ret


