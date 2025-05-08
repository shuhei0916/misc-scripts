import pygame.midi
import mido
import time

MIDI_FILE = "data/techno_aiva01 - Reduced.mid"

def tick_to_seconds(ticks, tempo, ticks_per_beat):
    return (tempo * ticks) / (ticks_per_beat * 1_000_000)

def play_midi(filename):
    pygame.midi.init()

    try:
        output_id = pygame.midi.get_default_output_id()
        if output_id == -1:
            raise RuntimeError("⛔ MIDI出力デバイスが見つかりません")
        player = pygame.midi.Output(output_id)

        mid = mido.MidiFile(filename)
        ticks_per_beat = mid.ticks_per_beat
        tempo = 500000  # デフォルト120 BPM

        print(f"🎵 再生開始: {filename}")
        print(f"🛠 ticks_per_beat: {ticks_per_beat}")

        for i, track in enumerate(mid.tracks):
            print(f"🔁 トラック {i}: {track.name if track.name else 'Unnamed'}")
            tick_accum = 0
            for msg in track:
                tick_accum += msg.time
                if msg.type == 'set_tempo':
                    tempo = msg.tempo
                    print(f"⏱ テンポ変更: {tempo} μs/beat (BPM={mido.tempo2bpm(tempo):.2f})")

                if not msg.is_meta:
                    delay = tick_to_seconds(msg.time, tempo, ticks_per_beat)
                    # print(f"🎼 イベント: {msg} | tick={msg.time}, 秒={delay:.4f}")
                    if delay > 0:
                        time.sleep(delay)
                    if msg.type == 'note_on':
                        player.note_on(msg.note, msg.velocity)
                    elif msg.type == 'note_off':
                        player.note_off(msg.note, msg.velocity)
    finally:
        pygame.midi.quit()
        print("🛑 再生終了")

if __name__ == "__main__":
    play_midi(MIDI_FILE)
