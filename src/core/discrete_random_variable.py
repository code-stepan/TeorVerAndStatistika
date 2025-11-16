from __future__ import annotations
import math
from typing import Dict, List, Tuple
from dataclasses import dataclass

@dataclass
class ProbabilityMass:
    value: float
    probability: float

class DiscreteRandomVariable:
    """Класс дискретной случайной величины"""

    def __init__(self, values_probs: List[Tuple[float, float]] = None):
        self._pmf: List[ProbabilityMass] = []
        if values_probs:
            self._validate_probabilities([p for _, p in values_probs])
            # Добавляем все значения без нормализации, потом нормализуем один раз
            for value, prob in values_probs:
                if prob < 0 or prob > 1:
                    raise ValueError("Вероятность должна быть в диапазоне [0, 1]")
                
                # Проверка уникальности значения
                for pm in self._pmf:
                    if math.isclose(pm.value, value, rel_tol=1e-9):
                        raise ValueError(f"Значение {value} уже существует")
                
                self._pmf.append(ProbabilityMass(value, prob))
            
            # Нормализуем только один раз после добавления всех значений
            self._normalize()
    
    def _validate_probabilities(self, probabilities: List[float]):
        """Проверка суммы вероятностей"""
        total_prob = sum(probabilities)
        if not math.isclose(total_prob, 1.0, rel_tol=1e-9):
            raise ValueError(f"Сумма вероятностей должна равняться 1.0, получено {total_prob}")

    def add_value(self, value: float, probability: float) -> None:
        """Добавление значения с вероятностью"""
        if probability < 0 or probability > 1:
            raise ValueError("Вероятность должна быть в диапазоне [0, 1]")

        # Проверка уникальности значения
        for pm in self._pmf:
            if math.isclose(pm.value, value, rel_tol=1e-9):
                raise ValueError(f"Значение {value} уже существует")

        self._pmf.append(ProbabilityMass(value, probability))
        self._normalize()

    def _normalize(self) -> None:
        """Нормализация вероятностей"""
        total_prob = sum(pm.probability for pm in self._pmf)
        if total_prob > 0:
            for pm in self._pmf:
                pm.probability /= total_prob

    @property
    def values(self) -> List[float]:
        return [pm.value for pm in self._pmf]
    
    @property
    def probabilities(self) -> List[float]:
        return [pm.probability for pm in self._pmf]

    def get_pmf(self) -> List[Tuple[float, float]]:
        return [(pm.value, pm.probability) for pm in self._pmf]

    def __mul__(self, other) -> DiscreteRandomVariable:
        """Умножение: если other - число (скаляр), умножает на скаляр;
        если other - DiscreteRandomVariable, умножает две случайные величины"""
        if isinstance(other, (int, float)):
            # Умножение на скаляр
            new_pmf = [(pm.value * other, pm.probability) for pm in self._pmf]
            return DiscreteRandomVariable(new_pmf)
        elif isinstance(other, DiscreteRandomVariable):
            # Умножение двух случайных величин
            new_pmf_list: List[Tuple[float, float]] = []
            
            for pm1 in self._pmf:
                for pm2 in other._pmf:
                    new_value = pm1.value * pm2.value
                    new_prob = pm1.probability * pm2.probability
                    
                    # Ищем близкое значение с учетом точности
                    found = False
                    for i, (v, p) in enumerate(new_pmf_list):
                        if math.isclose(v, new_value, rel_tol=1e-9):
                            new_pmf_list[i] = (v, p + new_prob)
                            found = True
                            break
                    
                    if not found:
                        new_pmf_list.append((new_value, new_prob))
            
            return DiscreteRandomVariable(new_pmf_list)
        else:
            return NotImplemented

    def __rmul__(self, scalar: float) -> DiscreteRandomVariable:
        """Умножение справа на скаляр"""
        return self.__mul__(scalar)

    def __add__(self, other: DiscreteRandomVariable) -> DiscreteRandomVariable:
        """Сложение двух случайных величин"""
        if not isinstance(other, DiscreteRandomVariable):
            return NotImplemented
        
        new_pmf_list: List[Tuple[float, float]] = []
        
        for pm1 in self._pmf:
            for pm2 in other._pmf:
                new_value = pm1.value + pm2.value
                new_prob = pm1.probability * pm2.probability
                
                # Ищем близкое значение с учетом точности
                found = False
                for i, (v, p) in enumerate(new_pmf_list):
                    if math.isclose(v, new_value, rel_tol=1e-9):
                        new_pmf_list[i] = (v, p + new_prob)
                        found = True
                        break
                
                if not found:
                    new_pmf_list.append((new_value, new_prob))
        
        return DiscreteRandomVariable(new_pmf_list)

    def to_dict(self) -> Dict:
        """Сериализация в словарь"""
        return {
            'pmf': [(pm.value, pm.probability) for pm in self._pmf]
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> DiscreteRandomVariable:
        """Десериализация из словаря"""
        return cls(data.get('pmf', []))

    def __repr__(self) -> str:
        return f"DiscreteRandomVariable({self.get_pmf()})"