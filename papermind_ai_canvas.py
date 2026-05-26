import customtkinter as ctk
from tkinter import messagebox
import json
import os
import platform
from google import genai
from google.genai import types

# 系統字型判定
if platform.system() == "Windows":
    main_font_family = "Segoe UI"
elif platform.system() == "Darwin":
    main_font_family = "PingFang TC"
else:
    main_font_family = "Arial"

ctk.set_appearance_mode("light")
main_font_family = "宅在家字動筆"

class PaperMindAICanvas(ctk.CTk):
    def __init__(self):
        super().__init__()

        # 💡 核心：如果專案資料夾裡有字型檔，優先讀取它！
        # font_name = "宅在家自動筆" # 填入你安裝/下載的字型名稱
        
        # 設定全域字型變數，隨時調用
        self.title_font = ctk.CTkFont(family=main_font_family, size=18, weight="bold")
        self.body_font = ctk.CTkFont(family=main_font_family, size=13)

        # 紫黃多巴胺色系
        self.bg_purple = "#C69FD5"      # 粉紫背景
        self.text_yellow = "#FDFDC9"    # 奶油黃字
        self.dark_purple = "#4A2E80"    # 深紫容器
        self.bar_bg = "#63439C"         # 軌道底色
        
        # 馬卡龍四大結構字卡顏色
        self.card_colors = {
            "研究目的": "#FFB3BA",       # 櫻花粉
            "核心方法": "#BAE1FF",       # 天空藍
            "關鍵指標/結果": "#FDFDC9",   # 奶油黃（字搭配深色）
            "未來挑戰": "#BAFFC9"        # 薄荷綠
        }

        self.title("PaperMind AI Canvas - Academic Abstract Summarizer 🔬")
        self.geometry("980x600") # 寬螢幕黃金佈局
        self.resizable(False, False)
        self.configure(fg_color=self.bg_purple)

        # 初始化 Gemini 客戶端 (會自動讀取作業系統中名為 GEMINI_API_KEY 的環境變數)
        # 你也可以直接寫成 client = genai.Client(api_key="你的KEY")
        try:
            self.ai_client = genai.Client(api_key="AIzaSyCcpMHkMfiYWoElAuKNvzQQO1Huvb93ALY")
        except Exception as e:
            self.ai_client = None

        self.title_font = ctk.CTkFont(family=main_font_family, size=18, weight="bold")
        self.body_font = ctk.CTkFont(family=main_font_family, size=13)
        self.card_title_font = ctk.CTkFont(family=main_font_family, size=14, weight="bold")
        self.btn_font = ctk.CTkFont(family=main_font_family, size=13, weight="bold")

        self.setup_ui()

    def setup_ui(self):
        # 主雙欄配置外框
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        main_frame.grid_columnconfigure(0, weight=45) # 左欄：原始論文貼上面板
        main_frame.grid_columnconfigure(1, weight=55) # 右欄：AI 結構化字卡牆
        main_frame.grid_rowconfigure(0, weight=1)

        # =====================================================================
        # 📝 【左欄】：原始論文 Abstract 輸入區
        # =====================================================================
        left_column = ctk.CTkFrame(main_frame, fg_color=self.dark_purple, corner_radius=12)
        left_column.grid(row=0, column=0, padx=(0, 10), sticky="nsew", pady=5)

        ctk.CTkLabel(left_column, text="📝 Paste Paper Abstract / Text", font=self.title_font, text_color=self.text_yellow).pack(pady=(15, 5))

        # 大文字輸入框
        self.txt_input = ctk.CTkTextbox(left_column, fg_color="#FFFFFF", text_color="#000000", font=self.body_font, corner_radius=8)
        self.txt_input.pack(fill="both", expand=True, padx=20, pady=10)
        # 預設置入一段防呆提示，方便測試
        self.txt_input.insert("1.0", "Paste English abstract here...")

        # 核心分析鈕
        self.btn_analyze = ctk.CTkButton(
            left_column, text="🔬 AI 智能結構化分析", font=self.btn_font, height=40,
            fg_color=self.bg_purple, hover_color="#B58BC4", text_color=self.dark_purple,
            command=self.start_ai_analysis
        )
        self.btn_analyze.pack(fill="x", padx=20, pady=(5, 20))

        # =====================================================================
        # 📊 【右欄】：AI 馬卡龍結構化字卡展示牆
        # =====================================================================
        self.right_column = ctk.CTkFrame(main_frame, fg_color="transparent")
        self.right_column.grid(row=0, column=1, padx=(10, 0), sticky="nsew", pady=5)

        ctk.CTkLabel(self.right_column, text="📊 AI Structured Insight Canvas", font=self.title_font, text_color=self.dark_purple).pack(anchor="w", padx=5, pady=(5, 5))

        # 可滾動的字卡面板（無邊框參數）
        self.scroll_canvas = ctk.CTkScrollableFrame(self.right_column, fg_color=self.dark_purple, corner_radius=12)
        self.scroll_canvas.pack(fill="both", expand=True)
        self.scroll_canvas._scrollbar.configure(width=0)
        self.scroll_canvas._scrollbar.pack_forget()

        # 初始狀態提示
        self.lbl_init_tips = ctk.CTkLabel(self.scroll_canvas, text="Waiting for analysis stream... 🚀\n請在左側貼上內文並點擊按鈕。", font=self.body_font, text_color="gray")
        self.lbl_init_tips.pack(pady=150)

    # --- 🤖 核心 Gemini API 串接與結構化輸出邏輯 ---
    def start_ai_analysis(self):
        paper_text = self.txt_input.get("1.0", "end").strip()
        if not paper_text or paper_text == "Paste English abstract here...":
            messagebox.showwarning("Warning", "Please paste some valid paper text first!", parent=self)
            return

        if not self.ai_client:
            # 防呆：嘗試在點擊時再次抓取，或手動補上
            try:
                self.ai_client = genai.Client()
            except:
                messagebox.showerror("API Error", "Gemini Client initialization failed!\n請確認系統環境變數中是否有設定 GEMINI_API_KEY。", parent=self)
                return

        self.btn_analyze.configure(state="disabled", text="AI Thinking... ⚡")
        self.update()

        # 💡 定義我們期望 AI 吐出的固定 Pydantic/JSON 結構類別
        import pydantic
        class PaperAnalysisSchema(pydantic.BaseModel):
            研究目的: str
            核心方法: str
            關鍵指標_結果: str
            未來挑戰: str
            關鍵字標籤: list[str]

        try:
            # 使用 Google 2025 全新 SDK 呼叫當前最高性價比的 gemini-2.5-flash 模型
            response = self.ai_client.models.generate_content(
                model='gemini-2.5-flash',
                contents=f"請分析以下這段學術文獻，並精準提取出核心重點。必須使用中文回答：\n\n{paper_text}",
                config=types.GenerateContentConfig(
                    # ✨ 核心魔法：強迫模型完美回傳我們定義的格式，不帶任何廢話
                    response_mime_type="application/json",
                    response_schema=PaperAnalysisSchema,
                    temperature=0.2 # 低隨機性，確保內容嚴謹扎實
                ),
            )

            # 解析回傳的 JSON 戰果
            result_json = json.loads(response.text)
            self.render_structured_cards(result_json)

        except Exception as e:
            messagebox.showerror("AI Processing Error", f"發生錯誤：{str(e)}\n請檢查網路連線或 API Key 狀態。", parent=self)
        finally:
            self.btn_analyze.configure(state="normal", text="🔬 AI 智能結構化分析")

    # --- 🎨 字卡動態渲染與排版 ---
    def render_structured_cards(self, data_dict):
        # 清空右側滾動面板
        for widget in self.scroll_canvas.winfo_children():
            widget.destroy()

        # 1. 渲染四大硬核指標卡片
        core_keys = ["研究目的", "核心方法", "關鍵指標/結果", "未來挑戰"]
        
        # 由於 JSON 欄位命名限制，轉回對應的顯示字串
        json_mapping = {
            "研究目的": "研究目的",
            "核心方法": "核心方法",
            "關鍵指標/結果": "關鍵指標_結果",
            "未來挑戰": "未來挑戰"
        }

        for key in core_keys:
            json_field = json_mapping[key]
            content_text = data_dict.get(json_field, "無對應解析內容")
            bg_color = self.card_colors[key]

            # 建立大字卡外框
            card = ctk.CTkFrame(self.scroll_canvas, fg_color=bg_color, corner_radius=10)
            card.pack(fill="x", padx=12, pady=6)

            # 字卡內的小標題（深紫色字體，維持多巴胺撞色）
            lbl_title = ctk.CTkLabel(card, text=f"📌 {key}", font=self.card_title_font, text_color=self.dark_purple)
            lbl_title.pack(anchor="w", padx=15, pady=(10, 2))

            # 內文（自動換行，文字顏色自動根據底色調配）
            lbl_content = ctk.CTkLabel(
                card, text=content_text, font=self.body_font, 
                text_color="#1A1A24" if bg_color != self.dark_purple else self.text_yellow,
                wraplength=430, justify="left"
            )
            lbl_content.pack(anchor="w", padx=15, pady=(0, 12))

        # 2. 底部渲染：關鍵字標籤牆 (Keyword Tags Wall) - 終極自動換行版 
        tags = data_dict.get("關鍵字標籤", [])
        if tags:
            tag_title = ctk.CTkLabel(self.scroll_canvas, text="🏷️ 核心關鍵字標籤 (Keywords)  ", font=self.card_title_font, text_color=self.text_yellow)
            tag_title.pack(anchor="w", padx=15, pady=(15, 2))

            # ✨ 關鍵修正：拋棄傳統 Frame，改用 Textbox 當作標籤牆容器！
            # 這樣裡面的字數再多、手寫體再寬，都會在右側邊界自動「優雅換行」，絕對不消失！
            tag_box = ctk.CTkTextbox(
                self.scroll_canvas, 
                height=60,                  # 給它足夠兩行換行的基本高度
                fg_color="transparent",     # 隱藏外框底色，完美融入深紫背景
                text_color="#E8D7FF",       # 標籤字體顏色
                font=self.body_font, 
                wrap="char"                 # 啟動字元層級自動換行
            )
            tag_box.pack(fill="x", padx=12, pady=5)

            # 將所有關鍵字串接起來，中間用亮眼的特殊符號隔開，營造手寫筆記標籤感！
            # 例如：[ #全腦功能成像 ]   [ #時間解析度 ]   [ #非線性正規化 ]
            tag_string = ""
            for tag in tags:
                tag_string += f" [ #{tag} ]    "
            
            # 將串接好的完整標籤文字塞進文字框
            tag_box.insert("1.0", tag_string)
            
            # 💡 重要防呆：將文字框設定為「唯讀」，這樣使用者就不能點進去亂刪改 AI 的標籤了
            tag_box.configure(state="disabled")


if __name__ == "__main__":
    app = PaperMindAICanvas()
    app.mainloop()