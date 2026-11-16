# Getting started

## 1. Flash MicroPython

Use the generic ESP32 firmware (`ESP32_GENERIC-...bin`) for the ACEBOTT ESP32 Max
(ESP32-WROOM-32E). In Thonny: **Tools → Options → Interpreter → MicroPython (ESP32)
→ Install or update MicroPython**.

## 2. Install the drivers

**mpremote** (board on USB, no Wi-Fi needed):

    pip install mpremote
    mpremote mip install github:aitumik/lancola              # everything
    mpremote mip install github:aitumik/lancola/drivers/servo # just one

**Thonny shell** (board on Wi-Fi):

```python
import network, mip
w = network.WLAN(network.STA_IF)
w.active(True)
w.connect("WIFI-NAME", "password")
while not w.isconnected():
    pass
mip.install("github:aitumik/lancola")
```

**Thonny, no internet:** open the driver's `.py` file, then
**File → Save as… → MicroPython device** and save it inside `/lib`.

The drivers land in `/lib` on the board. Check with:

    mpremote ls :lib

## 3. Run an example

Open a file from `examples/` in Thonny and press **Run** (F5).
Or from a terminal:

    mpremote run examples/blink_demo.py

The examples are not copied to the board, so they never take up its flash.

## 4. Updating

Run the same install command again; it overwrites the old files.
GitHub can serve a cached copy for a few minutes after a push.
After installing, reset the board (`mpremote reset`, or Thonny's Stop/Restart)
so it loads the new version.
