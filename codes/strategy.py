from backtest import BacktestEngine
from codes import config
from codes.handles import tick

class MyStrategy(BacktestEngine):

    def __init__(self):
        super().__init__()

    def on_tick(self):
        tick.handle(config.threshold)

    def on_bar(self):
        pass

    def on_order(self):
        pass

def main():
    engine = MyStrategy()
    engine.load_data()
    engine.run()
    engine.plot_results()
main()