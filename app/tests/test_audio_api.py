from unittest import mock
from datetime import datetime

import pytest

from fastapi.testclient import TestClient

from main import app

DT_FORMAT = '%Y-%m-%dT%H:%M:%S.%f'

