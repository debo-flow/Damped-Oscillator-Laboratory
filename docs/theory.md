## 9. Frequency-Domain and Spectral Analysis
To understand the frequency content of the oscillator, we transform the time-domain signal $x(t)$ into the frequency domain using the **Fast Fourier Transform (FFT)**:
$$X(f) = \mathcal{F}\{x(t)\}$$

### Sampling Principles
For a signal recorded over a total duration $T$ with a discrete timestep $dt$ and $N$ total samples, the fundamental parameters defining the spectrum are:
*   **Sampling Frequency:** $f_s = \frac{1}{dt}$
*   **Nyquist Limit:** $f_{Nyquist} = \frac{f_s}{2}$. Frequencies above this limit cannot be resolved and will "alias" (fold back) into lower frequencies.
*   **Frequency Resolution:** $\Delta f = \frac{f_s}{N} \approx \frac{1}{T}$. To distinguish two closely spaced frequencies, the observation duration $T$ must be increased.

### Normalization and Spectral Leakage
For real-valued time signals, the FFT generates a symmetric spectrum. We discard the negative frequencies to create a **One-Sided Amplitude Spectrum**. To match the physical amplitude of a sine wave, the magnitude is scaled by $\frac{2}{N}$ (excluding the DC component).

If a signal's frequency does not land exactly on a discrete bin integer ($k \cdot \Delta f$), the energy spreads into adjacent bins. This phenomenon is called **Spectral Leakage**. Applying **Window Functions** (e.g., Hann, Hamming, Blackman) before the FFT tapers the edges of the time signal to zero, severely reducing leakage at the cost of slightly widening the main frequency peak.

### Power Spectral Density (PSD)
While the FFT Amplitude Spectrum displays raw displacement (meters), the **Power Spectral Density** (often calculated via Welch's Method) represents how the power of the signal is distributed across frequencies. Welch's method computes averaged, overlapping windowed periodograms to smooth out noise in highly dynamic or stochastic signals.
