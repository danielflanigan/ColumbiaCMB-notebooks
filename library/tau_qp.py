from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
import lmfit


def exponential_fall(amplitude, tau, t):
    return amplitude * np.exp(-t / tau)


def single_exponential_model(params, t):
    baseline = params['baseline'].value
    amplitude = params['amplitude'].value
    tau = params['tau'].value
    fall_index = params['fall_index'].value
    return baseline + exponential_fall(amplitude, tau, t[fall_index:] - t[fall_index])


def dual_exponential_model(params, t):
    baseline = params['baseline'].value
    fast_amplitude = params['fast_amplitude'].value
    fast_tau = params['fast_tau'].value
    slow_amplitude = params['slow_amplitude'].value
    slow_tau = params['slow_tau'].value
    fall_index = params['fall_index'].value
    return (baseline +
            exponential_fall(fast_amplitude, fast_tau, t[fall_index:] - t[fall_index]) +
            exponential_fall(slow_amplitude, slow_tau, t[fall_index:] - t[fall_index]))


def single_residual(params, t, data, errors=1):
    fall_index = params['fall_index'].value
    return (data[fall_index:] - single_exponential_model(params, t)) / errors


def dual_residual(params, t, data, errors=1):
    fall_index = params['fall_index'].value
    return (data[fall_index:] - dual_exponential_model(params, t)) / errors


# For pulse only.
def single_guess(t, data, fall_time, left_samples, right_samples):
    p = lmfit.Parameters()
    fall_index = np.searchsorted(t, np.array([fall_time]))[0]
    p.add('fall_index', value=fall_index, vary=False)
    peak = data[fall_index-left_samples:fall_index+right_samples].mean()
    baseline = data[t < 0].mean()
    excursion = peak - baseline 
    p.add('amplitude', value=excursion, vary=False)
    p.add('baseline', value=baseline, vary=False)
    p.add('tau', value=t.ptp()/10, min=0)
    return p


def dual_guess(t, data, fall_time, left_samples, right_samples):
    p = lmfit.Parameters()
    fall_index = np.searchsorted(t, np.array([fall_time]))[0]
    p.add('fall_index', value=fall_index, vary=False)
    peak = data[fall_index-left_samples:fall_index+right_samples].mean()
    baseline = data[t < 0].mean()
    excursion = peak - baseline
    p.add('excursion', value=excursion, vary=False)
    p.add('baseline', value=baseline, vary=False)
    p.add('fast_amplitude', value=0.9*excursion, min=0, max=excursion) # / 2
    p.add('fast_tau', value=0.001*t.ptp(), min=0) # / 10
    p.add('delta_tau', value=t.ptp(), min=0) # / 2
    p.add('slow_amplitude', expr='excursion - fast_amplitude')
    p.add('slow_tau', expr='fast_tau + delta_tau')
    return p


def single_fit(t, data, fall_time, left_samples=100, right_samples=0):
    rms = data[t < 0].std()
    guess = single_guess(t, data, fall_time, left_samples, right_samples)
    fit = lmfit.minimize(single_residual, guess, args=[t, data, rms])
    return fit   


def dual_fit(t, data, fall_time, left_samples=100, right_samples=0):
    rms = data[t < 0].std()
    guess = dual_guess(t, data, fall_time, left_samples, right_samples)
    fit = lmfit.minimize(dual_residual, guess, args=[t, data, rms])
    return fit


def plot_single_fit(params, t, data):
    fall_index = params['fall_index'].value
    time_scale = 1e3
    tau_scale = 1e6
    t0 = t[fall_index]
    fig, ax = plt.subplots()
    ax.plot(time_scale * t[:fall_index], data[:fall_index], ',', color='gray')
    ax.plot(time_scale * t[fall_index:], data[fall_index:], ',', color='black')
    ax.plot(time_scale * t[fall_index:], single_exponential_model(params, t),
            '-r', linewidth=0.5,
            label=r'$\tau = $' + '{:.0f}'.format(tau_scale * params['tau'].value) + r'$\, \mu s$')
    ax.legend(loc='best')
    ax.set_xlabel('time / [ms]')
    ax.set_ylabel('signal / [V]')
    return fig, ax


def plot_dual_fit(params, t, data):
    fall_index = params['fall_index'].value
    time_scale = 1e3
    tau_scale = 1e6
    t0 = t[fall_index]
    fig, ax = plt.subplots()
    ax.plot(time_scale * t[:fall_index], data[:fall_index], ',', color='gray')
    ax.plot(time_scale * t[fall_index:], data[fall_index:], ',', color='black')
    ax.plot(time_scale * t[fall_index:], params['baseline'].value + exponential_fall(params['slow_amplitude'].value, params['slow_tau'].value, t[fall_index:] - t0),
            '-g', linewidth=0.5,
            label=r'$\tau_s = $' + '{:.0f}'.format(tau_scale * params['slow_tau'].value) + r'$\, \mu s$')
    ax.plot(time_scale * t[fall_index:], params['baseline'].value + exponential_fall(params['fast_amplitude'].value, params['fast_tau'].value, t[fall_index:] - t0),
            '-b', linewidth=0.5,
            label=r'$\tau_f = $' + '{:.0f}'.format(tau_scale * params['fast_tau'].value) + r'$\, \mu s$')
    ax.plot(time_scale * t[fall_index:], dual_exponential_model(params, t),
            '-r', linewidth=0.5, label='sum')
    ax.legend(loc='best')
    ax.set_xlabel('time / [ms]')
    ax.set_ylabel('signal / [V]')
    return fig, ax
