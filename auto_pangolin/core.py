import datetime
import json
import logging
import os
import re
import shutil
import subprocess
import uuid

from typing import Iterator, Optional


def analyze(config):
    """
    Initiate an analysis
    """
    analysis_parent_dir = config['analysis_parent_dir']
    analysis_output_dir = config['analysis_output_dir']
    base_analysis_work_dir = config['analysis_work_dir']
    if 'notification_email_addresses' in config:
        notification_email_addresses = config['notification_email_addresses']
    else:
        notification_email_addresses = []
    for pipeline in config['pipelines']:
        pipeline_parameters = pipeline['pipeline_parameters']
        pipeline_short_name = pipeline['pipeline_name'].split('/')[1].replace('_', '-')
        pipeline_minor_version = '.'.join(pipeline['pipeline_version'].split('.')[0:2])
        analysis_timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        analysis_date = datetime.datetime.now().strftime('%Y-%m-%d')
        analysis_work_dir = os.path.abspath(os.path.join(base_analysis_work_dir, 'work-' + analysis_timestamp))
        analysis_trace_path = os.path.abspath(os.path.join(analysis_work_dir, 'nextflow_trace.tsv'))
        pipeline_command = [
            'nextflow',
            'run',
            pipeline['pipeline_name'],
            '-r', pipeline['pipeline_version'],
            '-profile', 'conda',
            '--cache', os.path.join(os.path.expanduser('~'), '.conda/envs'),
            '--analysis_parent_dir', analysis_parent_dir,
            '--outdir', analysis_output_dir,
            '-work-dir', analysis_work_dir,
            '-with-trace', analysis_trace_path,
        ]
        if 'send_notification_emails' in config and config['send_notification_emails']:
            pipeline_command += ['-with-notification', ','.join(notification_email_addresses)]

        logging.info(json.dumps({"event_type": "analysis_started", "pipeline_command": " ".join(pipeline_command)}))

        try:
            subprocess.run(pipeline_command, capture_output=True, check=True)
            logging.info(json.dumps({"event_type": "analysis_completed", "pipeline_command": " ".join(pipeline_command)}))
            original_output_file_path = os.path.join(analysis_output_dir, 'pangolin_lineages.csv')
            final_output_file_path = os.path.join(analysis_output_dir, analysis_date + '_pangolin_lineages.csv')
            shutil.move(original_output_file_path, final_output_file_path)
            logging.info(json.dumps({"event_type": "renamed_output_file", "original_output_file_path": original_output_file_path, "final_output_file_path": final_output_file_path}))
            shutil.rmtree(analysis_work_dir, ignore_errors=True)
            logging.info(json.dumps({"event_type": "analysis_work_dir_deleted", "analysis_work_dir_path": analysis_work_dir}))
        except subprocess.CalledProcessError as e:
            logging.error(json.dumps({"event_type": "analysis_failed", "pipeline_command": " ".join(pipeline_command)}))
        except OSError as e:
            logging.error(json.dumps({"event_type": "delete_analysis_work_dir_failed", "analysis_work_dir_path": analysis_work_dir}))
