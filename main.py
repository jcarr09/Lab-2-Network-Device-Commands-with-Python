import logging
import os

os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    filename="logs/lab.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)

import getpass
import json
from netmiko import ConnectHandler
from netmiko.exceptions import NetmikoTimeoutException, NetmikoAuthenticationException, SSHException
from ntc_templates.parse import parse_output

def get_creds():
    host = input("Enter device IP address or hostname: ")
    username = input("Enter username: ")
    password = getpass.getpass("Enter password: ")
    logging.info("[CREDENTIALS_COLLECTED] Host: %s, Username: %s", host, username)
    return host, username, password

def device_connect(host, username, password):
    device = {
        "device_type": "cisco_ios",
        "host": host,
        "username": username,
        "password": password,
    }
    
    try:
        connection = ConnectHandler(**device)
        logging.info("[CONNECT_OK] Successfully connected to device: %s", host)
        return connection
    except NetmikoTimeoutException:
        print("Connection timed out. Please check the device IP address/hostname and try again.")
        logging.error("[CONNECT_FAIL] Connection timed out for device: %s", host)
    except NetmikoAuthenticationException:
        print("Authentication failed. Please check the username and password and try again.")
        logging.error("[CONNECT_FAIL] Authentication failed for device: %s", host)
    except SSHException:
        print("SSH connection failed. Please check the device configuration and try again.")
        logging.error("[CONNECT_FAIL] SSH connection failed for device: %s", host)
    except Exception as error:
        print(f"General Error: {type(error).__name__}")
        logging.error("[CONNECT_FAIL] %s", type(error).__name__)

def comm_run(connection):
    netinfo = {}
    commands = ["sh ver", "sh ip int br", "sh inv"]
    for comm in commands:
            output = connection.send_command(comm)
            logging.info("[CMD_RUN] %s", comm)
            filename = f"data/raw/{comm.replace(' ', '_')}.txt"
            with open(filename, "w") as f:
                f.write(output)
            netinfo[comm] = output
    return netinfo

def parse(netinfo):
    parsedata = {}
    for comm, output in netinfo.items():
        try:
            parsed_output = parse_output(platform="cisco_ios", command=comm, data=output)
            parsedata[comm] = parsed_output
            logging.info("[PARSE_OK] Successfully parsed output for command: %s", comm)
        except Exception as error:
            print(f"Failed to parse data for command '{comm}': {type(error).__name__}")
            logging.error("[PARSE_FAIL] %s for command: %s", type(error).__name__, comm)
    return parsedata

def write_report(parsedata):
    verdata = parsedata.get("sh ver", [{}])[0]
    int_br = parsedata.get("sh ip int br", {})
    hostname = verdata.get("hostname", "Unknown")
    version = verdata.get("version", "Unknown")
    model = ", ".join(verdata.get("hardware", [])) or "Unknown"
    serial = ", ".join(verdata.get("serial", [])) or "Unknown"
    isup = [intf for intf in int_br if intf.get("status") == "up"]

    repdata = [
        "::::: Device Report :::::",
        f"Hostname: {hostname}",
        f"Model: {model}",
        f"Version: {version}",
        f"Serial Number: {serial}",
        f"Number of Interfaces Up: {len(isup)}",
        "",
        "Interface Status:",
    ]
    for i in int_br:
        repdata.append(f"{i.get('interface', 'Unknown')}: {i.get('status', 'Unknown')}")

    report_path = "data/reports/device_summary.txt"
    with open(report_path, "w") as f:
        f.write("\n".join(repdata))
        logging.info("[REPORT_SAVED] Device summary report saved to %s", report_path)
        print(repdata)

def main():
    logging.info("[STEP 2] Dev Container Started")
    host, username, password = get_creds()
    connection = device_connect(host, username, password)

    if connection is None:
        return main()
    try:
        os.makedirs("data/raw", exist_ok=True)
        os.makedirs("data/reports", exist_ok=True)
        print(f"Connected to {host}: {connection.find_prompt()}")
        netinfo = comm_run(connection)
        parsedata = parse(netinfo)
        write_report(parsedata)
    except Exception as error:
        print(f"General Error: {type(error).__name__}")
    finally:
        connection.disconnect()
        print(f"Disconnected from device: {host}")

if __name__ == "__main__":
    logging.info("[LAB2-START]")
    main()
    logging.info("[LAB2-END]")

