"""Example Steamship Importer Plugin.

An Importer is responsible for fetching data for import into the Steamship platform.
"""
import json
from datetime import datetime

from steamship import MimeTypes
from steamship.app import App, Response, post, create_handler
from steamship.base.error import SteamshipError
from steamship.plugin.file_importer import FileImporter
from steamship.plugin.inputs.file_import_plugin_input import FileImportPluginInput
from steamship.plugin.outputs.raw_data_plugin_output import RawDataPluginOutput
from steamship.plugin.service import PluginRequest
from zenpy import Zenpy


class FileImporterPlugin(FileImporter, App):
    """"Example Steamship File Importer plugin."""

    def run(self, request: PluginRequest[FileImportPluginInput]) -> Response[RawDataPluginOutput]:
        """Imports ZenDesk tickets."""

        n_tickets = int(self.config["n_tickets"])
        t_start = datetime.strptime(self.config["t_start"], '%d/%m/%y %H:%M:%S')
        t_end = datetime.strptime(self.config["t_end"], '%d/%m/%y %H:%M:%S')
        zendesk_credentials = {
            "email": self.config["zendesk_email"],
            "password": self.config["zendesk_password"],
            "subdomain": self.config["zendesk_subdomain"],
        }

        zenpy_client = Zenpy(**zendesk_credentials)

        try:
            tickets = []
            for ix, ticket in enumerate(zenpy_client.tickets(created_between=[t_start, t_end])):
                if ix > n_tickets:
                    break
                tickets.append(ticket.to_dict())
            # data = json.dumps([{"description": "this is a test", "priority": "high"} for _ in range(20)])
            data = json.dumps(tickets)
        except Exception as error:
            raise SteamshipError(message="There was an error ingesting the support tickets from Zendesk.", error=error)

        return Response(data=RawDataPluginOutput(string=data, mime_type=MimeTypes.JSON))


handler = create_handler(FileImporterPlugin)
