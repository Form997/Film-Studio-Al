"""Cổng ComfyUI tùy chọn. Không chứa mã nguồn của ComfyUI."""
from __future__ import annotations

import os
import uuid
import httpx


def configured_url() -> str:
    url = os.getenv("COMFYUI_URL", "http://127.0.0.1:8188").rstrip("/")
    if not (url.startswith("http://127.0.0.1:") or url.startswith("http://localhost:")):
        raise ValueError("V0.2 chỉ hỗ trợ ComfyUI loopback để giảm rủi ro SSRF")
    return url


async def submit_workflow(workflow: dict) -> dict:
    """Workflow API do chủ dự án tự cấu hình; không tự tạo video nếu chưa cài model."""
    if not isinstance(workflow, dict) or not workflow:
        raise ValueError("Workflow không hợp lệ")
    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.post(configured_url() + "/prompt", json={"prompt": workflow, "client_id": str(uuid.uuid4())})
        response.raise_for_status()
        return response.json()


async def get_history(prompt_id: str) -> dict:
    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.get(configured_url() + "/history/" + str(uuid.UUID(prompt_id)))
        response.raise_for_status()
        return response.json()
