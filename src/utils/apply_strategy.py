import os
import requests


class ApplyStrategy:
    @staticmethod
    def requires_root() -> bool:
        return os.geteuid() != 0
    
    @staticmethod
    def apply_strategy(strategy_name: str) -> bool:
        URL: str = f"https://raw.githubusercontent.com/Sesdear/zapret2-cp-cfgs/refs/heads/main/{strategy_name}"
        STRATEGY_FILE = "/opt/zapret2/config"
        
        try:
            response = requests.get(URL)
            response.raise_for_status()
            
            with open(STRATEGY_FILE, 'w') as file:
                file.write(response.text)
            
            return True
        except requests.RequestException as e:
            print(f"Error fetching strategy '{strategy_name}': {e}")
            return False
        except IOError as e:
            print(f"Error writing strategy to file: {e}")
            return False