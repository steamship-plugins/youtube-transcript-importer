"""Test youtube-file-importer via unit tests."""

from steamship import Steamship, MimeTypes
from steamship.plugin.inputs.file_import_plugin_input import FileImportPluginInput
from steamship.plugin.request import PluginRequest

from src.api import YoutubeTranscriptFileImporter
from test import TEST_URL


def test_import():
    """Unit test the Youtube File Importer without triggering edge cases."""
    with Steamship.temporary_workspace() as client:
        importer = YoutubeTranscriptFileImporter(client=client)

        request = PluginRequest(data=FileImportPluginInput(url=TEST_URL))
        response_run = importer.run(request)
        _test_response(response_run)

        response_endpoint = importer.run_endpoint(**request.dict())
        _test_response(response_endpoint)


def _test_response(response):
    assert response.data is not None
    response_data = response.data
    assert response_data.data is not None
    assert response_data.mime_type == MimeTypes.TXT
