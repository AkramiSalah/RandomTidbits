#!/usr/bin/env python3
"""Audio passthrough with stable terminal EQ-style visualizer using moving max smoothing."""
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
parser.add_argument('-i', '--input-device', type=int_or_str, help='input device ID or substring')
parser.add_argument('-o', '--output-device', type=int_or_str, help='output device ID or substring')
parser.add_argument('-c', '--channels', type=int, default=2, help='number of channels')
parser.add_argument('-t', '--dtype', help='audio data type')
parser.add_argument('-s', '--samplerate', type=float, help='sampling rate')
parser.add_argument('-b', '--blocksize', type=int, help='block size')
parser.add_argument('-l', '--latency', type=float, help='latency in seconds')
args = parser.parse_args()

# Terminal size
term_width, term_height = shutil.get_terminal_size((80, 24))
num_bars = min(term_width // 2, 60)  # max 60 bars, leave spacing
max_height = term_height - 4        # leave room for info lines

threshold = 1e-4  # minimum magnitude to show a bar
decay = 0.95      # decay factor for moving max

# moving maximum for normalization
max_bar = 1e-6

try:
    def callback(indata, outdata, frames, time, status):
        global max_bar
        if status:
            print(status, file=sys.stderr)

        # Mix stereo to mono
        mono = np.mean(indata, axis=1)

        # Compute FFT
        fft = np.fft.rfft(mono)
        magnitude = np.abs(fft)

        # Split FFT into bars
        bar_size = len(magnitude) // num_bars
        bars = []
        for i in range(num_bars):
            start = i * bar_size
            end = start + bar_size
            bar_level = magnitude[start:end].mean()
            bars.append(bar_level)

        # Update moving max for smooth scaling
        current_max = max(bars) or 1e-6
        if current_max > max_bar:
            max_bar = current_max  # grow instantly
        else:
            max_bar *= decay  # decay slowly

        # Normalize and apply threshold with log scaling
        bars = [int((np.log1p(b) / np.log1p(max_bar)) * max_height) if b > threshold else 0 for b in bars]

        # Build display lines
        lines = []
        for row in range(max_height, 0, -1):
            line = ''
            for b in bars:
                line += '█' if b >= row else ' '
                line += ' '
            lines.append(line)

        # Move cursor to top and print
        print("\033[H", end='')  # cursor home
        print('\n'.join(lines))
        print("-" * term_width)
        print("Press Ctrl+C to quit")

        # Pass audio through
        outdata[:] = indata

    with sd.Stream(device=(args.input_device, args.output_device),
                   samplerate=args.samplerate, blocksize=args.blocksize,
                   dtype=args.dtype, latency=args.latency,
                   channels=args.channels, callback=callback):
        # Clear screen before starting
        print("\033[2J")
        input()  # wait for Return to quit

except KeyboardInterrupt:
    parser.exit('\nInterrupted by user')
except Exception as e:
    parser.exit(type(e).__name__ + ': ' + str(e))
