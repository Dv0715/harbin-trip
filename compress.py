import os
from PIL import Image

def compress_images(input_folder, max_size=1920, quality=80):
    # 支援的格式
    valid_extensions = ('.jpg', '.jpeg', '.png', '.JPG', '.PNG')
    
    # 遍歷資料夾（包含子資料夾）
    for root, dirs, files in os.walk(input_folder):
        for file in files:
            if file.endswith(valid_extensions):
                file_path = os.path.join(root, file)
                
                try:
                    with Image.open(file_path) as img:
                        # 1. 處理旋轉問題 (部分手機照片會有方向資訊)
                        img = img.convert("RGB")
                        
                        # 2. 計算縮放比例 (維持原比例，長邊最大 1920)
                        w, h = img.size
                        if max(w, h) > max_size:
                            if w > h:
                                new_w = max_size
                                new_h = int(h * (max_size / w))
                            else:
                                new_h = max_size
                                new_w = int(w * (max_size / h))
                            img = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
                        
                        # 3. 準備輸出路徑 (副檔名改成 .webp)
                        output_path = os.path.splitext(file_path)[0] + ".webp"
                        
                        # 4. 儲存並壓縮
                        img.save(output_path, "WEBP", quality=quality)
                        
                    # 5. (選用) 刪除原來的舊檔，節省空間
                    # 如果你想保留原檔，請註解掉下面這行
                    os.remove(file_path)
                    
                    print(f"✅ 已處理: {file} -> {os.path.basename(output_path)}")
                
                except Exception as e:
                    print(f"❌ 無法處理 {file}: {e}")

if __name__ == "__main__":
    # 這裡直接填入你的 albums 資料夾路徑
    # 如果腳本就在 Halbin_travel 裡面，寫 'albums' 即可
    album_dir = 'albums' 
    
    if os.path.exists(album_dir):
        print(f"🚀 偵測到相簿路徑：{os.path.abspath(album_dir)}")
        print("開始批次處理所有子資料夾中的圖片...")
        compress_images(album_dir)
        print("✨ 全部相簿處理完成！")
    else:
        print(f"❌ 找不到路徑: {album_dir}，請確認腳本放置位置或手動輸入完整路徑。")