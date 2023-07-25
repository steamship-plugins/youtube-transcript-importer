import logging
from typing import Dict, Any

from langchain.document_loaders import YoutubeLoader
from steamship import Tag, MimeTypes
from steamship.base.error import SteamshipError
from steamship.invocable import InvocableResponse
from steamship.plugin.file_importer import FileImporter
from steamship.plugin.inputs.file_import_plugin_input import FileImportPluginInput
from steamship.plugin.outputs.raw_data_plugin_output import RawDataPluginOutput
from steamship.plugin.request import PluginRequest


def metadata_to_tags(metadata: Dict[str, Any]):
    return [Tag(kind=k, name=v) for k, v in metadata.items()]


class YoutubeTranscriptFileImporter(FileImporter):
    """File Importer that downloads the transcripts of Youtube videos."""

    def run(
            self, request: PluginRequest[FileImportPluginInput]
    ) -> InvocableResponse[RawDataPluginOutput]:
        """Import the audio from Youtube videos a Steamship file.

        Each file contains a raw binary containing the audio.
        """
        youtube_url = request.data.url

        try:
            document = YoutubeLoader.from_youtube_url(
                youtube_url, add_video_info=True
            ).load()[0]

        except Exception as e:
            logging.error(e)
            raise SteamshipError(
                message="There was an error downloading the transcript from the given Youtube URL.",
                error=e,
            )

        return InvocableResponse(
            data=RawDataPluginOutput(string=document.page_content,
                                     mime_type=MimeTypes.TXT,
                                     tags=metadata_to_tags(document.metadata))
        )
