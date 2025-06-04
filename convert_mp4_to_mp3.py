from moviepy.editor import VideoFileClip

def convert_mp4_to_mp3(mp4_path, mp3_path):
    video = VideoFileClip(mp4_path)
    video.audio.write_audiofile(mp3_path)
    print(f"変換完了: {mp3_path}")

# 使い方の例
if __name__ == "__main__":
    input_path = "C:/Users\Ito\Desktop\VID_20250603_182217.mp4"
    output_path = "C:/Users\Ito\Desktop\output.mp3"

    convert_mp4_to_mp3(input_path, output_path)
