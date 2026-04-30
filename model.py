import json
from datetime import datetime
from collections import deque
from abc import ABC, abstractmethod


class Transaction:
    """Класс транзакции"""
    def __init__(self, type, amount, date=None):
        self.type = type
        #"пополнение", "снятие", "перевод со счёта", "поступление на счёт"
        self.amount = amount
        self.date = date if date else datetime.now().strftime("%Y-%m-%d, %H:%M:%S")

    
class TransactionHistoryQueue:
    """Класс очереди транзакций"""
    def __init__(self):
        self.queue = deque()

    """Добавление транзакции в очередь"""
    def add_transaction(self, transaction): 
        self.queue.append(transaction)

    def get_all(self):
        return list(self.queue)
    
    """Фильтрация по типу транзакции"""
    def filter_by_type(self, t_type):
        transactions = []
        for trans in self.queue:
            if trans.type == t_type:
                transactions.append(trans)
        return transactions
    
    """Фильтрация по дате"""
    def filter_by_date(self, date_str):
        transactions = []
        for trans in self.queue:
            if trans.date.startswith(date_str):
                transactions.append(trans)
        return transactions
    
    def clear(self):
        self.queue.clear()

    def to_dict(self):
        transactions = []
        for trans in self.queue:
            data = {"type" : trans.type,
                    "amount" : trans.amount,
                    "date" : trans.date}
            transactions.append(data)
        return transactions
    
    def from_dict(self, data):
        self.queue.clear()
        for item in data:
            trans = Transaction(item['type'], item['amount'], item['date'])
            self.queue.append(trans)


class Account(ABC):
    """Абстрактный класс аккаунта"""
    def __init__(self, account_number, owner_name, inital_balance=0):
        self.balance = inital_balance 
        self.account_number = account_number
        self.owner = owner_name
        self.history = TransactionHistoryQueue()

    @abstractmethod
    def get_account_type(self):
        pass


    def get_balance(self):
        return self.balance
    

    def get_account_number(self):
        return self.account_number
    

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            self.history.add_transaction(Transaction("Пополнение", amount))
            return True
        else:
            raise ValueError("Сумма должна быть положительной")
        
    def withdraw(self, amount):
        if amount > self.balance:
            raise ValueError("Недостаточно средств")
        if amount <= 0:
            raise ValueError("Сумма должна быть положительной")
        else:
            self.balance -= amount
            self.history.add_transaction(Transaction("Снятие", amount))
            return True
            
    
    def to_dict(self):
        return { "account_number" : self.account_number,
                "owner" : self.owner, 
                "balance" : self.balance,
                "type" : self.get_account_type(),
                "history" : self.history.to_dict() }

    def from_dict(self, data):
        self.account_number = data['account_number']
        self.owner = data['owner']
        self.balance = data['balance']
        self.history.from_dict(data.get('history', []))

    
class CheckingAccount(Account):
    """ Обычный расчетный счёт """
    def __init__(self, account_number, owener_name, inital_balance=0):
        super().__init__(account_number, owener_name, inital_balance)
        self.type = "Расчётный"


    def get_account_type(self):
        return "Расчётный"
    

class SavingsAccount(Account):
    """ Сберегательный счёт, есть минимум остатка"""
    def __init__(self, account_number, owener_name, inital_balance=0, min_balance=50):
        super().__init__(account_number, owener_name, inital_balance)
        self.min_balance = min_balance
        self.type = "Сберегательный"
    
    def get_account_type(self):
        return "Сберегательный"
    

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Сумма должна быть положительной")
        elif self.balance - amount < self.min_balance:
            raise ValueError(f"Недостаточно средств❗Минимальный остаток: {self.min_balance}")
        else:
            self.balance -= amount
            self.history.add_transaction(Transaction("Снятие", amount))
            return True

    def to_dict(self):
        data = super().to_dict()
        data['min_balance'] = self.min_balance
        return data
    
    def from_dict(self, data):
        super().from_dict(data)
        self.min_balance = data.get('min_balance',50)

    
class CreditAccount(Account):
    """ Кредитный счет, заимствование у банка, лимит на транзакции """
    def __init__(self, account_number, owener_name, inital_balance=0, credit_limit = 500):
        super().__init__(account_number, owener_name, inital_balance)
        self.credit_limit = credit_limit
        self.type = "Кредитный"


    def get_account_type(self):
        return "Кредитный"

    
    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Сумма должна быть положительной")
        elif self.balance - amount < -self.credit_limit:
            raise ValueError(f"Превышен кредитный лимит в {self.credit_limit} руб.")
        else:
            self.balance -= amount
            self.history.add_transaction(Transaction("Снятие", amount))
            return True
        
    
    def to_dict(self):
        data = super().to_dict()
        data['credit_limit'] = self.credit_limit
        return data
    

    def from_dict(self, data):
        super().from_dict(data)
        self.credit_limit = data.get('credit_limit', 500)


class BankModel:
    """Модель банка, управляет всеми счетами"""
    def __init__(self):
        self.accounts = {}
    
    def add_account(self, account):
        if account.account_number in self.accounts:
            raise ValueError(f"Счет #{account.account_number} уже существует")
        self.accounts[account.account_number] = account
    
    def get_account(self, account_number):
        if account_number not in self.accounts:
            raise ValueError(f"Счет {account_number} не найден")
        return self.accounts[account_number]
    
    def transfer(self, from_id, to_id, amount):
        if from_id == to_id:
            raise ValueError("Нельзя перевести деньги на тот же счет")
        
        from_account = self.get_account(from_id)
        to_account = self.get_account(to_id)
        
        # Снимаем
        from_account.withdraw(amount)
        
        # Добавляем на другой счет
        to_account.deposit(amount)
        
        # Записываем транзакции перевода
        from_account.history.add_transaction(
            Transaction("Перевод со счёта", amount)
        )
        to_account.history.add_transaction(
            Transaction("Поступление на счёт", amount)
        )
        return True
    
    def list_accounts(self):
        return list(self.accounts.values())
    
    def save_to_file(self, filename="data.json"):
        data = {
            "accounts": [acc.to_dict() for acc in self.accounts.values()]
        }
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
    
    def load_from_file(self, filename="data.json"):
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            self.accounts.clear()
            for acc_data in data['accounts']:
                acc_type = acc_data['type']
                if acc_type == "Расчётный":
                    acc = CheckingAccount(0, "")
                elif acc_type == "Сберегательный":
                    acc = SavingsAccount(0, "")
                elif acc_type == "Кредитный":
                    acc = CreditAccount(0, "")
                else:
                    continue
                acc.from_dict(acc_data)
                self.accounts[acc.account_number] = acc
            return True
        except FileNotFoundError:
            return False





    

    
