"""
Продвинутые примеры использования библиотеки дискретных случайных величин
"""
import sys
import os

# Добавляем путь к модулям
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core.discrete_random_variable import DiscreteRandomVariable
from src.core.statistics import StatisticsCalculator


def example_1_multiplication():
    """Пример 1: Умножение двух случайных величин"""
    print("=" * 60)
    print("Пример 1: Умножение двух случайных величин")
    print("=" * 60)
    
    X = DiscreteRandomVariable([
        (1, 0.5),
        (2, 0.5)
    ])
    
    Y = DiscreteRandomVariable([
        (3, 0.3),
        (4, 0.7)
    ])
    
    Z = X * Y
    print(f"X: {X.get_pmf()}")
    print(f"Y: {Y.get_pmf()}")
    print(f"Z = X * Y: {Z.get_pmf()}")
    
    mean_X = StatisticsCalculator.expectation(X)
    mean_Y = StatisticsCalculator.expectation(Y)
    mean_Z = StatisticsCalculator.expectation(Z)
    
    print(f"\nE(X) = {mean_X:.4f}")
    print(f"E(Y) = {mean_Y:.4f}")
    print(f"E(X*Y) = {mean_Z:.4f}")
    print(f"E(X) * E(Y) = {mean_X * mean_Y:.4f}")
    print(f"Примечание: E(X*Y) != E(X)*E(Y), так как X и Y не независимы в данном случае")
    print()


def example_2_complex_distribution():
    """Пример 2: Сложное распределение с добавлением значений"""
    print("=" * 60)
    print("Пример 2: Постепенное добавление значений")
    print("=" * 60)
    
    drv = DiscreteRandomVariable()
    
    # Добавляем значения по одному
    drv.add_value(5, 0.25)
    drv.add_value(10, 0.25)
    drv.add_value(15, 0.25)
    drv.add_value(20, 0.25)
    
    print(f"Распределение после добавления всех значений:")
    print(f"  {drv.get_pmf()}")
    
    stats = StatisticsCalculator.get_all_statistics(drv)
    print(f"\nПолная статистика:")
    for key, value in stats.items():
        print(f"  {key}: {value:.4f}")
    print()


def example_3_binomial_approximation():
    """Пример 3: Приближение биномиального распределения"""
    print("=" * 60)
    print("Пример 3: Приближение биномиального распределения")
    print("=" * 60)
    
    # Биномиальное распределение B(5, 0.3)
    # P(X=k) = C(5,k) * 0.3^k * 0.7^(5-k)
    from math import comb
    
    n = 5
    p = 0.3
    
    values_probs = []
    for k in range(n + 1):
        prob = comb(n, k) * (p ** k) * ((1 - p) ** (n - k))
        values_probs.append((k, prob))
    
    binomial = DiscreteRandomVariable(values_probs)
    
    print(f"Биномиальное распределение B({n}, {p}):")
    for value, prob in binomial.get_pmf():
        print(f"  P(X={value:.0f}) = {prob:.4f}")
    
    stats = StatisticsCalculator.get_all_statistics(binomial)
    print(f"\nСтатистика:")
    print(f"  Математическое ожидание: {stats['expectation']:.4f} (ожидается {n * p:.4f})")
    print(f"  Дисперсия: {stats['variance']:.4f} (ожидается {n * p * (1 - p):.4f})")
    print()


def example_4_skewness_kurtosis():
    """Пример 4: Асимметрия и эксцесс"""
    print("=" * 60)
    print("Пример 4: Асимметрия и эксцесс")
    print("=" * 60)
    
    # Асимметричное распределение
    asymmetric = DiscreteRandomVariable([
        (1, 0.1),
        (2, 0.2),
        (3, 0.4),
        (4, 0.2),
        (5, 0.1)
    ])
    
    # Симметричное распределение
    symmetric = DiscreteRandomVariable([
        (1, 0.1),
        (2, 0.2),
        (3, 0.4),
        (4, 0.2),
        (5, 0.1)
    ])
    
    print("Асимметричное распределение:")
    stats1 = StatisticsCalculator.get_all_statistics(asymmetric)
    print(f"  Коэффициент асимметрии: {stats1['skewness']:.4f}")
    print(f"  Коэффициент эксцесса: {stats1['kurtosis']:.4f}")
    
    print("\nСимметричное распределение:")
    stats2 = StatisticsCalculator.get_all_statistics(symmetric)
    print(f"  Коэффициент асимметрии: {stats2['skewness']:.4f}")
    print(f"  Коэффициент эксцесса: {stats2['kurtosis']:.4f}")
    print()


def example_5_chained_operations():
    """Пример 5: Цепочка операций"""
    print("=" * 60)
    print("Пример 5: Цепочка операций")
    print("=" * 60)
    
    X = DiscreteRandomVariable([(1, 0.5), (2, 0.5)])
    Y = DiscreteRandomVariable([(3, 0.4), (4, 0.6)])
    
    # Сложная операция: 2X + Y
    result = 2 * X + Y
    
    print(f"X: {X.get_pmf()}")
    print(f"Y: {Y.get_pmf()}")
    print(f"2X: {(2 * X).get_pmf()}")
    print(f"2X + Y: {result.get_pmf()}")
    
    mean_result = StatisticsCalculator.expectation(result)
    mean_X = StatisticsCalculator.expectation(X)
    mean_Y = StatisticsCalculator.expectation(Y)
    
    print(f"\nE(2X + Y) = {mean_result:.4f}")
    print(f"2*E(X) + E(Y) = {2 * mean_X + mean_Y:.4f}")
    print(f"Проверка линейности: E(2X + Y) = 2E(X) + E(Y)")
    print()


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("ПРОДВИНУТЫЕ ПРИМЕРЫ ИСПОЛЬЗОВАНИЯ")
    print("=" * 60 + "\n")
    
    try:
        example_1_multiplication()
        example_2_complex_distribution()
        example_3_binomial_approximation()
        example_4_skewness_kurtosis()
        example_5_chained_operations()
        
        print("=" * 60)
        print("Все примеры выполнены успешно!")
        print("=" * 60)
        
    except Exception as e:
        print(f"Ошибка: {e}")
        import traceback
        traceback.print_exc()

