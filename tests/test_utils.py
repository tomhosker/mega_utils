"""
This code tests the utils module.
"""

# Standard imports.
from unittest.mock import Mock, patch

# Source imports.
from source.utils import (
    mega_login,
    mega_logout,
    mega_sync,
    mega_get
)

###########
# TESTING #
###########

@patch("source.utils.getpass", Mock(return_value="password"))
@patch("source.utils.run_mega_command", Mock(return_value=True))
def test_full_run():
    """ Test that the functions run without crashing. """
    mega_login("username")
    mega_sync("local/path", "remote/path")
    mega_get("url", "local/path")
    mega_logout()
