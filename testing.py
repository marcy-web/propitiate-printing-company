import wave
import math
import struct
import os
import time

# Define the frequencies for a C major scale (C4 to C5)
# do=C, re=D, mi=E, fa=F, so=G, la=A, ti=B, do=C
NOTE_FREQUENCIES = {
    "C4": 261.63,  # do
    "D4": 293.66,  # re
    "E4": 329.63,  # mi
    "F4": 349.23,  # fa
    "G4": 392.00,  # so
    "A4": 440.00,  # la
    "B4": 493.88,  # ti
    "C5": 523.25   # do (octave higher)
}

def generate_piano_note(frequency, duration=0.5, volume=0.5, sample_rate=44100):
    """Generate audio data for a piano-like note"""
    num_samples = int(sample_rate * duration)
    audio_data = []
    
    # Parameters for a more piano-like sound
    attack_time = 0.01  # Short attack
    decay_time = 0.1    # Quick initial decay
    release_time = 0.3  # Longer release tail
    
    # Number of samples for each phase
    attack_samples = int(attack_time * sample_rate)
    decay_samples = int(decay_time * sample_rate)
    release_samples = int(release_time * sample_rate)
    
    # Add overtones (harmonics) with decreasing amplitudes
    overtones = [
        (1.0, 0.7),     # Fundamental frequency (strongest)
        (2.0, 0.2),     # 1st overtone (an octave up)
        (3.0, 0.05),    # 2nd overtone
        (4.0, 0.03),    # 3rd overtone
        (5.0, 0.02),    # 4th overtone
        (6.0, 0.01),    # 5th overtone
    ]
    
    for i in range(num_samples):
        sample = 0
        # Calculate envelope
        if i < attack_samples:
            # Attack phase (quick ramp up)
            envelope = (i / attack_samples) * volume
        elif i < attack_samples + decay_samples:
            # Decay phase (quick drop to sustain level)
            decay_progress = (i - attack_samples) / decay_samples
            envelope = volume * (1.0 - (decay_progress * 0.3))
        elif i > num_samples - release_samples:
            # Release phase (gradual fade out)
            release_progress = (i - (num_samples - release_samples)) / release_samples
            envelope = volume * 0.7 * (1.0 - release_progress)
        else:
            # Sustain phase
            envelope = volume * 0.7
        
        # Add all overtones with their respective amplitudes
        for overtone_ratio, amplitude in overtones:
            sample += envelope * amplitude * math.sin(2 * math.pi * frequency * overtone_ratio * i / sample_rate)
        
        # Add a slight detuning for richness (piano strings aren't perfectly tuned)
        slight_detune = envelope * 0.02 * math.sin(2 * math.pi * frequency * 1.003 * i / sample_rate)
        sample += slight_detune
        
        # Soft clipping to prevent harsh distortion
        if sample > 1.0:
            sample = 1.0 - (1.0 / (sample + 0.1))
        elif sample < -1.0:
            sample = -1.0 + (1.0 / (-sample + 0.1))
            
        audio_data.append(int(sample * 32767))
    
    # Pack as signed 16-bit PCM
    return struct.pack('h' * len(audio_data), *audio_data)

def generate_scale(filename, note_durations=0.3, volume=0.5, sample_rate=44100):
    """Generate a WAV file with the C major scale (do re mi fa so la ti do)"""
    # Open the WAV file
    with wave.open(filename, 'wb') as wav_file:
        wav_file.setnchannels(1)  # Mono
        wav_file.setsampwidth(2)  # 2 bytes (16 bits)
        wav_file.setframerate(sample_rate)
        
        # Generate and write each note in the scale
        for note_name in ["C4", "D4", "E4", "F4", "G4", "A4", "B4", "C5"]:
            frequency = NOTE_FREQUENCIES[note_name]
            note_data = generate_piano_note(frequency, note_durations, volume, sample_rate)
            wav_file.writeframes(note_data)
    
    # Play the file using system commands
    if os.name == 'nt':  # Windows
        os.system(f'start {filename}')
    elif os.name == 'posix':  # Mac/Linux
        os.system(f'aplay {filename}' if os.system('which aplay > /dev/null') == 0 else f'afplay {filename}')

def generate_melody(filename, notes, durations=None, volume=0.5, sample_rate=44100):
    """
    Generate a WAV file with a custom melody
    
    Args:
        filename: Output WAV filename
        notes: List of note names (e.g., ["C4", "E4", "G4"])
        durations: List of note durations in seconds (defaults to 0.3s for each note)
        volume: Volume from 0.0 to 1.0
        sample_rate: Audio sample rate
    """
    if durations is None:
        durations = [0.3] * len(notes)
    
    with wave.open(filename, 'wb') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        
        for i, note_name in enumerate(notes):
            frequency = NOTE_FREQUENCIES[note_name]
            duration = durations[i]
            note_data = generate_piano_note(frequency, duration, volume, sample_rate)
            wav_file.writeframes(note_data)
    
    # Play the file
    if os.name == 'nt':
        os.system(f'start {filename}')
    elif os.name == 'posix':
        os.system(f'aplay {filename}' if os.system('which aplay > /dev/null') == 0 else f'afplay {filename}')

notes = ["C4", "E4", "G4", "C5", "G4", "E4", "A4", "F4", "A4", "C5", "A4", "F4"]
durations = [0.7, 0.7, 0.7, 1.4, 0.7, 0.7, 0.7, 0.7, 0.7, 1.4, 0.7, 0.7]
generate_melody("mary.wav", notes, durations)


# Example usage
# generate_scale("do_re_mi.wav")