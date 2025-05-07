import pygame.midi
import time
import mido

MIDI_FILE = "data/techno_aiva01 - Reduced.mid"

def play_midi(midi_path):
    # 初期化
    pygame.midi.init()
    player = pygame.midi.Output(pygame.midi.get_default_output_id())

    mid = mido.MidiFile(midi_path)
    tempo = 500000  # 初期テンポ（120BPM）

    ticks_per_beat = mid.ticks_per_beat

    for msg in mid:
        time.sleep(msg.time * mido.tempo2seconds(tempo, ticks_per_beat))

        if msg.type == 'set_tempo':
            tempo = msg.tempo

        elif msg.type in ['note_on', 'note_off']:
            player.write_short(
                0x90 if msg.type == 'note_on' else 0x80,
                msg.note,
                msg.velocity
            )

    player.close()
    pygame.midi.quit()

if __name__ == "__main__":
    print(f"🎵 再生開始: {MIDI_FILE}")
    play_midi(MIDI_FILE)
    print("✅ 再生終了")
