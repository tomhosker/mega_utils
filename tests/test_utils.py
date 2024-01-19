"""
This code tests the utils module.
"""

# Standard imports.
import shutil
from pathlib import Path
from unittest.mock import Mock, patch

# Source imports.
from source.utils import (
    GetReturnCode,
    mega_login,
    mega_logout,
    mega_sync,
    mega_get_dir,
    mega_get
)

###########
# TESTING #
###########

@patch("source.utils.getpass", Mock(return_value="password"))
@patch("source.utils.run_mega_command", Mock(return_value=True))
def test_mega_login():
    """ Test the function runs. """
    assert mega_login("username")

@patch("source.utils.run_mega_command", Mock(return_value=True))
def test_mega_logout():
    """ Test the function runs. """
    assert mega_logout()

@patch("source.utils.run_mega_command", Mock(return_value=True))
def test_mega_sync():
    """ Test the function runs. """
    assert mega_sync("here", "there")

@patch("source.utils.get_yes_no")
@patch("source.utils.run_mega_command")
def test_mega_get_dir(run_mock, yes_no_mock):
    """ Test the function runs. """
    path_to_local_test_folder = "local_test_folder"
    path_obj_to_local_test_folder = Path(path_to_local_test_folder)
    shutil.rmtree(path_to_local_test_folder, ignore_errors=True)
    run_mock.return_value = True
    # Test folder does NOT already exist.
    result = mega_get_dir("here", path_to_local_test_folder)
    assert result == GetReturnCode.SUCCESS
    shutil.rmtree(path_to_local_test_folder)
    # Test folder already exists; delete.
    yes_no_mock.return_value = True
    path_obj_to_local_test_folder.mkdir()
    result = mega_get_dir("here", path_to_local_test_folder)
    assert result == GetReturnCode.SUCCESS
    shutil.rmtree(path_to_local_test_folder)
    # Test folder already exists; keep.
    yes_no_mock.return_value = False
    path_obj_to_local_test_folder.mkdir()
    result = mega_get_dir("here", path_to_local_test_folder)
    assert result == GetReturnCode.PRESENT
    shutil.rmtree(path_to_local_test_folder)
    # Test folder already exists; auto delete.
    path_obj_to_local_test_folder.mkdir()
    result = mega_get_dir("here", path_to_local_test_folder, auto_delete=True)
    assert result == GetReturnCode.SUCCESS
    shutil.rmtree(path_to_local_test_folder)
    # Test folder already exists; auto keep.
    path_obj_to_local_test_folder.mkdir()
    result = mega_get_dir("here", path_to_local_test_folder, auto_keep=True)
    assert result == GetReturnCode.PRESENT
    shutil.rmtree(path_to_local_test_folder)
    # Test Mega returns non-zero exit code.
    run_mock.return_value = False
    result = mega_get_dir("here", path_to_local_test_folder)
    assert result == GetReturnCode.FAILURE

@patch("source.utils.run_mega_command")
def test_mega_get(run_mock):
    """ Test the function runs. """
    path_to_local_test_file = "local_test_file.txt"
    path_obj_to_local_test_file = Path(path_to_local_test_file)
    path_obj_to_local_test_file.unlink(missing_ok=True)
    run_mock.return_value = True
    # Test file does NOT already exist.
    result = mega_get("here", path_to_local_test_file)
    assert result == GetReturnCode.SUCCESS
    # Test file already exists.
    path_obj_to_local_test_file.touch()
    result = mega_get("here", path_to_local_test_file)
    assert result == GetReturnCode.PRESENT
    path_obj_to_local_test_file.unlink()
    # Test Mega returns non-zero exit code.
    run_mock.return_value = False
    result = mega_get("here", path_to_local_test_file)
    assert result == GetReturnCode.FAILURE
