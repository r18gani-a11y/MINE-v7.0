import os
from kivy.lang import Builder
from kivy.properties import BooleanProperty
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.list import OneLineListItem
from mine_backend import security, vault


class LockScreen(MDScreen):
    def try_unlock(self, code):
        if not code:
            self.ids.msg.text = "Enter a code"
            return
        if not os.path.exists(security.STORE):
            security.set_passcode(code)
            vault.init(code)
            self.manager.current = "main"
            return
        if security.verify(code):
            vault.init(code)
            self.manager.current = "main"
        else:
            self.ids.msg.text = "Wrong code"


class ChatScreen(MDScreen):
    def on_mic(self):
        from mine_backend import voice
        try:
            t = voice.listen()
            self.ids.chat_log.text += f"\nYou: {t}"
            r = voice.reply(t)
            self.ids.chat_log.text += f"\nMINE: {r}"
            voice.speak(r)
        except Exception as e:
            self.ids.chat_log.text += f"\nError: {e}"


class MeScreen(MDScreen):
    pass


class VaultScreen(MDScreen):
    def on_enter(self):
        self.ids.file_list.clear_widgets()
        try:
            for fid, name, _ in vault.list_files():
                self.ids.file_list.add_widget(OneLineListItem(text=name))
        except Exception:
            pass


class MainTabs(MDScreen):
    decoy_mode = BooleanProperty(False)


class MineApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Cyan"
        return Builder.load_file("mine.kv")


if __name__ == "__main__":
    MineApp().run()
