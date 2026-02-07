import re
import shlex
import string
from datetime import datetime, timezone

from flask import make_response, request

from .template import render_template


def ping_get():
    """Handle GET request for ping page."""
    html = render_template("Xenon Ping", get_ping_content())
    response = make_response(html)
    return response


def ping_post():
    """Handle POST request for ping page with command injection simulation."""
    target = request.form.get("target", "").strip()
    error_html = ""
    result_html = ""
    if not target:
        error_html = """
        <div class='alert-error'>
            <strong>Error:</strong> Target address required
        </div>
        """
    else:
        result = simulate_ping_command(target)
        result_html = f"""
        <div class='alert-info'>
            <strong>Command Output:</strong>
            <pre style='padding:12px; margin:8px 0; border-radius:4px; font-family:monospace; white-space:pre-wrap;'>{result}</pre>
        </div>
        """
    html = render_template("Xenon Ping", get_ping_content() + error_html + result_html)
    response = make_response(html)
    return response


def simulate_ping_command(target):
    """Simulate ping command execution with potential command injection."""
    # Check for command injection (semicolon, pipe, ampersand, etc.)
    injection_chars = [";", "|", "&", "&&", "||", "`", "$", "$("]
    has_injection = any(char in target for char in injection_chars)

    if has_injection:
        # Split the target to get IP and injected command using all injection operators
        # Handles multi-character operators like '&&' and '||' as well as single-character ones
        injection_pattern = r"(;|\|\||&&|\||&|`|\$|\$\()"
        parts = re.split(injection_pattern, target, 1)
        ip_part = parts[0].strip()
        if len(parts) > 2:
            # parts[1] is the matched operator, parts[2] is the rest
            injected_part = parts[2].strip()
        elif len(parts) > 1:
            injected_part = parts[1].strip()
        else:
            injected_part = ""

        # Handle the IP part first
        if ip_part:
            if is_valid_ipv4(ip_part):
                ping_output = generate_ping_output(ip_part)
            elif is_ipv6(ip_part):
                ping_output = "ping: connect: Network is unreachable"
            elif is_domain_name(ip_part):
                ping_output = "ping: Temporary failure in name resolution"
            else:
                ping_output = "ping: usage error: Destination address required"
        else:
            ping_output = "ping: usage error: Destination address required"

        # Handle the injected command
        injected_output = ""
        if injected_part:
            injected_output = simulate_command_output(injected_part)

        # Combine outputs
        if injected_output:
            return f"{ping_output}\n{injected_output}"
        else:
            return ping_output
    else:
        # No injection, handle as normal ping
        if is_valid_ipv4(target):
            return generate_ping_output(target)
        elif is_ipv6(target):
            return "ping: connect: Network is unreachable"
        elif is_domain_name(target):
            return "ping: Temporary failure in name resolution"
        else:
            return "ping: usage error: Destination address required"


def is_valid_ipv4(ip):
    """Check if the string is a valid IPv4 address."""
    pattern = r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"
    return re.match(pattern, ip) is not None


def is_ipv6(ip):
    """Check if the string looks like an IPv6 address."""
    return ":" in ip and len(ip.split(":")) >= 3


def is_domain_name(target):
    """Check if the string looks like a domain name."""
    # Simple check for domain-like strings
    # Must have at least one dot, and should look like a real domain
    if "." not in target or is_valid_ipv4(target) or is_ipv6(target):
        return False

    # Check if it looks like a domain (letters, numbers, dots, hyphens)
    valid_chars = string.ascii_letters + string.digits + ".-"
    if not all(c in valid_chars for c in target):
        return False

    # Must not start or end with dot or hyphen
    if (
        target.startswith(".")
        or target.endswith(".")
        or target.startswith("-")
        or target.endswith("-")
    ):
        return False

    # Split by dots and check each part
    parts = target.split(".")
    if len(parts) < 2:
        return False

    # Check if it looks like a realistic domain name
    # The TLD (last part) should be at least 2 characters and all letters
    tld = parts[-1]
    if len(tld) < 2 or not tld.isalpha():
        return False

    # At least one part should have more than one character
    if all(len(part) == 1 for part in parts):
        return False

    for part in parts:
        if not part or part.startswith("-") or part.endswith("-"):
            return False
        # Each part should contain only letters, numbers, or hyphens
        if not all(c.isalnum() or c == "-" for c in part):
            return False

    return True


def generate_ping_output(ip):
    """Generate realistic ping output for a given IP address."""
    return f"""PING {ip} ({ip}) 56(84) bytes of data.
64 bytes from {ip}: icmp_seq=1 ttl=64 time=0.036 ms

--- {ip} ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 0.036/0.036/0.036/0.000 ms"""


