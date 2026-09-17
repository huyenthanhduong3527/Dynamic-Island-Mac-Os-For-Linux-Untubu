<div align="center">

# 🏝️ Dynamic Island & macOS Menu Bar for Ubuntu Linux
### Mang trải nghiệm Apple Dynamic Island 60 FPS và Thanh Menu macOS cao cấp lên Ubuntu GNOME

[![Ubuntu](https://img.shields.io/badge/Ubuntu-22.04%20|%2024.04%20|%2026.04-E95420?style=for-the-badge&logo=ubuntu&logoColor=white)](https://ubuntu.com)
[![GNOME](https://img.shields.io/badge/GNOME-Shell%2042%20--%2050-4a86cf?style=for-the-badge&logo=gnome&logoColor=white)](https://www.gnome.org)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![GTK](https://img.shields.io/badge/GUI-GTK3%20%2B%20Cairo-4B275F?style=for-the-badge)](https://www.gtk.org)
[![License](https://img.shields.io/badge/License-MIT-22c55e?style=for-the-badge)](LICENSE)

*Một giải pháp độc lập, trọn gói (Standalone) biến chiếc máy tính Ubuntu của bạn thành một tác phẩm nghệ thuật mượt mà chuẩn Apple.*

[⚡ Cài Đặt Nhanh](#-cài-đặt-nhanh-cho-người-dùng) • [🚀 Cách Sử Dụng](#-hướng-dẫn-sử-dụng--khởi-chạy) • [✨ Tính Năng](#-tính-năng-nổi-bật) • [⌨️ Lệnh Điều Khiển CLI](#-điều-khiển-bằng-dòng-lệnh-cli--ipc) • [🔧 Xử Lý Sự Cố](#-khắc-phục-sự-cố-thường-gặp) • [🗑️ Gỡ Cài Đặt](#-gỡ-cài-đặt-uninstall)

---

</div>

## ⚡ Cài Đặt Nhanh Cho Người Dùng

Bạn **không cần** cài đặt bất kỳ công cụ lập trình hay phần mềm phụ trợ nào. Chỉ cần mở **Terminal** (`Ctrl + Alt + T`) trên Ubuntu và chạy 3 dòng lệnh sau:

```bash
# 1. Tải mã nguồn về máy
git clone https://github.com/huyenthanhduong3527/DYNAMIC-ISLNAD-FOR-UNTUBU-LINUX.git

# 2. Di chuyển vào thư mục dự án
cd DYNAMIC-ISLNAD-FOR-UNTUBU-LINUX

# 3. Chạy script cài đặt tự động
chmod +x install.sh run.sh main.py
./install.sh
```

### 🤖 Script `install.sh` sẽ tự động thực hiện mọi thứ:
1. **Cài đặt thư viện hệ thống cần thiết** (`python3-gi`, `python3-gi-cairo`, `gir1.2-gtk-3.0`, `python3-psutil`, `python3-dbus`, `x11-xserver-utils`) hoàn toàn tự động qua `apt`.
2. **Đăng ký ứng dụng vào hệ thống**: Thêm icon vector độ phân giải cao và tạo lối tắt `Dynamic Island` trong menu ứng dụng của Ubuntu (Application Grid).
3. **Kích hoạt tự khởi động (Autostart)**: Tự động chạy ngầm mỗi khi bạn bật máy hoặc đăng nhập vào Ubuntu.
4. **Cài đặt Extension macOS Menu Bar**: Tích hợp thanh menu chuẩn macOS vào GNOME Shell (Apple logo , File, Edit, View, Window, Settings, Help, khay trạng thái...).
5. **Tối ưu trải nghiệm hệ thống**:
   - Ẩn hoàn toàn thanh âm lượng mặc định của GNOME để âm lượng chỉ hiển thị độc quyền trên Dynamic Island.
   - Vô hiệu hoá cơ chế ping liveness của Mutter để triệt tiêu hoàn toàn lỗi *"Main.py Is Not Responding"*.

---

## 🚀 Hướng Dẫn Sử Dụng & Khởi Chạy

Sau khi chạy `./install.sh`, bạn có thể sử dụng ứng dụng ngay theo bất kỳ cách nào dưới đây:

### Cách 1: Mở từ Menu ứng dụng (Không cần mở Terminal)
- Nhấn phím **Super** (phím Windows) trên bàn phím.
- Gõ tìm kiếm **Dynamic Island** và nhấp vào biểu tượng ứng dụng để mở.

### Cách 2: Khởi chạy từ Terminal
```bash
./run.sh
```
*(Nếu muốn chạy ngầm để tắt cửa sổ terminal: `nohup ./run.sh >/dev/null 2>&1 &`)*

### Cách 3: Tự động khởi động cùng máy
- `install.sh` đã tự tạo cấu hình autostart tại `~/.config/autostart/dynamic-island.desktop`. 
- Mỗi khi bạn mở máy hoặc đăng nhập, Dynamic Island sẽ tự động xuất hiện trên màn hình.

---

## 🎮 Thao Tác Chuột Trực Quan

| Thao tác | Hành động |
| :--- | :--- |
| **Click chuột trái vào viên thuốc** | Bung mở đảo thành **Hub điều khiển đa năng** (Tabs: Media, Vitals, Controls, Timer, Notifications, Settings). |
| **Click chuột trái vào thanh trên Hub** | Thu nhỏ đảo trở lại thành viên thuốc gọn gàng. |
| **Click chuột phải vào viên thuốc** | Mở Menu ngữ cảnh nhanh để nhảy trực tiếp vào từng tab chức năng hoặc **Thoát ứng dụng**. |
| **Nhấn phím Volume / Chuyển bài** | Viên thuốc tự động mở rộng hiển thị mức âm lượng hoặc tên bài hát rồi tự thu nhỏ sau 3.5 giây. |
| **Viên thuốc ở giữa thanh Menu Bar (`🏝️ Island`)** | - **Click trái**: Mở menu danh mục phím tắt của đảo.<br>- **Click phải**: Bật / Tắt (Toggle) hiển thị Dynamic Island ngay lập tức. |

---

## ✨ Tính Năng Nổi Bật

### 1. 🏝️ Dynamic Island Hub (Python GTK3 + Cairo Anti-Aliased)
- **Đồ họa OLED Squircle sắc nét**: Thiết kế viên thuốc đen bóng theo tiêu chuẩn Apple với specular glow viền ngoài, đổ bóng mượt mà 60 FPS.
- **Tương thích hoàn hảo Wayland & X11**: Tự động nhận diện và hiển thị lớp overlay chuẩn xác ở mép trên màn hình.
- **🎵 Trình phát nhạc thông minh (MPRIS2 & PipeWire)**:
  - Tự động bắt nhạc từ **Spotify, YouTube trên trình duyệt (Chrome, Firefox, Brave), VLC, Amberol, Rhythmbox...**
  - Hiển thị ảnh bìa album, tên bài hát, nghệ sĩ, thanh tua thời gian và nút Play/Pause/Next.
  - **Live Audio Visualizer**: 10 dải sóng âm chuyển động theo giai điệu bài hát theo thời gian thực.
- **⚡ Giám sát phần cứng (Vitals Tab)**:
  - Đo % tải CPU, dung lượng RAM sử dụng và trạng thái Pin/Sạc (UPower) trực tiếp từ nhân Linux.
- **🎛️ Bảng điều khiển nhanh (Controls Tab)**:
  - Thanh trượt điều chỉnh âm lượng Master mượt mà qua PipeWire/WirePlumber, nút bật/tắt Mute.
  - Phím tắt chụp màn hình nhanh và khoá màn hình 1 chạm.
  - Nút chuyển đổi giao diện **Dark Mode 🌙 / Light Mode ☀️**.
- **⏱️ Đồng hồ đếm giờ & Pomodoro (Timer Tab)**:
  - Hẹn giờ học tập Pomodoro 25 phút hoặc bấm giờ thể thao chính xác 1/10 giây.
- **🔔 Lịch sử thông báo (Notifications Tab)**:
  - Tổng hợp các thông báo hệ thống và ứng dụng, hỗ trợ xoá tất cả nhanh.
- **⚙️ Tuỳ biến vị trí (Settings Tab)**:
  - Điều chỉnh khoảng cách đỉnh (Top Offset) từ 0px đến 120px để Dynamic Island vừa khít với tai thỏ hoặc viền màn hình của bạn.

---

### 2. 🍏 macOS Menu Bar (GNOME Shell Extension)
Biến thanh trên cùng của Ubuntu thành thanh Menu chuẩn macOS:
- ** Apple Menu**: Thông tin hệ thống, Cài đặt, Sleep, Restart, Shut Down, Lock Screen, Log Out.
- **Active App Menu**: Tên ứng dụng in đậm (**Dynamic Island**) kèm các tuỳ chọn nhanh.
- **Global Menus**: File, Edit, View, Window, Settings, Help.
- **🏝️ Center Island Widget**: Biểu tượng đảo mini ở giữa thanh panel cho phép thao tác nhanh.
- **Khay trạng thái chuẩn macOS (Right Status Tray)**:
  - ☀️ **Thời tiết trực tiếp**: Hiển thị nhiệt độ và biểu tượng thời tiết thực tế.
  - 🔍 **Spotlight Search**: Mở nhanh thanh tìm kiếm ứng dụng.
  - 📅 **Đồng hồ & Lịch**: Thứ, ngày tháng và giờ phong cách macOS.
  - Tích hợp liền mạch với Control Center và chỉ số Vitals của hệ thống.

---

## ⌨️ Điều Khiển Bằng Dòng Lệnh (CLI / IPC)

Bạn có thể gán phím tắt tùy chỉnh trong `GNOME Settings -> Keyboard -> Custom Shortcuts` để gọi các lệnh này:

```bash
# Bung mở hoặc thu nhỏ đảo
./main.py toggle

# Mở rộng đảo
./main.py expand

# Thu nhỏ đảo về dạng viên thuốc
./main.py collapse

# Chuyển đổi theme Sáng / Tối toàn hệ thống
./main.py theme

# Mở nhanh từng tab chức năng cụ thể:
./main.py tab media       # Tab Trình nghe nhạc & Visualizer
./main.py tab vitals      # Tab Tài nguyên CPU / RAM / Pin
./main.py tab controls    # Tab Bảng điều khiển âm lượng
./main.py tab timer       # Tab Đếm giờ & Pomodoro
./main.py tab notifs      # Tab Lịch sử thông báo
./main.py tab settings    # Tab Cài đặt giao diện

# Thoát hoàn toàn Dynamic Island
./main.py quit
```

---

## 🔧 Khắc Phục Sự Cố Thường Gặp

<details>
<summary><b>1. Làm sao để Dynamic Island không bị hiện đè 2 thanh âm lượng khi bấm phím volume?</b></summary>
<br>

Phiên bản này đã tự động tắt thanh OSD mặc định của GNOME ở dưới đáy màn hình bằng CSS theme hệ thống. 
Nếu bạn vừa đổi theme GNOME Shell và thấy thanh OSD cũ xuất hiện lại, chỉ cần chạy lại lệnh cài đặt:
```bash
./install.sh
```
Sau đó **Đăng xuất (Log Out)** và **Đăng nhập lại** là thanh âm lượng mặc định sẽ biến mất hoàn toàn.
</details>

<details>
<summary><b>2. Có bao giờ bị lỗi "Main.py Is Not Responding" không?</b></summary>
<br>

Không! Dự án đã xử lý triệt để lỗi này bằng 2 lớp bảo vệ:
1. Gỡ bỏ cờ `_NET_WM_PING` khỏi thuộc tính `WM_PROTOCOLS` của cửa sổ X11.
2. Tắt hoàn toàn timeout kiểm tra treo của Mutter (`gsettings set org.gnome.mutter check-alive-timeout 0`).
Cửa sổ Dynamic Island được GNOME công nhận là một Desktop Dock tĩnh và sẽ không bao giờ bị hiện hộp thoại báo treo.
</details>

<details>
<summary><b>3. Làm sao chỉnh Dynamic Island dịch lên sát mép trên hoặc xuống dưới một chút?</b></summary>
<br>

Click vào viên thuốc để mở Hub -> Chọn tab **Cài đặt (⚙️)** -> Kéo thanh trượt **Top Offset (Y Margin)** để căn chỉnh theo ý muốn của bạn trong thời gian thực.
</details>

<details>
<summary><b>4. Thanh Menu macOS chưa hiện lên sau khi chạy install.sh?</b></summary>
<br>

Do cơ chế bảo mật của GNOME Shell trên Wayland, các extension mới kích hoạt cần khởi động lại phiên làm việc:
- Bạn chỉ cần **Đăng xuất (Log Out)** và **Đăng nhập lại**.
- Hoặc mở ứng dụng **Extensions** (hoặc **Extension Manager**) và bật công tắc cho tiện ích **macOS Menu Bar**.
</details>

---

## 🗑️ Gỡ Cài Đặt (Uninstall)

Nếu bạn không muốn sử dụng nữa, bạn có thể gỡ bỏ sạch sẽ mọi thành phần chỉ với một dòng lệnh:

```bash
# Tắt tiến trình đang chạy
./main.py quit 2>/dev/null || pkill -f "python3 main.py"

# Xoá file desktop, autostart, icon và extension
rm -f ~/.local/share/applications/dynamic-island.desktop
rm -f ~/.config/autostart/dynamic-island.desktop
rm -f ~/.local/share/icons/hicolor/scalable/apps/dynamic-island.svg
rm -rf ~/.local/share/gnome-shell/extensions/macos-menu-bar@Nguyenthanhtam
rm -rf ~/.config/dynamic_island
rm -f ~/.local/share/dynamic-island

# Bật lại thanh thông báo OSD nếu cần
gsettings set org.gnome.mutter check-alive-timeout 5000

echo "✅ Đã gỡ bỏ Dynamic Island hoàn toàn sạch sẽ khỏi máy tính của bạn!"
```

---

## 📂 Cấu Trúc Mã Nguồn

```
DYNAMIC-ISLNAD-FOR-UNTUBU-LINUX/
├── main.py                     # Entrypoint & bộ xử lý lệnh CLI / IPC
├── run.sh                      # Script khởi chạy môi trường X11/Wayland
├── install.sh                  # Bộ cài đặt tự động 1 bước trọn gói
├── dynamic-island.desktop      # File launcher cho GNOME App Grid & Autostart
├── requirements.txt            # Danh sách gói phụ thuộc hệ thống
├── README.md                   # Hướng dẫn sử dụng chi tiết
│
├── extensions/
│   └── macos-menu-bar@Nguyenthanhtam/
│       ├── extension.js        # Logic GNOME Shell Extension
│       ├── menu.js             # Menu macOS & hook triệt tiêu OSD GNOME
│       ├── stylesheet.css      # CSS giao diện Top Bar macOS
│       ├── metadata.json       # Cấu hình tương thích GNOME 42 - 50
│       └── apple-symbolic.svg  # Logo Apple vector
│
└── src/
    ├── config.py               # Quản lý cấu hình JSON (~/.config/dynamic_island/)
    ├── animator.py             # Tính toán vật lý lò xo 60 FPS
    ├── window.py               # Cửa sổ chính Cairo trong suốt & phân luồng sự kiện
    ├── ipc.py                  # Socket IPC chống chạy trùng tiến trình
    ├── modules/
    │   ├── media.py            # Bắt nhạc D-Bus MPRIS2 & PipeWire
    │   ├── audio.py            # Điều khiển âm thanh PipeWire/WirePlumber
    │   ├── system.py           # Giám sát phần cứng CPU, RAM, Pin
    │   ├── timer.py            # Bộ đếm giờ Pomodoro & bấm giờ
    │   └── notification.py     # Lắng nghe thông báo D-Bus hệ thống
    ├── ui/
    │   ├── styles.css          # CSS phong cách Apple OLED Dark Glassmorphism
    │   ├── compact_view.py     # Giao diện viên thuốc thu nhỏ
    │   ├── expanded_view.py    # Giao diện Hub mở rộng chia Tab
    │   ├── event_banner.py     # Capsule sự kiện âm lượng & bài hát
    │   └── tabs/               # Các tab chức năng (Media, Vitals, Controls...)
    └── utils/
        ├── icons.py            # Thư viện icon vector SVG
        ├── theme.py            # Quản lý chuyển đổi Dark / Light mode
        └── visualizer.py       # Thuật toán sóng âm âm nhạc nhảy theo nhịp
```

---

## 📄 Giấy Phép (License)

Dự án được phân phối mã nguồn mở theo giấy phép **[MIT License](LICENSE)**. Bạn có thể tự do sao chép, chỉnh sửa và chia sẻ cho cộng đồng.

<div align="center">
⭐ <i>Nếu bạn thấy dự án hữu ích, hãy tặng 1 sao (Star) trên GitHub nhé!</i> ⭐
</div>
