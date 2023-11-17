# based on https://github.com/xdxxxdx/ldes-conformance-monitor-exporter

import json
import logging
import os
import time
import xml.etree.ElementTree as elementTree

import requests
from prometheus_client import start_http_server, Gauge


# function to extract values from nested JSON dict
def extract_values_by_key(data, key):
    values = []

    if isinstance(data, dict):
        for k, v in data.items():
            if k == key:
                values.append(v)
            elif isinstance(v, (dict, list)):
                values.extend(extract_values_by_key(v, key))
    elif isinstance(data, list):
        for item in data:
            values.extend(extract_values_by_key(item, key))

    return values


def calculate_percentage_not_equal(dictionary, target_value):
    # Count the number of values not equal to the target value
    not_equal_count = sum(1 for value in dictionary.values() if value != target_value)

    # Calculate the percentage
    total_items = len(dictionary)
    percentage_not_equal = (not_equal_count / total_items) * 100

    return percentage_not_equal


# Interaction with ITB
# function to send start request to ITB for a specific test session and return the session ids
def send_curl_start_request(
    start_api_endpoint, start_system, itb_api_key, actor_key, test_cases
):
    url = start_api_endpoint
    payload = json.dumps(
        {
            "system": start_system,
            "actor": actor_key,
            "testCase": test_cases,
        }
    )
    headers = {"ITB_API_KEY": itb_api_key, "Content-Type": "text/plain"}
    response = requests.request("POST", url, headers=headers, data=payload)
    logging.info("Sending start request to: " + url + "\n with payload: " + payload)
    return extract_values_by_key(response.json(), "session")


# function to get report request from ITB for a specific test session
def get_curl_report_request(sessions, itb_api_key, report_api_endpoint):
    results = {}
    namespace = {"ns2": "http://www.gitb.com/core/v1/"}
    for session in sessions:
        url = report_api_endpoint + session
        logging.info("Getting report for: " + url)
        payload = {}
        headers = {"ITB_API_KEY": itb_api_key}
        response = requests.request("GET", url, headers=headers, data=payload)

        # When the response is success 200 with a valid test result, return the report to the prometheuse.
        while (response.status_code != 200) or elementTree.fromstring(
            response.text
        ).find("{http://www.gitb.com/tr/v1/}result").text == "UNDEFINED":
            response = requests.request("GET", url, headers=headers, data=payload)
        test_descripton = (
            elementTree.fromstring(response.text)
            .find(".//ns2:name", namespaces=namespace)
            .text
        )
        result = (
            elementTree.fromstring(response.text)
            .find("{http://www.gitb.com/tr/v1/}result")
            .text
        )

        results[test_descripton] = (
            elementTree.fromstring(response.text)
            .find("{http://www.gitb.com/tr/v1/}result")
            .text
        )
        logging.info("result for " + test_descripton + "is: " + result)
    return results


def conformance_monitor():
    # load configurable parameters
    port = int(os.getenv("PORT"))
    check_interval = int(os.getenv("TEST_INTERVAL_SECONDS"))
    start_api_endpoint = os.getenv("START_API_ENDPOINT")
    start_systems = os.getenv("START_SYSTEM").split(",")
    system_names = os.getenv("SYSTEM_NAMES").split(",")
    itb_api_key = os.getenv("ITB_API_KEY")
    debug_level = os.getenv("DEBUG_LEVEL")
    report_api_endpoint = os.getenv("REPORT_API_ENDPOINT")
    actor_key = os.getenv("ACTOR_KEY")
    test_cases = os.getenv("TEST_CASES").split(",")
    logging.basicConfig(level=debug_level)

    logging.info(f"Starting service on port %d", port)
    start_http_server(port)

    # Create Gauge metric for each system
    reported_results = {}
    for ix, system in enumerate(start_systems):
        reported_results[system_names[ix]] = Gauge(
            f"conformance_{system_names[ix]}", f"Conformance % of {system}"
        )

    while True:
        for index, start_system in enumerate(start_systems):
            try:
                sessions = send_curl_start_request(
                    start_api_endpoint, start_system, itb_api_key, actor_key, test_cases
                )
                test_results = get_curl_report_request(
                    sessions, itb_api_key, report_api_endpoint
                )
                result_percentage = calculate_percentage_not_equal(
                    test_results, "SUCCESS"
                )
                reported_results[system_names[index]].set(100 - result_percentage)
            except Exception as e:
                logging.error(f"error while running test for {start_system}: {e}")
                reported_results[system_names[index]].set(0)
            index = index + 1
        logging.info(f"sleeping for %d seconds", check_interval)
        time.sleep(check_interval)


if __name__ == "__main__":
    conformance_monitor()
