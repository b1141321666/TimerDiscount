
import tkinter as tk
from tkinter import messagebox
import serial
import threading
import queue

# UART 設定
PORT = "COM5"
BAUD_RATE = 115200

# 建立 GUI
root = tk.Tk()
root.title("計時折扣機 - 10秒折扣大挑戰")
root.geometry("520x420")
root.resizable(False, False)
root.configure(bg="#F4F6FA")

data_queue = queue.Queue()
running = True
ser = None

# 標題
tk.Label(
    root,
    text="10 秒折扣大挑戰",
    font=("Microsoft JhengHei", 24, "bold"),
    bg="#F4F6FA",
    fg="#203050"
).pack(pady=(25, 10))

tk.Label(
    root,
    text="按下開發板 B1 開始，再按一次停止",
    font=("Microsoft JhengHei", 12),
    bg="#F4F6FA"
).pack(pady=(0, 15))

# 結果顯示
time_var = tk.StringVar(value="--.--- s")
error_var = tk.StringVar(value="--.--- s")
discount_var = tk.StringVar(value="-- 折")
status_var = tk.StringVar(value="正在連線...")

def make_row(title, variable):
    frame = tk.Frame(root, bg="white", padx=20, pady=12)
    frame.pack(fill="x", padx=45, pady=5)

    tk.Label(
        frame,
        text=title,
        font=("Microsoft JhengHei", 14),
        bg="white",
        width=12,
        anchor="w"
    ).pack(side="left")

    tk.Label(
        frame,
        textvariable=variable,
        font=("Arial", 19, "bold"),
        bg="white",
        fg="#1766C2"
    ).pack(side="right")

make_row("Time", time_var)
make_row("Error", error_var)
make_row("Discount", discount_var)

tk.Label(
    root,
    textvariable=status_var,
    font=("Microsoft JhengHei", 11),
    bg="#F4F6FA",
    fg="#555555"
).pack(pady=20)


# 接收 STM32 資料
def uart_worker():
    global ser

    try:
        ser = serial.Serial(
            port=PORT,
            baudrate=BAUD_RATE,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            timeout=0.2
        )

        data_queue.put(("status", f"已連接 {PORT} / 115200"))

        while running:
            raw = ser.readline()

            if not raw:
                continue

            line = raw.decode("utf-8", errors="replace").strip()

            try:
                fields = {}

                for item in line.split(","):
                    key, value = item.split(":", 1)
                    fields[key.strip().upper()] = value.strip()

                t = float(fields["TIME"])
                e = float(fields["ERROR"])
                d = int(fields["DISCOUNT"])

                if d not in (50, 70, 90, 100):
                    continue

                data_queue.put(("result", (t, e, d)))

            except (ValueError, KeyError):
                continue

    except (serial.SerialException, OSError) as exc:
        data_queue.put(("status", f"連線失敗：{exc}"))

    finally:
        if ser is not None and ser.is_open:
            ser.close()


# 更新 GUI（只在主執行緒執行）
def update_gui():
    while not data_queue.empty():
        kind, value = data_queue.get_nowait()

        if kind == "status":
            status_var.set(value)

        elif kind == "result":
            t, e, d = value

            time_var.set(f"{t:.3f} s")
            error_var.set(f"{e:.3f} s")
            discount_var.set(f"{d // 10} 折")
            status_var.set("挑戰完成！可以進行下一輪")

    if running:
        root.after(100, update_gui)


def on_close():
    global running
    running = False
    root.destroy()


root.protocol("WM_DELETE_WINDOW", on_close)

threading.Thread(target=uart_worker, daemon=True).start()
root.after(100, update_gui)

root.mainloop()
