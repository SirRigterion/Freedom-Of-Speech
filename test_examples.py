"""
Тестовые примеры для демонстрации функциональности приложения.
Работает БЕЗ графического интерфейса (не требует PyQt6) — тестирует
только логику проверки текста.
"""

import sys
import re
from dataclasses import dataclass
from typing import List, Tuple


# --- Логика скопирована из russian_law_checker.py, чтобы не требовать PyQt6 ---

@dataclass
class Violation:
    category: str
    description: str
    article: str
    punishment: str
    severity: str


@dataclass
class SensitiveData:
    data_type: str
    value: str
    position: Tuple[int, int]
    risk_level: str


class RussianLawDatabase:
    def __init__(self):
        self.violations_db = [
            Violation("Экстремизм", "Пропаганда ненависти по признакам расы, религии, национальности",
                       "УК РФ ст. 282", "Штраф до 300 000 руб. или лишение свободы до 4 лет", "critical"),
            Violation("Терроризм", "Публичное призывание к террористической деятельности",
                       "УК РФ ст. 205.2", "Штраф до 100 000 руб. или лишение свободы до 5 лет", "critical"),
            Violation("Оскорбление", "Оскорбление должностного лица",
                       "УК РФ ст. 319", "Штраф до 30 000 руб. или исправительные работы до 40 часов", "high"),
            Violation("Клевета", "Распространение заведомо ложной информации",
                       "УК РФ ст. 128.1", "Штраф до 500 000 руб.", "high"),
            Violation("Авторские права", "Нарушение авторских прав",
                       "УК РФ ст. 146", "Штраф до 200 000 руб. или лишение свободы до 2 лет", "high"),
            Violation("Мошенничество", "Обман с целью присвоения имущества",
                       "УК РФ ст. 159", "Штраф до 120 000 руб. или лишение свободы до 2 лет", "high"),
            Violation("Фишинг", "Попытка получить конфиденциальную информацию",
                       "УК РФ ст. 159.3", "Штраф до 100 000 руб. или лишение свободы до 3 лет", "critical"),
            Violation("ПДн", "Несанкционированное распространение персональных данных",
                       "ФЗ 'О защите ПДн' ст. 3", "Штраф до 6 000 000 руб. или блокировка сайта", "critical"),
            Violation("Экология", "Загрязнение окружающей среды",
                       "УК РФ ст. 252", "Штраф до 250 000 руб. или лишение свободы до 2 лет", "medium"),
        ]

    def check_violations(self, text: str) -> List[Violation]:
        found = []
        extremism = [
            r'(уби\w*|убе\w*|уничтож\w*|истреб\w*)\s+(всех\s+)?(мусульман\w*|евре\w*|христиан\w*|славян\w*|татар\w*)',
            r'(бей\w*|убива\w*|расстрелива\w*|веша\w*)\s+(русск\w*|евре\w*|татар\w*|кавказц\w*)',
            r'(подожг\w*|сожг\w*|разруш\w*)\s+(мечет\w*|синагог\w*|храм\w*|церкв\w*)',
        ]
        for p in extremism:
            if re.search(p, text, re.IGNORECASE):
                found.append(self.violations_db[0]); break

        terrorism = [
            r'организ\w*\s+(взрыв\w*|теракт\w*|атак\w*)',
            r'(взорв\w*|подожг\w*|поджеч\w*)\s+(здани\w*|школ\w*|больниц\w*|метро)',
        ]
        for p in terrorism:
            if re.search(p, text, re.IGNORECASE):
                found.append(self.violations_db[1]); break

        if re.search(r'(президент\w*|министр\w*|губернатор\w*|судь\w*).{0,20}(идиот\w*|дебил\w*|мудак\w*|ублюдк\w*|ублюдо\w*)', text, re.IGNORECASE):
            found.append(self.violations_db[2])
        if re.search(r'(доказан\w*|известн\w*).{0,20}(укра\w*|взял\w*\s+взятк\w*|получил\w*\s+взятк\w*)', text, re.IGNORECASE):
            found.append(self.violations_db[3])
        if re.search(r'(скач\w*|скопир\w*|распростран\w*)\s+(фильм\w*|книг\w*|музык\w*|торрент\w*)', text, re.IGNORECASE):
            found.append(self.violations_db[4])
        if re.search(r'(верн\w*|отправ\w*|перевед\w*|переведи)\s+(деньг\w*|биткоин\w*|криптовалют\w*).{0,30}(выигра\w*|назначен\w*)', text, re.IGNORECASE):
            found.append(self.violations_db[5])
        if re.search(r'(укаж\w*|введ\w*|отправ\w*|сообщ\w*).{0,15}(парол\w*|пин-?код\w*|реквизит\w*|номер\s+карт\w*)', text, re.IGNORECASE):
            found.append(self.violations_db[6])

        return found

    def detect_sensitive_data(self, text: str) -> List[SensitiveData]:
        items = []
        for m in re.finditer(r'\b\d{4}\s+\d{6}\b', text):
            items.append(SensitiveData("Паспорт РФ", m.group(), m.span(), "critical"))
        for m in re.finditer(r'(?:\+7|8)[-\s]?\d{3}[-\s]?\d{3}[-\s]?\d{2}[-\s]?\d{2}', text):
            items.append(SensitiveData("Номер телефона", m.group(), m.span(), "high"))
        for m in re.finditer(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b', text):
            items.append(SensitiveData("Email адрес", m.group(), m.span(), "high"))
        for m in re.finditer(r'\b(?:\d{4}[-\s]?){3}\d{4}\b', text):
            if len(re.sub(r'\D', '', m.group())) == 16:
                items.append(SensitiveData("Номер кредитной карты", m.group(), m.span(), "critical"))
        for m in re.finditer(r'\b\d{12}\b', text):
            items.append(SensitiveData("ИНН", m.group(), m.span(), "critical"))
        for m in re.finditer(r'\b\d{3}[-\s]?\d{3}[-\s]?\d{3}[-\s]?\d{2}\b', text):
            items.append(SensitiveData("СНИЛС", m.group(), m.span(), "critical"))
        pwd = r'(?:пароль|password|pwd|pass)[\s:=]*([^\s,;]+)'
        for m in re.finditer(pwd, text, re.IGNORECASE):
            items.append(SensitiveData("Возможный пароль", m.group(1), m.span(), "critical"))
        return items


def print_header(title: str):
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80 + "\n")


