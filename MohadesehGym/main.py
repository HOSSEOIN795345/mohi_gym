from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock
from kivy.core.text import LabelBase
from kivy.graphics import Color, RoundedRectangle
from kivy.animation import Animation

import json
import os
import arabic_reshaper
from bidi.algorithm import get_display

# ==========================
# فونت فارسی
# ==========================

LabelBase.register(name="Vazir", fn_regular="Vazirmatn-Bold.ttf")


def fa(text):
    return get_display(arabic_reshaper.reshape(str(text)))


# ==========================
# ذخیره رکوردها
# ==========================

RECORD_FILE = "records.json"


def load_records():
    if os.path.exists(RECORD_FILE):
        with open(RECORD_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_records(data):
    with open(RECORD_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


# ==========================
# برنامه تمرینی
# ==========================

days = {
    "روز اول": [
        "دوچرخه",
        "پرس سرشانه",
        "نشر جانب",
        "فلای بک",
        "بارفیکس",
        "پرس سینه هالتر",
        "جلو بازو اسپایدر",
        "پشت بازو خوابیده هالتر",
        "دمبل چکشی",
        "شکم آویزان از بارفیکس",
    ],
    "روز دوم": [
        "دوچرخه",
        "جلو پا ماشین",
        "پشت پا ماشین",
        "اسکوات",
        "پرس پا",
        "هیپ تراست",
        "ددلیفت",
    ],
    "روز سوم": [
        "دوچرخه",
        "ساق پا ایستاده دستگاه",
        "جلو پا دستگاه",
        "لانگز",
        "فیس پول",
        "فلای سینه",
        "بالاسینه سیم‌کش",
        "پشت بازو سیم‌کش تک دست",
        "شکم موربی",
    ],
}


# ==========================
# دکمه زیبا
# ==========================


class PurpleButton(Button):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.font_name = "Vazir"
        self.font_size = 18

        self.background_normal = ""
        self.background_color = (0, 0, 0, 0)

        with self.canvas.before:
            Color(0.55, 0.25, 0.75, 1)

            self.rect = RoundedRectangle(radius=[20])

        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, *args):

        self.rect.pos = self.pos
        self.rect.size = self.size

    def on_press(self):

        Animation(size=(self.width * 0.95, self.height * 0.95), duration=0.1).start(
            self
        )

        Animation(size=(self.width, self.height), duration=0.1).start(self)


# ==========================
# صفحه اصلی
# ==========================


class Home(Screen):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)

        box = BoxLayout(orientation="vertical", padding=30, spacing=25)

        box.add_widget(
            Label(text=fa("💜 باشگاه محدثه 💜"), font_name="Vazir", font_size=30)
        )

        buttons = [
            ("🏋️ برنامه تمرینی", "training"),
            ("🏆 بیشترین رکوردها", "records"),
            ("✨ قبل از باشگاه", "before"),
        ]

        for text, page in buttons:

            b = PurpleButton(text=fa(text), size_hint_y=None, height=70)

            b.bind(on_press=lambda x, p=page: self.go(p))

            box.add_widget(b)

        self.add_widget(box)

    def go(self, page):

        self.manager.current = page


# ==========================
# صفحه روزها
# ==========================


class Training(Screen):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)

        self.box = BoxLayout(orientation="vertical", padding=20, spacing=20)

        self.box.add_widget(
            Label(text=fa("برنامه تمرینی محدثه"), font_name="Vazir", font_size=25)
        )

        for day in days:

            b = PurpleButton(text=fa(day), height=70, size_hint_y=None)

            b.bind(on_press=lambda x, d=day: self.open_day(d))

            self.box.add_widget(b)

        back = PurpleButton(text=fa("بازگشت"), height=60, size_hint_y=None)

        back.bind(on_press=lambda x: self.back())

        self.box.add_widget(back)

        self.add_widget(self.box)

    def open_day(self, day):

        workout = self.manager.get_screen("workout")

        workout.load_day(day, days[day])

        self.manager.current = "workout"

    def back(self):

        self.manager.current = "home"
        # ==========================


# صفحه تمرین هر روز
# ==========================


