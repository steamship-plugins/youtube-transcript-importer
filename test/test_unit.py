"""Test zendesk-file-importer via unit tests."""
import base64
import json
from datetime import datetime, timedelta
from test import TEST_DATA
from typing import Any, Dict

import pytest
from steamship import MimeTypes
from steamship.base.error import SteamshipError
from steamship.plugin.inputs.file_import_plugin_input import FileImportPluginInput
from steamship.plugin.service import PluginRequest
from zenpy import Zenpy

from src.api import DATETIME_FORMAT, ZendeskFileImporter


def _load_config(n_tickets: int, t_start: datetime, t_end: datetime) -> Dict[str, Any]:
    config = json.load((TEST_DATA / "config.json").open())
    return {
        "n_tickets": n_tickets,
        "t_start": t_start.strftime(DATETIME_FORMAT),
        "t_end": t_end.strftime(DATETIME_FORMAT),
        **config,
    }


def test_zendesk_import():
    """Unit test the Zendesk File Importer without triggering edge cases."""
    n_tickets = 20
    config = _load_config(n_tickets, datetime.today() - timedelta(weeks=4), datetime.today())
    importer = ZendeskFileImporter(config=config)

    request = PluginRequest(data=FileImportPluginInput())
    response_run = importer.run(request)
    _test_response(n_tickets, response_run.data)

    response_endpoint = importer.run_endpoint(**request.dict())
    _test_response(n_tickets, response_endpoint.data)


def test_zendesk_import_no_tickets_found():
    """Unit test the Zendesk File Importer without any tickets."""
    n_tickets = 0
    config = _load_config(n_tickets, datetime.today() - timedelta(weeks=4), datetime.today())
    importer = ZendeskFileImporter(config=config)

    request = PluginRequest(data=FileImportPluginInput())
    response_run = importer.run(request)
    _test_response(n_tickets, response_run.data)

    response_endpoint = importer.run_endpoint(**request.dict())
    _test_response(n_tickets, response_endpoint.data)


def test_zendesk_import_all_tickets():
    """Unit test the Zendesk File Importer without any tickets."""
    n_tickets = -1

    config = _load_config(n_tickets, datetime.today() - timedelta(weeks=4), datetime.today())
    importer = ZendeskFileImporter(config=config)

    request = PluginRequest(data=FileImportPluginInput())
    response_run = importer.run(request)

    zendesk_credentials = {
        "email": config["zendesk_email"],
        "password": config["zendesk_password"],
        "subdomain": config["zendesk_subdomain"],
    }

    zenpy_client = Zenpy(**zendesk_credentials)
    n_tickets = zenpy_client.tickets().count
    _test_response(n_tickets, response_run.data)

    response_endpoint = importer.run_endpoint(**request.dict())
    _test_response(n_tickets, response_endpoint.data)


def test_zendesk_import_inverse_dates():
    """Unit test the Zendesk File Importer with swapping t_start and t_end."""
    n_tickets = 20
    config = _load_config(n_tickets, datetime.today(), datetime.today() - timedelta(weeks=4))
    importer = ZendeskFileImporter(config=config)

    request = PluginRequest(data=FileImportPluginInput())
    response_run = importer.run(request)
    _test_response(n_tickets, response_run.data)

    response_endpoint = importer.run_endpoint(**request.dict())
    _test_response(n_tickets, response_endpoint.data)


def test_zendesk_import_invalid_credentials():
    """Unit test the Zendesk File Importer with invalid Zendesk credentials."""
    config = _load_config(20, datetime.today() - timedelta(weeks=4), datetime.today())
    config["zendesk_email"] = "INCORRECT"
    importer = ZendeskFileImporter(config=config)

    request = PluginRequest(data=FileImportPluginInput())
    with pytest.raises(SteamshipError):
        _ = importer.run(request)

    with pytest.raises(SteamshipError):
        _ = importer.run_endpoint(**request.dict())


def test_zendesk_import_api_parameters():
    """Unit test the Zendesk File Importer without triggering edge cases."""
    n_tickets = 40
    config = _load_config(0, datetime.today() - timedelta(weeks=4), datetime.today())
    importer = ZendeskFileImporter(config=config)

    request = PluginRequest(data=FileImportPluginInput())
    response_endpoint = importer.run_endpoint(**request.dict(), n_tickets=n_tickets)
    _test_response(n_tickets, response_endpoint.data)


def _test_response(n_tickets, file_data):
    assert file_data is not None
    result = json.loads(base64.b64decode(file_data.data))
    assert len(result) == n_tickets
    assert file_data.mime_type == MimeTypes.JSON
