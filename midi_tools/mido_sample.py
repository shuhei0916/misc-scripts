import mido
import json
import sys

# ==== 設定 ====
INPUT_MIDI = "data/techno_aiva01 - Reduced.mid"  # 入力MIDIファイル名
OUTPUT_JSON = "data/ASGORE.json"
INSTRUMENT_NAME = "guitar"  # 固定するならここを変更

mid = mido.MidiFile(INPUT_MIDI)

print(f"ticks_per_beat: {mid.ticks_per_beat}")
print(f"tracks: {len(mid.tracks)}")

for i, track in enumerate(mid.tracks):
    print(f"Track {i}: {track.name}")
    for msg in track:
        print(msg)


from mido import MidiFile, tempo2bpm

for track in mid.tracks:
    for msg in track:
        if msg.type == 'set_tempo':
            bpm = tempo2bpm(msg.tempo)
            print(f"BPM: {bpm}")

notes = []
current_time = 0

for track in mid.tracks:
    for msg in track:
        current_time += msg.time
        if msg.type == 'note_on' and msg.velocity > 0:
            notes.append({
                'note': msg.note,
                'time': current_time,
                'channel': msg.channel,
            })

print(notes)