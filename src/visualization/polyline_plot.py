import matplotlib.pyplot as plt
from ..core.discrete_random_variable import DiscreteRandomVariable


class PolylinePlot:
    """Отображение в виде полилайна"""
    
    @staticmethod
    def plot(drv: DiscreteRandomVariable, ax=None, title="Полилайн распределения"):
        """Построение полилайна"""
        if ax is None:
            fig, ax = plt.subplots(figsize=(10, 6))
        
        pmf = drv.get_pmf()
        values = [v for v, _ in pmf]
        probs = [p for _, p in pmf]
        
        ax.plot(values, probs, 'o-', linewidth=2, markersize=8, 
                color='green', alpha=0.7)
        
        ax.set_xlabel('Значения')
        ax.set_ylabel('Вероятности')
        ax.set_title(title)
        ax.grid(True, alpha=0.3)
        
        return ax