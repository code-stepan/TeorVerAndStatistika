import matplotlib.pyplot as plt
from ..core.discrete_random_variable import DiscreteRandomVariable


class CDFPlot:
    """Отображение функции распределения"""
    
    @staticmethod
    def plot(drv: DiscreteRandomVariable, ax=None, title="Функция распределения"):
        """Построение функции распределения"""
        if ax is None:
            fig, ax = plt.subplots(figsize=(10, 6))
        
        pmf = drv.get_pmf()
        values = sorted([v for v, _ in pmf])
        probs = [p for _, p in sorted(pmf, key=lambda x: x[0])]
        
        # Строим ступенчатую функцию
        cdf_x = []
        cdf_y = []
        
        cumulative = 0
        for i, (v, p) in enumerate(zip(values, probs)):
            if i == 0:
                cdf_x.append(v - 1)  # Начало
                cdf_y.append(0)
            
            cdf_x.append(v)
            cdf_y.append(cumulative)
            
            cumulative += p
            cdf_x.append(v)
            cdf_y.append(cumulative)
        
        # Добавляем конечную точку
        cdf_x.append(values[-1] + 1)
        cdf_y.append(1)
        
        ax.step(cdf_x, cdf_y, where='post', linewidth=2, color='purple')
        ax.set_xlabel('Значения')
        ax.set_ylabel('F(x)')
        ax.set_title(title)
        ax.grid(True, alpha=0.3)
        ax.set_ylim(0, 1.1)
        
        return ax