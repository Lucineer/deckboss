"""Model management — loading, unloading, selection."""
import subprocess
import os
from .config import get_api_key

def check_ollama() -> bool:
    """Check if ollama is installed and running."""
    try:
        result = subprocess.run(["ollama", "list"], capture_output=True, text=True, timeout=5)
        return result.returncode == 0
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False

def check_vllm() -> bool:
    """Check if vllm is importable."""
    try:
        import vllm
        return True
    except ImportError:
        return False

def ollama_pull(model_name: str):
    """Pull a model with ollama."""
    subprocess.run(["ollama", "pull", model_name], check=True)

def list_ollama_models() -> list:
    """List available ollama models."""
    try:
        result = subprocess.run(["ollama", "list"], capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            lines = result.stdout.strip().split("\n")[1:]  # Skip header
            return [line.split()[0] for line in lines if line.strip()]
    except: pass
    return []

def generate_response(config: dict, model_cfg: dict, messages: list) -> str:
    """Generate a response using the configured model."""
    engine = model_cfg.get("engine", "cloud")
    source = model_cfg.get("source", "cloud")
    
    if source == "local" and engine == "ollama":
        return _ollama_generate(model_cfg["model"], messages)
    elif source == "cloud":
        return _cloud_generate(config, model_cfg, messages)
    else:
        return f"Model engine '{engine}' source '{source}' not yet implemented. Use ollama or cloud."

def _ollama_generate(model: str, messages: list) -> str:
    """Generate using local ollama."""
    import json
    prompt = "\n".join(f"{'User' if m['role']=='user' else 'Assistant'}: {m['content']}" for m in messages[-6:])
    prompt += "\nAssistant: "
    
    try:
        result = subprocess.run(
            ["ollama", "run", model, prompt],
            capture_output=True, text=True, timeout=120
        )
        return result.stdout.strip() if result.returncode == 0 else f"Ollama error: {result.stderr[:200]}"
    except subprocess.TimeoutExpired:
        return "Model generation timed out (120s). Try a smaller model or shorter prompt."
    except Exception as e:
        return f"Ollama error: {e}"

def _cloud_generate(config: dict, model_cfg: dict, messages: list) -> str:
    """Generate using cloud API (DeepSeek, z.ai, DeepInfra, SiliconFlow)."""
    import json
    import urllib.request
    
    provider = model_cfg.get("provider", "deepseek")
    env_var = model_cfg.get("api_key_env", "")
    api_key = get_api_key(config, env_var)
    
    if not api_key:
        return f"No API key found for {provider}. Set {env_var} in your secrets or environment."
    
    # Provider endpoints
    endpoints = {
        "deepseek": ("https://api.deepseek.com/v1/chat/completions", model_cfg.get("model", "deepseek-chat")),
        "zai": ("https://open.bigmodel.cn/api/paas/v4/chat/completions", model_cfg.get("model", "glm-4-flash")),
        "deepinfra": ("https://api.deepinfra.com/v1/chat/completions", model_cfg.get("model", "Qwen/Qwen3-32B")),
        "siliconflow": ("https://api.siliconflow.com/v1/chat/completions", model_cfg.get("model", "deepseek-ai/DeepSeek-V3")),
    }
    
    if provider not in endpoints:
        return f"Unknown cloud provider: {provider}"
    
    endpoint, model = endpoints[provider]
    
    body = json.dumps({
        "model": model,
        "messages": [{"role": m["role"], "content": m["content"]} for m in messages[-10:]],
        "temperature": 0.7,
        "max_tokens": 2048,
    }).encode()
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    
    try:
        req = urllib.request.Request(endpoint, data=body, headers=headers)
        with urllib.request.urlopen(req, timeout=60) as r:
            data = json.loads(r.read())
            return data["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Cloud API error ({provider}): {e}"
