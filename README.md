# From my ex

💕 _Sending all the love from my ex to my new happy and promisucous social media life._ 💕

In other words, this app gets the new posts (except replies and reposts) from my ex-social media and post to the new ones.

## Roadmap

See [the roadmap issues](https://github.com/cuducos/from-my-ex/labels/roadmap) to follow up the MVP development.

## Getting started

### Requirements

* Python 3.9 or newer
* [Poetry](https://python-poetry.org)

### Configuration

These environment variables are required:

| Name | Description | Example |
|---|---|---|
| `FROM_MY_EX_USERNAME` | User handle used in the ex, the blue bird one | `"cuducos"` (not `"@cuducos"`) |
| `FROM_MY_EX_NITTER_INSTANCE` | A [Nitter](https://nitter.net/) instance [with RSS enabled](https://github.com/zedeus/nitter/wiki/Instances) | `"https://nitter.d420.de"` |

### Optional

#### To repost in [Bluesky](https://bsky.app)

| Name | Description | Example | Default value |
| `FROM_MY_EX_BSKY_AGENT` | Bluesky instance | `"https://bsky.social"` | `"https://bsky.social"` |
| `FROM_MY_EX_BSKY_EMAIL` | Email used in Bluesky | | `"cuducos@mailinator.com"` | `None` |
| `FROM_MY_EX_BSKY_PASSWORD` | Password used in Bluesky | As created in [App Passwords](https://bsky.app/settings/app-passwords) | `None` |

Not setting `FROM_MY_EX_BSKY_EMAIL` **or** `FROM_MY_EX_BSKY_PASSWORD` disables Bluesky reposting.

## Usage

```console
$ poetry install
$ poetry run python -m from_my_ex
```

At this time, this will list new posts formatted as they would be reposted in new social medias.
The output skips images (but they are downloaded and they bytes cached in memory, ready to be reposted).

## Contributing

The tests include [Black](https://black.readthedocs.io/en/stable/), [Ruff](https://docs.astral.sh/ruff/) and [`isort`](https://pycqa.github.io/isort/):

```console
$ poetry run pytest
```
