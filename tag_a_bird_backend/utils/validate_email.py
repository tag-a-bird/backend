import validate_email

def check_email(email_typed_in):
    return validate_email(
    email_address=email_typed_in,
    check_format=True,
    check_blacklist=True,
    check_dns=True,
    dns_timeout=10,
    # check_smtp=True,
    # smtp_timeout=10,
    # smtp_helo_host='my.host.name',
    # smtp_from_address='my@from.addr.ess',
    # smtp_skip_tls=False,
    # smtp_tls_context=None,
    # smtp_debug=False,
    )