"""
Пакет для работы с дискретными случайными величинами
"""

__version__ = '1.0.0'
__author__ = 'Your Name'

from .core import DiscreteRandomVariable, StatisticsCalculator
from .io import DRVSerializer
from .visualization import DistributionPlot, PolylinePlot, CDFPlot
from .gui import MainWindow, VariableEditor, PlotWidget

__all__ = [
    'DiscreteRandomVariable',
    'StatisticsCalculator', 
    'DRVSerializer',
    'DistributionPlot',
    'PolylinePlot',
    'CDFPlot',
    'MainWindow',
    'VariableEditor',
    'PlotWidget'
]