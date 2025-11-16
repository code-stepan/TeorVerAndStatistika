import matplotlib.pyplot as plt
from ..core.discrete_random_variable import DiscreteRandomVariable


class DistributionPlot:
    """Отображение закона распределения"""
    
    @staticmethod
    def plot(drv: DiscreteRandomVariable, ax=None, title="Закон распределения"):
        """Построение графика закона распределения"""
        if ax is None:
            fig, ax = plt.subplots(figsize=(10, 6))
        
        pmf = drv.get_pmf()
        values = [v for v, _ in pmf]
        probs = [p for _, p in pmf]
        
        ax.bar(values, probs, width=0.1, alpha=0.7, color='skyblue', edgecolor='navy')
        ax.scatter(values, probs, color='red', zorder=5)
        
        ax.set_xlabel('Значения')
        ax.set_ylabel('Вероятности')
        ax.set_title(title)
        ax.grid(True, alpha=0.3)
        
        return ax