# Zendesk File Importer

This plugin imports Zendesk tickets to be blockified by
the [zendesk-blockifier](https://github.com/steamship-plugins/zendesk-blockifier).

To instantiate this plugin, you must provide the following configuration parameters:

| Parameter | Description                                        | DType  |
|-----------|----------------------------------------------------|--------|
| n_tickets | Number of tickets you want to scrape.              | number |
| t_start   | The start timestamp used to query Zendesk tickets. | string |
| t_end   | The end timestamp used to query Zendesk tickets.   | string |
| zendesk_email   | Email used to authenticate with Zendesk.           | string |
| zendesk_password   | Password used to authenticate with Zendesk.        | string |
| zendesk_subdomain   | Subdomain used to authenticate with Zendesk.       | string       |

## Getting Started

### Usage

Once deployed, the Zendesk File Importer can be referenced by the handle `zendesk-file-importer`.

```python
from steamship import File, Plugin, PluginInstance, Steamship

IMPORTER_HANDLE = "zendesk-file-importer"
config = {
    "n_tickets": "FILL_IN",
    "t_start": "FILL_IN",
    "t_end": "FILL_IN",
    "zendesk_email": "FILL_IN",
    "zendesk_password": "FILL_IN",
    "zendesk_subdomain": "FILL_IN",
}
client = Steamship()
plugin = Plugin.get(client, IMPORTER_HANDLE).data
plugin_instance = PluginInstance.create(
    client,
    plugin_handle=IMPORTER_HANDLE,
    upsert=False,
    plugin_id=plugin.id,
    config=config,
).data
file = File.create(client, plugin_instance=plugin_instance.handle)
```

## Contributing

We recommend using a Python virtual environments for development.
To set one up, run the following command from this directory:

**Your first time**, create the virtual environment with:

```bash
python3 -m venv .venv
```

**Each time**, activate your virtual environment with:

```bash
source .venv/bin/activate
```

**Your first time**, install the required dependencies with:

```bash
python -m pip install -r requirements.dev.txt
python -m pip install -r requirements.txt
```

## Developing

All the code for this plugin is located in the `src/api.py` file.

## Testing

Tests are located in the `test/` folder. You can run them with:

```bash
pytest
```

We have provided sample data in the `test_data/` folder.

## Deploying

Deploy your plugin to Steamship by running:

```bash
ship plugin:deploy
```

That will deploy your plugin to Steamship and register it as a plugin for use.