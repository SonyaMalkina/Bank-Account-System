class BankView:
    """Консольное представление"""
    
    @staticmethod
    def show_menu():
        print("\n" + "="*50)
        print("        БАНКОВСКАЯ СИСТЕМА")
        print("="*50)
        print("1. Создать новый счет")
        print("2. Посмотреть все счета")
        print("3. Пополнить счет")
        print("4. Снять со счета")
        print("5. Перевести между счетами")
        print("6. История транзакций")
        print("7. Фильтровать историю")
        print("8. Сохранить данные в JSON")
        print("9. Загрузить данные из JSON")
        print("0. Выход")
        print("-"*50)
        return input("Выберите действие: ")
    
    @staticmethod
    def get_account_creation_data():
        print("\n--- Создание нового счета ---")
        acc_type = input("Тип счета (1-Расчётный, 2-Сберегательный, 3-Кредитный): ")
        acc_id = input("Номер счета: ")
        owner = input("Имя владельца: ")
        balance = float(input("Начальный баланс: "))
        
        if not acc_id or not owner:
            raise ValueError("Номер и имя не могут быть пустыми")
        
        type_map = {'1': 'Расчётный', '2': 'Сберегательный', '3': 'Кредитный'}
        return type_map.get(acc_type, 'Расчётный'), acc_id, owner, balance
    
    @staticmethod
    def get_amount(prompt="Сумма: "):
        return float(input(prompt))
    
    @staticmethod
    def get_account_number(prompt="Номер счета: "):
        return input(prompt)
    
    @staticmethod
    def show_message(msg, is_error=False):
        if is_error:
            print(f"❌ Ошибка: {msg}")
        else:
            print(f"✅ {msg}")
    
    @staticmethod
    def show_accounts(accounts):
        if not accounts:
            print("Нет счетов")
            return
        print("\n--- Список счетов ---")
        for acc in accounts:
            print(f" {acc.owner}: {acc.type} счет #{acc.account_number} Баланс: {acc.balance}руб.")
    
    @staticmethod
    def show_transactions(transactions):
        if not transactions:
            print("Нет транзакций")
            return
        print("\n--- История транзакций ---")
        for t in transactions:
            print(f"{t.type}: {t.amount}руб.  Дата: {t.date}")
    
    @staticmethod
    def get_filter_criteria():
        print("\n--- Фильтр транзакций ---")
        print("1. По типу")
        print("2. По дате (ГГГГ-ММ-ДД)")
        choice = input("Выберите фильтр: ")
        
        if choice == '1':
            trans_type = input("Тип (Пополнение/Снятие/Перевод со счёта/Поступление на счёт): ")
            return 'type', trans_type
        elif choice == '2':
            date = input("Дата (ГГГГ-ММ-ДД): ")
            return 'date', date
        else:
            return None, None

    

    