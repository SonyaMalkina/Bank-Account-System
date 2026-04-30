import unittest
import os
from model import (
    Account, CheckingAccount, SavingsAccount, CreditAccount,
    Transaction, TransactionHistoryQueue, BankModel
)


class TestBank(unittest.TestCase):
    """Полный набор тестов для банковской системы"""
    
    def setUp(self):
        """Подготовка перед каждым тестом - создаем тестовые счета"""
        self.checking = CheckingAccount("C001", "Расчёт Тест", 1000)
        self.savings = SavingsAccount("S001", "Сберег Тест", 500, min_balance=100)
        self.credit = CreditAccount("CR001", "Кредит Тест", -200, credit_limit=1000)
        self.model = BankModel()
        
        # Добавляем счета в модель
        self.model.add_account(self.checking)
        self.model.add_account(self.savings)
        self.model.add_account(self.credit)
    
    # ==================== ТЕСТЫ КЛАССА TRANSACTION ====================
    
    def test_transaction_creation(self):
        """Тест создания транзакции"""
        trans = Transaction("Пополнение", 100)
        self.assertEqual(trans.type, "Пополнение")
        self.assertEqual(trans.amount, 100)
        self.assertIsNotNone(trans.date)

    # ==================== ТЕСТЫ ОЧЕРЕДИ ТРАНЗАКЦИЙ ====================
    
    def test_transaction_queue_add(self):
        """Тест добавления в очередь транзакций"""
        queue = TransactionHistoryQueue()
        queue.add_transaction(Transaction("Пополнение", 100))
        queue.add_transaction(Transaction("Снятие", 50))
        self.assertEqual(len(queue.get_all()), 2)
    
    
    def test_transaction_queue_filter_by_type(self):
        """Тест фильтрации по типу транзакции"""
        queue = TransactionHistoryQueue()
        queue.add_transaction(Transaction("Пополнение", 100))
        queue.add_transaction(Transaction("Снятие", 50))
        queue.add_transaction(Transaction("Пополнение", 200))
        
        deposits = queue.filter_by_type("Пополнение")
        withdraws = queue.filter_by_type("Снятие")
        
        self.assertEqual(len(deposits), 2)
        self.assertEqual(len(withdraws), 1)
    
    def test_transaction_queue_filter_by_date(self):
        """Тест фильтрации по дате"""
        queue = TransactionHistoryQueue()
        queue.add_transaction(Transaction("Пополнение", 100, "2026-01-01 10:00:00"))
        queue.add_transaction(Transaction("Снятие", 50, "2026-01-02 11:00:00"))
        queue.add_transaction(Transaction("Пополнение", 200, "2026-01-01 15:00:00"))
        
        filtered = queue.filter_by_date("2026-01-01")
        self.assertEqual(len(filtered), 2)
    
    def test_transaction_queue_to_from_dict(self):
        """Тест сериализации очереди"""
        queue = TransactionHistoryQueue()
        queue.add_transaction(Transaction("Пополнение", 100))
        queue.add_transaction(Transaction("Снятие", 50))
        
        data = queue.to_dict()
        new_queue = TransactionHistoryQueue()
        new_queue.from_dict(data)
        
        self.assertEqual(len(new_queue.get_all()), 2)
        self.assertEqual(new_queue.get_all()[0].amount, 100)
    
    # ==================== ТЕСТЫ СЧЕТОВ ====================
    
    def test_checking_account_deposit(self):
        """Тест пополнения расчетного счета"""
        self.checking.deposit(500)
        self.assertEqual(self.checking.balance, 1500)
    
    def test_checking_account_withdraw(self):
        """Тест снятия с расчетного счета"""
        self.checking.withdraw(300)
        self.assertEqual(self.checking.balance, 700)
    
    def test_checking_account_withdraw_insufficient_funds(self):
        """Тест ошибки при недостатке средств"""
        with self.assertRaises(ValueError) as context:
            self.checking.withdraw(2000)
        self.assertIn("Недостаточно средств", str(context.exception))
    
    def test_savings_account_withdraw_min_balance(self):
        """Тест сберегательного счета - проверка минимального остатка"""
        # Успешное снятие (остаток 400 >= 100)
        self.savings.withdraw(100)
        self.assertEqual(self.savings.balance, 400)

    
    def test_credit_account_withdraw_credit_limit(self):
        """Тест кредитного счета - проверка кредитного лимита"""
        # Успешное снятие в рамках лимита
        self.credit.withdraw(500)  # Баланс станет -700 (лимит 1000)
        self.assertEqual(self.credit.balance, -700)
        
        # Ошибка - превышение лимита
        with self.assertRaises(ValueError) as context:
            self.credit.withdraw(400)  # Станет -1100, лимит 1000
        self.assertIn("кредитный лимит", str(context.exception))
    
    def test_account_negative_amount(self):
        """Тест на отрицательную сумму"""
        with self.assertRaises(ValueError):
            self.checking.deposit(-100)
        
        with self.assertRaises(ValueError):
            self.checking.withdraw(-50)
    
    def test_account_transaction_history(self):
        """Тест истории транзакций счета"""
        self.checking.deposit(200)
        self.checking.withdraw(50)
        
        history = self.checking.history.get_all()
        self.assertEqual(len(history), 2)
        self.assertEqual(history[0].type, "Пополнение")
        self.assertEqual(history[1].type, "Снятие")
    
    def test_account_get_type(self):
        """Тест определения типа счета"""
        self.assertEqual(self.checking.get_account_type(), "Расчётный")
        self.assertEqual(self.savings.get_account_type(), "Сберегательный")
        self.assertEqual(self.credit.get_account_type(), "Кредитный")
  


def run_tests():
    """Функция для запуска всех тестов"""
    # Создаем загрузчик тестов
    loader = unittest.TestLoader()
    
    # Создаем набор тестов
    suite = unittest.TestSuite()
    suite.addTests(loader.loadTestsFromTestCase(TestBank))
    
    # Запускаем тесты с подробным выводом
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Выводим результат
    return result 


if __name__ == "__main__":
    # Запускаем тесты
    unittest.main(verbosity=2)