# Youtube Transcript Importer

This plugin imports the transcript from Youtube videos.

## Getting Started

### Usage

Once deployed, the Youtube Importer can be used with the handle `youtube-transcript-importer`.

```python
from steamship import File, Steamship

IMPORTER_HANDLE = "youtube-transcript-importer"
ship = Steamship()

plugin_instance = ship.use_plugin(
    plugin_handle=IMPORTER_HANDLE
)
file_creation_task = File.create_with_plugin(ship, plugin_instance=plugin_instance.handle, URL="YOUR_URL")
file_creation_task.wait()
audio_bytes = file_creation_task.output.raw()
```

## Developing

Development instructions are located in [DEVELOPING.md](DEVELOPING.md)

## Testing

Testing instructions are located in [TESTING.md](TESTING.md)

## Deploying

Deployment instructions are located in [DEPLOYING.md](DEPLOYING.md)