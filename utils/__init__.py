import os
import sys
from dataclasses import dataclass

import yaml


@dataclass(frozen=True)
class Config:
    url: str
    app_version: str
    debug: bool


config = None

if os.path.isfile('config.yaml'):
    with open('config.yaml', 'r') as f:
        try:
            data = yaml.safe_load(f)

            config = Config(
                url=data['server']['url'],
                app_version=data['env_variables']['app_version'],
                debug=data['env_variables']['debug'],
            )

        except yaml.YAMLError as exc:
            print('[CONFIG] Read config file error: ')
            print(exc)
            sys.exit(0)
else:
    raise FileNotFoundError('config.yaml not found')
