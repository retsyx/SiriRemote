import sys
from remote import SiriRemote, RemoteListener
from hid_input import Input

hid_input = Input()


class Callback(RemoteListener):
    def event_battery(self, remote, percent: int):
        print("Battery", percent)

    def event_power(self, remote, charging: bool):
        print("Charging", charging)

    def event_button(self, remote, button: int):
        handle_button_event(remote, button)

    def event_touches(self, remote, touches):
        handle_touches(remote, touches)


prevXY = [None, None]


def handle_touches(remote, touches):
    touch = touches[0]
    sensi = 8
    x = touch.x * sensi
    y = touch.y * - sensi
    p = touch.p

    if prevXY[0] and prevXY[1]:
        hid_input.move_cursor(x - prevXY[0], y - prevXY[1])

    if p == 0:
        prevXY[0] = prevXY[1] = None
    else:
        prevXY[0] = x
        prevXY[1] = y


def handle_button_event(remote, button):
    btns = remote.profile.buttons
    if button == btns.RELEASED:
        hid_input.release()
        return

    if button & btns.BUTTON_HOME:
        hid_input.add_key(Input.KEY_NEXTSONG)

    if button & btns.BUTTON_VOLUME_UP:
        hid_input.add_key(Input.KEY_VOLUMEUP)

    if button & btns.BUTTON_VOLUME_DOWN:
        hid_input.add_key(Input.KEY_VOLUMEDOWN)

    if button & btns.BUTTON_SELECT:
        hid_input.add_key(Input.BTN_LEFT)

    if button & btns.BUTTON_POWER:
        hid_input.add_key(Input.KEY_SCREENLOCK)

    if button & btns.BUTTON_SIRI:
        hid_input.add_key(Input.BTN_RIGHT)

    if button & btns.BUTTON_BACK:
        hid_input.add_key(Input.KEY_PREVIOUSSONG)

    if button & btns.BUTTON_MUTE:
        hid_input.add_key(Input.KEY_MUTE)

    if button & btns.BUTTON_PLAY_PAUSE:
        hid_input.add_key(Input.KEY_PLAYPAUSE)

    if button & btns.BUTTON_UP:
        hid_input.add_key(Input.KEY_UP)

    if button & btns.BUTTON_DOWN:
        hid_input.add_key(Input.KEY_DOWN)

    if button & btns.BUTTON_LEFT:
        hid_input.add_key(Input.KEY_LEFT)

    if button & btns.BUTTON_RIGHT:
        hid_input.add_key(Input.KEY_RIGHT)

    hid_input.press()


if __name__ == '__main__':
    try:
        if len(sys.argv) > 1:
            mac = sys.argv[1]
            SiriRemote(mac, Callback())
        else:
            print("error: no mac address")
    except KeyboardInterrupt:
        hid_input.close()
        exit()
