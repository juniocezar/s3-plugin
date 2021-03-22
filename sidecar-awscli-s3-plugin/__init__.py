import os
import warnings


PROXY = 'proxy'
COMMANDS = ['s3', 's3api']
VERIFY_SSL = 'verify_ssl'
CA_BUNDLE = 'ca_bundle'

def str2bool(value):
    return str(value).lower() in ['1', 'yes', 'y', 'true', 'on']


def get_ca_bundle_from_profile(profile, command):
    return profile.get(command, {}).get(CA_BUNDLE)

def get_verify_from_profile(profile, command):
    verify = True
    if command in profile:
        if VERIFY_SSL in profile[command]:
            verify = str2bool(profile[command][VERIFY_SSL])
    return verify

def set_verify_from_profile(parsed_args, **kwargs):
    verify_ssl = parsed_args.verify_ssl
    command = parsed_args.command
    # By default verify_ssl is set to true
    # if --no-verify-ssl is specified, parsed_args.verify_ssl is False
    # so keep it
    if verify_ssl:
        session = kwargs['session']
        # Set profile to session so we can load profile from config
        if parsed_args.profile:
            session.set_config_variable('profile', parsed_args.profile)
        service_verify = get_verify_from_profile(session.get_scoped_config(), command)
        if service_verify is not None:
            parsed_args.verify_ssl = service_verify
            if not service_verify:
                warnings.filterwarnings('ignore', 'Unverified HTTPS request')

def set_ca_bundle_from_profile(parsed_args, **kwargs):
    # Respect command line arg if present
    if parsed_args.ca_bundle:
        return

    command = parsed_args.command
    session = kwargs['session']
    # Set profile to session so we can load profile from config
    if parsed_args.profile:
        session.set_config_variable('profile', parsed_args.profile)
    parsed_args.ca_bundle = get_ca_bundle_from_profile(session.get_scoped_config(), command)

def get_proxy_from_profile(profile, command):
    proxy = None

    if command in profile:
        if PROXY in profile[command]:
            proxy = profile[command][PROXY]

    return proxy

def set_proxy_from_profile(parsed_args, **kwargs):
    command = parsed_args.command
    session = kwargs['session']

    if parsed_args.profile:
        session.set_config_variable('profile', parsed_args.profile)

    service_proxy = get_proxy_from_profile(session.get_scoped_config(), command)

    if (service_proxy is not None) and (command in COMMANDS):
        print('[plugin] Detected command: ' + command)
        print('[plugin] Using Sidecar: ' + service_proxy + "\n")

        os.environ['http_proxy'] = service_proxy
        os.environ['https_proxy'] = service_proxy
        os.environ['HTTP_PROXY'] = service_proxy
        os.environ['HTTPS_PROXY'] = service_proxy
        os.environ['NO_PROXY'] = '169.254.169.254'

def awscli_initialize(cli):
    cli.register('top-level-args-parsed', set_proxy_from_profile)
    cli.register('top-level-args-parsed', set_verify_from_profile)
    cli.register('top-level-args-parsed', set_ca_bundle_from_profile)
