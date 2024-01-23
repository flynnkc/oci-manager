#!/bin/python3.11

import logging

from argparse import Namespace

from modules.utilities import Utilities


class Config:
    def __init__(self, args: Namespace):
        self.log = logging.getLogger(f'{__name__}.Config')
        self.args = args
        self.set_config()
        self.log.debug(f'Initializing Config object: {self}')
        self.profile, self.signer = self.set_signer(args)
        

    # Set dependencies
    def set_config(self):
        # Debug mode
        if self.args.debug:
            logging.basicConfig(level=logging.DEBUG)
            self.log.debug('Log Level set to DEBUG')
        else:
            logging.basicConfig(level=logging.INFO)

        # Set logging on Utilities
        Utilities()

    def set_signer(self, args: Namespace) -> dict | None:
        cfg, signer = Utilities.create_signer(args.auth, profile=args.profile)
        return cfg, signer
        