def simulate_command_output(command):
    """Simulate output for common commands used in command injection."""
    command = command.strip()

    # Common command outputs
    if command == "id":
        return "uid=0(root) gid=0(root) groups=0(root)"
    elif command == "whoami":
        return "root"
    elif command == "pwd":
        return "/home/xenon"
    elif command.startswith("cat /etc/passwd"):
        return """root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
bin:x:2:2:bin:/bin:/usr/sbin/nologin
sys:x:3:3:sys:/dev:/usr/sbin/nologin
sync:x:4:65534:sync:/bin:/bin/sync
games:x:5:60:games:/usr/games:/usr/sbin/nologin
man:x:6:12:man:/var/cache/man:/usr/sbin/nologin
lp:x:7:7:lp:/var/spool/lpd:/usr/sbin/nologin
mail:x:8:8:mail:/var/mail:/usr/sbin/nologin
news:x:9:9:news:/var/spool/news:/usr/sbin/nologin
xenon:x:1000:1000:Xenon User,,,:/home/xenon:/bin/bash"""
    elif command.startswith("ls"):
        # NOTE: In a real application, using shlex.split() on user input is unsafe and can introduce security risks.
        # Here, it is used intentionally for educational simulation of command parsing and injection.
        parts = shlex.split(command)
        args = parts[1:]
        # Find first non-flag argument as directory
        dir_arg = None
        for arg in args:
            if arg.startswith("-"):
                continue
            dir_arg = arg
            break
        if dir_arg is not None:
            # Simulate plausible output for known home dir, else generic empty
            if dir_arg in ["./app", "app", "/app"]:
                return "total 0"
            elif dir_arg in [".", "./", "~", "/home/xenon", "/root", "/"]:
                # Home/root dirs: show normal listing
                return (
                    "total 24\n"
                    "drwxr-xr-x 3 xenon xenon 4096 Dec 10 14:32 .\n"
                    "drwxr-xr-x 3 root  root  4096 Dec 10 14:30 ..\n"
                    "-rw-r--r-- 1 xenon xenon  220 Dec 10 14:30 .bash_logout\n"
                    "-rw-r--r-- 1 xenon xenon 3771 Dec 10 14:30 .bashrc\n"
                    "-rw-r--r-- 1 xenon xenon  807 Dec 10 14:30 .profile\n"
                    "drwxr-xr-x 2 xenon xenon 4096 Dec 10 14:32 app"
                )
            else:
                # Any other directory: plausible empty
                return f"ls: cannot access '{dir_arg}': No such file or directory"
        # No directory arg: show home dir listing
        return (
            "total 24\n"
            "drwxr-xr-x 3 xenon xenon 4096 Dec 10 14:32 .\n"
            "drwxr-xr-x 3 root  root  4096 Dec 10 14:30 ..\n"
            "-rw-r--r-- 1 xenon xenon  220 Dec 10 14:30 .bash_logout\n"
            "-rw-r--r-- 1 xenon xenon 3771 Dec 10 14:30 .bashrc\n"
            "-rw-r--r-- 1 xenon xenon  807 Dec 10 14:30 .profile\n"
            "drwxr-xr-x 2 xenon xenon 4096 Dec 10 14:32 app"
        )
    elif command == "uname -a":
        return "Linux xenon-server 5.15.0-89-generic #99-Ubuntu SMP Mon Oct 30 20:42:41 UTC 2023 x86_64 x86_64 x86_64 GNU/Linux"
    elif command == "ps aux" or command == "ps":
        return """USER         PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
root           1  0.0  0.1 168568  2832 ?        Ss   14:30   0:01 /sbin/init
root          89  0.0  0.1  25892  3012 ?        Ss   14:30   0:00 /lib/systemd/systemd-udevd
xenon        1001  0.1  0.5  76320 10240 ?        S    14:32   0:00 python3 app.py
xenon        1015  0.0  0.1  17504  2048 pts/0    R+   14:35   0:00 ps aux"""
    elif command.startswith("cat") and "/etc/" in command:
        return f"cat: {command.split()[-1]}: Permission denied"
    elif command.startswith("cat") and "flag" in command.lower():
        return "flag{this_is_a_simulated_flag_not_real}"
    elif command == "env" or command == "printenv":
        return """PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
HOME=/home/xenon
USER=xenon
SHELL=/bin/bash
PWD=/home/xenon/app
FLASK_APP=app.py
FLASK_ENV=development"""
    elif command.startswith("echo"):
        # Extract the text after echo
        echo_text = command[4:].strip()
        if echo_text.startswith('"') and echo_text.endswith('"'):
            echo_text = echo_text[1:-1]
        elif echo_text.startswith("'") and echo_text.endswith("'"):
            echo_text = echo_text[1:-1]
        return echo_text
    elif command == "date":
        now = datetime.now(timezone.utc)
        # Format: Mon Dec 11 14:35:42 UTC 2023
        return now.strftime("%a %b %d %H:%M:%S UTC %Y")
    else:
        # For unknown commands, simulate command not found
        return (
            f"{command.split()[0] if command.split() else command}: command not found"
        )


def get_ping_content():
    """Return the content HTML for the ping page (excluding header/footer)."""
    return """
    <div style="margin-bottom:10px;"><a href="/" class="back-link">&larr; Back to Home</a></div>
    <h1>Ping Tool</h1>
    <div class="ping-desc">
        Test network connectivity by pinging an IPv4 address.<br /><br />
        Enter an IPv4 address (e.g., 127.0.0.1, 8.8.8.8) to test connectivity.
    </div>
    <form method="post" action="/ping">
        <input type="text" name="target" placeholder="Enter IPv4 address..." required />
        <button type="submit">Ping</button>
    </form>
    """
