from PIL import Image
import os

def merge_sprites(folder_path, output_name, frame_count=8):
    """
    將指定資料夾內的 1.png ~ 8.png 合併為橫向長條圖
    """
    images = []
    widths = []
    heights = []

    # 1. 依序讀取 A_1.png 到 A_8.png (請確保檔案名稱正確)
    for i in range(1, frame_count + 1):
        # 這裡根據你的檔名調整，例如 'A_1.png' 或 '1.png'
        file_path = os.path.join(folder_path, f'{i}.png')
        
        if os.path.exists(file_path):
            img = Image.open(file_path).convert("RGBA")
            images.append(img)
            widths.append(img.width)
            heights.append(img.height)
        else:
            print(f"警告：找不到檔案 {file_path}")

    if not images:
        print("沒有讀取到任何圖片，請檢查路徑與檔名。")
        return

    # 2. 計算總畫布大小
    total_width = sum(widths)
    max_height = max(heights)

    # 3. 建立透明底的畫布
    sprite_sheet = Image.new('RGBA', (total_width, max_height), (0, 0, 0, 0))

    # 4. 依序貼上圖片
    x_offset = 0
    for img in images:
        sprite_sheet.paste(img, (x_offset, 0))
        x_offset += img.width

    # 5. 儲存結果
    sprite_sheet.save(output_name)
    print(f"✅ 成功生成長條圖：{output_name}")
    print(f"總尺寸：{total_width}x{max_height}")

# --- 執行區 ---
# 假設你的圖片放在 images/runners/char1 資料夾下
# merge_sprites('images/runners/char1', 'char1_sprite.png')

# 如果圖片就在腳本同一個資料夾下，直接執行：
merge_sprites('.', 'runner_combined.png')