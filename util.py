import jinja2


def js_format_datetime(timestamp):
    # Append a Z to the timestamp, to indicate that this string is in UTC. For some
    # inexplicable reason, JS decides that it is local time otherwise. *sigh*
    # We also provide a noscript tag for people who disable javascript.
    date = "datefns.format('{0}Z', 'MMMM Do YYYY, HH:mm:ss')".format(timestamp)
    script = "<script>document.write({0});</script>".format(date)
    noscript = "<noscript>{0} UTC</noscript>".format(timestamp.strftime("%Y-%m-%d %H:%M:%S"))
    return jinja2.Markup("".join([script, noscript]))