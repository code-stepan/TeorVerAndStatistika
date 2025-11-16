"""
Базовые примеры использования библиотеки дискретных случайных величин
"""
import sys
import os

# Добавляем путь к модулям
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core.discrete_random_variable import DiscreteRandomVariable
from src.core.statistics import StatisticsCalculator
from src.io.serialization import DRVSerializer


def example_1_basic_creation():
    """Пример 1: Создание простой дискретной случайной величины"""
    print("=" * 60)
    print("Пример 1: Создание простой случайной величины")
    print("=" * 60)
    
    # Бросание кубика
    dice = DiscreteRandomVariable([
        (1, 1/6),
        (2, 1/6),
        (3, 1/6),
        (4, 1/6),
        (5, 1/6),
        (6, 1/6)
    ])
    
    print(f"Случайная величина: {dice}")
    print(f"Значения: {dice.values}")
    print(f"Вероятности: {dice.probabilities}")
    
    stats = StatisticsCalculator.get_all_statistics(dice)
    print(f"\nСтатистика:")
    print(f"  Математическое ожидание: {stats['expectation']:.4f}")
    print(f"  Дисперсия: {stats['variance']:.4f}")
    print(f"  Стандартное отклонение: {stats['standard_deviation']:.4f}")
    print()


def example_2_coin_toss():
    """Пример 2: Подбрасывание монеты"""
    print("=" * 60)
    print("Пример 2: Подбрасывание монеты")
    print("=" * 60)
    
    coin = DiscreteRandomVariable([
        (0, 0.5),  # Решка
        (1, 0.5)   # Орел
    ])
    
    print(f"Монета: {coin.get_pmf()}")
    
    stats = StatisticsCalculator.get_all_statistics(coin)
    print(f"\nСтатистика:")
    for key, value in stats.items():
        print(f"  {key}: {value:.4f}")
    print()


def example_3_operations():
    """Пример 3: Операции со случайными величинами"""
    print("=" * 60)
    print("Пример 3: Операции со случайными величинами")
    print("=" * 60)
    
    # Два кубика
    dice1 = DiscreteRandomVariable([
        (1, 1/6), (2, 1/6), (3, 1/6), 
        (4, 1/6), (5, 1/6), (6, 1/6)
    ])
    
    dice2 = DiscreteRandomVariable([
        (1, 1/6), (2, 1/6), (3, 1/6), 
        (4, 1/6), (5, 1/6), (6, 1/6)
    ])
    
    # Сумма двух кубиков
    sum_dice = dice1 + dice2
    print(f"Сумма двух кубиков (первые 5 значений):")
    pmf = sum_dice.get_pmf()[:5]
    for value, prob in pmf:
        print(f"  {value}: {prob:.4f}")
    print(f"  ... (всего {len(sum_dice.values)} значений)")
    
    # Математическое ожидание суммы
    mean_sum = StatisticsCalculator.expectation(sum_dice)
    print(f"\nМатематическое ожидание суммы: {mean_sum:.4f}")
    print(f"Ожидаемое значение: {StatisticsCalculator.expectation(dice1) + StatisticsCalculator.expectation(dice2):.4f}")
    print()


def example_4_scalar_multiplication():
    """Пример 4: Умножение на скаляр"""
    print("=" * 60)
    print("Пример 4: Умножение на скаляр")
    print("=" * 60)
    
    X = DiscreteRandomVariable([
        (1, 0.3),
        (2, 0.5),
        (3, 0.2)
    ])
    
    # Умножение на 2
    Y = 2 * X
    print(f"Исходная величина X: {X.get_pmf()}")
    print(f"Y = 2X: {Y.get_pmf()}")
    
    print(f"\nМатематическое ожидание X: {StatisticsCalculator.expectation(X):.4f}")
    print(f"Математическое ожидание 2X: {StatisticsCalculator.expectation(Y):.4f}")
    print(f"Проверка: 2 * E(X) = {2 * StatisticsCalculator.expectation(X):.4f}")
    print()


def example_5_serialization():
    """Пример 5: Сохранение и загрузка"""
    print("=" * 60)
    print("Пример 5: Сохранение и загрузка")
    print("=" * 60)
    
    drv = DiscreteRandomVariable([
        (10, 0.2),
        (20, 0.3),
        (30, 0.4),
        (40, 0.1)
    ])
    
    # Сохраняем
    test_file = "test_data_example.json"
    DRVSerializer.save_to_file(drv, test_file)
    print(f"Сохранено в {test_file}")
    
    # Загружаем
    loaded_drv = DRVSerializer.load_from_file(test_file)
    print(f"Загружено из {test_file}")
    print(f"Исходная: {drv.get_pmf()}")
    print(f"Загруженная: {loaded_drv.get_pmf()}")
    
    # Удаляем тестовый файл
    if os.path.exists(test_file):
        os.remove(test_file)
    print()


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("БАЗОВЫЕ ПРИМЕРЫ ИСПОЛЬЗОВАНИЯ")
    print("=" * 60 + "\n")
    
    try:
        example_1_basic_creation()
        example_2_coin_toss()
        example_3_operations()
        example_4_scalar_multiplication()
        example_5_serialization()
        
        print("=" * 60)
        print("Все примеры выполнены успешно!")
        print("=" * 60)
        
    except Exception as e:
        print(f"Ошибка: {e}")
        import traceback
        traceback.print_exc()

