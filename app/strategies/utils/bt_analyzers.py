from backtrader.analyzers import AnnualReturn, Returns, DrawDown, Calmar, PositionsValue, Transactions, VWR, SQN, PyFolio


def analyzers(cerebro):
    cerebro.addanalyzer(SQN, _name='sqn')
    cerebro.addanalyzer(AnnualReturn, _name='annual_return')
    cerebro.addanalyzer(Returns, _name='returns')
    cerebro.addanalyzer(DrawDown, _name='drawdown')
    cerebro.addanalyzer(Calmar, _name='calmar')
    cerebro.addanalyzer(PositionsValue, _name='positions_value')
    cerebro.addanalyzer(Transactions, _name='transactions')
    cerebro.addanalyzer(VWR, _name='vwr')
    # cerebro.addanalyzer(PyFolio, _name='pyfolio')
    return cerebro

def analyzer_printout(results):
    res = results[0]
    print('System Quality Number:', res.analyzers.sqn.get_analysis())
    print('Annual return:', res.analyzers.annual_return.get_analysis())
    print('Returns:', res.analyzers.returns.get_analysis())
    print('DrawDown:', res.analyzers.drawdown.get_analysis())
    print('Calmar:', res.analyzers.calmar.get_analysis())
    print('Positions value:', res.analyzers.positions_value.get_analysis())
    print('Transactions:', res.analyzers.transactions.get_analysis())
    print('Variability-Weighted Return:', res.analyzers.vwr.get_analysis())
