import json
import logging
import typing


def load(source: typing.Union[str, dict]) -> dict:
    """
    If source is a string, a settings object is loaded from the file at the
    specified source path. If source is a dict, the settings object is created
    by deep copying the source object to create a clean copy that has no shared
    connection to the original object.

    :param source: [str, dict]
        Either the path to a settings object to load, or a dictionary to use
        as the settings object. If a dictionary, it will be deep copied to
        create the settings object to prevent corruption by sharing.
    """

    if not isinstance(source, str):
        # Return a deep copy of the configs object to prevent sharing issues
        # between trials
        out = json.loads(json.dumps(source))
    else:
        try:
            with open(source, 'r') as f:
                out = json.load(f)
            out['source_path'] = source
        except Exception:
            logging.getLogger('boarding').exception(
                'Missing or invalid settings file at: "{}"'.format(source)
            )
            raise

    # Default required configuration settings
    fetch_put(out, 'delay', dict())
    fetch_put(out['delay'], 'seating', 0)
    fetch_put(out['delay'], 'interchange', 0)

    summary = out.get('summary')
    if summary and isinstance(summary, (list, tuple)):
        summary = ' '.join(summary)
        out['summary'] = summary

    return out


def fetch_put(source: dict, key: str, default_value = None):
    """
    Fetches the value of the key if such a value exists, otherwise returns the
    default value while assigning that default value to the settings dictionary
    as well

    :param source:
    :param key:
    :param default_value:
    :return:
    """
    if source.get(key) is not None:
        return source[key]

    if default_value is not None:
        source[key] = default_value

    return default_value
