"""Onboarding wizard — first-run configuration."""
import os
import sys
import yaml

CONFIG_DIR = os.path.expanduser("~/.deckboss")
CHARACTER_PATH = os.path.join(CONFIG_DIR, "character.yaml")

def needs_onboarding() -> bool:
    return not os.path.exists(CHARACTER_PATH)

def _prompt(text, default=""):
    if default:
        result = input(f"  {text} [{default}]: ").strip()
        return result if result else default
    return input(f"  {text}: ").strip()

def _prompt_bool(text, default=False):
    hint = "Y/n" if default else "y/N"
    result = input(f"  {text} ({hint}): ").strip().lower()
    if not result:
        return default
    return result in ("y", "yes")

def _detect_hardware():
    """Detect connected hardware."""
    hw = {"device": "unknown", "ram_gb": 0, "vram_gb": 0, "detected": {}}
    
    # Detect device type
    if os.path.exists("/etc/nv_tegra_release"):
        hw["device"] = "Jetson (Tegra)"
        try:
            with open("/etc/nv_tegra_release") as f:
                for line in f:
                    if "BOARD" in line:
                        hw["device"] = f"Jetson {line.split('=')[1].strip()}"
                        break
        except: pass
    elif os.path.exists("/proc/device-tree/model"):
        try:
            with open("/proc/device-tree/model") as f:
                model = f.read().strip("\x00")
                if "Raspberry Pi" in model:
                    hw["device"] = model
        except: pass
    else:
        hw["device"] = "Generic Linux"
    
    # RAM
    try:
        with open("/proc/meminfo") as f:
            for line in f:
                if line.startswith("MemTotal"):
                    kb = int(line.split()[1])
                    hw["ram_gb"] = round(kb / 1024 / 1024, 1)
                    break
    except: pass
    
    # VRAM (NVIDIA)
    if os.path.exists("/proc/driver/nvidia/gpus"):
        try:
            import subprocess
            result = subprocess.run(["nvidia-smi", "--query-gpu=memory.total", "--format=csv,noheader"],
                capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                mb = int(result.stdout.strip().split()[0])
                hw["vram_gb"] = round(mb / 1024, 1)
        except: pass
    
    # Storage
    if os.path.exists("/mnt/nvme"):
        hw["storage"] = "/mnt/nvme"
    else:
        hw["storage"] = os.path.expanduser("~/.deckboss")
    
    # CSI cameras
    csi_count = 0
    for dev in os.listdir("/dev"):
        if dev.startswith("video"):
            csi_count += 1
    if csi_count > 0:
        hw["detected"]["cameras"] = csi_count
    
    # USB audio
    if os.path.exists("/dev/snd"):
        hw["detected"]["audio"] = True
    
    # GPIO (RPi)
    if os.path.exists("/sys/class/gpio"):
        hw["detected"]["gpio"] = True
    
    return hw

def run_onboarding():
    print("")
    print("╔══════════════════════════════════════════════╗")
    print("║          Deckboss — First Run Setup         ║")
    print("╚══════════════════════════════════════════════╝")
    print("")
    
    # 1. Hardware detection
    print("Step 1/6: Hardware Detection")
    print("  Scanning your system...")
    hw = _detect_hardware()
    print(f"  Device: {hw['device']}")
    print(f"  RAM: {hw['ram_gb']} GB")
    if hw['vram_gb']:
        print(f"  VRAM: {hw['vram_gb']} GB (shared)")
    print(f"  Storage: {hw['storage']}")
    if hw['detected']:
        for k, v in hw['detected'].items():
            print(f"  Detected: {k} = {v}")
    print("")
    
    # 2. Model engine
    print("Step 2/6: Local Model Engine")
    print("  ollama = serial single-model use (recommended, lighter)")
    print("  vllm  = parallel/swarm inference (more powerful, more RAM)")
    engine = _prompt("  Choose model engine", "ollama")
    print("")
    
    # 3. API keys
    print("Step 3/6: Cloud API Keys (optional — press Enter to skip)")
    api_keys = {}
    for name, env_var in [("DeepSeek", "DEEPSEEK_API_KEY"), ("z.ai", "ZAI_API_KEY"),
                           ("DeepInfra", "DEEPINFRA_API_KEY"), ("SiliconFlow", "SILICONFLOW_API_KEY")]:
        key = _prompt(f"  {name} API key")
        if key:
            api_keys[env_var] = key
    print(f"  Configured {len(api_keys)} cloud provider(s)")
    print("")
    
    # 4. I/O setup
    print("Step 4/6: Input/Output")
    print("  How will you interact with Deckboss?")
    
    io_primary = "terminal"
    io_secondary = []
    
    if _prompt_bool("  Enable LAN API (HTTP endpoint on local network)?"):
        port = _prompt("  LAN API port", "8080")
        io_secondary.append({"type": "lan_api", "port": int(port)})
    
    if _prompt_bool("  Enable Telegram bot?"):
        io_secondary.append({"type": "telegram", "bot_token_env": "TELEGRAM_BOT_TOKEN"})
    
    if _prompt_bool("  Enable Discord bot?"):
        io_secondary.append({"type": "discord", "bot_token_env": "DISCORD_BOT_TOKEN"})
    
    stt_setup = None
    if hw["detected"].get("audio") or _prompt_bool("  Set up local STT (speech-to-text)?"):
        stt_setup = {"engine": "whisper", "model": "medium", "source": "local"}
    
    tts_setup = None
    if _prompt_bool("  Set up local TTS (text-to-speech)?"):
        tts_setup = {"engine": "piper", "model": "en_US-lessac-medium", "source": "local"}
    
    print("")
    
    # 5. Profile
    print("Step 5/6: Agent Profile")
    print("  Profiles are curated collections of git-agent repos.")
    print("  lucineer/marine — IoT in marine environments, local-first edge")
    print("  (more profiles available after adding profile sources)")
    profile = _prompt("  Select profile", "lucineer/marine")
    
    role = _prompt("  Your role", "system-designer")
    # Common roles
    print("  Common roles: system-designer, robotics-operator, content-creator, ideation")
    print("")
    
    # 6. Character sheet
    print("Step 6/6: Generating Character Sheet")
    
    # Determine resource plan
    available_vram = hw["vram_gb"] or 0
    shared_overhead = 2.0  # OS + Python overhead in GB
    
    if engine == "vllm":
        pipeline = "parallel"
        max_model = max(1, (available_vram - shared_overhead) / 2)
    else:
        pipeline = "serial"
        max_model = max(1, available_vram - shared_overhead)
    
    # Determine model choices
    primary_model = "phi3:mini" if engine == "ollama" else "Qwen/Qwen2.5-7B-Instruct"
    
    character = {
        "version": "0.1.0",
        "hardware": hw,
        "resource_plan": {
            "model_engine": engine,
            "max_gpu_model_size_gb": round(max_model, 1),
            "pipeline_mode": pipeline,
        },
        "models": {
            "primary": {
                "engine": engine,
                "source": "local",
                "model": primary_model,
                "context": 4096,
                "priority": 1,
            },
        },
    }
    
    if stt_setup:
        character["models"]["stt"] = {**stt_setup, "priority": 3}
    if tts_setup:
        character["models"]["tts"] = {**tts_setup, "priority": 5}
    
    # Add cloud models if keys provided
    if "DEEPSEEK_API_KEY" in api_keys:
        character["models"]["reasoning"] = {
            "engine": "cloud", "provider": "deepseek",
            "model": "deepseek-reasoner", "api_key_env": "DEEPSEEK_API_KEY",
            "priority": 2,
        }
    if "ZAI_API_KEY" in api_keys:
        character["models"]["fast"] = {
            "engine": "cloud", "provider": "zai",
            "model": "glm-5-turbo", "api_key_env": "ZAI_API_KEY",
            "priority": 2,
        }
    
    character["io"] = {
        "primary": io_primary,
        "secondary": io_secondary,
    }
    character["profile"] = profile
    character["role"] = role
    character["agents_path"] = os.path.join(CONFIG_DIR, "agents")
    character["logs_path"] = os.path.join(CONFIG_DIR, "logs")
    
    # Write character sheet
    os.makedirs(CONFIG_DIR, exist_ok=True)
    with open(CHARACTER_PATH, "w") as f:
        yaml.dump(character, f, default_flow_style=False)
    
    # Write API keys to secrets file (not in character sheet)
    if api_keys:
        secrets_path = os.path.join(CONFIG_DIR, "secrets.yaml")
        with open(secrets_path, "w") as f:
            yaml.dump({"api_keys": api_keys}, f, default_flow_style=False)
        os.chmod(secrets_path, 0o600)
    
    print(f"  Character sheet written to {CHARACTER_PATH}")
    print("")
    print("Setup complete! Run: deckboss")
    print("")
