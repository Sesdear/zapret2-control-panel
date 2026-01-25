import requests
import json

class ConfigsList:
    CONFIGS_URL = "https://raw.githubusercontent.com/Sesdear/zapret2-cp-cfgs/refs/heads/main/list.json"
    
    @staticmethod
    def fetch_configs() -> list:
        try:
            response = requests.get(ConfigsList.CONFIGS_URL)
            response.raise_for_status()
            raw_configs = response.json()
            configs = raw_configs.get("configs", [])
            return configs
        except requests.RequestException as e:
            print(f"Error fetching configurations: {e}")
            return []

if __name__ == "__main__":
    configs = ConfigsList.fetch_configs()
    for config in configs:
        print(f"{config}")