# auto-pangolin
Automated lineage calling of SARS-CoV-2 sequence data using the [BCCDC-PHL/pangolin-nf](https://github.com/BCCDC-PHL/pangolin-nf) pipeline.

# Installation

# Usage
Start the tool as follows:

```bash
auto-pangolin --config config.json
```

See the Configuration section of this document for details on preparing a configuration file.

More detailed logs can be produced by controlling the log level using the `--log-level` flag:

```bash
auto-pangolin --config config.json --log-level debug
```

# Configuration
This tool takes a single config file, in JSON format, with the following structure:

```json
{
    "analysis_parent_dir": "/path/to/analysis_by_run",
    "analysis_work_dir": "/path/to/work-auto-pangolin",
    "analysis_output_dir": "/path/to/pangolin_lineages_by_date",
    "notification_email_addresses": [
	"someone@example.org"
    ],
    "send_notification_emails": false,
    "analysis_time": "07:00",
    "pipelines": [
	{
	    "pipeline_name": "BCCDC-PHL/pangolin-nf",
	    "pipeline_version": "v0.4.0",
	    "pipeline_parameters": {
		"analysis_parent_dir": null,
		"outdir": null
	    }
	}
    ]
    
}
```

# Logging
This tool outputs [structured logs](https://www.honeycomb.io/blog/structured-logging-and-your-team/) in [JSON Lines](https://jsonlines.org/) format:

Every log line should include the fields:

- `timestamp`
- `level`
- `module`
- `function_name`
- `line_num`
- `message`

...and the contents of the `message` key will be a JSON object that includes at `event_type`. The remaining keys inside the `message` will vary by event type.

```json
{"timestamp": "2022-09-22T11:32:52.287", "level": "INFO", "module", "core", "function_name": "scan", "line_num", 56, "message": {"event_type": "scan_start"}}
```
