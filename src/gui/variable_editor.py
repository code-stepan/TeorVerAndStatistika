from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, 
                            QTableWidgetItem, QPushButton, QLabel,
                            QMessageBox, QHeaderView, QDoubleSpinBox)
from PyQt6.QtCore import Qt, pyqtSignal
from ..core.discrete_random_variable import DiscreteRandomVariable


class VariableEditor(QWidget):
    """Редактор дискретной случайной величины"""
    
    # Сигнал об изменении переменной
    variable_changed = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.drv = DiscreteRandomVariable()
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Таблица значений
        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(['Значение', 'Вероятность'])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(QLabel("Таблица распределения:"))
        layout.addWidget(self.table)
        
        # Панель добавления
        add_layout = QHBoxLayout()
        add_layout.addWidget(QLabel("Значение:"))
        self.value_input = QDoubleSpinBox()
        self.value_input.setRange(-1000000, 1000000)
        self.value_input.setDecimals(4)
        add_layout.addWidget(self.value_input)
        
        add_layout.addWidget(QLabel("Вероятность:"))
        self.prob_input = QDoubleSpinBox()
        self.prob_input.setRange(0, 1)
        self.prob_input.setSingleStep(0.01)
        self.prob_input.setDecimals(4)
        add_layout.addWidget(self.prob_input)
        
        self.add_btn = QPushButton("Добавить")
        self.add_btn.clicked.connect(self.add_value)
        add_layout.addWidget(self.add_btn)
        
        self.delete_btn = QPushButton("Удалить выделенное")
        self.delete_btn.clicked.connect(self.delete_value)
        add_layout.addWidget(self.delete_btn)
        
        layout.addLayout(add_layout)
        
        # Информация
        self.info_label = QLabel("Добавьте значения и вероятности")
        layout.addWidget(self.info_label)
        
        self.setLayout(layout)
        
        # Подключаем обработчик изменений в таблице
        self.table.itemChanged.connect(self.on_table_item_changed)
        
        self.update_info()
    
    def add_value(self):
        value = self.value_input.value()
        prob = self.prob_input.value()
        
        try:
            self.drv.add_value(value, prob)
            self.update_table()
            self.update_info()
            # Отправляем сигнал об изменении переменной
            self.variable_changed.emit()
        except ValueError as e:
            QMessageBox.warning(self, "Ошибка", str(e))
    
    def delete_value(self):
        current_row = self.table.currentRow()
        if current_row >= 0:
            # Блокируем сигналы, чтобы избежать двойной обработки
            self.table.blockSignals(True)
            self.table.removeRow(current_row)
            self.table.blockSignals(False)
            self.recreate_from_table()
    
    def on_table_item_changed(self, item):
        """Обработка изменений в таблице вручную"""
        if item is None:
            return
        
        # Блокируем сигналы, чтобы избежать рекурсии
        self.table.blockSignals(True)
        try:
            self.recreate_from_table()
        finally:
            self.table.blockSignals(False)
    
    def recreate_from_table(self):
        """Пересоздание DRV из данных таблицы"""
        values_probs = []
        for row in range(self.table.rowCount()):
            value_item = self.table.item(row, 0)
            prob_item = self.table.item(row, 1)
            if value_item and prob_item:
                try:
                    value_str = value_item.text().strip()
                    prob_str = prob_item.text().strip()
                    
                    if not value_str or not prob_str:
                        continue
                    
                    value = float(value_str)
                    prob = float(prob_str)
                    
                    if prob < 0:
                        QMessageBox.warning(self, "Ошибка", 
                                          f"Вероятность в строке {row + 1} не может быть отрицательной")
                        # Восстанавливаем предыдущее состояние
                        self.update_table()
                        return
                    
                    values_probs.append((value, prob))
                except ValueError:
                    QMessageBox.warning(self, "Ошибка", 
                                      f"Неверный формат данных в строке {row + 1}")
                    # Восстанавливаем предыдущее состояние
                    self.update_table()
                    return
        
        # Если нет значений, создаем пустой DRV
        if not values_probs:
            self.drv = DiscreteRandomVariable()
            self.update_info()
            return
        
        # Нормализуем вероятности перед созданием DRV
        total_prob = sum(prob for _, prob in values_probs)
        if total_prob <= 0:
            QMessageBox.warning(self, "Ошибка", 
                              "Сумма вероятностей должна быть больше нуля")
            self.update_table()
            return
        
        # Нормализуем, чтобы сумма была равна 1.0
        normalized_values_probs = [(value, prob / total_prob) for value, prob in values_probs]
        
        try:
            old_drv = self.drv
            self.drv = DiscreteRandomVariable(normalized_values_probs)
            self.update_info()
            # Обновляем таблицу, чтобы показать нормализованные значения
            self.update_table()
            # Отправляем сигнал об изменении переменной
            self.variable_changed.emit()
        except ValueError as e:
            # Восстанавливаем предыдущее состояние при ошибке
            QMessageBox.warning(self, "Ошибка", str(e))
            self.drv = old_drv
            self.update_table()
    
    def update_table(self):
        """Обновление таблицы из DRV (без вызова сигналов)"""
        # Блокируем сигналы, чтобы избежать рекурсии
        self.table.blockSignals(True)
        try:
            self.table.setRowCount(0)
            for value, prob in self.drv.get_pmf():
                row = self.table.rowCount()
                self.table.insertRow(row)
                self.table.setItem(row, 0, QTableWidgetItem(f"{value:.4f}"))
                self.table.setItem(row, 1, QTableWidgetItem(f"{prob:.4f}"))
        finally:
            self.table.blockSignals(False)
    
    def update_info(self):
        total_prob = sum(self.drv.probabilities)
        count = len(self.drv.values)
        self.info_label.setText(f"Количество значений: {count}, Сумма вероятностей: {total_prob:.4f}")
    
    def get_variable(self) -> DiscreteRandomVariable:
        return self.drv
    
    def set_variable(self, drv: DiscreteRandomVariable):
        self.drv = drv
        self.update_table()
        self.update_info()
        # Отправляем сигнал об изменении переменной
        self.variable_changed.emit()