"""Test youtube-file-importer via integration tests."""

from test.test_unit import load_config
from test.utils import TEST_URL

import pytest
from steamship import File, PluginInstance, Steamship

FILE_IMPORTER_HANDLE = "youtube-file-importer"
ENVIRONMENT = "prod"


@pytest.fixture
def youtube_importer() -> PluginInstance:
    """Instantiate a youtube file importer."""
    ship = Steamship(profile=ENVIRONMENT)
    config = load_config()

    plugin_instance = ship.use_plugin(
        plugin_handle=FILE_IMPORTER_HANDLE,
        config=config,
    )

    assert plugin_instance is not None
    assert plugin_instance.id is not None
    return plugin_instance


def test_file_importer(youtube_importer: PluginInstance) -> None:
    """Test the Youtube File Importer via an integration test."""
    client = Steamship(profile=ENVIRONMENT)

    file_creation_task = File.create_with_plugin(
        client, plugin_instance=youtube_importer.handle, url=TEST_URL
    )
    file_creation_task.wait()
    file = file_creation_task.output
    _validate_file(file)


def _validate_file(file: File) -> None:
    raw_data = file.raw()
    assert raw_data is not None
    assert isinstance(raw_data, bytes)
    assert file.mime_type in ("audio/mp4", "audio/webm")
