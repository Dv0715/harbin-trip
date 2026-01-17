import os
import argparse
from PIL import Image, ImageOps
from PIL.ExifTags import TAGS
from datetime import datetime

def get_taken_date(file_path):
    """取得照片的拍攝日期，若無則回傳檔案修改時間"""
    try:
        with Image.open(file_path) as img:
            exif = img.getexif()
            if exif:
                # 36867 是 DateTimeOriginal, 306 是 DateTime
                for tag_id in (36867, 306):
                    date_str = exif.get(tag_id)
                    if date_str:
                        return datetime.strptime(date_str, '%Y:%m:%d %H:%M:%S')
    except Exception:
        pass
    # 如果讀不到 EXIF，就拿檔案最後修改時間
    return datetime.fromtimestamp(os.path.getmtime(file_path))

def process_images(input_dir, output_dir, base_name, max_size):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 1. 搜集所有圖片並讀取時間
    image_data = []
    supported_ext = ('.png', '.jpg', '.jpeg', '.webp')
    
    files = [f for f in os.listdir(input_dir) if f.lower().endswith(supported_ext)]
    for f in files:
        full_path = os.path.join(input_dir, f)
        taken_time = get_taken_date(full_path)
        image_data.append({'filename': f, 'path': full_path, 'time': taken_time})

    # 2. 依照「拍攝時間」排序
    image_data.sort(key=lambda x: x['time'])
    
    print(f"找到 {len(image_data)} 張圖片，開始依拍攝時間處理...")

    # 3. 處理圖片
    for count, item in enumerate(image_data, start=1):
        with Image.open(item['path']) as img:
            img = ImageOps.exif_transpose(img) # 自動轉正
            
            w, h = img.size
            if w > h:
                new_w, new_h = max_size, int(h * (max_size / w))
            else:
                new_h, new_w = max_size, int(w * (max_size / h))
            
            img = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
            
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")
            
            # 加入 .strip() 移除頭尾隱形換行符，並建議改為 .webp
            clean_name = base_name.strip()
            new_filename = f"{clean_name}_{count}.webp"
            
            # 儲存格式改為 WEBP，體積會小非常多
            img.save(os.path.join(output_dir, new_filename), "WEBP", quality=80)
            
            print(f"[{count}] {item['filename']} -> {new_filename} (拍攝於: {item['time']})")

    print("\n--- 處理完成！ ---")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="圖片壓縮與自動命名工具")
    parser.add_argument("--src", default="raw_images", help="原始圖片資料夾 (預設: raw_images)")
    parser.add_argument("--out", default="w_images", help="輸出圖片資料夾 (預設: images)")
    parser.add_argument("--name", default="harbin", help="命名開頭 (預設: harbin)")
    parser.add_argument("--size", type=int, default=1200, help="長邊最大尺寸 (預設: 1200)")

    args = parser.parse_args()
    process_images(args.src, args.out, args.name, args.size)