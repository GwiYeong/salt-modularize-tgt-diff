def auth_check_expanded(self,
                        auth_list,
                        funs,
                        args,
                        tgt,
                        tgt_type='glob',
                        groups=None,
                        publish_validate=False):

    # Here's my thinking
    # 1. Retrieve anticipated targeted minions
    # 2. Iterate through each entry in the auth_list
    # 3. If it is a minion_id, check to see if any targeted minions match.
    #    If there is a match, check to make sure funs are permitted
    #    (if it's not a match we don't care about this auth entry and can
    #     move on)
    #    a. If funs are permitted, Add this minion_id to a new set of allowed minion_ids
    #       If funs are NOT permitted, can short-circuit and return FALSE
    #    b. At the end of the auth_list loop, make sure all targeted IDs
    #       are in the set of allowed minion_ids.  If not, return FALSE
    # 4. If it is a target (glob, pillar, etc), retrieve matching minions
    #    and make sure that ALL targeted minions are in the set.
    #    then check to see if the funs are permitted
    #    a. If ALL targeted minions are not in the set, then return FALSE
    #    b. If the desired fun doesn't mass the auth check with any
    #       auth_entry's fun, then return FALSE

    # NOTE we are not going to try to allow functions to run on partial
    # sets of minions.  If a user targets a group of minions and does not
    # have access to run a job on ALL of these minions then the job will
    # fail with 'Eauth Failed'.

    # The recommended workflow in that case will be for the user to narrow
    # his target.

    # This should cover adding the AD LDAP lookup functionality while
    # preserving the existing auth behavior.

    # Recommend we config-get this behind an entry called
    # auth.enable_expanded_auth_matching
    # and default to False
    v_tgt_type = tgt_type
    if tgt_type.lower() in ('pillar', 'pillar_pcre'):
        v_tgt_type = 'pillar_exact'
    elif tgt_type.lower() == 'compound':
        v_tgt_type = 'compound_pillar_exact'
    _res = self.check_minions(tgt, v_tgt_type)
    v_minions = set(_res['minions'])

    _res = self.check_minions(tgt, tgt_type)
    minions = set(_res['minions'])

    mismatch = bool(minions.difference(v_minions))
    # If the non-exact match gets more minions than the exact match
    # then pillar globbing or PCRE is being used, and we have a
    # problem
    if publish_validate:
        if mismatch:
            return False
    # compound commands will come in a list so treat everything as a list
    if not isinstance(funs, list):
        funs = [funs]
        args = [args]

    # Take the auth list and get all the minion names inside it
    allowed_minions = set()

    auth_dictionary = {}

    # Make a set, so we are guaranteed to have only one of each minion
    # Also iterate through the entire auth_list and create a dictionary
    # so it's easy to look up what functions are permitted
    for auth_list_entry in auth_list:
        if isinstance(auth_list_entry, six.string_types):
            for fun in funs:
                # represents toplevel auth entry is a function.
                # so this fn is permitted by all minions
                if self.match_check(auth_list_entry, fun):
                    return True
            continue
        if isinstance(auth_list_entry, dict):
            if len(auth_list_entry) != 1:
                log.info('Malformed ACL: {0}'.format(auth_list_entry))
                continue
        allowed_minions.update(set(auth_list_entry.keys()))
        for key in auth_list_entry:
            for match in self._expand_matching(key):
                if match in auth_dictionary:
                    auth_dictionary[match].extend(auth_list_entry[key])
                else:
                    auth_dictionary[match] = auth_list_entry[key]

    allowed_minions_from_auth_list = set()
    for next_entry in allowed_minions:
        allowed_minions_from_auth_list.update(self._expand_matching(next_entry))
    # 'minions' here are all the names of minions matched by the target
    # if we take out all the allowed minions, and there are any left, then
    # the target includes minions that are not allowed by eauth
    # so we can give up here.
    if len(minions - allowed_minions_from_auth_list) > 0:
        return False

    try:
        for minion in minions:
            results = []
            for num, fun in enumerate(auth_dictionary[minion]):
                results.append(self.match_check(fun, funs))
            if not any(results):
                return False
        return True

    except TypeError:
        return False
    return False

