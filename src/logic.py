import httpx
import sys
import os
from datetime import datetime

class GarbageLogic:
    def __init__(self):
        # 台北市垃圾車即時位置 API (臺北市政府資料開放平台)
        self.tp_realtime_url = "https://data.taipei/api/v1/dataset/f8146764-67d7-4001-92b0-8192b0c4109f?scope=resourceAquire"
        # 台北市垃圾清運點 API (經緯度、時間)
        self.tp_stations_url = "https://data.taipei/api/v1/dataset/800c978b-3046-4444-8b6b-3f0e03e7c7a1?scope=resourceAquire"
        
    async def fetch_json(self, url: str):
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(url)
                response.raise_for_status()
                return response.json()
        except Exception as e:
            print(f"Error fetching data: {e}", file=sys.stderr)
            return None

    async def get_tp_realtime(self, car_number: str = None):
        """獲取台北市垃圾車即時位置"""
        data = await self.fetch_json(self.tp_realtime_url)
        if not data or "result" not in data or "results" not in data["result"]:
            return {"error": "無法獲取即時資料"}
        
        results = data["result"]["results"]
        if car_number:
            filtered = [r for r in results if car_number.upper() in r.get("car", "")]
            return filtered
        return results[:50]  # 回傳前50筆避免過大

    async def get_tp_stations(self, district: str = None, keyword: str = None):
        """搜尋台北市清運點資料"""
        data = await self.fetch_json(self.tp_stations_url)
        if not data or "result" not in data or "results" not in data["result"]:
            return {"error": "無法獲取清運點資料"}
            
        results = data["result"]["results"]
        filtered = results
        
        if district:
            filtered = [r for r in filtered if district in r.get("行政區", "")]
        if keyword:
            filtered = [r for r in filtered if keyword in str(r.values())]
            
        return filtered[:30]

    def format_car_info(self, car):
        """格式化單輛車資訊"""
        return f"車號: {car.get('car')}\n經緯度: {car.get('x')}, {car.get('y')}\n更新時間: {car.get('updateTime')}"
