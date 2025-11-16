"""
Скрипт для тестирования загрузки JSON файлов
"""
import sys
import os

# Добавляем путь к модулям
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.io.serialization import DRVSerializer
from src.core.statistics import StatisticsCalculator


def test_load_file(filepath):
    """Тестирует загрузку одного файла"""
    print(f"\n{'=' * 60}")
    print(f"Тестирование файла: {filepath}")
    print(f"{'=' * 60}")
    
    if not os.path.exists(filepath):
        print(f"[ОШИБКА] Файл не найден: {filepath}")
        return False
    
    try:
        # Загружаем файл
        drv = DRVSerializer.load_from_file(filepath)
        
        print(f"[OK] Файл успешно загружен")
        print(f"\nРаспределение:")
        pmf = drv.get_pmf()
        for value, prob in pmf:
            print(f"  Значение: {value:8.4f}, Вероятность: {prob:.6f}")
        
        # Проверяем, что сумма вероятностей равна 1
        total_prob = sum(drv.probabilities)
        print(f"\nСумма вероятностей: {total_prob:.10f}")
        
        if abs(total_prob - 1.0) < 1e-6:
            print("[OK] Сумма вероятностей корректна (= 1.0)")
        else:
            print(f"[ВНИМАНИЕ] Сумма вероятностей отклоняется от 1.0 на {abs(total_prob - 1.0):.10f}")
        
        # Вычисляем статистику
        stats = StatisticsCalculator.get_all_statistics(drv)
        print(f"\nСтатистические характеристики:")
        print(f"  Математическое ожидание: {stats['expectation']:10.4f}")
        print(f"  Дисперсия:               {stats['variance']:10.4f}")
        print(f"  Стандартное отклонение:  {stats['standard_deviation']:10.4f}")
        print(f"  Коэффициент асимметрии:  {stats['skewness']:10.4f}")
        print(f"  Коэффициент эксцесса:    {stats['kurtosis']:10.4f}")
        
        return True
        
    except Exception as e:
        print(f"[ОШИБКА] Ошибка при загрузке файла: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Основная функция для тестирования всех файлов"""
    print("\n" + "=" * 60)
    print("ТЕСТИРОВАНИЕ ЗАГРУЗКИ JSON ФАЙЛОВ")
    print("=" * 60)
    
    # Получаем путь к test_data
    current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    test_data_dir = os.path.join(current_dir, "test_data")
    
    # Список файлов для тестирования
    test_files = [
        os.path.join(test_data_dir, "dice.json"),
        os.path.join(test_data_dir, "coin_toss.json"),
        os.path.join(test_data_dir, "binomial_5_03.json"),
        os.path.join(test_data_dir, "custom_distribution.json"),
        os.path.join(test_data_dir, "two_dice_sum.json"),
        os.path.join(test_data_dir, "poisson_like.json"),
    ]
    
    results = []
    for filepath in test_files:
        result = test_load_file(filepath)
        results.append((os.path.basename(filepath), result))
    
    # Итоговый отчет
    print(f"\n{'=' * 60}")
    print("ИТОГОВЫЙ ОТЧЕТ")
    print(f"{'=' * 60}")
    
    successful = sum(1 for _, result in results if result)
    total = len(results)
    
    for filename, result in results:
        status = "[OK] Успешно" if result else "[ОШИБКА] Ошибка"
        print(f"  {status:18} - {filename}")
    
    print(f"\nВсего файлов: {total}")
    print(f"Успешно загружено: {successful}")
    print(f"Ошибок: {total - successful}")
    
    if successful == total:
        print("\n[OK] Все файлы успешно загружены!")
    else:
        print(f"\n[ВНИМАНИЕ] Некоторые файлы не удалось загрузить")
    
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()