class Workout(Screen):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)

        self.day_name = ""
        self.moves = []
        self.current_move = 0
        self.current_set = 0
        self.timer = None

        self.main = BoxLayout(orientation="vertical", padding=15, spacing=15)

        self.title = Label(font_name="Vazir", font_size=24, size_hint_y=None, height=50)

        self.main.add_widget(self.title)

        self.scroll = ScrollView()

        self.move_box = BoxLayout(orientation="vertical", spacing=15, size_hint_y=None)

        self.move_box.bind(minimum_height=self.move_box.setter("height"))

        self.scroll.add_widget(self.move_box)

        self.main.add_widget(self.scroll)

        self.status = Label(font_name="Vazir", size_hint_y=None, height=40)

        self.main.add_widget(self.status)

        self.weight = TextInput(
            hint_text=fa("وزنه"),
            font_name="Vazir",
            size_hint=(0.5, None),
            height=50,
            pos_hint={"center_x": 0.5},
        )

        self.main.add_widget(self.weight)

        self.action = PurpleButton(text=fa("ثبت رکورد"), size_hint_y=None, height=60)

        self.action.bind(on_press=self.complete_set)

        self.main.add_widget(self.action)

        back = PurpleButton(text=fa("بازگشت"), size_hint_y=None, height=60)

        back.bind(on_press=lambda x: self.back())

        self.main.add_widget(back)

        self.add_widget(self.main)

    def load_day(self, day, moves):

        self.day_name = day

        self.moves = moves

        self.current_move = 0

        self.current_set = 0

        self.show_moves()

    def show_moves(self):

        self.move_box.clear_widgets()

        self.title.text = fa(self.day_name)

        for i, move in enumerate(self.moves):

            b = PurpleButton(
                text=fa(f"حرکت {i+1} از {len(self.moves)}\n{move}"),
                size_hint_y=None,
                height=75,
            )

            # قانون قفل حرکات

            if i == 0 or i == 1:
                b.disabled = False

            elif i <= self.current_move:
                b.disabled = False

            else:
                b.disabled = True

            b.bind(on_press=lambda x, index=i: self.select_move(index))

            self.move_box.add_widget(b)

    def select_move(self, index):

        self.current_move = index

        self.current_set = 0

        move = self.moves[index]

        if move == "دوچرخه":

            self.status.text = fa("دوچرخه ثابت - ۵ دقیقه")

            self.start_timer()

        else:

            self.stop_timer()

            self.update_status()

    def update_status(self):

        self.status.text = fa(
            f"{self.moves[self.current_move]} | ست {self.current_set+1} از 3"
        )

    def start_timer(self):

        self.stop_timer()

        self.seconds = 300

        self.status.text = fa("دوچرخه: 05:00")

        self.timer = Clock.schedule_interval(self.count_down, 1)

    def count_down(self, dt):

        if self.seconds > 0:

            self.seconds -= 1

            m = self.seconds // 60

            s = self.seconds % 60

            self.status.text = fa(f"دوچرخه: {m:02}:{s:02}")

        else:

            self.stop_timer()

            self.status.text = fa("دوچرخه تمام شد 💜")

    def stop_timer(self):

        if self.timer:

            self.timer.cancel()

            self.timer = None

    def complete_set(self, instance):

        move = self.moves[self.current_move]

        if move == "دوچرخه":

            return

        if self.weight.text == "":

            return

        weight = int(self.weight.text)

        records = load_records()

        if move not in records or weight > records[move]:

            records[move] = weight

            save_records(records)

        self.weight.text = ""

        self.current_set += 1

        if self.current_set < 3:

            self.update_status()

        else:

            self.status.text = fa("💜 آفرین محدثه، حرکت کامل شد 🔥")

            if self.current_move + 1 < len(self.moves):

                self.current_move += 1

            self.show_moves()

            self.current_set = 0

            if self.current_move == len(self.moves) - 1:

                Clock.schedule_once(lambda x: self.finish_day(), 3)

    def finish_day(self):

        self.status.text = fa("💜 تمرین امروز کامل شد قهرمان 👑")

        self.current_move = 0

        self.current_set = 0

        Clock.schedule_once(lambda x: self.back(), 3)

    def back(self):

        self.stop_timer()

        self.manager.current = "training"


# ==========================
# صفحه قبل از باشگاه
# ==========================


