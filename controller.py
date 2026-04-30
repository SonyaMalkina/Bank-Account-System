from model import BankModel, CheckingAccount, CreditAccount, SavingsAccount
from view import BankView


class BankController:
    def __init__(self):
        self.model = BankModel()
        self.view = BankView()
    
    def create_account(self):
        try:
            acc_type, acc_id, owner, balance = self.view.get_account_creation_data()
            
            # Проверка на существующий ID
            if acc_id in self.model.accounts:
                self.view.show_message(f"Счет {acc_id} уже существует", True)
                return
            
            if acc_type == 'Расчётный':
                account = CheckingAccount(acc_id, owner, balance)
            elif acc_type == 'Сберегательный':
                min_bal = float(input("Минимальный остаток (по умолчанию 50): ") or 50)
                account = SavingsAccount(acc_id, owner, balance, min_bal)
            elif acc_type == 'Кредитный':
                credit_lim = float(input("Кредитный лимит (по умолчанию 500): ") or 500)
                account = CreditAccount(acc_id, owner, balance, credit_lim)
            else:
                self.view.show_message("Неверный тип счета", True)
                return
            
            self.model.add_account(account)
            self.view.show_message(f"Счет {acc_id} создан!")
            
        except ValueError as e:
            self.view.show_message(str(e), True)
    
    def show_all_accounts(self):
        accounts = self.model.list_accounts()
        self.view.show_accounts(accounts)
    
    def deposit(self):
        try:
            acc_id = self.view.get_account_number()
            amount = self.view.get_amount()
            account = self.model.get_account(acc_id)
            account.deposit(amount)
            self.view.show_message(f"Пополнено {amount:.2f}руб. Новый баланс: {account.balance:.2f}руб.")
        except ValueError as e:
            self.view.show_message(str(e), True)
    
    def withdraw(self):
        try:
            acc_id = self.view.get_account_number()
            amount = self.view.get_amount()
            account = self.model.get_account(acc_id)
            account.withdraw(amount)
            self.view.show_message(f"Снято {amount:.2f}руб. Новый баланс: {account.balance:.2f}руб.")
        except ValueError as e:
            self.view.show_message(str(e), True)
    
    def transfer(self):
        try:
            from_id = self.view.get_account_number("С какого счета: ")
            to_id = self.view.get_account_number("На какой счет: ")
            amount = self.view.get_amount()
            self.model.transfer(from_id, to_id, amount)
            self.view.show_message(f"Переведено {amount:.2f}руб. со счета {from_id} на {to_id}")
        except ValueError as e:
            self.view.show_message(str(e), True)
    
    def show_transactions(self):
        try:
            acc_id = self.view.get_account_number()
            account = self.model.get_account(acc_id)
            transactions = account.history.get_all()
            self.view.show_transactions(transactions)
        except ValueError as e:
            self.view.show_message(str(e), True)
    
    def filter_transactions(self):
        try:
            acc_id = self.view.get_account_number()
            account = self.model.get_account(acc_id)
            filter_type, filter_value = self.view.get_filter_criteria()
            
            if filter_type == 'type':
                result = account.history.filter_by_type(filter_value)
            elif filter_type == 'date':
                result = account.history.filter_by_date(filter_value)
            else:
                return
            
            self.view.show_transactions(result)
        except ValueError as e:
            self.view.show_message(str(e), True)
    
    def save_data(self):
        try:
            self.model.save_to_file()
            self.view.show_message("Данные сохранены в data.json")
        except Exception as e:
            self.view.show_message(f"Ошибка сохранения: {e}", True)
    
    def load_data(self):
        try:
            if self.model.load_from_file():
                self.view.show_message("Данные загружены из data.json")
            else:
                self.view.show_message("Файл не найден, создана новая база")
        except Exception as e:
            self.view.show_message(f"Ошибка загрузки: {e}", True)
    
    def run(self):
        self.view.show_message("Добро пожаловать в банковскую систему!")
        self.load_data()  # Автозагрузка
        
        while True:
            choice = self.view.show_menu()
            
            if choice == '1':
                self.create_account()
            elif choice == '2':
                self.show_all_accounts()
            elif choice == '3':
                self.deposit()
            elif choice == '4':
                self.withdraw()
            elif choice == '5':
                self.transfer()
            elif choice == '6':
                self.show_transactions()
            elif choice == '7':
                self.filter_transactions()
            elif choice == '8':
                self.save_data()
            elif choice == '9':
                self.load_data()
            elif choice == '0':
                self.save_data()  # Автосохранение при выходе
                self.view.show_message("До свидания!")
                break
            else:
                self.view.show_message("Неверный выбор", True)







        

        


