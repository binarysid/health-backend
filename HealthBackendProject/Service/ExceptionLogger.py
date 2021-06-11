import sentry_sdk

def track(e:Exception):
    sentry_sdk.capture_exception(e)
