import warnings
warnings.simplefilter('ignore')

from scipy import stats
from pandas import DataFrame


cdfs = [
    'norm',            #Normal (Gaussian)
    'alpha',           #Alpha
    'anglit',          #Anglit
    'arcsine',         #Arcsine
    'beta',            #Beta
    'betaprime',       #Beta Prime
    'bradford',        #Bradford
    'burr',            #Burr
    'cauchy',          #Cauchy
    'chi',             #Chi
    'chi2',            #Chi-squared
    'cosine',          #Cosine
    'dgamma',          #Double Gamma
    'dweibull',        #Double Weibull
    'erlang',          #Erlang
    'expon',           #Exponential
    'exponweib',       #Exponentiated Weibull
    'exponpow',        #Exponential Power
    'fatiguelife',     #Fatigue Life (Birnbaum-Sanders)
    'foldcauchy',      #Folded Cauchy
    'f',               #F (Snecdor F)
    'fisk',            #Fisk
    'foldnorm',        #Folded Normal
    'frechet_r',       #Frechet Right Sided, Extreme Value Type II
    'frechet_l',       #Frechet Left Sided, Weibull_max
    'gamma',           #Gamma
    'gausshyper',      #Gauss Hypergeometric
    'genexpon',        #Generalized Exponential
    'genextreme',      #Generalized Extreme Value
    'gengamma',        #Generalized gamma
    'genlogistic',     #Generalized Logistic
    'genpareto',       #Generalized Pareto
    'genhalflogistic', #Generalized Half Logistic
    'gilbrat',         #Gilbrat
    'gompertz',        #Gompertz (Truncated Gumbel)
    'gumbel_l',        #Left Sided Gumbel, etc.
    'gumbel_r',        #Right Sided Gumbel
    'halfcauchy',      #Half Cauchy
    'halflogistic',    #Half Logistic
    'halfnorm',        #Half Normal
    'hypsecant',       #Hyperbolic Secant
    'invgamma',        #Inverse Gamma
    'invnorm',         #Inverse Normal
    'invweibull',      #Inverse Weibull
    'johnsonsb',       #Johnson SB
    'johnsonsu',       #Johnson SU
    'laplace',         #Laplace
    'logistic',        #Logistic
    'loggamma',        #Log-Gamma
    'loglaplace',      #Log-Laplace (Log Double Exponential)
    'lognorm',         #Log-Normal
    'lomax',           #Lomax (Pareto of the second kind)
    'maxwell',         #Maxwell
    'mielke',          #Mielke's Beta-Kappa
    'nakagami',        #Nakagami
    'ncx2',            #Non-central chi-squared
#    'ncf',             #Non-central F
    'nct',             #Non-central Student's T
    'norm'           # Normal
    'pareto',          #Pareto
    'powerlaw',        #Power-function
    'powerlognorm',    #Power log normal
    'powernorm',       #Power normal
    'rdist',           #R distribution
    'reciprocal',      #Reciprocal
    'rayleigh',        #Rayleigh
    'rice',            #Rice
    'recipinvgauss',   #Reciprocal Inverse Gaussian
    'semicircular',    #Semicircular
    't',               #Student's T
    'triang',          #Triangular
    'truncexpon',      #Truncated Exponential
    'truncnorm',       #Truncated Normal
    'tukeylambda',     #Tukey-Lambda
    'uniform',         #Uniform
    'vonmises',        #Von-Mises (Circular)
    'wald',            #Wald
    'weibull_min',     #Minimum Weibull (see Frechet)
    'weibull_max',     #Maximum Weibull (see Frechet)
    'wrapcauchy',      #Wrapped Cauchy
    'ksone',           #Kolmogorov-Smirnov one-sided (no stats)
    'kstwobign']       #Kolmogorov-Smirnov two-sided test for Large N

def distr_finder(data):
    res = []
    for cdf in cdfs:
        try:
            params = eval('stats.'+cdf+'.fit(data)')
            D, p = stats.kstest(data, cdf, args=params)
            D = round(D, 5)
            p = round(p, 5)
            res.append([cdf.ljust(16), D, p])
        except Exception as err:
            continue
    return DataFrame(res, columns=['Distribution', 'D', 'p']).sort_values('D')

def get_params(cdf, data):
    return eval('stats.'+cdf+'.fit(data)')

def gen_data(cdf, params, size):
    roll = eval('stats.'+cdf+'.rvs(params[0], size=size)')
    return roll
