# Xenon

Welcome to Xenon, a test service designed to simulate vulnerabilities in a safe and controlled environment. This application is used for testing security scanners and tools with realistic, but non-exploitable, responses.

> [!NOTE]
> All vulnerabilities in this service are simulated. No real security risks exist, and no sensitive data is present. Use this system for safe, realistic security testing and training.

This project was created to aid in the testing of [yawast-ng](https://github.com/adcaudill/yawast-ng), a security scanner for web applications. By providing a variety of simulated vulnerabilities, Xenon allows developers and security professionals to test their tools and techniques against realistic scenarios without risking harm to real systems.

## Simulated Vulnerabilities
The following vulnerabilities are intentionally simulated by Xenon for testing purposes. Each item lists the source file that demonstrates the behavior and a short description of the simulated issue.

- **Cookie misconfiguration** (`xenon/home.py`): the home page sets a variety of cookies including a bare cookie with no security flags and examples that show combinations of `HttpOnly`, `Secure`, and `SameSite` settings to illustrate cookie-related risks.
- **Login timing side-channel & session cookie** (`xenon/login.py`): login handling introduces an artificial delay for known usernames (simulating a timing oracle) and sets a `session` cookie with `HttpOnly` and `SameSite=Lax` (demonstrates session cookie properties; secure flag intentionally omitted for testing).
- **Command injection simulation** (`xenon/ping.py`): the ping endpoint parses input for injection operators and returns plausible outputs for injected commands (e.g., `id`, `cat /etc/passwd`, `ls`) to demonstrate command-injection detection and response behaviors.
- **Password reset timing/info simulation** (`xenon/reset.py`): reset handling adds a delay for known usernames and returns different messages for existing vs. non-existing users, simulating an account-enumeration/timing scenario.
- **SQL error / injection simulation** (`xenon/search.py`): search handling returns a simulated MySQL syntax error when the query contains a single quote, mimicking an SQL error disclosure; otherwise it returns humorous/taunting responses to illustrate input handling.
- **Server information disclosure (phpinfo)** (`xenon/resources/phpinfo.html` + route in `xenon/app.py`): a `phpinfo()`-style page is served at `/phpinfo.php` and the response includes an `X-Powered-By` header, demonstrating information exposure about server software/version.

All simulated vulnerabilities are non-exploitable and included purely for safe testing and training.

## Local Deployment

To run Xenon locally, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/adcaudill/xenon.git
   cd xenon
    ```
2. Create a virtual environment and activate it:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
3. Install the required dependencies:
   ```bash
   pipenv install --dev
   ```
4. Start the application:
   ```bash
   ./run-local.sh
   ```
5. Access the application in your web browser at `http://localhost:5000`.

## Unit Testing

To run unit tests, use the following command:

```bash
pytest tests/
```