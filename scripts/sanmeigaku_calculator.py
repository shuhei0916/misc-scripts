"""
算命学 命式計算スクリプト
生年月日から算命学の命式を計算する
"""

from datetime import datetime, date
from typing import Dict, List, Tuple, Optional
import json

class SanmeigakuCalculator:
    def __init__(self):
        self.kanshi_list = [
            "甲子", "乙丑", "丙寅", "丁卯", "戊辰", "己巳", "庚午", "辛未", "壬申", "癸酉",
            "甲戌", "乙亥", "丙子", "丁丑", "戊寅", "己卯", "庚辰", "辛巳", "壬午", "癸未",
            "甲申", "乙酉", "丙戌", "丁亥", "戊子", "己丑", "庚寅", "辛卯", "壬辰", "癸巳",
            "甲午", "乙未", "丙申", "丁酉", "戊戌", "己亥", "庚子", "辛丑", "壬寅", "癸卯",
            "甲辰", "乙巳", "丙午", "丁未", "戊申", "己酉", "庚戌", "辛亥", "壬子", "癸丑",
            "甲寅", "乙卯", "丙辰", "丁巳", "戊午", "己未", "庚申", "辛酉", "壬戌", "癸亥"
        ]
        self.kanshi_map = {k: i + 1 for i, k in enumerate(self.kanshi_list)}
        self.tenkan = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
        self.chishi = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
        
        self.tenchukill_map = {
            1: "戌亥", 2: "戌亥", 3: "申酉", 4: "申酉", 5: "午未", 6: "午未", 7: "辰巳", 8: "辰巳", 9: "寅卯", 10: "寅卯",
            11: "子丑", 12: "子丑", 13: "戌亥", 14: "戌亥", 15: "申酉", 16: "申酉", 17: "午未", 18: "午未", 19: "辰巳", 20: "辰巳",
            21: "寅卯", 22: "寅卯", 23: "子丑", 24: "子丑", 25: "戌亥", 26: "戌亥", 27: "申酉", 28: "申酉", 29: "午未", 30: "午未",
            31: "辰巳", 32: "辰巳", 33: "寅卯", 34: "寅卯", 35: "子丑", 36: "子丑", 37: "戌亥", 38: "戌亥", 39: "申酉", 40: "申酉",
            41: "午未", 42: "午未", 43: "辰巳", 44: "辰巳", 45: "寅卯", 46: "寅卯", 47: "子丑", 48: "子丑", 49: "戌亥", 50: "戌亥",
            51: "申酉", 52: "申酉", 53: "午未", 54: "午未", 55: "辰巳", 56: "辰巳", 57: "寅卯", 58: "寅卯", 59: "子丑", 60: "子丑"
        }
        
        # 提供された情報に基づいて蔵干表を更新
        self.zoukan_map = {
            "子": ["癸"] * 31,
            "丑": ["癸"] * 10 + ["辛"] * 3 + ["己"] * 18,
            "寅": ["戊"] * 8 + ["丙"] * 7 + ["甲"] * 16,
            "卯": ["乙"] * 31,
            "辰": ["乙"] * 10 + ["癸"] * 3 + ["戊"] * 18,
            "巳": ["戊"] * 6 + ["庚"] * 9 + ["丙"] * 16,
            "午": ["己"] * 13 + ["丁"] * 18,
            "未": ["丁"] * 10 + ["乙"] * 3 + ["己"] * 18,
            "申": ["戊"] * 10 + ["壬"] * 4 + ["庚"] * 17,
            "酉": ["辛"] * 31,
            "戌": ["辛"] * 10 + ["丁"] * 3 + ["戊"] * 18,
            "亥": ["甲"] * 13 + ["壬"] * 18
        }
        
        self.judai_shusei_map = {
            ("甲", "甲"): "貫索星", ("甲", "乙"): "石門星", ("甲", "丙"): "鳳閣星", ("甲", "丁"): "調舒星", ("甲", "戊"): "禄存星",
            ("甲", "己"): "司禄星", ("甲", "庚"): "牽牛星", ("甲", "辛"): "車騎星", ("甲", "壬"): "龍高星", ("甲", "癸"): "玉堂星",
            ("乙", "甲"): "石門星", ("乙", "乙"): "貫索星", ("乙", "丙"): "調舒星", ("乙", "丁"): "鳳閣星", ("乙", "戊"): "司禄星",
            ("乙", "己"): "禄存星", ("乙", "庚"): "車騎星", ("乙", "辛"): "牽牛星", ("乙", "壬"): "玉堂星", ("乙", "癸"): "龍高星",
            ("丙", "甲"): "龍高星", ("丙", "乙"): "玉堂星", ("丙", "丙"): "貫索星", ("丙", "丁"): "石門星", ("丙", "戊"): "鳳閣星",
            ("丙", "己"): "調舒星", ("丙", "庚"): "禄存星", ("丙", "辛"): "司禄星", ("丙", "壬"): "牽牛星", ("丙", "癸"): "車騎星",
            ("丁", "甲"): "玉堂星", ("丁", "乙"): "龍高星", ("丁", "丙"): "石門星", ("丁", "丁"): "貫索星", ("丁", "戊"): "調舒星",
            ("丁", "己"): "鳳閣星", ("丁", "庚"): "司禄星", ("丁", "辛"): "禄存星", ("丁", "壬"): "車騎星", ("丁", "癸"): "牽牛星",
            ("戊", "甲"): "牽牛星", ("戊", "乙"): "車騎星", ("戊", "丙"): "龍高星", ("戊", "丁"): "玉堂星", ("戊", "戊"): "貫索星",
            ("戊", "己"): "石門星", ("戊", "庚"): "鳳閣星", ("戊", "辛"): "調舒星", ("戊", "壬"): "禄存星", ("戊", "癸"): "司禄星",
            ("己", "甲"): "車騎星", ("己", "乙"): "牽牛星", ("己", "丙"): "玉堂星", ("己", "丁"): "龍高星", ("己", "戊"): "石門星",
            ("己", "己"): "貫索星", ("己", "庚"): "調舒星", ("己", "辛"): "鳳閣星", ("己", "壬"): "司禄星", ("己", "癸"): "禄存星",
            ("庚", "甲"): "禄存星", ("庚", "乙"): "司禄星", ("庚", "丙"): "牽牛星", ("庚", "丁"): "車騎星", ("庚", "戊"): "龍高星",
            ("庚", "己"): "玉堂星", ("庚", "庚"): "貫索星", ("庚", "辛"): "石門星", ("庚", "壬"): "鳳閣星", ("庚", "癸"): "調舒星",
            ("辛", "甲"): "司禄星", ("辛", "乙"): "禄存星", ("辛", "丙"): "車騎星", ("辛", "丁"): "牽牛星", ("辛", "戊"): "玉堂星",
            ("辛", "己"): "龍高星", ("辛", "庚"): "石門星", ("辛", "辛"): "貫索星", ("辛", "壬"): "調舒星", ("辛", "癸"): "鳳閣星",
            ("壬", "甲"): "鳳閣星", ("壬", "乙"): "調舒星", ("壬", "丙"): "禄存星", ("壬", "丁"): "司禄星", ("壬", "戊"): "牽牛星",
            ("壬", "己"): "車騎星", ("壬", "庚"): "龍高星", ("壬", "辛"): "玉堂星", ("壬", "壬"): "貫索星", ("壬", "癸"): "石門星",
            ("癸", "甲"): "調舒星", ("癸", "乙"): "鳳閣星", ("癸", "丙"): "司禄星", ("癸", "丁"): "禄存星", ("癸", "戊"): "車騎星",
            ("癸", "己"): "牽牛星", ("癸", "庚"): "玉堂星", ("癸", "辛"): "龍高星", ("癸", "壬"): "石門星", ("癸", "癸"): "貫索星"
        }
        
        self.juni_daijusei_map = {
            ("甲", "子"): "天報星", ("甲", "丑"): "天印星", ("甲", "寅"): "天貴星", ("甲", "卯"): "天恍星", ("甲", "辰"): "天南星", ("甲", "巳"): "天禄星",
            ("甲", "午"): "天将星", ("甲", "未"): "天堂星", ("甲", "申"): "天胡星", ("甲", "酉"): "天極星", ("甲", "戌"): "天庫星", ("甲", "亥"): "天馳星",
            ("乙", "子"): "天極星", ("乙", "丑"): "天庫星", ("乙", "寅"): "天馳星", ("乙", "卯"): "天報星", ("乙", "辰"): "天印星", ("乙", "巳"): "天貴星",
            ("乙", "午"): "天恍星", ("乙", "未"): "天南星", ("乙", "申"): "天禄星", ("乙", "酉"): "天将星", ("乙", "戌"): "天堂星", ("乙", "亥"): "天胡星",
            ("丙", "子"): "天胡星", ("丙", "丑"): "天極星", ("丙", "寅"): "天庫星", ("丙", "卯"): "天馳星", ("丙", "辰"): "天報星", ("丙", "巳"): "天印星",
            ("丙", "午"): "天貴星", ("丙", "未"): "天恍星", ("丙", "申"): "天南星", ("丙", "酉"): "天禄星", ("丙", "戌"): "天将星", ("丙", "亥"): "天堂星",
            ("丁", "子"): "天堂星", ("丁", "丑"): "天胡星", ("丁", "寅"): "天極星", ("丁", "卯"): "天庫星", ("丁", "辰"): "天馳星", ("丁", "巳"): "天報星",
            ("丁", "午"): "天印星", ("丁", "未"): "天貴星", ("丁", "申"): "天恍星", ("丁", "酉"): "天南星", ("丁", "戌"): "天禄星", ("丁", "亥"): "天将星",
            ("戊", "子"): "天報星", ("戊", "丑"): "天印星", ("戊", "寅"): "天貴星", ("戊", "卯"): "天恍星", ("戊", "辰"): "天南星", ("戊", "巳"): "天禄星",
            ("戊", "午"): "天将星", ("戊", "未"): "天堂星", ("戊", "申"): "天胡星", ("戊", "酉"): "天極星", ("戊", "戌"): "天庫星", ("戊", "亥"): "天馳星",
            ("己", "子"): "天極星", ("己", "丑"): "天庫星", ("己", "寅"): "天馳星", ("己", "卯"): "天報星", ("己", "辰"): "天印星", ("己", "巳"): "天貴星",
            ("己", "午"): "天恍星", ("己", "未"): "天南星", ("己", "申"): "天禄星", ("己", "酉"): "天将星", ("己", "戌"): "天堂星", ("己", "亥"): "天胡星",
            ("庚", "子"): "天胡星", ("庚", "丑"): "天極星", ("庚", "寅"): "天庫星", ("庚", "卯"): "天馳星", ("庚", "辰"): "天報星", ("庚", "巳"): "天印星",
            ("庚", "午"): "天貴星", ("庚", "未"): "天恍星", ("庚", "申"): "天南星", ("庚", "酉"): "天禄星", ("庚", "戌"): "天将星", ("庚", "亥"): "天堂星",
            ("辛", "子"): "天堂星", ("辛", "丑"): "天胡星", ("辛", "寅"): "天極星", ("辛", "卯"): "天庫星", ("辛", "辰"): "天馳星", ("辛", "巳"): "天報星",
            ("辛", "午"): "天印星", ("辛", "未"): "天貴星", ("辛", "申"): "天恍星", ("辛", "酉"): "天南星", ("辛", "戌"): "天禄星", ("辛", "亥"): "天将星",
            ("壬", "子"): "天報星", ("壬", "丑"): "天印星", ("壬", "寅"): "天貴星", ("壬", "卯"): "天恍星", ("壬", "辰"): "天南星", ("壬", "巳"): "天禄星",
            ("壬", "午"): "天将星", ("壬", "未"): "天堂星", ("壬", "申"): "天胡星", ("壬", "酉"): "天極星", ("壬", "戌"): "天庫星", ("壬", "亥"): "天馳星",
            ("癸", "子"): "天極星", ("癸", "丑"): "天庫星", ("癸", "寅"): "天馳星", ("癸", "卯"): "天報星", ("癸", "辰"): "天印星", ("癸", "巳"): "天貴星",
            ("癸", "午"): "天恍星", ("癸", "未"): "天南星", ("癸", "申"): "天禄星", ("癸", "酉"): "天将星", ("癸", "戌"): "天堂星", ("癸", "亥"): "天胡星"
        }
        
        self.kangouu_map = {
            "甲": "己", "乙": "庚", "丙": "辛", "丁": "壬", "戊": "癸",
            "己": "甲", "庚": "乙", "辛": "丙", "壬": "丁", "癸": "戊"
        }
        
        self.ijou_kanshi = [11, 12, 18, 23, 24, 25, 30, 35, 36, 37, 41, 42, 48, 54]

        self.getsu_kanshi_map = {
            ("甲", "己"): {2: "丙寅", 3: "丁卯", 4: "戊辰", 5: "己巳", 6: "庚午", 7: "辛未", 8: "壬申", 9: "癸酉", 10: "甲戌", 11: "乙亥", 12: "丙子", 1: "丁丑"},
            ("乙", "庚"): {2: "戊寅", 3: "己卯", 4: "庚辰", 5: "辛巳", 6: "壬午", 7: "癸未", 8: "甲申", 9: "乙酉", 10: "丙戌", 11: "丁亥", 12: "戊子", 1: "己丑"},
            ("丙", "辛"): {2: "庚寅", 3: "辛卯", 4: "壬辰", 5: "癸巳", 6: "甲午", 7: "乙未", 8: "丙申", 9: "丁酉", 10: "戊戌", 11: "己亥", 12: "庚子", 1: "辛丑"},
            ("丁", "壬"): {2: "壬寅", 3: "癸卯", 4: "甲辰", 5: "乙巳", 6: "丙午", 7: "丁未", 8: "戊申", 9: "己酉", 10: "庚戌", 11: "辛亥", 12: "壬子", 1: "癸丑"},
            ("戊", "癸"): {2: "甲寅", 3: "乙卯", 4: "丙辰", 5: "丁巳", 6: "戊午", 7: "己未", 8: "庚申", 9: "辛酉", 10: "壬戌", 11: "癸亥", 12: "甲子", 1: "乙丑"}
        }

    def get_kanshi_info(self, kanshi_num: int) -> Dict[str, str]:
        if kanshi_num < 1 or kanshi_num > 60:
            raise ValueError("干支番号は1-60の範囲で指定してください")
        kanshi = self.kanshi_list[kanshi_num - 1]
        return {"kanshi": kanshi, "tenkan": kanshi[0], "chishi": kanshi[1], "tenchukill": self.tenchukill_map[kanshi_num]}

    def get_nen_kanshi(self, year: int) -> Tuple[int, str, str]:
        tenkan_index = (year - 4) % 10
        chishi_index = (year - 4) % 12
        nen_kan = self.tenkan[tenkan_index]
        nen_shi = self.chishi[chishi_index]
        nen_kanshi_str = nen_kan + nen_shi
        nen_kanshi_num = self.kanshi_map[nen_kanshi_str]
        return nen_kanshi_num, nen_kan, nen_shi

    def get_getsu_kanshi(self, nen_kan: str, month: int) -> int:
        for kan_pair, month_map in self.getsu_kanshi_map.items():
            if nen_kan in kan_pair:
                getsu_kanshi_str = month_map.get(month)
                if getsu_kanshi_str:
                    return self.kanshi_map[getsu_kanshi_str]
        raise ValueError(f"月干支が見つかりません: 年干={nen_kan}, 月={month}")

    def calculate_day_kanshi(self, year: int, month: int, day: int) -> Tuple[int, int, int]:
        base_date = date(1900, 1, 31)
        target_date = date(year, month, day)
        days_diff = (target_date - base_date).days
        day_kanshi_num = (days_diff % 60) + 1
        prev_setsu_days = 8
        next_setsu_days = 22
        return day_kanshi_num, prev_setsu_days, next_setsu_days

    def get_zoukan(self, chishi: str, days_from_setsu: int) -> str:
        zoukan_list = self.zoukan_map.get(chishi)
        if not zoukan_list: raise ValueError(f"不正な地支: {chishi}")
        index = min(days_from_setsu, len(zoukan_list) - 1)
        return zoukan_list[index]

    def get_judai_shusei(self, nikkan: str, target_kan: str) -> str:
        return self.judai_shusei_map.get((nikkan, target_kan), "不明")

    def get_juni_daijusei(self, nikkan: str, target_shi: str) -> str:
        return self.juni_daijusei_map.get((nikkan, target_shi), "不明")

    def calculate_taiun(self, gender: str, year_kanshi_num: int, next_setsu_days: int) -> Tuple[str, int]:
        year_kanshi_info = self.get_kanshi_info(year_kanshi_num)
        is_you_kan = year_kanshi_info["tenkan"] in ["甲", "丙", "戊", "庚", "壬"]
        direction = ("順回り" if gender == "男性" else "逆回り") if is_you_kan else ("逆回り" if gender == "男性" else "順回り")
        saiun = round(next_setsu_days / 3) if direction == "順回り" else round(8 / 3)
        if saiun == 0: saiun = 1
        elif saiun == 11: saiun = 10
        return direction, saiun

    def check_special_destiny(self, insen: Dict) -> Dict[str, bool]:
        special = {}
        special["異常干支"] = any(insen[key]["kanshi_num"] in self.ijou_kanshi for key in ["年", "月", "日"])
        tenchukill = insen["日"]["tenchukill"]
        special["生年天中殺"] = insen["年"]["chishi"] in tenchukill
        special["生月天中殺"] = insen["月"]["chishi"] in tenchukill
        day_kanshi_num = insen["日"]["kanshi_num"]
        special["日座中殺"] = day_kanshi_num in [11, 12]
        special["日居中殺"] = day_kanshi_num in [41, 42]
        return special

    def calculate_meishiki(self, year: int, month: int, day: int, gender: str) -> Dict:
        adj_year, adj_month = (year, month)
        if month == 1 or (month == 2 and day <= 3):
            adj_year -= 1
        
        year_kanshi_num, nen_kan, _ = self.get_nen_kanshi(adj_year)
        month_kanshi_num = self.get_getsu_kanshi(nen_kan, adj_month)
        day_kanshi_num, prev_setsu_days, next_setsu_days = self.calculate_day_kanshi(year, month, day)
        
        year_info = self.get_kanshi_info(year_kanshi_num)
        month_info = self.get_kanshi_info(month_kanshi_num)
        day_info = self.get_kanshi_info(day_kanshi_num)
        
        year_zoukan = self.get_zoukan(year_info["chishi"], prev_setsu_days)
        month_zoukan = self.get_zoukan(month_info["chishi"], prev_setsu_days)
        day_zoukan = self.get_zoukan(day_info["chishi"], prev_setsu_days)
        
        insen = {
            "年": {"kanshi_num": year_kanshi_num, "tenkan": year_info["tenkan"], "chishi": year_info["chishi"], "zoukan": year_zoukan},
            "月": {"kanshi_num": month_kanshi_num, "tenkan": month_info["tenkan"], "chishi": month_info["chishi"], "zoukan": month_zoukan},
            "日": {"kanshi_num": day_kanshi_num, "tenkan": day_info["tenkan"], "chishi": day_info["chishi"], "zoukan": day_zoukan, "tenchukill": day_info["tenchukill"]}
        }
        
        nikkan = insen["日"]["tenkan"]
        judai_shusei = {
            "頭": self.get_judai_shusei(nikkan, insen["年"]["tenkan"]), "右手": self.get_judai_shusei(nikkan, insen["日"]["zoukan"]),
            "胸": self.get_judai_shusei(nikkan, insen["月"]["zoukan"]), "左手": self.get_judai_shusei(nikkan, insen["年"]["zoukan"]),
            "腹": self.get_judai_shusei(nikkan, insen["月"]["tenkan"]), "右肩": self.get_judai_shusei(nikkan, self.kangouu_map.get(insen["年"]["tenkan"], ""))
        }
        juni_daijusei = {
            "左肩": self.get_juni_daijusei(nikkan, insen["年"]["chishi"]), "左足": self.get_juni_daijusei(nikkan, insen["日"]["chishi"]),
            "右足": self.get_juni_daijusei(nikkan, insen["月"]["chishi"])
        }
        yosen = {"十大主星": judai_shusei, "十二大従星": juni_daijusei}
        
        taiun_direction, taiun_saiun = self.calculate_taiun(gender, year_kanshi_num, next_setsu_days)
        special_destiny = self.check_special_destiny(insen)
        
        return {
            "陰占": insen, "陽占": yosen,
            "大運": {"方向": taiun_direction, "歳運": taiun_saiun},
            "特殊性": special_destiny
        }

