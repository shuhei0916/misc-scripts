import mido
import json
import sys

# ==== 設定 ====
INPUT_MIDI = "input.mid"  # 入力MIDIファイル名
OUTPUT_JSON = "output.json"
INSTRUMENT_NAME = "guitar"  # 固定するならここを変更

# ==== MIDI設定 ====
BPM = 120  # 任意に設定（後でMIDIから取得可能に拡張可）
TIME_SIGNATURE = "4/4"
TICKS_PER_BEAT = 480  # 通常MIDIの分解能、midoから取得も可

# ==== 実行 ====
mid = mido.MidiFile(INPUT_MIDI)
ticks_per_beat = mid.ticks_per_beat

notes = []

current_tick = 0
measure = 1
beats_per_measure = int(TIME_SIGNATURE.split('/')[0])

for track in mid.tracks:
    tick = 0
    for msg in track:
        tick += msg.time
        if msg.type == 'note_on' and msg.velocity > 0:
            # tick → beat変換
            total_beats = tick / ticks_per_beat
            measure = int(total_beats // beats_per_measure) + 1
            beat_in_measure = (total_beats % beats_per_measure) + 1
            notes.append({
                "measure": measure,
                "beat": round(beat_in_measure, 3),
                "instrument": INSTRUMENT_NAME
            })

# JSON出力
output = {
    "bpm": BPM,
    "timeSignature": TIME_SIGNATURE,
    "notes": notes
}

with open(OUTPUT_JSON, 'w') as f:
    json.dump(output, f, indent=2)

print(f"✅ JSONファイル生成完了: {OUTPUT_JSON}")
