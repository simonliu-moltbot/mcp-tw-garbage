# MCP Taiwan Garbage Truck (台北市垃圾車即時資訊)

一個提供台北市垃圾車即時位置與清運點查詢的 MCP Server。

## 功能
- `get_tp_realtime_location`: 查詢台北市垃圾車目前即時位置。
- `search_tp_garbage_stations`: 查詢台北市各行政區的清運點時間與地址。

## 安裝

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 設定

### Dive
- **Type**: `stdio`
- **Command**: `[YOUR_PYTHON_PATH]`
- **Args**: `[PROJECT_PATH]/src/server.py`
