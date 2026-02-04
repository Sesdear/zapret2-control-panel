import requests
import json

class IpsetList:
    IPSETS_URL = "https://raw.githubusercontent.com/Sesdear/zapret2-cp-cfgs/refs/heads/main/ipsets_list.json"
    
    @staticmethod
    def fetch_ipsets() -> list:
        try:
            response = requests.get(IpsetList.IPSETS_URL)
            response.raise_for_status()
            raw_configs = response.json()
            configs = raw_configs.get("ipsets", [])
            return configs
        except requests.RequestException as e:
            print(f"Error fetching configurations: {e}")
            return []

if __name__ == "__main__":
    configs = IpsetList.fetch_ipsets()
    for config in configs:
        print(f"{config}")