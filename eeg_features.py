# EEG preprocessing
import numpy as np
import scipy.signal

def lr_assymetry_pfl(channels, band="alpha"):
	# asymmetry between left-right prefrontal areas alpha waves, most related to emotional state, and approach withdrawal
	# Prefrontal Cortex, Emotion, and Approach/Withdrawal Motivation
	# Jeffrey M. Spielberg, Jennifer L. Stewart, Rebecca L. Levin, Gregory A. Miller, and Wendy Heller

	# Left Nodes = f3 (3 in the data)
	# Right Nodes = f4 (20)
	f3 = channels[2]
	f4 = channels[19]

	alphaL, thetaL, betaL = power_spectrums_specific(f3)
	alphaR, thetaR, betaR = power_spectrums_specific(f4)

	if (band == "alpha"):
		assymetry_result = np.log(np.absolute(alphaR)) - np.log(np.absolute(alphaL))
	elif (band == "theta"):
		assymetry_result = np.log(np.absolute(thetaR)) - np.log(np.absolute(thetaL))
	else:
		assymetry_result = np.log(np.absolute(betaR)) - np.log(np.absolute(betaL))

	assymetry_result = np.log(np.absolute(alphaR))-np.log(np.absolute(alphaL))
	return assymetry_result

def lr_assymetry_ears(channels, band="alpha"):
	# asymmetry between left-right ear areas alpha waves, most related to emotional state, and approach withdrawal
	# Prefrontal Cortex, Emotion, and Approach/Withdrawal Motivation
	# Jeffrey M. Spielberg, Jennifer L. Stewart, Rebecca L. Levin, Gregory A. Miller, and Wendy Heller

	# Left Nodes = f3 (3 in the data)
	# Right Nodes = f4 (20)
	t7 = channels[7]
	t8 = channels[25]

	alphaL, thetaL, betaL = power_spectrums_specific(t7)
	alphaR, thetaR, betaR = power_spectrums_specific(t8)

	if (band == "alpha"):
		assymetry_result = np.log(np.absolute(alphaR)) - np.log(np.absolute(alphaL))
	elif (band == "theta"):
		assymetry_result = np.log(np.absolute(thetaR)) - np.log(np.absolute(thetaL))
	else:
		assymetry_result = np.log(np.absolute(betaR)) - np.log(np.absolute(betaL))

	assymetry_result = np.log(np.absolute(alphaR))-np.log(np.absolute(alphaL))
	return assymetry_result

def lr_assymetry_back(channels, band="alpha"):
	# asymmetry between left right back areas alpha waves, most related to emotional state, and approach withdrawal
	# "OCCIPITAL AREA" related to vision
	# Jeffrey M. Spielberg, Jennifer L. Stewart, Rebecca L. Levin, Gregory A. Miller, and Wendy Heller

	# Left Nodes = f3 (3 in the data)
	# Right Nodes = f4 (20)
	o1 = channels[7]
	o2 = channels[25]

	alphaL, thetaL, betaL = power_spectrums_specific(o1)
	alphaR, thetaR, betaR = power_spectrums_specific(o2)

	if (band == "alpha"):
		assymetry_result = np.log(np.absolute(alphaR)) - np.log(np.absolute(alphaL))
	elif (band == "theta"):
		assymetry_result = np.log(np.absolute(thetaR)) - np.log(np.absolute(thetaL))
	else:
		assymetry_result = np.log(np.absolute(betaR)) - np.log(np.absolute(betaL))

	assymetry_result = np.log(np.absolute(alphaR))-np.log(np.absolute(alphaL))
	return assymetry_result

def eeg_bands(signal):
	# returns the alpha, theta, beta
	eeg = signal 
	pi = np.pi
	y = np.array(eeg)  # faster array
	L = len(eeg)       # signal length
	fs = 128.0     # frequency sampling 128Hz
	T = 1/fs           # sample time
	t = np.linspace(1,L,L)*T

	f = fs*np.linspace(0,L/10,L/10)/L  # single side frequency vector, real frequency up to fs/2
	Y = np.fft.fft(y)

	filtered = []
	b= [] # store filter coefficient
	cutoff = [0.5,4.0,8.0,12.0,30.0] # delta, alpha, theta, beta bands

	for band in xrange(0, len(cutoff)-1):
		wl = 2*cutoff[band]/fs*pi
		wh = 2*cutoff[band+1]/fs*pi
		M = 512      # Set number of weights as 128
		bn = np.zeros(M)

		for i in xrange(0,M):     # Generate bandpass weighting function
			n = i-  M/2       # Make symmetrical
			if n == 0:
				bn[i] = wh/pi - wl/pi;
			else:
				bn[i] = (np.sin(wh*n))/(pi*n) - (np.sin(wl*n))/(pi*n)   # Filter impulse response

		bn = bn*np.kaiser(M,5.2)  # apply Kaiser window, alpha= 5.2
		b.append(bn)

		[w,h]= scipy.signal.freqz(bn,1)
		filtered.append(np.convolve(bn, y)) # filter the signal by convolving the signal with filter coefficients


	alpha = filtered[1]
	alpha = np.fft.fft(alpha [ M/2:L+M/2])
	theta = filtered[2]
	theta = np.fft.fft(theta [ M/2:L+M/2])
	beta = filtered[3]
	beta = np.fft.fft(beta [ M/2:L+M/2])

	return alpha, theta, beta

def power_spectrums(signal):
	# calculates the concatenated vector of the power spectra
	# for the alpha, theta, beta bands
	# via the welch method for estimating spectral density
	c = scipy.signal.welch(signal, fs=128, scaling = 'spectrum')
	interestingPower = c[1][8:61]
	return interestingPower

def power_spectrums_specific(signal):
	# calculates the concatenated vector of the power spectra
	# for the alpha, theta, beta bands
	# via the welch method for estimating spectral density
	baseline = scipy.signal.welch(signal[:384], fs=128, scaling = 'spectrum')
	trial_freq = scipy.signal.welch(signal[4224:], fs=128, scaling = 'spectrum')
	c = trial_freq-baseline
	alpha = (c[1])[8:17]
	theta = (c[1])[16:25]
	beta = (c[1])[25:61]

	return alpha, theta, beta

def eeg_w_beta(signal):
	# calculates eeg_w
	# Chanel et al Emotion assessment from physiological signals for 
	# adaptation of game difficulty
	alpha, theta, beta = eeg_bands(signal[4224:])
	nomin = np.sum(beta)
	denom = np.sum(theta + alpha)
	eeg_w = np.log(np.absolute(nomin/denom))
	return eeg_w


