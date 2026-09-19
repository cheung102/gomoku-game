import wave
import struct
import math
import os

def generate_sine_wave(frequency, duration, sample_rate=44100, amplitude=0.5):
    """生成正弦波"""
    num_samples = int(sample_rate * duration)
    samples = []
    for i in range(num_samples):
        t = i / sample_rate
        value = amplitude * math.sin(2 * math.pi * frequency * t)
        samples.append(value)
    return samples

def generate_square_wave(frequency, duration, sample_rate=44100, amplitude=0.5):
    """生成方波"""
    num_samples = int(sample_rate * duration)
    samples = []
    for i in range(num_samples):
        t = i / sample_rate
        value = amplitude * (1 if math.sin(2 * math.pi * frequency * t) > 0 else -1)
        samples.append(value)
    return samples

def generate_noise(duration, sample_rate=44100, amplitude=0.1):
    """生成白噪声"""
    import random
    num_samples = int(sample_rate * duration)
    samples = [amplitude * (random.random() * 2 - 1) for _ in range(num_samples)]
    return samples

def save_wav(filename, samples, sample_rate=44100):
    """保存为WAV文件"""
    with wave.open(filename, 'w') as wav_file:
        wav_file.setnchannels(1)  # 单声道
        wav_file.setsampwidth(2)  # 16位
        wav_file.setframerate(sample_rate)
        
        # 将浮点样本转换为16位整数
        max_sample = max(abs(s) for s in samples) if samples else 1
        if max_sample > 0:
            samples = [int(s / max_sample * 32767) for s in samples]
        else:
            samples = [0] * len(samples)
        
        wav_file.writeframes(struct.pack(f'<{len(samples)}h', *samples))

def generate_place_sound():
    """生成落子音效 - 轻柔的木头敲击声"""
    samples = []
    # 柔和的低频点击
    click_samples = generate_sine_wave(250, 0.03, amplitude=0.10)
    samples.extend(click_samples)
    # 轻微的高频泛音
    over_samples = generate_sine_wave(500, 0.015, amplitude=0.03)
    samples.extend(over_samples)
    # 快速衰减
    decay_samples = generate_sine_wave(180, 0.025, amplitude=0.06)
    samples.extend(decay_samples)
    return samples


def generate_win_sound():
    """生成胜利音效 - 柔和的上升旋律"""
    samples = []
    # 柔和的音符序列 (C5 -> E5 -> G5)
    frequencies = [523, 659, 784]
    for freq in frequencies:
        note_samples = generate_sine_wave(freq, 0.1, amplitude=0.12)
        samples.extend(note_samples)
        silence = [0] * int(44100 * 0.03)
        samples.extend(silence)
    # 柔和的结尾
    end_samples = generate_sine_wave(523, 0.15, amplitude=0.10)
    samples.extend(end_samples)
    return samples


def generate_draw_sound():
    """生成平局音效 - 平缓的音调"""
    samples = []
    note_samples = generate_sine_wave(300, 0.12, amplitude=0.10)
    samples.extend(note_samples)
    silence = [0] * int(44100 * 0.06)
    samples.extend(silence)
    note_samples = generate_sine_wave(280, 0.15, amplitude=0.08)
    samples.extend(note_samples)
    return samples


def generate_undo_sound():
    """生成悔棋音效 - 柔和的下降音调"""
    samples = []
    frequencies = [440, 370, 311]  # A4 -> F#4 -> D#4
    for freq in frequencies:
        note_samples = generate_sine_wave(freq, 0.06, amplitude=0.10)
        samples.extend(note_samples)
        silence = [0] * int(44100 * 0.02)
        samples.extend(silence)
    return samples


def generate_hint_sound():
    """生成提示音效 - 柔和的叮声"""
    samples = []
    samples.extend(generate_sine_wave(660, 0.06, amplitude=0.12))
    silence = [0] * int(44100 * 0.02)
    samples.extend(silence)
    samples.extend(generate_sine_wave(880, 0.08, amplitude=0.10))
    return samples


def generate_click_sound():
    """生成按钮点击音效 - 轻柔的点击"""
    samples = []
    samples.extend(generate_sine_wave(350, 0.015, amplitude=0.08))
    return samples


def main():
    if not os.path.exists('sounds'):
        os.makedirs('sounds')

    sounds = [
        ("sounds/place.wav", generate_place_sound, "落子音效"),
        ("sounds/win.wav", generate_win_sound, "胜利音效"),
        ("sounds/draw.wav", generate_draw_sound, "平局音效"),
        ("sounds/undo.wav", generate_undo_sound, "悔棋音效"),
        ("sounds/hint.wav", generate_hint_sound, "提示音效"),
        ("sounds/click.wav", generate_click_sound, "点击音效"),
    ]

    for file_path, generator, name in sounds:
        print(f"生成{name}...")
        samples = generator()
        save_wav(file_path, samples)

    print("音效文件生成完成！")

if __name__ == "__main__":
    main()