#!/bin/bash
set -euo pipefail
pid=$(pgrep -u 1000 -x icewm | head -1)
for name in DISPLAY XAUTHORITY XDG_RUNTIME_DIR DBUS_SESSION_BUS_ADDRESS; do
    value=$(tr '\0' '\n' < "/proc/$pid/environ" | sed -n "s/^$name=//p")
    [[ -z $value ]] || export "$name=$value"
done
export DISPLAY=${DISPLAY:-:0}
export XAUTHORITY=${XAUTHORITY:-/home/aika/.Xauthority}
sudo apk add python3
curl -fsS http://10.0.2.2:18087/test-browser.py -o /tmp/test-browser.py
mkdir -p /tmp/aika-video-profile
cat > /tmp/aika-video-profile/user.js <<'JS'
user_pref("media.autoplay.default",0);
user_pref("gfx.webrender.software",true);
user_pref("browser.shell.checkDefaultBrowser",false);
JS
aika-browser --no-remote --profile /tmp/aika-video-profile --marionette file:///usr/share/aikaos-mini/welcome.html > /tmp/firefox-test.log 2>&1 &
python3 /tmp/test-browser.py > /tmp/video-test.log 2>&1
curl -fsS -T /tmp/aika-video-result.json http://10.0.2.2:18087/youtube-test.json
pactl list short sink-inputs
echo AIKA_VIDEO_TEST_FINISHED
