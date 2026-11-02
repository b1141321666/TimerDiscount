# STM32 10 秒計時折扣機（TimerDiscount）

## 一、專題介紹

本專題使用 STM32 NUCLEO-G474RE 開發板，製作一個「10 秒計時折扣挑戰」遊戲。

玩家按下開發板上的按鈕開始計時，再按一次停止計時。系統會計算玩家的時間與 10 秒之間的誤差，並顯示對應的折扣結果。

## 二、使用設備與軟體

- STM32 NUCLEO-G474RE 開發板
- STM32CubeMX、STM32CubeIDE
- C 語言、STM32 HAL 函式庫
- Python 3
- tkinter 圖形介面
- pyserial 串列通訊
- LED、220Ω 電阻及杜邦線

## 三、系統功能

1. **按鈕計時**：按下 B1 按鈕開始計時，再按一次停止計時。
2. **硬體計時器**：使用 TIM2 計算經過時間。
3. **折扣判定**：根據計時結果與 10 秒的誤差，判斷折扣等級。
4. **LED 呼吸燈**：計時結束後，透過 TIM3 PWM 控制黃色 LED 呼吸閃爍三次。
5. **UART 傳輸**：透過 LPUART1 將計時結果傳送至電腦。
6. **Python GUI**：使用 tkinter 顯示計時秒數、誤差與折扣結果。

## 四、硬體接線

| 元件 | STM32 腳位 |
|---|---|
| B1 使用者按鈕 | PC13（開發板內建） |
| 黃色 LED | PA6（D12，透過 220Ω 電阻） |
| LED 負極 | GND |
| 電腦串列通訊 | ST-LINK Virtual COM Port |

## 五、操作方式

1. 使用 USB 連接 STM32 開發板與電腦。
2. 將 STM32 程式燒錄至開發板。
3. 安裝 Python 所需的 `pyserial` 套件。
4. 執行 `TimerDiscount_GUI.py`。
5. 設定正確的 COM 埠與 115200 baud。
6. 按下開發板 B1 按鈕開始計時。
7. 再按一次 B1 按鈕停止計時。
8. 在電腦 GUI 查看時間、誤差與折扣結果，並觀察 LED 呼吸效果。

## 六、專案檔案

- `Core/`：STM32 主要程式與標頭檔
- `Drivers/`：STM32 HAL 與相關驅動程式
- `TimerDiscount.ioc`：STM32CubeMX 腳位及周邊設定
- `TimerDiscount_GUI.py`：Python 圖形介面程式

## 七、專題成果

本專題已完成按鈕計時、10 秒誤差計算、折扣結果顯示、UART 通訊，以及 LED 呼吸燈控制，並可連續進行多回合挑戰。
