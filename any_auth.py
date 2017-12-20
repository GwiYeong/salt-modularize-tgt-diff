def any_auth(self, form, auth_list, fun, arg, tgt=None, tgt_type='glob'):
    '''
    Read in the form and determine which auth check routine to execute
    '''
    # This function is only called from salt.auth.Authorize(), which is also
    # deprecated and will be removed in Neon.
    salt.utils.versions.warn_until(
        'Neon',
        'The \'any_auth\' function has been deprecated. Support for this '
        'function will be removed in Salt {version}.'
    )
    if form == 'publish':
        return self.auth_check(
                auth_list,
                fun,
                arg,
                tgt,
                tgt_type)
    return self.spec_check(
            auth_list,
            fun,
            arg,
            form)

