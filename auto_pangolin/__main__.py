#!/usr/bin/env python

import argparse
import datetime
import json
import logging
import os
import time

import auto_pangolin.config
import auto_pangolin.core as core


DEFAULT_SCAN_INTERVAL_SECONDS = 60.0


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config')
    parser.add_argument('--log-level')
    args = parser.parse_args()

    config = {}

    try:
        log_level = getattr(logging, args.log_level.upper())
    except AttributeError as e:
        log_level = logging.INFO

    logging.basicConfig(
        format='{"timestamp": "%(asctime)s.%(msecs)03d", "level": "%(levelname)s", "module", "%(module)s", "function_name": "%(funcName)s", "line_num", %(lineno)d, "message": %(message)s}',
        datefmt='%Y-%m-%dT%H:%M:%S',
        encoding='utf-8',
        level=log_level,
    )
    logging.debug(json.dumps({"event_type": "debug_logging_enabled"}))

    quit_when_safe = False

    while(True):
        try:
            if args.config:
                try:
                    config = auto_pangolin.config.load_config(args.config)
                    logging.info(json.dumps({"event_type": "config_loaded", "config_file": os.path.abspath(args.config)}))
                except json.decoder.JSONDecodeError as e:
                    # If we fail to load the config file, we continue on with the
                    # last valid config that was loaded.
                    logging.error(json.dumps({"event_type": "load_config_failed", "config_file": os.path.abspath(args.config)}))

            scan_interval = DEFAULT_SCAN_INTERVAL_SECONDS
            if "scan_interval_seconds" in config:
                try:
                    scan_interval = float(str(config['scan_interval_seconds']))
                except ValueError as e:
                    pass

            analysis_window = 0.5 * (scan_interval + (0.1 * scan_interval))
            if "analysis_time" in config:
                analysis_time_str = config['analysis_time']
                today = datetime.date.today()
                analysis_time = datetime.datetime.strptime(analysis_time_str, "%H:%M").time()
                analysis_datetime_today = datetime.datetime.combine(datetime.datetime.now(), analysis_time)
                current_time = datetime.datetime.now()
                time_diff = abs((current_time - analysis_datetime_today).total_seconds())
                todays_output_path = os.path.join(config['analysis_output_dir'], str(today) + '_pangolin_lineages.csv')
                todays_output_exists = os.path.exists(todays_output_path)

                logging.info(json.dumps({"event_type": "checked_analysis_time", "current_time": str(current_time.time()), "scheduled_analysis_time": str(analysis_time), "time_diff_seconds": time_diff, "analysis_window_seconds": analysis_window, "within_analysis_window": time_diff < analysis_window, "todays_output_exists": todays_output_exists}))

                if time_diff < analysis_window and not todays_output_exists:
                    core.analyze(config)

            if quit_when_safe:
                exit(0)

            
            time.sleep(scan_interval)

        except KeyboardInterrupt as e:
            logging.info(json.dumps({"event_type": "quit_when_safe_enabled"}))
            quit_when_safe = True


if __name__ == '__main__':
    main()
