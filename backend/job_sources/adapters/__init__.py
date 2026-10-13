"""Adapters package"""
from .base import BaseJobAdapter
from .arbeitnow_adapter import ArbeitnowAdapter
from .remotive_adapter import RemotiveAdapter
from .technopark_adapter import TechnoparkAdapter
from .infopark_adapter import InfoparkAdapter
from .south_india_direct_adapter import SouthIndiaDirectAdapter

__all__ = [
    'BaseJobAdapter',
    'ArbeitnowAdapter',
    'RemotiveAdapter',
    'TechnoparkAdapter',
    'InfoparkAdapter',
    'SouthIndiaDirectAdapter',
]