def run_tests():
    calculator = SanmeigakuCalculator()
    try:
        with open('data/sanmeigaku_test_cases.json', 'r', encoding='utf-8') as f:
            test_cases = json.load(f)
    except FileNotFoundError:
        print("Error: data/sanmeigaku_test_cases.json not found.")
        return

    print("Running tests...")
    passed_count = 0
    failed_count = 0

    for i, case in enumerate(test_cases):
        print(f"\n--- Test Case {i+1} ---")
        inputs = case["input"]
        expected = case["expected_yosen"]
        print(f"Input: {inputs['year']}/{inputs['month']}/{inputs['day']} ({inputs['gender']})")
        
        calculated_meishiki = calculator.calculate_meishiki(inputs["year"], inputs["month"], inputs["day"], inputs["gender"])
        calculated_yosen = {**calculated_meishiki["陽占"]["十大主星"], **calculated_meishiki["陽占"]["十二大従星"]}
        
        is_match = True
        mismatched_items = {}
        key_map = {"頭": "頭", "胸": "胸", "腹": "腹", "右手": "右手", "左手": "左手", "左肩": "左肩", "右足": "右足", "左足": "左足"}

        for web_key, calc_key in key_map.items():
            expected_star = expected.get(web_key)
            calculated_star = calculated_yosen.get(calc_key)
            if expected_star != calculated_star:
                is_match = False
                mismatched_items[web_key] = {"expected": expected_star, "calculated": calculated_star}

        if is_match:
            print("Result: PASSED")
            passed_count += 1
        else:
            print("Result: FAILED")
            failed_count += 1
            print("Mismatched items:")
            for key, values in mismatched_items.items():
                print(f"  - {key}: Expected '{values['expected']}', but got '{values['calculated']}'")

    print("\n--- Test Summary ---")
    print(f"Total cases: {len(test_cases)}")
    print(f"Passed: {passed_count}")
    print(f"Failed: {failed_count}")
    if failed_count > 0:
        print("\nNote: Failures may still occur due to simplified logic for setsuiri (節入り).")

if __name__ == '__main__':
    run_tests()
