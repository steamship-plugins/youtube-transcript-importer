"""File Importer for Youtube videos.

Import the audio of Youtube video's to a file.
"""
import io
import logging
from typing import Type

from pytube import YouTube
from steamship.base.error import SteamshipError
from steamship.invocable import Config, InvocableResponse, create_handler
from steamship.plugin.file_importer import FileImporter
from steamship.plugin.inputs.file_import_plugin_input import FileImportPluginInput
from steamship.plugin.outputs.raw_data_plugin_output import RawDataPluginOutput
from steamship.plugin.request import PluginRequest


class YoutubeFileImporter(FileImporter):
    """File Importer for Youtube videos."""

    def config_cls(self) -> Type[Config]:
        """Config class used to create a YoutubeFileImporter."""
        return Config

    def run(
        self, request: PluginRequest[FileImportPluginInput]
    ) -> InvocableResponse[RawDataPluginOutput]:
        """Import the audio from Youtube videos a Steamship file.

        Each file contains a raw binary containing the audio.
        """
        youtube_url = request.data.url

        try:
            yt = YouTube(youtube_url)
            audio_stream = sorted(
                yt.streams.filter(only_audio=True), key=lambda x: -int(x.abr[:-4])
            )[0]
            stream = yt.streams.get_by_itag(audio_stream.itag)
            buffer = io.BytesIO()
            stream.stream_to_buffer(buffer)
            buffer.seek(0)

        except Exception as e:
            logging.error(e)
            raise SteamshipError(
                message="There was an error downloading the audio stream from the given Youtube URL.",
                error=e,
            )

        return InvocableResponse(
            data=RawDataPluginOutput(_bytes=buffer, mime_type=audio_stream.mime_type)
        )


handler = create_handler(YoutubeFileImporter)
