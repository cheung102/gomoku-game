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
    """生成落子音效 - 短促的点击声"""
    samples = []
    
    # 主音：短促的点击
    click_samples = generate_square_wave(800, 0.05, amplitude=0.3)
    samples.extend(click_samples)
    
    # 添加一些噪声
    noise_samples = generate_noise(0.02, amplitude=0.1)
    samples.extend(noise_samples)
    
    # 添加衰减
    decay_samples = generate_sine_wave(400, 0.03, amplitude=0.2)
    samples.extend(decay_samples)
    
    return samples

def generate_win_sound():
    """生成胜利音效 - 上升的音调"""
    samples = []
    
    # 上升音调序列
    frequencies = [523, 659, 784, 1047]  # C5, E5, G5, C6
    for freq in frequencies:
        note_samples = generate_sine_wave(freq, 0.15, amplitude=0.4)
        samples.extend(note_samples)
        # 添加短暂间隔
        silence = [0] * int(44100 * 0.05)
        samples.extend(silence)
    
    return samples

def generate_draw_sound():
    """生成平局音效 - 平淡的音调"""
    samples = []
    note_samples = generate_sine_wave(440, 0.2, amplitude=0.3)
    samples.extend(note_samples)
    silence = [0] * int(44100 * 0.1)
    samples.extend(silence)
    note_samples = generate_sine_wave(440, 0.2, amplitude=0.3)
    samples.extend(note_samples)
    return samples


def generate_undo_sound():
    """生成悔棋音效 - 下降音调"""
    samples = []
    frequencies = [784, 659, 523]  # G5, E5, C5
    for freq in frequencies:
        note_samples = generate_sine_wave(freq, 0.1, amplitude=0.3)
        samples.extend(note_samples)
        silence = [0] * int(44100 * 0.03)
        samples.extend(silence)
    return samples


def generate_hint_sound():
    """生成提示音效 - 清脆的叮声"""
    samples = []
    samples.extend(generate_sine_wave(1047, 0.1, amplitude=0.4))
    silence = [0] * int(44100 * 0.05)
    samples.extend(silence)
    samples.extend(generate_sine_wave(1319, 0.15, amplitude=0.3))
    return samples


def generate_click_sound():
    """生成按钮点击音效"""
    samples = []
    samples.extend(generate_square_wave(600, 0.03, amplitude=0.2))
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