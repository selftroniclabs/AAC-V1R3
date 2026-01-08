import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import pyttsx3
import threading
import time
import random

class AACApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Selftronic AAC V1R3 (Python Desktop)")
        self.geometry("1100x750")
        self.configure(bg="#f0f2f5")

        # --- 语言设置 ---
        self.current_language = 'en'  # 默认为英文
        
        # 翻译字典
        self.translations = {
            'en': {
                'title': 'Selftronic AAC',
                'settings': '⚙️ Settings',
                'play': '🔊 Play',
                'ai_btn': '✨ Magic',
                'delete': '⌫ Del',
                'clear': '🗑️ Clear',
                'keyboard': '⌨️ Type',
                'emergency': '🔔 HELP',
                'placeholder': 'Click icons or use keyboard...',
                'ai_thinking': '⏳ Thinking...',
                'ai_result_title': 'AI Assistant',
                'ai_result_msg': 'Expanded Result:\n\n“{}”',
                'cat_people': 'People',
                'cat_action': 'Action',
                'cat_food': 'Food',
                'cat_object': 'Object',
                'cat_feeling': 'Feeling',
                'voice_speed': 'Voice Speed',
                'voice_select': 'Voice Selection',
                'save': 'Save',
                'input_title': 'Type Word',
                'input_msg': 'Please type what you want to say:',
                'emergency_msg': 'Emergency! I need help immediately!'
            },
            'zh': {
                'title': 'Selftronic AAC',
                'settings': '⚙️ 设置',
                'play': '🔊 播放',
                'ai_btn': '✨ 完整句',
                'delete': '⌫ 删除',
                'clear': '🗑️ 清空',
                'keyboard': '⌨️ 输入',
                'emergency': '🔔 紧急',
                'placeholder': '点击图标或使用键盘输入...',
                'ai_thinking': '⏳ 思考中...',
                'ai_result_title': 'AI 助手扩展',
                'ai_result_msg': '扩展结果：\n\n“{}”',
                'cat_people': '人物',
                'cat_action': '动作',
                'cat_food': '食物',
                'cat_object': '物品',
                'cat_feeling': '感觉',
                'voice_speed': '语速调节',
                'voice_select': '语音选择',
                'save': '保存',
                'input_title': '手动输入',
                'input_msg': '请输入您想说的话：',
                'emergency_msg': '紧急情况！请帮帮我！'
            }
        }

        # --- 初始化语音引擎 ---
        self.engine_init_lock = threading.Lock() 
        self.rate = 150
        
        # 预加载语音列表
        temp_engine = pyttsx3.init()
        self.voice_list = temp_engine.getProperty('voices')
        temp_engine.stop()
        del temp_engine

        # 自动查找最佳的中英文语音ID
        self.zh_voice_id = None
        self.en_voice_id = None
        
        for voice in self.voice_list:
            v_name = voice.name.lower()
            if "zh" in voice.languages or "chinese" in v_name or "sinji" in v_name or "ting-ting" in v_name:
                if not self.zh_voice_id: self.zh_voice_id = voice.id
            if "en" in voice.languages or "english" in v_name or "alex" in v_name or "david" in v_name:
                if not self.en_voice_id: self.en_voice_id = voice.id
        
        self.current_voice_id = self.en_voice_id if self.en_voice_id else (self.voice_list[0].id if self.voice_list else None)

        # --- 应用数据 ---
        self.sentence = [] 
        self.current_category = 'people'
        self.is_expanding = False

        # 分类定义
        self.categories_data = [
            {'id': 'people', 'label_zh': '人物', 'label_en': 'People', 'icon': '👤', 'color': '#3b82f6'},
            {'id': 'action', 'label_zh': '动作', 'label_en': 'Action', 'icon': '🎮', 'color': '#22c55e'},
            {'id': 'food', 'label_zh': '食物', 'label_en': 'Food', 'icon': '☕', 'color': '#f97316'},
            {'id': 'object', 'label_zh': '物品', 'label_en': 'Object', 'icon': '📦', 'color': '#a855f7'},
            {'id': 'feeling', 'label_zh': '感觉', 'label_en': 'Feeling', 'icon': '😄', 'color': '#eab308'},
        ]

        # 词汇数据库 (V1R3 Expanded)
        self.vocabulary_db = [
            # People
            {'id': 101, 'zh': '我', 'en': 'I', 'emoji': '🧑', 'category': 'people'},
            {'id': 102, 'zh': '爸爸', 'en': 'Dad', 'emoji': '👨', 'category': 'people'},
            {'id': 103, 'zh': '妈妈', 'en': 'Mom', 'emoji': '👩', 'category': 'people'},
            {'id': 104, 'zh': '老师', 'en': 'Teacher', 'emoji': '👩‍🏫', 'category': 'people'},
            {'id': 105, 'zh': '医生', 'en': 'Doctor', 'emoji': '👨‍⚕️', 'category': 'people'},
            {'id': 106, 'zh': '朋友', 'en': 'Friend', 'emoji': '👫', 'category': 'people'},
            
            # Action (Expanded)
            {'id': 201, 'zh': '想要', 'en': 'Want', 'emoji': '🤲', 'category': 'action'},
            {'id': 202, 'zh': '吃', 'en': 'Eat', 'emoji': '🍽️', 'category': 'action'},
            {'id': 203, 'zh': '喝', 'en': 'Drink', 'emoji': '🥤', 'category': 'action'},
            {'id': 204, 'zh': '去', 'en': 'Go', 'emoji': '🚶', 'category': 'action'},
            {'id': 205, 'zh': '玩', 'en': 'Play', 'emoji': '🎲', 'category': 'action'},
            {'id': 206, 'zh': '看', 'en': 'Look', 'emoji': '👀', 'category': 'action'},
            {'id': 207, 'zh': '帮忙', 'en': 'Help', 'emoji': '🆘', 'category': 'action'},
            {'id': 208, 'zh': '睡觉', 'en': 'Sleep', 'emoji': '🛌', 'category': 'action'},
            {'id': 209, 'zh': '跑', 'en': 'Run', 'emoji': '🏃', 'category': 'action'},
            {'id': 210, 'zh': '画画', 'en': 'Draw', 'emoji': '🎨', 'category': 'action'},
            {'id': 211, 'zh': '洗澡', 'en': 'Bath', 'emoji': '🛁', 'category': 'action'},
            {'id': 212, 'zh': '停', 'en': 'Stop', 'emoji': '🛑', 'category': 'action'},

            # Food
            {'id': 301, 'zh': '水', 'en': 'Water', 'emoji': '💧', 'category': 'food'},
            {'id': 302, 'zh': '饭', 'en': 'Rice', 'emoji': '🍚', 'category': 'food'},
            {'id': 303, 'zh': '苹果', 'en': 'Apple', 'emoji': '🍎', 'category': 'food'},
            {'id': 304, 'zh': '牛奶', 'en': 'Milk', 'emoji': '🥛', 'category': 'food'},
            {'id': 305, 'zh': '饼干', 'en': 'Cookie', 'emoji': '🍪', 'category': 'food'},
            {'id': 306, 'zh': '果汁', 'en': 'Juice', 'emoji': '🍹', 'category': 'food'},
            {'id': 307, 'zh': '面包', 'en': 'Bread', 'emoji': '🍞', 'category': 'food'},
            
            # Object
            {'id': 401, 'zh': '厕所', 'en': 'Toilet', 'emoji': '🚽', 'category': 'object'},
            {'id': 402, 'zh': '平板', 'en': 'Tablet', 'emoji': '📱', 'category': 'object'},
            {'id': 403, 'zh': '书', 'en': 'Book', 'emoji': '📖', 'category': 'object'},
            {'id': 404, 'zh': '床', 'en': 'Bed', 'emoji': '🛏️', 'category': 'object'},
            {'id': 405, 'zh': '家', 'en': 'Home', 'emoji': '🏠', 'category': 'object'},
            {'id': 406, 'zh': '公园', 'en': 'Park', 'emoji': '🌳', 'category': 'object'},

            # Feeling (Expanded)
            {'id': 501, 'zh': '开心', 'en': 'Happy', 'emoji': '😄', 'category': 'feeling'},
            {'id': 502, 'zh': '难过', 'en': 'Sad', 'emoji': '😢', 'category': 'feeling'},
            {'id': 503, 'zh': '痛', 'en': 'Pain', 'emoji': '🤕', 'category': 'feeling'},
            {'id': 504, 'zh': '累', 'en': 'Tired', 'emoji': '😫', 'category': 'feeling'},
            {'id': 505, 'zh': '好', 'en': 'Good', 'emoji': '👍', 'category': 'feeling'},
            {'id': 506, 'zh': '不', 'en': 'No', 'emoji': '🙅', 'category': 'feeling'},
            {'id': 507, 'zh': '生气', 'en': 'Angry', 'emoji': '😠', 'category': 'feeling'},
            {'id': 508, 'zh': '害怕', 'en': 'Scared', 'emoji': '😱', 'category': 'feeling'},
            {'id': 509, 'zh': '无聊', 'en': 'Bored', 'emoji': '😐', 'category': 'feeling'},
            {'id': 510, 'zh': '兴奋', 'en': 'Excited', 'emoji': '🤩', 'category': 'feeling'},
        ]

        self.setup_ui()
        self.update_ui_text() 

    def setup_ui(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TButton', font=('Arial', 12), padding=5)
        
        # --- Top Bar ---
        top_bar = tk.Frame(self, bg="white", height=60)
        top_bar.pack(side="top", fill="x")
        
        # Logo
        tk.Label(top_bar, text="S", bg="#2563eb", fg="white", font=("Arial", 16, "bold"), width=3).pack(side="left", padx=15, pady=10)
        self.title_label = tk.Label(top_bar, text="", bg="white", font=("Arial", 14, "bold"), fg="#1e293b")
        self.title_label.pack(side="left")
        
        # Right Buttons
        btn_frame = tk.Frame(top_bar, bg="white")
        btn_frame.pack(side="right", padx=15)

        # Emergency Button (New V1R3)
        self.emergency_btn = tk.Button(btn_frame, text="🔔", command=self.trigger_emergency, bg="#fee2e2", fg="red", relief="flat", font=("Arial", 12, "bold"))
        self.emergency_btn.pack(side="left", padx=5)

        self.lang_btn = tk.Button(btn_frame, text="🌐 EN/CN", command=self.toggle_language, bg="#e2e8f0", relief="flat", font=("Arial", 10))
        self.lang_btn.pack(side="left", padx=5)

        self.settings_btn = tk.Button(btn_frame, text="", command=self.open_settings, bg="#f1f5f9", relief="flat")
        self.settings_btn.pack(side="left", padx=5)

        # --- Sentence Strip ---
        strip_frame = tk.Frame(self, bg="white", pady=10)
        strip_frame.pack(side="top", fill="x", padx=15, pady=(15, 0))

        self.sentence_container = tk.Frame(strip_frame, bg="#f8fafc", highlightbackground="#e2e8f0", highlightthickness=2)
        self.sentence_container.pack(fill="x", ipady=10, padx=5)
        self.sentence_label = tk.Label(self.sentence_container, text="", bg="#f8fafc", fg="#94a3b8", font=("Arial", 12, "italic"))
        self.sentence_label.pack(side="left", padx=10)

        # Controls
        ctrl_frame = tk.Frame(strip_frame, bg="white", pady=10)
        ctrl_frame.pack(fill="x")
        
        self.btn_play = tk.Button(ctrl_frame, text="", bg="#2563eb", fg="white", font=("Arial", 12, "bold"), 
                  command=self.play_sentence, width=15, pady=5, relief="flat")
        self.btn_play.pack(side="left", padx=5)
        
        self.btn_ai = tk.Button(ctrl_frame, text="", bg="#9333ea", fg="white", font=("Arial", 12, "bold"), 
                  command=self.ai_expand, width=15, pady=5, relief="flat")
        self.btn_ai.pack(side="left", padx=5)
        
        self.btn_del = tk.Button(ctrl_frame, text="", bg="#ffedd5", fg="#c2410c", font=("Arial", 12), 
                  command=self.backspace, width=10, pady=5, relief="flat")
        self.btn_del.pack(side="left", padx=5)
        
        self.btn_clear = tk.Button(ctrl_frame, text="", bg="#fee2e2", fg="#dc2626", font=("Arial", 12), 
                  command=self.clear_sentence, width=10, pady=5, relief="flat")
        self.btn_clear.pack(side="left", padx=5)

        # --- Main Content ---
        content_frame = tk.Frame(self, bg="#f0f2f5")
        content_frame.pack(side="top", fill="both", expand=True, pady=15)

        # Sidebar Container
        sidebar_container = tk.Frame(content_frame, bg="white", width=120)
        sidebar_container.pack(side="left", fill="y", padx=(15, 0), pady=(0, 15))

        # Categories
        self.cat_frame = tk.Frame(sidebar_container, bg="white")
        self.cat_frame.pack(side="top", fill="x")

        # Keyboard Input Button (New V1R3) - Bottom of sidebar
        self.btn_keyboard = tk.Button(sidebar_container, text="⌨️", command=self.open_keyboard, bg="#f3f4f6", relief="flat", pady=10)
        self.btn_keyboard.pack(side="bottom", fill="x", padx=5, pady=10)
        
        self.grid_canvas = tk.Canvas(content_frame, bg="#f0f2f5", highlightthickness=0)
        self.grid_frame = tk.Frame(self.grid_canvas, bg="#f0f2f5")
        
        scrollbar = ttk.Scrollbar(content_frame, orient="vertical", command=self.grid_canvas.yview)
        self.grid_canvas.configure(yscrollcommand=scrollbar.set)
        
        scrollbar.pack(side="right", fill="y", pady=(0, 15), padx=(0, 15))
        self.grid_canvas.pack(side="left", fill="both", expand=True, padx=10, pady=(0, 15))
        
        self.grid_canvas.create_window((0, 0), window=self.grid_frame, anchor="nw")
        self.grid_frame.bind("<Configure>", lambda e: self.grid_canvas.configure(scrollregion=self.grid_canvas.bbox("all")))

    def update_ui_text(self):
        t = self.translations[self.current_language]
        
        self.title_label.config(text=t['title'])
        self.settings_btn.config(text=t['settings'])
        self.btn_play.config(text=t['play'])
        self.btn_ai.config(text=t['ai_btn'])
        self.btn_del.config(text=t['delete'])
        self.btn_clear.config(text=t['clear'])
        self.btn_keyboard.config(text=t['keyboard'])
        self.emergency_btn.config(text=t['emergency'])
        
        if not self.sentence:
            self.sentence_label.config(text=t['placeholder'])

        for widget in self.cat_frame.winfo_children():
            widget.destroy()
        
        for cat in self.categories_data:
            label_text = cat[f'label_{self.current_language}']
            bg_color = "#e0e7ff" if self.current_category == cat['id'] else "white"
            
            btn = tk.Button(self.cat_frame, text=f"{cat['icon']}\n{label_text}", 
                            font=("Arial", 11), bg=bg_color, relief="flat", pady=15,
                            command=lambda c=cat['id']: self.change_category(c))
            btn.pack(fill="x", padx=5, pady=2)

        self.render_grid()
        self.update_sentence_display()

        if self.current_language == 'zh':
            if self.zh_voice_id: self.current_voice_id = self.zh_voice_id
        else:
            if self.en_voice_id: self.current_voice_id = self.en_voice_id

    def toggle_language(self):
        self.current_language = 'zh' if self.current_language == 'en' else 'en'
        self.sentence = [] 
        self.update_ui_text()

    def render_grid(self):
        for widget in self.grid_frame.winfo_children():
            widget.destroy()

        items = [v for v in self.vocabulary_db if v['category'] == self.current_category]
        
        columns = 4
        for i, item in enumerate(items):
            row = i // columns
            col = i % columns
            
            display_text = item[self.current_language]
            
            card = tk.Frame(self.grid_frame, bg="white", bd=1, relief="solid")
            card.grid(row=row, column=col, padx=8, pady=8, ipadx=10, ipady=10, sticky="nsew")
            
            lbl_emoji = tk.Label(card, text=item['emoji'], font=("Segoe UI Emoji", 32), bg="white")
            lbl_emoji.pack()
            
            lbl_text = tk.Label(card, text=display_text, font=("Arial", 12, "bold"), bg="white", fg="#1e293b")
            lbl_text.pack()
            
            for w in [card, lbl_emoji, lbl_text]:
                w.bind("<Button-1>", lambda e, it=item: self.add_to_sentence(it))

    def change_category(self, cat_id):
        self.current_category = cat_id
        self.update_ui_text()

    def update_sentence_display(self):
        for widget in self.sentence_container.winfo_children():
            widget.destroy()
            
        t = self.translations[self.current_language]

        if not self.sentence:
            self.sentence_label = tk.Label(self.sentence_container, text=t['placeholder'], bg="#f8fafc", fg="#94a3b8", font=("Arial", 12, "italic"))
            self.sentence_label.pack(side="left", padx=10)
            return

        for item in self.sentence:
            # item 可能是普通词汇字典，也可能是手动输入的文本对象
            if 'manual_text' in item:
                txt = item['manual_text']
                emoji = "⌨️"
            else:
                txt = item[self.current_language]
                emoji = item['emoji']
                
            chip = tk.Frame(self.sentence_container, bg="white", bd=1, relief="solid")
            chip.pack(side="left", padx=5, pady=2)
            tk.Label(chip, text=f"{emoji} {txt}", font=("Arial", 12), bg="white", padx=5, pady=2).pack()

    def add_to_sentence(self, item):
        self.sentence.append(item)
        self.update_sentence_display()
        # 发音
        if 'manual_text' in item:
            self.speak_text(item['manual_text'])
        else:
            self.speak_text(item[self.current_language])

    def open_keyboard(self):
        t = self.translations[self.current_language]
        text = simpledialog.askstring(t['input_title'], t['input_msg'], parent=self)
        if text:
            # 创建一个临时的词汇对象
            manual_item = {'manual_text': text, 'category': 'manual'}
            self.add_to_sentence(manual_item)

    def trigger_emergency(self):
        t = self.translations[self.current_language]
        msg = t['emergency_msg']
        messagebox.showwarning(t['emergency'], msg)
        # 紧急呼叫，大声且快速
        def _alarm():
            try:
                with self.engine_init_lock:
                    engine = pyttsx3.init()
                    if self.current_voice_id:
                        try: engine.setProperty('voice', self.current_voice_id)
                        except: pass
                    engine.setProperty('rate', 170) # 快一点
                    engine.setProperty('volume', 1.0) # 最大音量
                    engine.say(msg)
                    engine.runAndWait()
            except: pass
        threading.Thread(target=_alarm).start()

    def backspace(self):
        if self.sentence:
            self.sentence.pop()
            self.update_sentence_display()

    def clear_sentence(self):
        self.sentence = []
        self.update_sentence_display()

    def play_sentence(self):
        if not self.sentence: return
        
        words = []
        for item in self.sentence:
            if 'manual_text' in item:
                words.append(item['manual_text'])
            else:
                words.append(item[self.current_language])
                
        full_text = " ".join(words)
        self.speak_text(full_text)

    def ai_expand(self):
        if not self.sentence: return
        t = self.translations[self.current_language]
        self.btn_ai.config(text=t['ai_thinking'])
        self.update() 
        threading.Thread(target=self._ai_process).start()

    def _ai_process(self):
        time.sleep(0.6)
        
        words = []
        last_category = 'other'
        last_word_text = ""
        
        # 提取单词和最后一个分类
        for item in self.sentence:
            if 'manual_text' in item:
                words.append(item['manual_text'])
                last_category = 'manual'
                last_word_text = item['manual_text']
            else:
                words.append(item[self.current_language])
                last_category = item['category']
                last_word_text = item[self.current_language].lower()

        full_text = " ".join(words)
        expanded_text = full_text 

        if self.current_language == 'zh':
            # --- 中文规则引擎 V3 ---
            expanded_text = f"请问我可以{full_text}吗？"
            
            # 1. 紧急处理
            if last_category == 'feeling' and last_word_text in ['痛', '害怕', '生气']:
                 expanded_text = f"我感到{last_word_text}，我很不舒服。"
            
            # 2. 动作处理
            elif last_category == 'action':
                if last_word_text in ['睡觉', '洗澡', '画画']:
                    expanded_text = f"我想去{last_word_text}。"
                elif last_word_text == '停':
                    expanded_text = "请停下来，我不喜欢这样。"
                else:
                    expanded_text = f"我想{last_word_text}。"
            
            # 3. 特定组合
            elif '我' in words and '家' in words: expanded_text = "我想回家了。"
            elif '不' in words and '吃' in words: expanded_text = "我不想吃这个。"
            
        else:
            # --- English Smart Rules Engine (V3) ---
            
            # 1. Negation (Improved)
            if 'no' in [w.lower() for w in words]:
                content_words = [w for w in words if w.lower() != 'no']
                if content_words:
                    expanded_text = f"I don't want {content_words[-1].lower()}."
                else:
                    expanded_text = "No, thank you."
            
            # 2. Feelings (New V3 Words)
            elif last_category == 'feeling':
                if last_word_text in ['pain', 'scared', 'angry']:
                    expanded_text = f"I am feeling {last_word_text}, please help."
                elif last_word_text in ['bored', 'tired']:
                    expanded_text = f"I am {last_word_text}, I want to do something else."
                else:
                    expanded_text = f"I feel {last_word_text}."
                
            # 3. Actions (Improved Grammar)
            elif last_category == 'action':
                # Distinguish between transitive and intransitive broadly
                if last_word_text in ['sleep', 'run', 'swim', 'bath', 'draw', 'go']:
                     expanded_text = f"I want to {last_word_text}."
                elif last_word_text == 'stop':
                    expanded_text = "Please stop that immediately."
                elif last_word_text == 'help':
                    expanded_text = "Please help me."
                else:
                    expanded_text = f"I want to {last_word_text}."

            # 4. People
            elif last_category == 'people':
                expanded_text = f"I want {last_word_text}."
            
            # 5. Default Requests
            elif last_category in ['food', 'object']:
                templates = [
                    f"May I have {last_word_text}, please?",
                    f"I would like {last_word_text}, please.",
                    f"Can I get {last_word_text}?"
                ]
                expanded_text = random.choice(templates)

        self.after(0, lambda: self._ai_done(expanded_text))

    def _ai_done(self, text):
        t = self.translations[self.current_language]
        self.btn_ai.config(text=t['ai_btn'])
        msg = t['ai_result_msg'].format(text)
        messagebox.showinfo(t['ai_result_title'], msg)
        self.speak_text(text)

    def speak_text(self, text):
        def _speak():
            try:
                with self.engine_init_lock:
                    engine = pyttsx3.init()
                    if self.current_voice_id:
                        try: engine.setProperty('voice', self.current_voice_id)
                        except: pass
                    engine.setProperty('rate', self.rate)
                    engine.say(text)
                    engine.runAndWait()
            except Exception as e:
                print(f"Speech error: {e}")

        threading.Thread(target=_speak).start()

    def open_settings(self):
        t = self.translations[self.current_language]
        win = tk.Toplevel(self)
        win.title(t['settings'])
        win.geometry("450x400")
        
        tk.Label(win, text=t['voice_speed'], font=("Arial", 10, "bold")).pack(pady=10)
        scale = tk.Scale(win, from_=50, to=300, orient="horizontal", length=200)
        scale.set(self.rate)
        scale.pack()
        
        tk.Label(win, text=t['voice_select'], font=("Arial", 10, "bold")).pack(pady=10)
        
        voice_var = tk.StringVar(value=self.current_voice_id)
        
        frame = tk.Frame(win)
        frame.pack(fill="both", expand=True, padx=20, pady=5)
        
        canvas = tk.Canvas(frame)
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        scroll_content = tk.Frame(canvas)

        scroll_content.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scroll_content, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        for voice in self.voice_list:
            v_name = voice.name
            tag = ""
            if "zh" in voice.languages or "Chinese" in v_name: tag = " [CN]"
            elif "en" in voice.languages or "English" in v_name: tag = " [EN]"
            
            tk.Radiobutton(scroll_content, text=f"{v_name}{tag}", variable=voice_var, value=voice.id).pack(anchor="w")

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        def save():
            self.rate = scale.get()
            self.current_voice_id = voice_var.get()
            win.destroy()
            
        tk.Button(win, text=t['save'], command=save, bg="#2563eb", fg="white").pack(pady=10)

if __name__ == "__main__":
    app = AACApp()
    app.mainloop()