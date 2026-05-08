import os
import re

def srt_to_vtt(srt_file):
    vtt_file = srt_file.replace('.srt', '.vtt')
    with open(srt_file, 'r', encoding='utf-8') as srt, open(vtt_file, 'w', encoding='utf-8') as vtt:
        vtt.write("WEBVTT\n\n")  # VTT header
        for line in srt:
            if "-->" in line:
                line = line.replace(',', '.', 1)  # Only replace the first comma in timestamps
            vtt.write(line)
    print(f'Converted: {srt_file} -> {vtt_file}')

def vtt_to_srt(vtt_file):
    srt_file = vtt_file.replace('.vtt', '.srt')
    with open(vtt_file, 'r', encoding='utf-8') as vtt, open(srt_file, 'w', encoding='utf-8') as srt:
        lines = vtt.readlines()
        if lines[0].strip() == "WEBVTT":
            lines = lines[1:]  # Remove WEBVTT header
        for line in lines:
            if "-->" in line:
                line = line.replace('.', ',', 1)  # Only replace the first period in timestamps
            srt.write(line)
    print(f'Converted: {vtt_file} -> {srt_file}')

def main():
    choice = input("What conversion do you need to perform?\n\n1. SRT ==> VTT\n2. VTT ==> SRT\n\nEnter your choice (1 or 2): ")
    if choice == '1':
        files = [f for f in os.listdir('.') if f.endswith('.srt')]
        if not files:
            print("No SRT files found.")
        for file in files:
            srt_to_vtt(file)
    elif choice == '2':
        files = [f for f in os.listdir('.') if f.endswith('.vtt')]
        if not files:
            print("No VTT files found.")
        for file in files:
            vtt_to_srt(file)
    else:
        print("Invalid choice.")

if __name__ == "__main__":
    main()
