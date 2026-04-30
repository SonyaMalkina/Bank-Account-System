class BankViewer:
    def display_message(message):
        print(message)


    def display_account_info(account):
        print("\n👤ИНФОРМАЦИЯ ОБ АККАУНТЕ👤")
        print("="*40)
        print(f"Тип аккаунта: {account.account_type}")
        print(f"Номер счета: {account.account_number}")
        print(f"Лимит на снятие: {account.withdraw_limit}")

    def show_start_menu():
        print("1 - Расчётный счёт")
        print("2 - Сберегательный счёт")
        print("3 - Кредитный счёт")

    def show_account_menu(account):
        print(f"\n{'='*40}")
        print(f" 🧭 МЕНЮ ДЕЙСТВИЙ")
        print(f"\n{'='*40}")
        print("1 — Пополнить")
        print("2 — Отправить деньги")
        print("3 — Показать баланс")
        print("4 — Сохранить в JSON")
        print("5 — Выход")


    

    