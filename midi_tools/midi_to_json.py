import mido
import json
from collections import defaultdict

def main():
    input_file = "data/techno_aiva01 - Reduced.mid"
    output_file = "data/techno_aiva01 - Reduced.json"

    midi_json = parse_midi_to_json(input_file)

    with open(output_file, "w") as f:
        json.dump(midi_json, f, indent=2)
    print(f"Exported to {output_file}")

def ticks_to_time(tick, tempo, ticks_per_beat):
    return mido.tick2second(tick, ticks_per_beat, tempo)

def time_to_measure_beat(time_sec, bpm, time_sig):
    beats_per_measure = time_sig[0]
    seconds_per_beat = 60.0 / bpm
    total_beats = time_sec / seconds_per_beat
    measure = int(total_beats // beats_per_measure) + 1
    beat = (total_beats % beats_per_measure) + 1
    return measure, round(beat, 3)

def program_to_instrument_name(program_number):
    # General MIDI program name list
    GM_PROGRAMS = [
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

    if 0 <= program_number < len(GM_PROGRAMS):
        return GM_PROGRAMS[program_number]
    else:
        return f"program {program_number}"


def parse_midi_to_json(filename):
    mid = mido.MidiFile(filename)
    ticks_per_beat = mid.ticks_per_beat

    bpm = 120
    time_signature = (4, 4)
    tempo = mido.bpm2tempo(bpm)

    output = {
        "bpm": bpm,
        "timeSignature": f"{time_signature[0]}/{time_signature[1]}",
        "tracks": []
    }

    for track in mid.tracks:
        track_data = {
            "name": track.name,
            "instrument": "unknown",
            "notes": []
        }
        current_program = 0
        channel = None
        abs_time = 0

        for msg in track:
            abs_time += msg.time

            if msg.type == 'set_tempo':
                tempo = msg.tempo
                bpm = round(mido.tempo2bpm(tempo))
                output["bpm"] = bpm  # Update bpm in the output
            elif msg.type == 'time_signature':
                time_signature = (msg.numerator, msg.denominator)
                output["timeSignature"] = f"{time_signature[0]}/{time_signature[1]}" # Update time signature
            elif msg.type == 'program_change':
                current_program = msg.program
                channel = msg.channel
                track_data["instrument"] = program_to_instrument_name(current_program)
            elif msg.type == 'note_on' and msg.velocity > 0:
                note_time = mido.tick2second(abs_time, ticks_per_beat, tempo)
                measure, beat = time_to_measure_beat(note_time, bpm, time_signature)
                track_data["notes"].append({
                    "measure": measure,
                    "beat": beat
                })

        if track_data["notes"]:  # Only add track if it has notes
            output["tracks"].append(track_data)

    return output

# 実行例
if __name__ == "__main__":
    main()