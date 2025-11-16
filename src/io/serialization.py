import json
from ..core.discrete_random_variable import DiscreteRandomVariable


class DRVSerializer:
    """Сериализатор для дискретных случайных величин"""
    
    @staticmethod
    def save_to_file(drv: DiscreteRandomVariable, filepath: str) -> None:
        """Сохранение в файл"""
        data = drv.to_dict()
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    @staticmethod
    def load_from_file(filepath: str) -> DiscreteRandomVariable:
        """Загрузка из файла"""
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return DiscreteRandomVariable.from_dict(data)