class BeforeGym(Screen):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)

        self.tasks = [
            "آب کافی بنوش",
            "غذای سبک بخور",
            "لباس و وسایل آماده کن",
            "بدن را گرم کن",
            "موسیقی انرژی بخش آماده کن",
            "هدف تمرین امروز را مشخص کن",
            "با انرژی مثبت وارد باشگاه شو",
        ]

        self.done = [False] * len(self.tasks)

        self.layout = BoxLayout(orientation="vertical", padding=20, spacing=12)

        self.title = Label(
            text=fa("کارهای قبل از باشگاه"),
            font_name="Vazir",
            font_size=24,
            size_hint_y=None,
            height=50,
        )

        self.layout.add_widget(self.title)

        self.buttons = []

        for i, t in enumerate(self.tasks):

            b = PurpleButton(text=fa(t), size_hint_y=None, height=60)

            b.bind(on_press=lambda x, index=i: self.check_task(index))

            self.buttons.append(b)

            self.layout.add_widget(b)

        self.message = Label(font_name="Vazir", size_hint_y=None, height=50)

        self.layout.add_widget(self.message)

        back = PurpleButton(text=fa("بازگشت"), size_hint_y=None, height=60)

        back.bind(on_press=lambda x: self.back())

        self.layout.add_widget(back)

        self.add_widget(self.layout)

    def check_task(self, index):

        self.done[index] = True

        self.buttons[index].text = fa("✔ " + self.tasks[index])

        if all(self.done):

            self.message.text = fa("💜 محدثه آماده تمرینی، برو بدرخش 🔥")

            Clock.schedule_once(self.reset, 4)

    def reset(self, dt):

        self.done = [False] * len(self.tasks)

        for i, b in enumerate(self.buttons):

            b.text = fa(self.tasks[i])

        self.message.text = ""

        self.manager.current = "home"

    def back(self):

        self.manager.current = "home"


# ==========================
# صفحه رکوردها
# ==========================


class Records(Screen):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)

        self.layout = BoxLayout(orientation="vertical", padding=20, spacing=15)

        self.title = Label(
            text=fa("🏆 بیشترین رکوردهای محدثه"),
            font_name="Vazir",
            font_size=24,
            size_hint_y=None,
            height=50,
        )

        self.layout.add_widget(self.title)

        self.scroll = ScrollView()

        self.records_box = BoxLayout(
            orientation="vertical", spacing=10, size_hint_y=None
        )

        self.records_box.bind(minimum_height=self.records_box.setter("height"))

        self.scroll.add_widget(self.records_box)

        self.layout.add_widget(self.scroll)

        delete_all = PurpleButton(
            text=fa("🗑 پاک کردن همه رکوردها"), size_hint_y=None, height=60
        )

        delete_all.bind(on_press=self.delete_all)

        self.layout.add_widget(delete_all)

        back = PurpleButton(text=fa("بازگشت"), size_hint_y=None, height=60)

        back.bind(on_press=lambda x: self.back())

        self.layout.add_widget(back)

        self.add_widget(self.layout)

    def on_enter(self):

        self.refresh()

    def refresh(self):

        self.records_box.clear_widgets()

        records = load_records()

        if not records:

            self.records_box.add_widget(
                Label(text=fa("هنوز رکوردی ثبت نشده"), font_name="Vazir")
            )

            return

        for move, value in records.items():

            row = BoxLayout(size_hint_y=None, height=60, spacing=10)

            label = Label(text=fa(f"{move} : {value} کیلو"), font_name="Vazir")

            delete = PurpleButton(text=fa("حذف"), size_hint_x=0.3)

            delete.bind(on_press=lambda x, m=move: self.delete_one(m))

            row.add_widget(label)

            row.add_widget(delete)

            self.records_box.add_widget(row)

    def delete_one(self, move):

        records = load_records()

        if move in records:

            del records[move]

            save_records(records)

        self.refresh()

    def delete_all(self, instance):

        save_records({})

        self.refresh()

    def back(self):

        self.manager.current = "home"
        # ==========================


# اجرای برنامه
# ==========================


class MohadesehGymApp(App):

    def build(self):

        sm = ScreenManager()

        sm.add_widget(Home(name="home"))
        sm.add_widget(Training(name="training"))
        sm.add_widget(Workout(name="workout"))
        sm.add_widget(BeforeGym(name="before"))
        sm.add_widget(Records(name="records"))

        return sm


if __name__ == "__main__":
    MohadesehGymApp().run()
