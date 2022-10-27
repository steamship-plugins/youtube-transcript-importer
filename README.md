# Youtube File Importer

This plugin imports the audio from Youtube videos.

## Getting Started

### Usage

Once deployed, the Youtube Importer can be used with the handle `youtube-file-importer`.

```python
from steamship import File, Steamship

IMPORTER_HANDLE = "youtube-file-importer"
ship = Steamship()

plugin_instance = ship.use_plugin(
    plugin_handle=IMPORTER_HANDLE
)
file = File.create_with_plugin(ship, plugin_instance=plugin_instance.handle, URL="YOUR_URL")
```

## Developing

Development instructions are located in [DEVELOPING.md](DEVELOPING.md)

## Testing

Testing instructions are located in [TESTING.md](TESTING.md)

## Deploying

Deployment instructions are located in [DEPLOYING.md](DEPLOYING.md)