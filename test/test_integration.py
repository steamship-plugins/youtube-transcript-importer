"""Test youtube-transcri-importer via integration tests."""

from steamship import File, Steamship, MimeTypes

from test import TEST_URL

FILE_IMPORTER_HANDLE = "youtube-transcript-importer"
ENVIRONMENT = "prod"


def test_file_importer() -> None:
    with Steamship.temporary_workspace(profile=ENVIRONMENT) as client:
        plugin_instance = client.use_plugin(
            plugin_handle=FILE_IMPORTER_HANDLE,
        )

        assert plugin_instance is not None
        assert plugin_instance.id is not None

        file_creation_task = File.create_with_plugin(
            client, plugin_instance=plugin_instance.handle, url=TEST_URL
        )
        file_creation_task.wait()
        file = file_creation_task.output
        _validate_file(file)


def _validate_file(file: File) -> None:
    raw_data = file.raw()
    assert raw_data is not None
    assert isinstance(raw_data, bytes)
    assert file.mime_type == MimeTypes.TXT
