import base64
import configparser
import json
from datetime import datetime, timedelta

from steamship import MimeTypes
from steamship.data.file import File
from steamship.plugin.service import PluginRequest

from src.api import FileImporterPlugin

from test import TEST_DATA


def test_zendesk_import():
    n_tickets = 20
    t_end = datetime.today()
    t_start = t_end - timedelta(weeks=4)

    config = json.load((TEST_DATA / "config.json").open())

    config = {
        "n_tickets": n_tickets,
        "t_start": t_start.strftime('%d/%m/%y %H:%M:%S'),
        "t_end": t_start.strftime('%d/%m/%y %H:%M:%S'),
        **config
    }
    importer = FileImporterPlugin(config=config)

    request = PluginRequest(data=File.CreateRequest())  # TODO (enias): It is weird I have to create a file here
    response_run = importer.run(request)

    response_endpoint = importer.run_endpoint(**request.to_dict())

    _test_response(n_tickets, response_run)
    _test_response(n_tickets, response_endpoint)


def _test_response(n_tickets, response_run):
    assert response_run.data is not None
    result = json.loads(base64.b64decode(response_run.data.data))
    assert len(result) == n_tickets
    assert response_run.data.mimeType == MimeTypes.JSON
