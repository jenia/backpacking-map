from unittest import mock

import app.config as conf


def test_get_config():
    expectedConfig = conf.Config(environ="DEBUG")
    yaml0 = """
        environ: "DEBUG"
    """

    with mock.patch('builtins.open', mock.mock_open(read_data=yaml0)):
        confGot = conf.config()

    assert confGot.environ == expectedConfig.environ
