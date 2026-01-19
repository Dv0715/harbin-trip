/* runners.js - 跑步小人與雪地底座整合系統 */

(function() {
    // 1. 自動注入 CSS 樣式
    const style = document.createElement('style');
    style.innerHTML = `
/* 總容器 */
        .footer-game-zone-wrap {
            position: fixed;
            bottom: 0; left: 0;
            width: 100%; height: 120px;
            z-index: 2000;
            pointer-events: none;
            display: flex;
            justify-content: center;
            align-items: flex-end;
            overflow: visible;
            /* 網頁版環境光暈 */
            filter: drop-shadow(0 20px 10px rgba(255, 255, 255, 0.7));
        }

/* 弧形雪地層 - ✅ 這裡修改網頁版數值 */
        .snow-base-layer {
            position: absolute;
            bottom: 0; left: 0; 
            width: 100%; 
            height: 25px; /* 👈 網頁版雪地調矮一點，防止擋住內容 */
            background: linear-gradient(to bottom, #ffffff 0%, #e0f0ff 100%);
            /* ✅ 網頁版弧度改為較平緩的 120% */
            clip-path: ellipse(120% 100% at 50% 100%); 
            z-index: 10;
            box-shadow: inset 0 0px 25px rgba(255, 255, 255, 0.9);
        }



        /* 跑步軌道 */
        .runner-track {
            position: absolute;
            bottom: 15px; /* 站在雪地上 */
            left: 0; width: 100%;
            display: flex;
            justify-content: center;
            align-items: flex-end;
            z-index: 20;
            transform: scale(0.7);
            transform-origin: bottom center;
        }
/* ✅ 跑步小人本體：加入人物光暈 */
        .runner {
            width: 600px; 
            height: 90px;
            background-image: url('images/runners/char00/00.webp');
            background-size: 800% 100%; 
            image-rendering: pixelated;
            animation: spriteRun 0.55s steps(7) infinite;
            /* 這裡使用 drop-shadow 產生跟隨形狀的藍白色光暈 */
            filter: drop-shadow(0 0 4px rgba(255, 255, 255, 0.14))
                    drop-shadow(0 0 2px rgba(135, 206, 250, 0.28));
        }




 



/* ✅ 雪人按鈕：加入發光與懸浮感 */
        .snowman-btn {
            position: absolute;
            bottom: 16px;
            width: 55px; height: 55px;
            z-index: 220;
            pointer-events: auto;
            transition: transform 0.2s, filter 0.3s;
            /* 雪人光暈 */
            filter: drop-shadow(0 0 3px rgba(255, 255, 255, 0.23));
        }
    .snowman-btn.left { left: -12px; }
    .snowman-btn.right { right: -12px; }
        
        /* 跑步小人本體 */
        .runner {
            width: 600px; /* 長條圖單格寬度調整 */
            height: 90px;
            background-image: url('images/runners/char00/00.webp');
            background-size: 800% 100%; 
            image-rendering: pixelated;
            animation: spriteRun 0.55s steps(7) infinite;
        }

        @keyframes spriteRun {
            from { background-position: 0% 0; }
            to { background-position: 100% 0; }
        }

        @media (max-width: 600px) {
            .runner-track { transform: scale(0.5); bottom: 10px; }
            .snow-base-layer { height: 17px; }
        }
    `;
    document.head.appendChild(style);

    // 2. 生成 HTML 結構
    function initRunners() {
        const wrap = document.createElement('div');
        wrap.className = 'footer-game-zone-wrap';
        wrap.innerHTML = `
            <div class="snow-base-layer"></div>
            <div class="runner-track">
                <div class="runner"></div>
            </div>
            </div>
        <div class="snow-base-layer"></div>
        <div class="snowman-btn left" onclick="attack('left')">
            <img src="images/runners/snowman02.webp" alt="左雪人" style="width: 100%; height: auto;">
        </div>
        <div class="snowman-btn right" onclick="attack('right')">
            <img src="images/runners/snowman01.webp" alt="右雪人" style="width: 100%; height: auto;">
        </div>
        `;
        document.body.appendChild(wrap);
    }

    // 3. 確保在頁面載入後執行
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initRunners);
    } else {
        initRunners();
    }
})();