# Fileglancer Demo App

A simple demo app for testing [Fileglancer](https://github.com/JaneliaSciComp/fileglancer) job submission. It sleeps for a configurable duration and prints a message repeatedly.

## Prerequisites

- [Pixi](https://pixi.sh)

## Usage

```bash
pixi run demo --message "Hello!" --sleep_seconds 2 --repeat 3 --verbose
```

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `--sleep_seconds` | integer | 5 | Seconds to sleep between messages (0-300) |
| `--message` | string | "Hello from Fileglancer!" | Message to print |
| `--repeat` | integer | 3 | Number of times to repeat (1-100) |
| `--output_dir` | directory | | Directory to write a summary file (optional) |
| `--verbose` | flag | false | Show sleep countdown |

## Fileglancer Integration

This repo contains a `runnables.yaml` manifest. To use it in Fileglancer, add the GitHub repo URL on the Apps page.
