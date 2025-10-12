#!/usr/bin/env python3
"""
Terminal EQ-style visualizer with live audio input.

- Left = low frequencies, right = high frequencies
- Bar height = volume/magnitude of that frequency
- Logarithmic frequency mapping
- ANSI colors for bar intensity
- No smoothing
"""
import argparse
import numpy as np
import sounddevice as sd
import shutil
import sys

def int_or_str(text):
    try:
        return int(text)
    except ValueError:
        return text

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('-i', '--input-device', type=int_or_str, help='input device ID')
parser.add_argument('-c', '--channels', type=int, default=2, help='number of channels')
parser.add_argument('-t', '--dtype', help='audio data type')
parser.add_argument('-s', '--samplerate', type=float, help='sampling rate')
parser.add_argument('-b', '--blocksize', type=int, default=2048, help='block size')
args = parser.parse_args()

term_width, term_height = shutil.get_terminal_size((80, 24))
num_bars = min(term_width // 2, 60)  # number of frequency bars to display
max_height = term_height - 4

# Generate logarithmic frequency mapping indices
def log_indices(n_fft, num_bars):
    freqs = np.logspace(np.log10(1), np.log10(n_fft), num_bars+1, dtype=int)
    return [(freqs[i], freqs[i+1]) for i in range(num_bars)]

try:
    def callback(indata, frames, time, status):
        if status:
            print(status, file=sys.stderr)

        # Mix stereo to mono
        mono = np.mean(indata, axis=1)

        # Compute FFT
        fft = np.fft.rfft(mono)
        magnitude = np.abs(fft)

        # Noise floor to avoid crazy spikes
        magnitude = np.maximum(magnitude, 1e-6)

        # Compute logarithmic bins
        bins = log_indices(len(magnitude), num_bars)
        bars = []
        max_mag = np.max(magnitude) or 1e-6  # avoid division by zero

        for start, end in bins:
            if end <= start:  # empty slice
                bars.append(0)
            else:
                bars.append(int(np.mean(magnitude[start:end]) / max_mag * max_height))

        # Build display lines
        lines = []
        for row in range(max_height, 0, -1):
            line = ''
            for bar in bars:
                if bar >= row:
                    # Color: green low, yellow mid, red high
                    if row > max_height * 0.66:
                        color = "\033[91m"  # red
                    elif row > max_height * 0.33:
                        color = "\033[93m"  # yellow
                    else:
                        color = "\033[92m"  # green
                    line += f"{color}█\033[0m "
                else:
                    line += '  '
            lines.append(line)

        # Move cursor to top and print
        print("\033[H", end='')
        print('\n'.join(lines))
        print("-" * term_width)
        print("Press Ctrl+C to quit")

    print("\033[2J")  # clear terminal

    with sd.InputStream(
        device=args.input_device,
        samplerate=args.samplerate,
        blocksize=args.blocksize,
        dtype=args.dtype,
        channels=args.channels,
        callback=callback
    ):
        input()  # wait for Return to quit

except KeyboardInterrupt:
    print("\nStopped by user")
except Exception as e:
    print(type(e).__name__, e)
