import socket
import ipaddress
import concurrent.futures
import argparse
from datetime import datetime
import json
from typing import List, Dict, Union, Optional
import time

def print_banner():
    """Print the stylized application banner with colors and version info."""
    # ANSI color codes
    BLUE = '\033[94m'
    YELLOW = '\033[93m'
    RESET = '\033[0m'
    
    version = "v1.0.0"
    release_date = "December 2024"
    
    banner = f"""{BLUE}
█▄░█ █▀▀ ▀█▀ █▀ █▀▀ █▀█ █▀█ █▀▀             Author: Jairo Morales Pérez{RESET}
{YELLOW}█░▀█ ██▄ ░█░ ▄█ █▄▄ █▄█ █▀▀ ██▄             Version: {version} ({release_date}){RESET}
    """
    print(banner)
    time.sleep(1)  # Add a small delay for dramatic effect

class NetworkScanner:
    def __init__(self, target_range: str, common_ports: bool = True):
        """
        Initialize the network scanner.
        
        Args:
            target_range: IP range in CIDR notation (e.g., '192.168.1.0/24')
            common_ports: If True, scan only common ports; if False, scan all ports
        """
        self.target_range = target_range
        self.common_ports = [20, 21, 22, 23, 25, 53, 80, 443, 445, 3389] if common_ports else range(1, 1025)
        self.results: Dict[str, Dict] = {}

    def scan_port(self, ip: str, port: int) -> Optional[Dict]:
        """
        Scan a specific port on an IP address.
        
        Args:
            ip: IP address to scan
            port: Port number to scan
            
        Returns:
            Dictionary containing port information if open, None if closed
        """
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(1)
                result = s.connect_ex((ip, port))
                if result == 0:
                    try:
                        service = socket.getservbyport(port)
                    except OSError:
                        service = "unknown"
                    return {
                        "port": port,
                        "state": "open",
                        "service": service
                    }
        except socket.error:
            pass
        return None

    def scan_host(self, ip: str) -> Dict:
        """
        Scan all specified ports on a host.
        
        Args:
            ip: IP address to scan
            
        Returns:
            Dictionary containing host scan results
        """
        open_ports = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
            future_to_port = {
                executor.submit(self.scan_port, ip, port): port 
                for port in self.common_ports
            }
            for future in concurrent.futures.as_completed(future_to_port):
                result = future.result()
                if result:
                    open_ports.append(result)
        
        return {
            "ip": ip,
            "timestamp": datetime.now().isoformat(),
            "open_ports": open_ports,
            "total_open_ports": len(open_ports)
        }

    def scan_network(self) -> Dict[str, Dict]:
        """
        Scan the entire network range.
        
        Returns:
            Dictionary containing results for all hosts
        """
        try:
            network = ipaddress.ip_network(self.target_range)
            print(f"\nScanning network: {self.target_range}")
            print(f"Time started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

            for ip in network.hosts():
                ip_str = str(ip)
                print(f"Scanning host: {ip_str}")
                host_result = self.scan_host(ip_str)
                if host_result["total_open_ports"] > 0:
                    self.results[ip_str] = host_result
                    self._print_host_results(host_result)

            return self.results

        except ValueError as e:
            print(f"Error: Invalid network range - {e}")
            return {}

    def save_results(self, filename: str) -> None:
        """
        Save scan results to a JSON file.
        
        Args:
            filename: Name of the file to save results to
        """
        with open(filename, 'w') as f:
            json.dump(self.results, f, indent=4)
        print(f"\nResults saved to {filename}")

    def _print_host_results(self, host_result: Dict) -> None:
        """
        Print results for a single host in a formatted way.
        
        Args:
            host_result: Dictionary containing host scan results
        """
        print(f"\nHost: {host_result['ip']}")
        print(f"Open ports: {host_result['total_open_ports']}")
        print("Port details:")
        for port_info in host_result['open_ports']:
            print(f"  {port_info['port']}/tcp - {port_info['service']}")
        print("-" * 50)

def main():
    # Print the banner first
    print_banner()

    parser = argparse.ArgumentParser(description='Network Scanner and Port Analyzer')
    parser.add_argument('target', help='Target network range (CIDR notation, e.g., 192.168.1.0/24)')
    parser.add_argument('--output', '-o', help='Output file for results (JSON format)', default='scan_results.json')
    parser.add_argument('--all-ports', '-a', action='store_true', help='Scan all ports (1-1024) instead of common ports')
    args = parser.parse_args()

    scanner = NetworkScanner(args.target, not args.all_ports)
    scanner.scan_network()
    scanner.save_results(args.output)

if __name__ == "__main__":
    main()