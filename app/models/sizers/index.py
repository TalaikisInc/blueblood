from numpy import array, abs, mean, round, product, min


def worst_loss(returns):
    return abs(min(returns))
 
def bound_returns(returns):
    return returns / worst_loss(returns)

def expected_arithmetic(returns):
    expected_arith = mean(returns)
    return expected_arith
 
def expected_geometric(returns):
    returns = array(returns)
    expected_geom = product(1 + returns) ** (1 / len(returns)) - 1
    return expected_geom

def kelly_fraction(returns):
    returns = array(returns)
    wins = returns[returns > 0]
    losses = returns[returns <= 0]
    W = len(wins) / len(returns)
    R = mean(wins) / abs(mean(losses))
    kelly_f = W - ( (1 - W) / R )
    return kelly_f
 
def kelly_results(returns):
    bounded_rets = bound_returns(returns)
    kelly_f = kelly_fraction(bounded_rets) / worst_loss(returns)
 
    exp_arith_kelly = expected_arithmetic(bounded_rets * kelly_f)
    exp_geom_kelly = expected_geometric(bounded_rets * kelly_f)
 
    print('Kelly f: {}'.format(round(kelly_f, 3)))
    print('Expected Value (Arithmetic): {}%'.format(round(exp_arith_kelly * 100, 5)))
    print('Expected Value (Geometric): {}%'.format(round(exp_geom_kelly * 100, 5)))
