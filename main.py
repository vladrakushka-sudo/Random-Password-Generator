import tkinter as tk
from tkinter import ttk, messagebox
import random
import string
import json
import os
from datetime import datetime


class PasswordGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Генератор случайных паролей")
        self.root.geometry("800x600")
        self.root.configure(bg='#1a1a2e')
        self.root.resizable(True, True)
        
        # Настройки по умолчанию
        self.min_length = 4
        self.max_length = 50
        self.default_length = 12
        
        # Файл для хранения истории
        self.history_file = "password_history.json"
        self.password_history = self.load_history()
        
        # Настройка интерфейса
        self.setup_ui()
        
    def setup_ui(self):
        """Создание пользовательского интерфейса"""
        
        # Главный заголовок
        title_frame = tk.Frame(self.root, bg='#16213e', height=80)
        title_frame.pack(fill=tk.X)
        
        title_label = tk.Label(
            title_frame,
            text="🔐 Генератор случайных паролей",
            font=("Arial", 20, "bold"),
            bg='#16213e',
            fg='#e94560',
            pady=20
        )
        title_label.pack()
        
        # Основной контейнер
        main_frame = tk.Frame(self.root, bg='#1a1a2e', padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Левая панель - настройки
        left_panel = tk.Frame(main_frame, bg='#0f3460', relief=tk.RAISED, bd=2)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Заголовок настроек
        tk.Label(
            left_panel,
            text="⚙️ НАСТРОЙКИ ПАРОЛЯ",
            font=("Arial", 14, "bold"),
            bg='#0f3460',
            fg='#e94560',
            pady=10
        ).pack(fill=tk.X)
        
        # Фрейм для длины пароля
        length_frame = tk.Frame(left_panel, bg='#0f3460', pady=20)
        length_frame.pack(fill=tk.X, padx=20)
        
        tk.Label(
            length_frame,
            text="Длина пароля:",
            font=("Arial", 12),
            bg='#0f3460',
            fg='white'
        ).pack(anchor=tk.W)
        
        # Отображение текущей длины
        self.length_var = tk.IntVar(value=self.default_length)
        self.length_label = tk.Label(
            length_frame,
            text=str(self.default_length),
            font=("Arial", 24, "bold"),
            bg='#0f3460',
            fg='#e94560'
        )
        self.length_label.pack(pady=5)
        
        # Ползунок для выбора длины
        self.length_scale = tk.Scale(
            length_frame,
            from_=self.min_length,
            to=self.max_length,
            orient=tk.HORIZONTAL,
            variable=self.length_var,
            command=self.update_length_label,
            bg='#0f3460',
            fg='white',
            troughcolor='#533483',
            activebackground='#e94560',
            length=300,
            highlightthickness=0
        )
        self.length_scale.pack(fill=tk.X)
        
        # Границы длины
        bounds_frame = tk.Frame(length_frame, bg='#0f3460')
        bounds_frame.pack(fill=tk.X)
        tk.Label(bounds_frame, text=str(self.min_length), bg='#0f3460', fg='#aaa').pack(side=tk.LEFT)
        tk.Label(bounds_frame, text=str(self.max_length), bg='#0f3460', fg='#aaa').pack(side=tk.RIGHT)
        
        # Чекбоксы для типов символов
        chars_frame = tk.Frame(left_panel, bg='#0f3460', pady=20)
        chars_frame.pack(fill=tk.X, padx=20)
        
        tk.Label(
            chars_frame,
            text="Типы символов:",
            font=("Arial", 12, "bold"),
            bg='#0f3460',
            fg='white'
        ).pack(anchor=tk.W, pady=(0, 10))
        
        # Переменные для чекбоксов
        self.use_uppercase = tk.BooleanVar(value=True)
        self.use_lowercase = tk.BooleanVar(value=True)
self.use_digits = tk.BooleanVar(value=True)
        self.use_special = tk.BooleanVar(value=True)
        
        # Функция для создания стилизованных чекбоксов
        self.create_checkbox(chars_frame, "Заглавные буквы (A-Z)", self.use_uppercase)
        self.create_checkbox(chars_frame, "Строчные буквы (a-z)", self.use_lowercase)
        self.create_checkbox(chars_frame, "Цифры (0-9)", self.use_digits)
        self.create_checkbox(chars_frame, "Спецсимволы (!@#$...)", self.use_special)
        
        # Кнопка генерации
        generate_btn = tk.Button(
            left_panel,
            text="🎲 СГЕНЕРИРОВАТЬ ПАРОЛЬ",
            command=self.generate_password,
            bg='#e94560',
            fg='white',
            font=("Arial", 14, "bold"),
            padx=20,
            pady=15,
            relief=tk.FLAT,
            cursor='hand2',
            activebackground='#c73e54'
        )
        generate_btn.pack(pady=20, padx=20, fill=tk.X)
        
        # Поле для отображения пароля
        self.password_var = tk.StringVar()
        password_entry = tk.Entry(
            left_panel,
            textvariable=self.password_var,
            font=("Courier", 16, "bold"),
            justify=tk.CENTER,
            bg='#16213e',
            fg='#00ff88',
            relief=tk.FLAT,
            state='readonly'
        )
        password_entry.pack(pady=10, padx=20, fill=tk.X)
        
        # Кнопка копирования
        copy_btn = tk.Button(
            left_panel,
            text="📋 Копировать в буфер",
            command=self.copy_to_clipboard,
            bg='#533483',
            fg='white',
            font=("Arial", 10),
            padx=15,
            pady=8,
            relief=tk.FLAT,
            cursor='hand2'
        )
        copy_btn.pack(pady=(0, 20), padx=20, fill=tk.X)
        
        # Правая панель - история
        right_panel = tk.Frame(main_frame, bg='#0f3460', relief=tk.RAISED, bd=2)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        # Заголовок истории
        history_header = tk.Frame(right_panel, bg='#0f3460')
        history_header.pack(fill=tk.X, pady=10, padx=10)
        
        tk.Label(
            history_header,
            text="📜 ИСТОРИЯ ПАРОЛЕЙ",
            font=("Arial", 14, "bold"),
            bg='#0f3460',
            fg='#e94560'
        ).pack(side=tk.LEFT)
        
        # Кнопка очистки истории
        clear_btn = tk.Button(
            history_header,
            text="🗑️ Очистить",
            command=self.clear_history,
            bg='#c73e54',
            fg='white',
            font=("Arial", 9),
            padx=10,
            pady=3,
            relief=tk.FLAT,
            cursor='hand2'
        )
        clear_btn.pack(side=tk.RIGHT)
        
        # Таблица истории
        table_frame = tk.Frame(right_panel, bg='#0f3460')
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        # Создание таблицы с прокруткой
        self.create_history_table(table_frame)
        
        # Загрузка истории
        self.update_history_display()
    
    def create_checkbox(self, parent, text, variable):
        """Создание стилизованного чекбокса"""
        frame = tk.Frame(parent, bg='#0f3460')
        frame.pack(anchor=tk.W, pady=2)
        
        cb = tk.Checkbutton(
            frame,
            text=text,
            variable=variable,
            bg='#0f3460',
            fg='white',
            selectcolor='#0f3460',
            activebackground='#0f3460',
            activeforeground='white',
            font=("Arial", 10)
        )
        cb.pack(anchor=tk.W)
    
    def create_history_table(self, parent):
        """Создание таблицы для отображения истории"""
        # Фрейм для таблицы
        tree_frame = tk.Frame(parent, bg='#0f3460')
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        # Создание Treeview
        columns = ('Время', 'Пароль', 'Длина')
self.history_tree = ttk.Treeview(
            tree_frame,
            columns=columns,
            show='headings',
            height=15
        )
        
        # Настройка столбцов
        self.history_tree.heading('Время', text='⏰ Время')
        self.history_tree.heading('Пароль', text='🔑 Пароль')
        self.history_tree.heading('Длина', text='📏 Длина')
        
        self.history_tree.column('Время', width=150)
        self.history_tree.column('Пароль', width=200)
        self.history_tree.column('Длина', width=50)
        
        # Стилизация
        style = ttk.Style()
        style.theme_use('default')
        style.configure(
            'Treeview',
            background='#16213e',
            foreground='white',
            rowheight=25,
            fieldbackground='#16213e'
        )
        style.configure(
            'Treeview.Heading',
            background='#533483',
            foreground='white',
            font=('Arial', 10, 'bold')
        )
        style.map('Treeview', background=[('selected', '#e94560')])
        
        # Добавление прокрутки
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.history_tree.yview)
        self.history_tree.configure(yscrollcommand=scrollbar.set)
        
        # Размещение
        self.history_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Привязка двойного клика
        self.history_tree.bind('<Double-Button-1>', self.copy_from_history)
    
    def update_length_label(self, value):
        """Обновление отображения длины пароля"""
        self.length_label.config(text=value)
    
    def generate_password(self):
        """Генерация случайного пароля"""
        # Проверка на выбранные типы символов
        if not any([
            self.use_uppercase.get(),
            self.use_lowercase.get(),
            self.use_digits.get(),
            self.use_special.get()
        ]):
            messagebox.showwarning(
                "⚠️ Предупреждение",
                "Выберите хотя бы один тип символов для генерации пароля!"
            )
            return
        
        # Формирование набора символов
        chars = ""
        if self.use_uppercase.get():
            chars += string.ascii_uppercase
        if self.use_lowercase.get():
            chars += string.ascii_lowercase
        if self.use_digits.get():
            chars += string.digits
        if self.use_special.get():
            chars += string.punctuation
        
        # Генерация пароля
        length = self.length_var.get()
        
        # Гарантируем наличие хотя бы одного символа каждого выбранного типа
        password_chars = []
        if self.use_uppercase.get():
            password_chars.append(random.choice(string.ascii_uppercase))
        if self.use_lowercase.get():
            password_chars.append(random.choice(string.ascii_lowercase))
        if self.use_digits.get():
            password_chars.append(random.choice(string.digits))
        if self.use_special.get():
            password_chars.append(random.choice(string.punctuation))
        
        # Дополняем до нужной длины
        remaining_length = length - len(password_chars)
        password_chars.extend(random.choices(chars, k=remaining_length))
        
        # Перемешиваем символы
        random.shuffle(password_chars)
        password = ''.join(password_chars)
        
        # Отображаем пароль
        self.password_var.set(password)
        
        # Сохраняем в историю
        self.add_to_history(password)
    
    def add_to_history(self, password):
        """Добавление пароля в историю"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        history_entry = {
            'timestamp': timestamp,
            'password': password,
            'length': len(password)
        }
        
        # Добавляем в начало списка
        self.password_history.insert(0, history_entry)
# Ограничиваем историю последними 50 записями
        if len(self.password_history) > 50:
            self.password_history = self.password_history[:50]
        
        # Сохраняем в файл
        self.save_history()
        
        # Обновляем отображение
        self.update_history_display()
    
    def update_history_display(self):
        """Обновление отображения истории в таблице"""
        # Очищаем таблицу
        for item in self.history_tree.get_children():
            self.history_tree.delete(item)
        
        # Добавляем записи
        for entry in self.password_history:
            self.history_tree.insert(
                '',
                tk.END,
                values=(
                    entry['timestamp'],
                    entry['password'],
                    entry['length']
                )
            )
    
    def copy_to_clipboard(self):
        """Копирование пароля в буфер обмена"""
        password = self.password_var.get()
        if password:
            self.root.clipboard_clear()
            self.root.clipboard_append(password)
            messagebox.showinfo("✅ Успешно", "Пароль скопирован в буфер обмена!")
        else:
            messagebox.showwarning("⚠️ Внимание", "Сначала сгенерируйте пароль!")
    
    def copy_from_history(self, event):
        """Копирование пароля из истории по двойному клику"""
        selection = self.history_tree.selection()
        if selection:
            item = self.history_tree.item(selection[0])
            password = item['values'][1]
            self.root.clipboard_clear()
            self.root.clipboard_append(password)
            messagebox.showinfo("✅ Успешно", "Пароль скопирован в буфер обмена!")
    
    def clear_history(self):
        """Очистка истории паролей"""
        if messagebox.askyesno(
            "🗑️ Подтверждение",
            "Вы уверены, что хотите очистить всю историю паролей?"
        ):
            self.password_history = []
            self.save_history()
            self.update_history_display()
            messagebox.showinfo("✅ Успешно", "История очищена!")
    
    def load_history(self):
        """Загрузка истории из JSON-файла"""
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError) as e:
                print(f"Ошибка загрузки истории: {e}")
        return []
    
    def save_history(self):
        """Сохранение истории в JSON-файл"""
        try:
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(self.password_history, f, indent=2, ensure_ascii=False)
        except IOError as e:
            messagebox.showerror("❌ Ошибка", f"Не удалось сохранить историю: {e}")


def main():
    root = tk.Tk()
    app = PasswordGenerator(root)
    root.mainloop()


if __name__ == "__main__":
    main()
