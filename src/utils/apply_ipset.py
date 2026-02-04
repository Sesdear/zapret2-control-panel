import os
import requests


class ApplyIpset:
    @staticmethod
    def requires_root() -> bool:
        return os.geteuid() != 0
    
    @staticmethod
    def apply_ipset(ipset_name: str) -> bool:
        URL: str = f"https://raw.githubusercontent.com/Sesdear/zapret2-cp-cfgs/refs/heads/main/ipsets/{ipset_name}"
        STRATEGY_FILE = "/opt/zapret2/ipset/zapret-hosts-user.txt"
        
        try:
            response = requests.get(URL)
            response.raise_for_status()
            
            with open(STRATEGY_FILE, 'w') as file:
                file.write(response.text)
            
            return True
        except requests.RequestException as e:
            print(f"Error fetching strategy '{ipset_name}': {e}")
            return False
        except IOError as e:
            print(f"Error writing strategy to file: {e}")
            return False