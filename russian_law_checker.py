"""
Проверка текста на соответствие законам РФ и выявление чувствительных данных
с графическим интерфейсом на Qt
"""

import sys
import re
from dataclasses import dataclass
from typing import List, Tuple
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTextEdit, QPushButton, QTableWidget, QTableWidgetItem, QLabel,
    QTabWidget, QHeaderView
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QFont


@dataclass
class Violation:
    """Класс для представления нарушения"""
    category: str
    description: str
    article: str
    punishment: str
    severity: str  # critical, high, medium, low


@dataclass
class SensitiveData:
    """Класс для представления чувствительных данных"""
    data_type: str
    value: str
    position: Tuple[int, int]
    risk_level: str  # critical, high, medium


class RussianLawDatabase:
    """Локальная база законов РФ"""

    def __init__(self):
        self.violations_db = [
            Violation(
                category="Экстремизм",
                description="Пропаганда или возбуждение ненависти по признакам социальной, расовой, национальной или религиозной принадлежности",
                article="УК РФ ст. 282",
                punishment="Штраф до 300 000 руб. или лишение свободы до 4 лет",
                severity="critical"
            ),
            Violation(
                category="Терроризм",
                description="Публичное призывание к осуществлению террористической деятельности",
                article="УК РФ ст. 205.2",
                punishment="Штраф до 100 000 руб. или лишение свободы до 5 лет",
                severity="critical"
            ),
            Violation(
                category="Оскорбление",
                description="Оскорбление должностного лица (унижающее честь и достоинство)",
                article="УК РФ ст. 319",
                punishment="Штраф до 30 000 руб. или исправительные работы до 40 часов",
                severity="high"
            ),
            Violation(
                category="Клевета",
                description="Распространение заведомо ложной информации, порочащей честь и деловую репутацию",
                article="УК РФ ст. 128.1",
                punishment="Штраф до 500 000 руб.",
                severity="high"
            ),
            Violation(
                category="Авторские права",
                description="Нарушение авторских прав (копирование без разрешения)",
                article="УК РФ ст. 146",
                punishment="Штраф до 200 000 руб. или лишение свободы до 2 лет",
                severity="high"
            ),
            Violation(
                category="Мошенничество",
                description="Мошенничество (обман с целью присвоения имущества)",
                article="УК РФ ст. 159",
                punishment="Штраф до 120 000 руб. или лишение свободы до 2 лет",
                severity="high"
            ),
            Violation(
                category="Фишинг",
                description="Попытка получить конфиденциальную информацию (пароли, реквизиты счетов)",
                article="УК РФ ст. 159.3",
                punishment="Штраф до 100 000 руб. или лишение свободы до 3 лет",
                severity="critical"
            ),
            Violation(
                category="ПДн",
                description="Несанкционированное распространение персональных данных физического лица",
                article="ФЗ 'О защите ПДн' ст. 3",
                punishment="Штраф до 6 000 000 руб. или блокировка сайта",
                severity="critical"
            ),
            Violation(
                category="Экология",
                description="Загрязнение окружающей среды (неправомерный выброс загрязняющих веществ)",
                article="УК РФ ст. 252",
                punishment="Штраф до 250 000 руб. или лишение свободы до 2 лет",
                severity="medium"
            ),
        ]

    def check_violations(self, text: str) -> List[Violation]:
        """Проверяет текст на нарушения законов"""
        found_violations = []

        # Паттерны используют корни слов + \w* для охвата русских словоформ
        # (убить/убей/убейте, укажите/укажи и т.д.), а не только словарной формы.
        extremism_keywords = [
            r'(уби\w*|убе\w*|уничтож\w*|истреб\w*)\s+(всех\s+)?(мусульман\w*|евре\w*|христиан\w*|славян\w*|татар\w*)',
            r'(бей\w*|убива\w*|расстрелива\w*|веша\w*)\s+(русск\w*|евре\w*|татар\w*|кавказц\w*)',
            r'(подожг\w*|сожг\w*|разруш\w*)\s+(мечет\w*|синагог\w*|храм\w*|церкв\w*)',
        ]
        for pattern in extremism_keywords:
            if re.search(pattern, text, re.IGNORECASE):
                found_violations.append(self.violations_db[0])
                break

        terrorism_keywords = [
            r'организ\w*\s+(взрыв\w*|теракт\w*|атак\w*)',
            r'(взорв\w*|подожг\w*|поджеч\w*)\s+(здани\w*|школ\w*|больниц\w*|метро)',
        ]
        for pattern in terrorism_keywords:
            if re.search(pattern, text, re.IGNORECASE):
                found_violations.append(self.violations_db[1])
                break

        if re.search(r'(президент\w*|министр\w*|губернатор\w*|судь\w*).{0,20}(идиот\w*|дебил\w*|мудак\w*|ублюдк\w*|ублюдо\w*)', text, re.IGNORECASE):
            found_violations.append(self.violations_db[2])

        if re.search(r'(доказан\w*|известн\w*).{0,20}(укра\w*|взял\w*\s+взятк\w*|получил\w*\s+взятк\w*)', text, re.IGNORECASE):
            found_violations.append(self.violations_db[3])

        if re.search(r'(скач\w*|скопир\w*|распростран\w*)\s+(фильм\w*|книг\w*|музык\w*|торрент\w*)', text, re.IGNORECASE):
            found_violations.append(self.violations_db[4])

        if re.search(r'(верн\w*|отправ\w*|перевед\w*|переведи)\s+(деньг\w*|биткоин\w*|криптовалют\w*).{0,30}(выигра\w*|назначен\w*)', text, re.IGNORECASE):
            found_violations.append(self.violations_db[5])

        if re.search(r'(укаж\w*|введ\w*|отправ\w*|сообщ\w*).{0,15}(парол\w*|пин-?код\w*|реквизит\w*|номер\s+карт\w*)', text, re.IGNORECASE):
            found_violations.append(self.violations_db[6])

        return found_violations

    def detect_sensitive_data(self, text: str) -> List[SensitiveData]:
        """Обнаруживает чувствительные данные в тексте"""
        sensitive_items = []

        for match in re.finditer(r'\b\d{4}\s+\d{6}\b', text):
            sensitive_items.append(SensitiveData("Паспорт РФ", match.group(), match.span(), "critical"))

        for match in re.finditer(r'(?:\+7|8)[-\s]?\d{3}[-\s]?\d{3}[-\s]?\d{2}[-\s]?\d{2}', text):
            sensitive_items.append(SensitiveData("Номер телефона", match.group(), match.span(), "high"))

        for match in re.finditer(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b', text):
            sensitive_items.append(SensitiveData("Email адрес", match.group(), match.span(), "high"))

        for match in re.finditer(r'\b(?:\d{4}[-\s]?){3}\d{4}\b', text):
            if len(re.sub(r'\D', '', match.group())) == 16:
                sensitive_items.append(SensitiveData("Номер кредитной карты", match.group(), match.span(), "critical"))

        for match in re.finditer(r'\b\d{12}\b', text):
            sensitive_items.append(SensitiveData("ИНН", match.group(), match.span(), "critical"))

        for match in re.finditer(r'\b\d{3}[-\s]?\d{3}[-\s]?\d{3}[-\s]?\d{2}\b', text):
            sensitive_items.append(SensitiveData("СНИЛС", match.group(), match.span(), "critical"))

        address_pattern = r'(ул\.|улица|пр\.|проспект|площадь|бульвар|переулок)\s+[А-Яа-я\s]+,?\s+д\.?\s+\d+[-/]?\d*'
        for match in re.finditer(address_pattern, text):
            sensitive_items.append(SensitiveData("Домашний адрес", match.group(), match.span(), "high"))

        password_pattern = r'(?:пароль|password|pwd|pass)[\s:=]*([^\s,;]+)'
        for match in re.finditer(password_pattern, text, re.IGNORECASE):
            sensitive_items.append(SensitiveData("Возможный пароль", match.group(1), match.span(), "critical"))

        return sensitive_items


class LawCheckerApp(QMainWindow):
    """Главное окно приложения"""

    def __init__(self):
        super().__init__()
        self.db = RussianLawDatabase()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Проверка текста на соответствие законам РФ")
        self.setGeometry(100, 100, 1200, 800)
        self.setStyleSheet(self.get_stylesheet())

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()

        title = QLabel("Проверка текста на соответствие законам РФ")
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title.setFont(title_font)
        main_layout.addWidget(title)

        main_layout.addWidget(QLabel("Введите текст для проверки:"))

        self.text_input = QTextEdit()
        self.text_input.setMinimumHeight(150)
        self.text_input.setPlaceholderText("Вставьте текст, который нужно проверить...")
        main_layout.addWidget(self.text_input)

        button_layout = QHBoxLayout()
        self.check_button = QPushButton("🔍 Проверить текст")
        self.check_button.setMinimumHeight(40)
        self.check_button.clicked.connect(self.check_text)
        button_layout.addWidget(self.check_button)

        self.clear_button = QPushButton("🗑️ Очистить")
        self.clear_button.setMinimumHeight(40)
        self.clear_button.clicked.connect(self.clear_all)
        button_layout.addWidget(self.clear_button)

        main_layout.addLayout(button_layout)

        self.tabs = QTabWidget()

        self.violations_table = QTableWidget()
        self.violations_table.setColumnCount(4)
        self.violations_table.setHorizontalHeaderLabels(["Нарушение", "Статья", "Наказание", "Серьезность"])
        self.violations_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.tabs.addTab(self.violations_table, "📋 Нарушения законов")

        self.sensitive_table = QTableWidget()
        self.sensitive_table.setColumnCount(4)
        self.sensitive_table.setHorizontalHeaderLabels(["Тип данных", "Значение", "Позиция", "Уровень риска"])
        self.sensitive_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.tabs.addTab(self.sensitive_table, "⚠️ Чувствительные данные")

        main_layout.addWidget(self.tabs)

        self.status_label = QLabel("Готов к проверке")
        main_layout.addWidget(self.status_label)

        central_widget.setLayout(main_layout)

    def check_text(self):
        text = self.text_input.toPlainText().strip()
        if not text:
            self.status_label.setText("❌ Ошибка: введите текст для проверки")
            return

        violations = self.db.check_violations(text)
        self.display_violations(violations)

        sensitive_data = self.db.detect_sensitive_data(text)
        self.display_sensitive_data(sensitive_data)

        self.status_label.setText(
            f"✓ Проверено: обнаружено {len(violations)} нарушений, {len(sensitive_data)} чувствительных данных"
        )

        if violations:
            self.tabs.setCurrentIndex(0)
        elif sensitive_data:
            self.tabs.setCurrentIndex(1)

    def display_violations(self, violations: List[Violation]):
        self.violations_table.setRowCount(0)
        for violation in violations:
            row = self.violations_table.rowCount()
            self.violations_table.insertRow(row)
            self.violations_table.setItem(row, 0, QTableWidgetItem(f"{violation.category}\n{violation.description}"))
            self.violations_table.setItem(row, 1, QTableWidgetItem(violation.article))
            self.violations_table.setItem(row, 2, QTableWidgetItem(violation.punishment))
            severity_item = QTableWidgetItem(self.get_severity_text(violation.severity))
            severity_item.setBackground(self.get_severity_color(violation.severity))
            self.violations_table.setItem(row, 3, severity_item)
        self.violations_table.resizeRowsToContents()

    def display_sensitive_data(self, sensitive_items: List[SensitiveData]):
        self.sensitive_table.setRowCount(0)
        for item in sensitive_items:
            row = self.sensitive_table.rowCount()
            self.sensitive_table.insertRow(row)
            self.sensitive_table.setItem(row, 0, QTableWidgetItem(item.data_type))
            self.sensitive_table.setItem(row, 1, QTableWidgetItem(self.mask_value(item.value)))
            self.sensitive_table.setItem(row, 2, QTableWidgetItem(f"{item.position[0]}-{item.position[1]}"))
            risk_item = QTableWidgetItem(self.get_risk_text(item.risk_level))
            risk_item.setBackground(self.get_risk_color(item.risk_level))
            self.sensitive_table.setItem(row, 3, risk_item)
        self.sensitive_table.resizeRowsToContents()

    @staticmethod
    def mask_value(value: str) -> str:
        if len(value) <= 4:
            return "***"
        return value[:2] + "***" + value[-2:]

    @staticmethod
    def get_severity_text(severity: str) -> str:
        return {"critical": "🔴 КРИТИЧНО", "high": "🟠 ВЫСОКОЕ", "medium": "🟡 СРЕДНЕЕ", "low": "🟢 НИЗКОЕ"}.get(severity, severity)

    @staticmethod
    def get_risk_text(risk: str) -> str:
        return {"critical": "🔴 КРИТИЧНЫЙ", "high": "🟠 ВЫСОКИЙ", "medium": "🟡 СРЕДНИЙ", "low": "🟢 НИЗКИЙ"}.get(risk, risk)

    @staticmethod
    def get_severity_color(severity: str) -> QColor:
        return {
            "critical": QColor(255, 100, 100),
            "high": QColor(255, 180, 100),
            "medium": QColor(255, 220, 100),
            "low": QColor(150, 255, 150),
        }.get(severity, QColor(255, 255, 255))

    @staticmethod
    def get_risk_color(risk: str) -> QColor:
        return LawCheckerApp.get_severity_color(risk)

    def clear_all(self):
        self.text_input.clear()
        self.violations_table.setRowCount(0)
        self.sensitive_table.setRowCount(0)
        self.status_label.setText("Готов к проверке")

    @staticmethod
    def get_stylesheet() -> str:
        return """
            QMainWindow { background-color: #f5f5f5; }
            QTextEdit {
                background-color: white; border: 1px solid #ddd; border-radius: 4px;
                padding: 8px; font-family: 'Courier New'; font-size: 10pt;
            }
            QPushButton {
                background-color: #4CAF50; color: white; border: none; border-radius: 4px;
                padding: 10px 20px; font-weight: bold; font-size: 11pt;
            }
            QPushButton:hover { background-color: #45a049; }
            QPushButton:pressed { background-color: #3d8b40; }
            QTableWidget { background-color: white; border: 1px solid #ddd; border-radius: 4px; gridline-color: #eee; }
            QHeaderView::section {
                background-color: #f0f0f0; padding: 5px; border: none;
                border-right: 1px solid #ddd; border-bottom: 1px solid #ddd;
            }
            QLabel { color: #333; font-size: 10pt; }
            QTabWidget::pane { border: 1px solid #ddd; }
            QTabBar::tab { background-color: #e0e0e0; padding: 8px 20px; border: 1px solid #ddd; margin-right: 2px; }
            QTabBar::tab:selected { background-color: white; border-bottom: 3px solid #4CAF50; }
        """


def main():
    app = QApplication(sys.argv)
    window = LawCheckerApp()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
