import os
import json

base_dir = 'albums'

def generate_album_json():
    if not os.path.exists(base_dir):
        print(f"❌ 找不到 {base_dir}")
        return

    folders = [f for f in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, f))]

    for folder in folders:
        album_path = os.path.join(base_dir, folder)
        img_dir = os.path.join(album_path, 'images')
        vid_dir = os.path.join(album_path, 'videos')

        images = []
        videos = []

        # 掃描圖片
        if os.path.exists(img_dir):
            for f in sorted(os.listdir(img_dir)):
                if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
                    images.append({"url": f})

        # 掃描影片 (增加更多格式支援)
        if os.path.exists(vid_dir):
            for f in sorted(os.listdir(vid_dir)):
                if f.lower().endswith(('.mp4', '.mov', '.m4v', '.webm')):
                    videos.append({"url": f})

        data = {"images": images, "videos": videos}
        
        with open(os.path.join(album_path, 'media.json'), 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        
        print(f"✅ {folder}: {len(images)} 圖, {len(videos)} 影片")

if __name__ == "__main__":
    generate_album_json()