import re

# adapated from https://gist.github.com/carlsmith/b2e6ba538ca6f58689b4c18f46fef11c
def _simultaneous_replace(string, substitutions, reverse=False):
    if reverse :
        return _simultaneous_replace(string, dict(
            (v,k) for k, v in substitutions.items()
        ))
    substrings = sorted(substitutions, key=len, reverse=True)
    regex = re.compile('|'.join(map(re.escape, substrings)))
    return regex.sub(lambda match: substitutions[match.group(0)], string)
_PATH_REPLACEMENTS = {
    '/': '_-',
    '_': '__',
}
def encode_path(path):
    '''
        Encode a url path so that is has no '/' characters, and can be used as a single segment in the path of another url.

        Note that standard url-encoding (replacing '/' with '%2F') won't work, because Django (or is it Apache?) decodes these into '/' before passing off to the url matching machinery.
    '''
    return _simultaneous_replace(path, _PATH_REPLACEMENTS)
def decode_path(path):
    '''
        Inverse operation of encode_path()
    '''
    return _simultaneous_replace(path, _PATH_REPLACEMENTS, reverse=True)