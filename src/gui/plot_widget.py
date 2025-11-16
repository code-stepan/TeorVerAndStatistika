from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTabWidget
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from ..core.discrete_random_variable import DiscreteRandomVariable
from ..visualization.distribution_plot import DistributionPlot
from ..visualization.polyline_plot import PolylinePlot
from ..visualization.cdf_plot import CDFPlot


class PlotWidget(QWidget):
    """Виджет для отображения графиков"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        self.tab_widget = QTabWidget()
        
        # Создаем вкладки с графиками
        self.distribution_tab = QWidget()
        self.polyline_tab = QWidget()
        self.cdf_tab = QWidget()
        
        self.distribution_layout = QVBoxLayout()
        self.polyline_layout = QVBoxLayout()
        self.cdf_layout = QVBoxLayout()
        
        self.distribution_tab.setLayout(self.distribution_layout)
        self.polyline_tab.setLayout(self.polyline_layout)
        self.cdf_tab.setLayout(self.cdf_layout)
        
        self.tab_widget.addTab(self.distribution_tab, "Закон распределения")
        self.tab_widget.addTab(self.polyline_tab, "Полилайн")
        self.tab_widget.addTab(self.cdf_tab, "Функция распределения")
        
        layout.addWidget(self.tab_widget)
        self.setLayout(layout)
    
    def plot_variable(self, drv: DiscreteRandomVariable):
        """Отображение всех графиков для переменной"""
        self.plot_distribution(drv)
        self.plot_polyline(drv)
        self.plot_cdf(drv)
    
    def plot_distribution(self, drv: DiscreteRandomVariable):
        """Отображение закона распределения"""
        # Очищаем предыдущий график
        for i in reversed(range(self.distribution_layout.count())):
            self.distribution_layout.itemAt(i).widget().setParent(None)
        
        fig = Figure(figsize=(8, 6))
        canvas = FigureCanvas(fig)
        ax = fig.add_subplot(111)
        
        DistributionPlot.plot(drv, ax)
        fig.tight_layout()
        
        self.distribution_layout.addWidget(canvas)
        canvas.draw()
    
    def plot_polyline(self, drv: DiscreteRandomVariable):
        """Отображение полилайна"""
        for i in reversed(range(self.polyline_layout.count())):
            self.polyline_layout.itemAt(i).widget().setParent(None)
        
        fig = Figure(figsize=(8, 6))
        canvas = FigureCanvas(fig)
        ax = fig.add_subplot(111)
        
        PolylinePlot.plot(drv, ax)
        fig.tight_layout()
        
        self.polyline_layout.addWidget(canvas)
        canvas.draw()
    
    def plot_cdf(self, drv: DiscreteRandomVariable):
        """Отображение функции распределения"""
        for i in reversed(range(self.cdf_layout.count())):
            self.cdf_layout.itemAt(i).widget().setParent(None)
        
        fig = Figure(figsize=(8, 6))
        canvas = FigureCanvas(fig)
        ax = fig.add_subplot(111)
        
        CDFPlot.plot(drv, ax)
        fig.tight_layout()
        
        self.cdf_layout.addWidget(canvas)
        canvas.draw()