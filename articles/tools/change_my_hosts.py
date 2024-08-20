# 修改本机hosts文件，追加github ip地址
# 执行本文件：sudo python3 change_my_hosts.py
import requests


def download_hosts(url):
    """Download the latest hosts file."""
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    return None


def parse_hosts(hosts_text):
    """Parse the hosts text to a dict."""
    hosts_dict = {}
    for line in hosts_text.split('\n'):
        if not line.strip().startswith('#') and line.strip():
            parts = line.split()
            ip = parts[0]
            domains = parts[1:]
            for domain in domains:
                hosts_dict[domain] = ip
    return hosts_dict


def update_local_hosts(hosts_dict):
    """Update the local hosts file."""
    local_hosts_path = '/etc/hosts'  # or 'C:\\Windows\\System32\\drivers\\etc\\hosts' on Windows
    with open(local_hosts_path, 'r') as file:
        lines = file.readlines()

    new_lines = []
    # 存储原本文档
    for line in lines:
        new_lines.append(line)

    # 只去了域名+ip重复，但是没有去除域名相同、ip不同的情况
    for domain in hosts_dict:
        line = f"{hosts_dict[domain]}\t{domain}\n"
        # if [domain in parts for item in new_lines for parts in item.split()]
        if line not in new_lines:
            new_lines.append(line)

    for line in new_lines:
        print(f'{line}')

    with open(local_hosts_path, 'w') as file:
        file.writelines(new_lines)


# Example usage
update_url = 'https://raw.hellogithub.com/hosts'
latest_hosts = download_hosts(update_url)
hosts_dict = parse_hosts(latest_hosts)
update_local_hosts(hosts_dict)
