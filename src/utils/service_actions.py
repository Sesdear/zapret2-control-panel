import subprocess
import npyscreen

class ServiceActions:
    @staticmethod
    def check_zapret_service() -> str:
        try:
            result = subprocess.run(
                ['systemctl', 'is-active', 'zapret2.service'], 
                capture_output=True, 
                text=True,
                timeout=5
            )
            return result.stdout.strip()
        except subprocess.TimeoutExpired:
            return "timeout"
        except Exception as e:
            print(f"Error checking service status: {e}")
            return "error"

    @staticmethod
    def toggle_zapret_service() -> str:
        status = ServiceActions.check_zapret_service()

        try:
            if status == "active":
                subprocess.run(
                    ['systemctl', 'stop', 'zapret2.service'],
                    check=True
                )
            else:
                subprocess.run(
                    ['systemctl', 'start', 'zapret2.service'],
                    check=True
                )

            return ServiceActions.check_zapret_service()

        except subprocess.CalledProcessError as e:
            return f"error: {e}"

    
    @staticmethod
    def restart_zapret_service() -> str:
        try:
            subprocess.run(['sudo', 'systemctl', 'restart', 'zapret2.service'], check=True)
            return "restarted"
        except subprocess.CalledProcessError as e:
            return f"Error: {e}"

    @staticmethod
    def check_zapret_auto_start() -> str:
        try:
            result = subprocess.run(
                ['systemctl', 'is-enabled', 'zapret2.service'], 
                capture_output=True, 
                text=True, 
                check=True,
                timeout=5
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError:
            return "disabled"
    
    @staticmethod
    def toggle_zapret_auto_start() -> str:
        status = ServiceActions.check_zapret_auto_start()
        try:
            if status == "enabled":
                subprocess.run(['sudo', 'systemctl', 'disable', 'zapret2.service'], check=True)
                return "disabled"
            else:
                subprocess.run(['sudo', 'systemctl', 'enable', 'zapret2.service'], check=True)
                return "enabled"
        except subprocess.CalledProcessError as e:
            return f"Error: {e}"
