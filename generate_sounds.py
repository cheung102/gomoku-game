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
    
    # 两个相同音调
    note_samples = generate_sine_wave(440, 0.2, amplitude=0.3)
    samples.extend(note_samples)
    
    # 短暂间隔
    silence = [0] * int(44100 * 0.1)
    samples.extend(silence)
    
    # 相同音调
    note_samples = generate_sine_wave(440, 0.2, amplitude=0.3)
    samples.extend(note_samples)
    
    return samples

def main():
    # 创建sounds目录
    if not os.path.exists('sounds'):
        os.makedirs('sounds')
    
    # 生成音效文件
    print("生成落子音效...")
    place_samples = generate_place_sound()
    save_wav('sounds/place.wav', place_samples)
    
    print("生成胜利音效...")
    win_samples = generate_win_sound()
    save_wav('sounds/win.wav', win_samples)
    
    print("生成平局音效...")
    draw_samples = generate_draw_sound()
    save_wav('sounds/draw.wav', draw_samples)
    
    print("音效文件生成完成！")
    print("文件位置：")
    print("  sounds/place.wav - 落子音效")
    print("  sounds/win.wav   - 胜利音效")
    print("  sounds/draw.wav  - 平局音效")

if __name__ == "__main__":
    main()