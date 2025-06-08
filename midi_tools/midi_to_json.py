import mido
import json
import sys

# ==== 設定 ====
INPUT_MIDI = "data/techno_aiva01 - Reduced.mid"
OUTPUT_JSON = "data/techno_aiva01 - Reduced.json"

# General MIDI program number to instrument name
GM_INSTRUMENTS = [
    "acoustic grand piano", "bright acoustic piano", "electric grand piano", "honky-tonk piano",
    "electric piano 1", "electric piano 2", "harpsichord", "clavinet",
    "celesta", "glockenspiel", "music box", "vibraphone",
    "marimba", "xylophone", "tubular bells", "dulcimer",
    "drawbar organ", "percussive organ", "rock organ", "church organ",
    "reed organ", "accordion", "harmonica", "tango accordion",
    "acoustic guitar (nylon)", "acoustic guitar (steel)", "electric guitar (jazz)", "electric guitar (clean)",
    "electric guitar (muted)", "overdriven guitar", "distortion guitar", "guitar harmonics",
    "acoustic bass", "electric bass (finger)", "electric bass (pick)", "fretless bass",
    "slap bass 1", "slap bass 2", "synth bass 1", "synth bass 2",
    "violin", "viola", "cello", "contrabass",
    "tremolo strings", "pizzicato strings", "orchestral harp", "timpani",
    "string ensemble 1", "string ensemble 2", "synth strings 1", "synth strings 2",
    "choir aahs", "voice oohs", "synth voice", "orchestra hit",
    "trumpet", "trombone", "tuba", "muted trumpet",
    "french horn", "brass section", "synth brass 1", "synth brass 2",
    "soprano sax", "alto sax", "tenor sax", "baritone sax",
    "oboe", "english horn", "bassoon", "clarinet",
    "piccolo", "flute", "recorder", "pan flute",
    "blown bottle", "shakuhachi", "whistle", "ocarina",
    "lead 1 (square)", "lead 2 (sawtooth)", "lead 3 (calliope)", "lead 4 (chiff)",
    "lead 5 (charang)", "lead 6 (voice)", "lead 7 (fifths)", "lead 8 (bass + lead)",
    "pad 1 (new age)", "pad 2 (warm)", "pad 3 (polysynth)", "pad 4 (choir)",
    "pad 5 (bowed)", "pad 6 (metallic)", "pad 7 (halo)", "pad 8 (sweep)",
    "fx 1 (rain)", "fx 2 (soundtrack)", "fx 3 (crystal)", "fx 4 (atmosphere)",
    "fx 5 (brightness)", "fx 6 (goblins)", "fx 7 (echoes)", "fx 8 (sci-fi)",
    "sitar", "banjo", "shamisen", "koto",
    "kalimba", "bagpipe", "fiddle", "shanai",
    "tinkle bell", "agogo", "steel drums", "woodblock",
    "taiko drum", "melodic tom", "synth drum", "reverse cymbal",
    "guitar fret noise", "breath noise", "seashore", "bird tweet",
    "telephone ring", "helicopter", "applause", "gunshot"
]

mid = mido.MidiFile(INPUT_MIDI)
ticks_per_beat = mid.ticks_per_beat
tempo = 500000  # デフォルト 120 BPM
channel_programs = {}  # channel → program number

notes = []

for track in mid.tracks:
    tick = 0
    for msg in track:
        tick += msg.time

        if msg.type == 'set_tempo':
            tempo = msg.tempo

        elif msg.type == 'program_change':
            channel_programs[msg.channel] = msg.program

        elif msg.type == 'note_on' and msg.velocity > 0:
            program = channel_programs.get(msg.channel, 0)
            instrument_name = GM_INSTRUMENTS[program]
            total_beats = tick / ticks_per_beat
            beats_per_measure = 4  # 4/4 固定（将来的にtime_signatureイベントから取得可）
            measure = int(total_beats // beats_per_measure) + 1
            beat_in_measure = (total_beats % beats_per_measure) + 1
            notes.append({
                "measure": measure,
                "beat": round(beat_in_measure, 3),
                "instrument": instrument_name
            })

# BPM算出
bpm = mido.tempo2bpm(tempo)

output = {
    "bpm": round(bpm),
    "timeSignature": "4/4",  # 今回は仮固定
    "notes": notes
}

with open(OUTPUT_JSON, 'w') as f:
    json.dump(output, f, indent=2)

print(f"✅ JSONファイル生成完了: {OUTPUT_JSON}")
