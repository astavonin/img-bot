def shorten_string(text, max_len=18):
    no_newline = text.replace('\n', ' ').replace('\r', '')
    postfix = "..."
    if len(no_newline) > max_len:
        return no_newline[:max_len - len(postfix)] + postfix
    else:
        return no_newline


def get_or(data, key, default=None):
    if data is None:
        return default
    else:
        return data[key] if key in data else default
