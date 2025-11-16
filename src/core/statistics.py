import math
from .discrete_random_variable import DiscreteRandomVariable

class StatisticsCalculator:
    """Калькулятор статистических характеристик"""

    @staticmethod
    def expectation(drv: DiscreteRandomVariable) -> float:
        """Математическое ожидание"""
        return sum(v * p for v, p in drv.get_pmf())

    @staticmethod
    def variance(drv: DiscreteRandomVariable) -> float:
        """Дисперсия"""
        mean = StatisticsCalculator.expectation(drv)
        return sum(p * (v - mean) ** 2 for v, p in drv.get_pmf())

    @staticmethod
    def standard_deviation(drv: DiscreteRandomVariable) -> float:
        """Стандартное отклонение"""
        return math.sqrt(StatisticsCalculator.variance(drv))

    @staticmethod
    def skewness(drv: DiscreteRandomVariable) -> float:
        """Коэффициент асимметрии"""
        mean = StatisticsCalculator.expectation(drv)
        std = StatisticsCalculator.standard_deviation(drv)
        
        if std == 0:
            return 0
            
        return sum(p * ((v - mean) / std) ** 3 for v, p in drv.get_pmf())
    
    @staticmethod
    def kurtosis(drv: DiscreteRandomVariable) -> float:
        """Коэффициент эксцесса"""
        mean = StatisticsCalculator.expectation(drv)
        std = StatisticsCalculator.standard_deviation(drv)
        
        if std == 0:
            return 0
            
        return sum(p * ((v - mean) / std) ** 4 for v, p in drv.get_pmf()) - 3
   
    @staticmethod
    def get_all_statistics(drv: DiscreteRandomVariable) -> dict:
        """Все статистические характеристики"""
        return {
            'expectation': StatisticsCalculator.expectation(drv),
            'variance': StatisticsCalculator.variance(drv),
            'standard_deviation': StatisticsCalculator.standard_deviation(drv),
            'skewness': StatisticsCalculator.skewness(drv),
            'kurtosis': StatisticsCalculator.kurtosis(drv)
        }