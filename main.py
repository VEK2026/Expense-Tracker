import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime

# Файл для хранения данных
DATA_FILE = "expenses.json"

def load_data():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

class ExpenseTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker (Трекер расходов)")
        self.root.geometry("700x500")

        self.expenses = load_data()

        # --- Форма ввода ---
        frame_form = ttk.LabelFrame(root, text="Добавить расход")
        frame_form.pack(pady=10, padx=10, fill="x")

        ttk.Label(frame_form, text="Сумма:").grid(row=0, column=0, padx=5, pady=5)
        self.entry_amount = ttk.Entry(frame_form)
        self.entry_amount.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(frame_form, text="Категория:").grid(row=0, column=2, padx=5, pady=5)
        self.combo_category = ttk.Combobox(frame_form, values=["Еда", "Транспорт", "Развлечения", "Дом"])
        self.combo_category.grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(frame_form, text="Дата (ГГГГ-ММ-ДД):").grid(row=1, column=0, padx=5, pady=5)
        self.entry_date = ttk.Entry(frame_form)
        self.entry_date.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.entry_date.grid(row=1, column=1, padx=5, pady=5)

        btn_add = ttk.Button(frame_form, text="Добавить", command=self.add_expense)
        btn_add.grid(row=1, column=3, padx=5, pady=5)

        # --- Таблица расходов ---
        self.tree = ttk.Treeview(root, columns=("Date", "Category", "Amount"), show="headings")
        self.tree.heading("Date", text="Дата")
        self.tree.heading("Category", text="Категория")
        self.tree.heading("Amount", text="Сумма")
        self.tree.pack(pady=10, padx=10, fill="both", expand=True)

        # --- Фильтрация и Итоги ---
        frame_filter = ttk.LabelFrame(root, text="Фильтр и Итого")
        frame_filter.pack(pady=10, padx=10, fill="x")

        ttk.Label(frame_filter, text="Категория:").pack(side="left", padx=5)
        self.filter_category = ttk.Combobox(frame_filter, values=["Все", "Еда", "Транспорт", "Развлечения", "Дом"])
        self.filter_category.current(0)
        self.filter_category.pack(side="left", padx=5)

        btn_filter = ttk.Button(frame_filter, text="Фильтр", command=self.view_expenses)
        btn_filter.pack(side="left", padx=10)

        self.label_total = ttk.Label(frame_filter, text="Итого: 0.0", font=("Arial", 12, "bold"))
        self.label_total.pack(side="right", padx=10)

        self.view_expenses()

    def add_expense(self):
        amount = self.entry_amount.get()
        category = self.combo_category.get()
        date = self.entry_date.get()

        # Проверка ввода
        try:
            amount = float(amount)
            if amount <= 0: raise ValueError
        except ValueError:
            messagebox.showerror("Ошибка", "Сумма должна быть положительным числом")
            return

        try:
            datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Ошибка", "Дата должна быть в формате ГГГГ-ММ-ДД")
            return

        self.expenses.append({"date": date, "category": category, "amount": amount})
        save_data(self.expenses)
        self.view_expenses()
        self.entry_amount.delete(0, tk.END)

    def view_expenses(self):
        # Очистка таблицы
        for i in self.tree.get_children():
            self.tree.delete(i)

        filter_cat = self.filter_category.get()
        total = 0.0

        for exp in sorted(self.expenses, key=lambda x: x['date'], reverse=True):
            if filter_cat == "Все" or exp['category'] == filter_cat:
                self.tree.insert("", "end", values=(exp['date'], exp['category'], exp['amount']))
                total += exp['amount']
        
        self.label_total.config(text=f"Итого: {total:.2f}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTrackerApp(root)
    root.mainloop()