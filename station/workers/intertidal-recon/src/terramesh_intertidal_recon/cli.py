from __future__ import annotations
import argparse
import contextlib
import json
import os
import shutil
import sys
import urllib.error
from . import NAME, VERSION
from .kit import EXIT_TEMPORARY, EXIT_UNSUPPORTED, Job, WorkerError, main as kit_main

def run(job: Job) -> None:
    ...

def main() -> None:
    ...
