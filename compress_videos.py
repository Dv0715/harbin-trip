import os
from moviepy.editor import VideoFileClip


def compress_videos(input_folder, max_height=720, target_bitrate="1000k"):
    valid_extensions = ('.mp4', '.mov', '.m4v', '.MOV')

    for root, dirs, files in os.walk(input_folder):
        for file in files:
            if file.endswith(valid_extensions):
                file_path = os.path.join(root, file)
                output_path = os.path.splitext(file_path)[0] + "_compressed.mp4"

                try:
                    print(f"🎬 正在處理: {file}...")
                    clip = VideoFileClip(file_path)

                    if clip.h > max_height:
                        clip = clip.resize(height=max_height)

                    clip.write_videofile(
                        youtput_path,
                        codec="libx264",
                        audio_codec="aac",
                        bitrate=target_bitrate,
                        temp_audiofile="temp-audio.m4a",
                        remove_temp=True,
                        preset="slow" # 使用 slow 預設值能讓檔案更小且畫質更好
                    )

                    clip.close()

                    os.remove(file_path)
                    os.rename(output_path, file_path)
                    print(f"✅ 完成: {file}")

                except Exception as e:
                    print(f"❌ 壓縮失敗 {file}: {e}")


if __name__ == "__main__":
    compress_videos("albums")
