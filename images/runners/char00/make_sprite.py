from PIL import Image
import os

def merge_sprites_to_webp(folder_path, output_name, frame_count=6, target_size=None):
    """
    將指定資料夾內的 1.png ~ n.png 合併為橫向 WebP 長條圖
    :param target_size: 格式為 (寬, 高)，例如 (1085, 230)，若為 None 則維持原圖大小
    """
    images = []
    
    # 1. 依序讀取圖片並處理縮放
    for i in range(1, frame_count + 1):
        file_path = os.path.join(folder_path, f'{i}.png')
        
        if os.path.exists(file_path):
            img = Image.open(file_path).convert("RGBA")
            
            # 如果有設定目標大小，自動執行手機版優化縮放
            if target_size:
                # 使用 LANCZOS 獲得最高品質的縮放效果
                img = img.resize(target_size, Image.Resampling.LANCZOS)
            
            images.append(img)
        else:
            print(f"警告：找不到檔案 {file_path}")

    if not images:
        print("沒有讀取到任何圖片，請檢查路徑與檔名。")
        return

    # 2. 計算總畫布大小
    single_w, single_h = images[0].size
    total_width = single_w * len(images)
    max_height = single_h

    # 3. 建立透明底的畫布
    sprite_sheet = Image.new('RGBA', (total_width, max_height), (0, 0, 0, 0))

    # 4. 依序貼上圖片
    for idx, img in enumerate(images):
        sprite_sheet.paste(img, (idx * single_w, 0))

    # 5. 儲存為 WebP 格式
    # 如果輸出檔名沒加 .webp，自動補上
    if not output_name.lower().endswith('.webp'):
        output_name = os.path.splitext(output_name)[0] + '.webp'

    # quality=100 表示最高品質，method=6 慢速壓縮但檔案最小
    sprite_sheet.save(output_name, "WEBP", quality=100, method=6)
    
    print(f"✅ 成功生成手機優化版 WebP：{output_name}")
    print(f"單格尺寸：{single_w}x{single_h} | 總尺寸：{total_width}x{max_height}")

# --- 執行區 ---
# 1. folder_path: 你的 1.png ~ 8.png 所在的資料夾
# 2. frame_count: 8 幀
# 3. target_size: 建議縮小，例如 (600, 76) 左右，這樣 8 張合併總寬約 4800px，比較安全
merge_sprites_to_webp(
    folder_path='.', 
    output_name='runner_combined.webp', 
    frame_count=8, 
    target_size=(600, 76) 
)