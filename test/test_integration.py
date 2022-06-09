"""Test zendesk-file-importer via integration tests."""
import json
from datetime import datetime, timedelta
from test.test_unit import _load_config

from steamship import File, MimeTypes, Plugin, PluginInstance, Steamship
from zenpy import Zenpy

FILE_IMPORTER_HANDLE = "zendesk-file-importer"
ENVIRONMENT = "staging"


def _get_steamship_client():
    return Steamship(profile=ENVIRONMENT)


def _get_plugin_instance(config) -> PluginInstance:
    client = _get_steamship_client()

    plugin = Plugin.get(client, FILE_IMPORTER_HANDLE).data
    assert plugin is not None
    assert plugin.id is not None
    plugin_instance = PluginInstance.create(
        client,
        plugin_handle=FILE_IMPORTER_HANDLE,
        upsert=False,
        plugin_id=plugin.id,
        config=config,
    ).data
    assert plugin_instance is not None
    assert plugin_instance.id is not None
    return plugin_instance


def test_file_importer():
    """Test the Zendesk File Importer via an integration test."""
    client = _get_steamship_client()
    n_tickets = 20
    config = _load_config(n_tickets, datetime.today() - timedelta(weeks=4), datetime.today())

    importer = _get_plugin_instance(config=config)

    file = File.create(client, plugin_instance=importer.handle)
    file.wait()
    file = file.data
    file_raw_data = file.raw().data
    _test_response(n_tickets, file, file_raw_data)


def test_file_importer_all_tickets():
    """Test the Zendesk File Importer via an integration test."""
    client = _get_steamship_client()
    n_tickets = -1
    config = _load_config(n_tickets, datetime.today() - timedelta(weeks=4), datetime.today())

    importer = _get_plugin_instance(config=config)

    file = File.create(client, plugin_instance=importer.handle)
    file.wait()
    file = file.data
    file_raw_data = file.raw().data

    zendesk_credentials = {
        "email": config["zendesk_email"],
        "password": config["zendesk_password"],
        "subdomain": config["zendesk_subdomain"],
    }

    zenpy_client = Zenpy(**zendesk_credentials)
    n_tickets = zenpy_client.tickets().count
    _test_response(n_tickets, file, file_raw_data)


def test_file_importer_all_tickets_api_parameters():
    """Test the Zendesk File Importer via an integration test."""
    # TODO (enias): Not supported by Steamship yet


def _test_response(n_tickets, file, file_raw_data):
    assert file_raw_data is not None
    assert isinstance(file_raw_data, bytes)
    result = json.loads(file_raw_data)
    assert len(result) == n_tickets
    assert file.mime_type == MimeTypes.JSON