def run_test(db, text, description):
    print(f"📝 {description}")
    print(f"Текст: '{text}'")

    violations = db.check_violations(text)
    if violations:
        print(f"  ✗ Нарушения ({len(violations)}):")
        for v in violations:
            print(f"     - {v.category} ({v.article}): {v.punishment} [{v.severity.upper()}]")
    else:
        print("  ✓ Нарушений не обнаружено")

    sensitive = db.detect_sensitive_data(text)
    if sensitive:
        print(f"  ⚠️  Чувствительные данные ({len(sensitive)}):")
        for s in sensitive:
            masked = s.value[:2] + "***" + s.value[-2:] if len(s.value) > 4 else "***"
            print(f"     - {s.data_type}: {masked} [{s.risk_level.upper()}]")
    else:
        print("  ✓ Чувствительные данные не найдены")
    print("-" * 80)


def main():
    db = RussianLawDatabase()

    print_header("ТЕСТИРОВАНИЕ ПРОВЕРКИ ТЕКСТА НА СООТВЕТСТВИЕ ЗАКОНАМ РФ")

    tests = [
        ("Нужно убить всех мусульман и евреев чтобы спасти страну", "Пропаганда экстремизма"),
        ("Организуем взрыв в метро чтобы напугать людей", "Призыв к теракту"),
        ("Президент России - полный идиот", "Оскорбление должностного лица"),
        ("Доказано что министр украл миллионы и взял взятку", "Клевета"),
        ("Укажите ваш пароль и номер карты для подтверждения", "Фишинг"),
        ("Переведите деньги, вы выиграли приз в лотерею", "Мошенничество"),
        ("Это совершенно нормальный текст без нарушений", "Безопасный текст"),
        ("Мой паспорт: 4501 123456, телефон +7-900-123-45-67", "Паспорт + телефон"),
        ("Email для связи: john.doe@example.com", "Email"),
        ("Номер карты: 4532-1234-5678-9010", "Кредитная карта"),
        ("Мой ИНН: 123456789012, СНИЛС: 123-456-789-01", "ИНН + СНИЛС"),
        ("Пароль: qwerty12345, ждем вас на сайте", "Явное указание пароля"),
    ]

    for text, desc in tests:
        run_test(db, text, desc)

    print_header("ТЕСТИРОВАНИЕ ЗАВЕРШЕНО")
    print("Для запуска полнофункционального приложения с GUI используйте:")
    print("  pip install PyQt6")
    print("  python3 russian_law_checker.py")


if __name__ == "__main__":
    main()
