import os
from moviepy.video.io.VideoFileClip import VideoFileClip


def compress_videos(input_folder, max_height=1080, target_bitrate="2000k"):
    # 支援的格式
    valid_extensions = ('.mp4', '.mov', '.m4v', '.MOV')
    
    for root, dirs, files in os.walk(input_folder):
        for file in files:
            if file.endswith(valid_extensions):
                file_path = os.path.join(root, file)
                # 建立臨時輸出路徑，避免直接覆蓋正在讀取的檔案
                output_path = os.path.splitext(file_path)[0] + "_compressed.mp4"
                
                try:
                    print(f"🎬 正在處理: {file}...")
                    clip = VideoFileClip(file_path)
                    
                    # 1. 如果高度超過 1080，則縮小解析度
                    if clip.h > max_height:
                        clip = clip.resize(height=max_height)
                    
                    # 2. 寫出壓縮後的影片 (使用 H.264 編碼)
                    # bitrate 可根據需要調整，2000k 對網頁來說非常清晰且檔案小
                    clip.write_videofile(output_path, codec="libx264", audio_codec="aac", bitrate=target_bitrate)
                    
                    clip.close()
                    
                    # 3. 替換舊檔案
                    os.remove(file_path)
                    os.rename(output_path, file_path)
                    print(f"✅ 完成: {file}")
                
                except Exception as e:
                    print(f"❌ 壓縮失敗 {file}: {e}")

if __name__ == "__main__":
    album_dir = 'albums' # 指向你的相簿資料夾
    compress_videos(album_dir)