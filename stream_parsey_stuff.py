"""
I just ended up writing a REALLY slow, very limited *ML parser, possibly because I was too annoyed to read the docs of
the better solutions and because I though "just grab <pre></pre> how hard can it be."
"""


def endswith_sans_whitespace(char_seq, string, test_lenght=None, ignore_case=True):
    """Strip whitespaces from char_seq and test if it ends with "string".

    Since char_seq can potentially be very long, test_lenght can be specified to limit the lenght of char_seq that is
    evaluated. Note that test_lenght is applied *before* whitespaces are removed.

    str's native "isspace" and "endswith" are used. Among other things, this means that all strings end with the empty
    string.
    """

    if test_lenght is not None:
        char_seq = char_seq[-test_lenght:]
    char_seq = list(char_seq)
    char_seq = [c for c in char_seq if not c.isspace()]
    char_seq = ''.join(char_seq)
    if ignore_case:
        char_seq = char_seq.lower()
        string = string.lower()
    if char_seq.endswith(string):
        return True
    else:
        return False

def get_pre_tag_content_from_subnetwork_text(html):
    read_chars = []
    subnet_listing = []
    inside_of_pre = False
    for char in html:
        read_chars.append(char)
        if inside_of_pre:
            subnet_listing.append(char)
        if endswith_sans_whitespace(read_chars, '<pre>'):
            inside_of_pre = True
        if endswith_sans_whitespace(read_chars, '</pre>'):
            subnet_listing = ''.join(subnet_listing)
            begin_of_tag = subnet_listing.rindex('<')
            subnet_listing = subnet_listing[:begin_of_tag]
            return subnet_listing
    else:
        pass  # raise an exception???


if __name__ == '__main__':
    html = open('/tmp/subnet_raw_html', 'r').read()
    print get_pre_tag_content_from_subnetwork_text(html)
