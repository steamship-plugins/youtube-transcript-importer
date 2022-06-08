"""File Importer for Zendesk tickets.

Import zendesk tickets to a single file where each block represents a ticket.
"""
import json
from datetime import datetime

from steamship import MimeTypes
from steamship.app import Response, create_handler
from steamship.base.error import SteamshipError
from steamship.plugin.file_importer import FileImporter
from steamship.plugin.inputs.file_import_plugin_input import FileImportPluginInput
from steamship.plugin.outputs.raw_data_plugin_output import RawDataPluginOutput
from steamship.plugin.service import PluginRequest
from zenpy import Zenpy

DATETIME_FORMAT = "%d/%m/%y %H:%M:%S"


class ZendeskFileImporter(FileImporter):
    """File Importer for Zendesk tickets.

    Attributes
    ----------
    config : Dict[str, Any]
        A dictionary containing the values for the following required configuration variables:
        - n_tickets : int
            The number of tickets that you want to scrape.
        - t_start : datetime.datetime
            The start timestamp used to query Zendesk tickets.
        - t_end : datetime.datetime
            The end timestamp used to query Zendesk tickets
        - zendesk_email : str
            Email used to authenticate with Zendesk.
        - zendesk_password : str
            Password used to authenticate with Zendesk.
        - zendesk_subdomain : str
            Subdomain used to authenticate with Zendesk.
    """

    def run(self, request: PluginRequest[FileImportPluginInput]) -> Response[RawDataPluginOutput]:
        """Import zendesk tickets to an archive file.

        Each file represents an archive collecting tickets using blocks.
        """
        n_tickets = int(self.config["n_tickets"])
        t_start = datetime.strptime(self.config["t_start"], DATETIME_FORMAT)
        t_end = datetime.strptime(self.config["t_end"], DATETIME_FORMAT)
        zendesk_credentials = {
            "email": self.config["zendesk_email"],
            "password": self.config["zendesk_password"],
            "subdomain": self.config["zendesk_subdomain"],
        }

        try:
            zenpy_client = Zenpy(**zendesk_credentials)
            tickets = []
            tickets_iterator = zenpy_client.tickets(created_between=[t_start, t_end])
            ix = 0
            while ix < n_tickets:
                tickets.append(next(tickets_iterator).to_dict())
                ix += 1

        except Exception as error:
            raise SteamshipError(
                message="There was an error ingesting the support tickets from Zendesk.",
                error=error,
            )

        return Response(
            data=RawDataPluginOutput(string=json.dumps(tickets), mime_type=MimeTypes.JSON)
        )


handler = create_handler(ZendeskFileImporter)
