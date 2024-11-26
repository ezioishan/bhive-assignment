from threading import Thread
import time
import random

def update_portfolio_values(portfolios):
    def update():
        while True:
            for portfolio in portfolios.values():
                for investment in portfolio.investments:
                    investment.current_value += random.uniform(-5, 5)
            time.sleep(3600)  # Simulate hourly updates

    thread = Thread(target=update, daemon=True)
    thread.start()
