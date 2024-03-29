# tap-superset

`tap-superset` is a Singer tap for Superset.

Built with the [Meltano Tap SDK](https://sdk.meltano.com) for Singer Taps.

## Installation


Install from GitHub:

```bash
pipx install git+https://github.com/ORG_NAME/tap-superset.git@main
```

## Configuration

### Accepted Config Options

# `tap-superset`

Superset tap class.

Built with the [Meltano Singer SDK](https://sdk.meltano.com).

## Capabilities

* `catalog`
* `state`
* `discover`
* `about`
* `stream-maps`
* `schema-flattening`
* `batch`

## Settings

| Setting             | Required | Default | Description |
|:--------------------|:--------:|:-------:|:------------|
| username            | True     | None    | Username of the db user that has access to superset api |
| password            | True     | None    | Password    |
| start_date          | False    | None    | The earliest record date to sync |
| base_url            | True     | https://superset.com | The url for the API service |
| stream_maps         | False    | None    | Config object for stream maps capability. For more information check out [Stream Maps](https://sdk.meltano.com/en/latest/stream_maps.html). |
| stream_map_config   | False    | None    | User-defined config values to be used within map expressions. |
| faker_config        | False    | None    | Config for the [`Faker`](https://faker.readthedocs.io/en/master/) instance variable `fake` used within map expressions. Only applicable if the plugin specifies `faker` as an addtional dependency (through the `singer-sdk` `faker` extra or directly). |
| flattening_enabled  | False    | None    | 'True' to enable schema flattening and automatically expand nested properties. |
| flattening_max_depth| False    | None    | The max depth to flatten schemas. |
| batch_config        | False    | None    |             |

A full list of supported settings and capabilities for this
tap is available by running:

```bash
tap-superset --about
```

### Configure using environment variables

This Singer tap will automatically import any environment variables within the working directory's
`.env` if the `--config=ENV` is provided, such that config values will be considered if a matching
environment variable is set either in the terminal context or in the `.env` file.

### Source Authentication and Authorization

tap-superset uses the /api/v1/security/login endpoint to get its Auth Token from superset.

So it is necessary to set the username and password variables for Authentication.
The user provided should have access to the superset API and you can create it with the superset cli
## Usage

You can easily run `tap-superset` by itself or in a pipeline using [Meltano](https://meltano.com/).

### Executing the Tap Directly

```bash
tap-superset --version
tap-superset --help
tap-superset --config CONFIG --discover > ./catalog.json
```

## Developer Resources

Follow these instructions to contribute to this project.

### Initialize your Development Environment

```bash
pipx install poetry
poetry install
```

### Create and Run Tests

Create tests within the `tests` subfolder and
  then run:

```bash
poetry run pytest
```

You can also test the `tap-superset` CLI interface directly using `poetry run`:

```bash
poetry run tap-superset --help
```

### Testing with [Meltano](https://www.meltano.com)

_**Note:** This tap will work in any Singer environment and does not require Meltano.
Examples here are for convenience and to streamline end-to-end orchestration scenarios._


Next, install Meltano (if you haven't already) and any needed plugins:

```bash
# Install meltano
pipx install meltano
# Initialize meltano within this directory
cd tap-superset
meltano install
```

Now you can test and orchestrate using Meltano:

```bash
# Test invocation:
meltano invoke tap-superset --version
# OR run a test `elt` pipeline:
meltano elt tap-superset target-jsonl
```

### SDK Dev Guide

See the [dev guide](https://sdk.meltano.com/en/latest/dev_guide.html) for more instructions on how to use the SDK to
develop your own taps and targets.
