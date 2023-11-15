"""
    Standalone tool to update TestRail test cases
"""
import argparse
import base64
import csv
import json
import pprint

import requests


class APIClient:
    def __init__(self, base_url):
        self.user = ""
        self.password = ""
        if not base_url.endswith("/"):
            base_url += "/"
        self.__url = base_url + "index.php?/api/v2/"

    def send_get(self, uri, filepath=None):
        """Issue a GET request (read) against the API.

        Args:
            uri: The API method to call including parameters, e.g. get_case/1.
            filepath: The path and file name for attachment download; used only
                for 'get_attachment/:attachment_id'.

        Returns:
            A dict containing the result of the request.
        """
        return self.__send_request("GET", uri, filepath)

    def send_post(self, uri, data):
        """Issue a POST request (write) against the API.

        Args:
            uri: The API method to call, including parameters, e.g. add_case/1.
            data: The data to submit as part of the request as a dict; strings
                must be UTF-8 encoded. If adding an attachment, must be the
                path to the file.

        Returns:
            A dict containing the result of the request.
        """
        return self.__send_request("POST", uri, data)

    def __send_request(self, method, uri, data):
        url = self.__url + uri

        auth = str(
            base64.b64encode(bytes("%s:%s" % (self.user, self.password), "utf-8")),
            "ascii",
        ).strip()
        headers = {"Authorization": "Basic " + auth}

        if method == "POST":
            if uri[:14] == "add_attachment":  # add_attachment API method
                files = {"attachment": (open(data, "rb"))}
                response = requests.post(url, headers=headers, files=files)
                files["attachment"].close()
            else:
                headers["Content-Type"] = "application/json"
                payload = bytes(json.dumps(data), "utf-8")
                response = requests.post(url, headers=headers, data=payload)
        else:
            headers["Content-Type"] = "application/json"
            response = requests.get(url, headers=headers)

        if response.status_code > 201:
            try:
                error = response.json()
            except:  # response.content not formatted as JSON
                error = str(response.content)
            raise APIError(
                "TestRail API returned HTTP %s (%s)" % (response.status_code, error)
            )
        else:
            if uri[:15] == "get_attachment/":  # Expecting file, not JSON
                try:
                    open(data, "wb").write(response.content)
                    return data
                except:
                    return "Error saving attachment."
            else:
                try:
                    return response.json()
                except:  # Nothing to return
                    return {}


class APIError(Exception):
    pass


expected_payload_template = {
    "title": None,
    "type_id": None,
    "priority_id": None,
    "estimate": None,
    "refs": None,
    "custom_automation_status": None,
    "custom_execution_type": None,
    "custom_cfd_testcase": None,
    "custom_automation_path": None,
    "custom_preconds": None,
    "custom_steps": None,
    "custom_expected": None,
    "custom_mission": None,
    "custom_goals": None,
    "custom_automation_owner": None,
}


# Functions to obtain various mappings for TestRail API
def get_custom_fields_map(case_fields):
    """
    Generates a dictionary mapping custom field labels to their system names.

    Args:
        case_fields: a list of dictionaries, each representing a custom field.

    Returns:
        A dictionary mapping custom field labels to their system names.
    """
    custom_fields_map = {
        d["label"]: d["system_name"]
        for d in case_fields
        # two fields have same label (Steps), so skipping 'custom_steps_separated'
        if not (d["label"] == "Steps" and d["name"] == "steps_separated")
    }
    return custom_fields_map


def get_project_id_map(active_projects):
    """
    Create a mapping of project names to project IDs.

    Args:
        active_projects (list): A list of active projects.

    Returns:
        dict: A dictionary mapping project names to project IDs.
    """
    project_id_map = {project["name"]: project["id"] for project in active_projects}
    return project_id_map


# TODO: implement mapping for every property
def get_priority_map(priorities):
    """
    Generates a dictionary mapping priority names to their ids.

    Args:
        priorities: a list of dictionaries, each representing a priority.

    Returns:
        A dictionary mapping priority names to their ids.
    """
    priorities_map = {d["name"]: d["id"] for d in priorities}
    return priorities_map


def get_case_type_map(case_types):
    """
    Generates a dictionary mapping case type names to their ids.

    Args:
        case_types: a list of dictionaries, each representing a case type.

    Returns:
        A dictionary mapping case type names to their ids.
    """
    # case_type_map = {}
    # for d in case_types:
    #     case_type_map.update({d["name"]: d["id"]})
    case_type_map = {d["name"]: d["id"] for d in case_types}
    return case_type_map


def get_custom_automation_status_map(case_fields, project_id):
    """
    Generates a dictionary mapping automation status values to their ids.

    Args:
        case_fields: a list of dictionaries, each representing a custom field.
        project_id: the id of the project for which to generate the map.

    Returns:
        A dictionary mapping automation status values to their ids.
    """
    field = next(field for field in case_fields if field["name"] == "automation_status")
    csv_automation_values = [
        config["options"]["items"]
        for config in field["configs"]
        if project_id in config["context"]["project_ids"]
    ][0]
    automation_status_map = {
        row[1]: int(row[0]) for row in csv.reader(csv_automation_values.splitlines())
    }
    return automation_status_map


# Function to process command line arguments
def args_processor():
    """
    Processes command line arguments for the script.

    Returns:
        An argparse.Namespace object containing the script arguments.
    """
    parser = argparse.ArgumentParser(
        description="TestRail Properties Bulk Update Tool",
        epilog="Supported input file format: csv",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument(
        "-f", "--file", type=str, required=True, help="TestRail exported CSV file"
    )
    parser.add_argument(
        "-H", "--host", type=str, required=True, help="TestRail address url"
    )
    parser.add_argument(
        "-u", "--username", type=str, required=True, help="TestRail username"
    )
    parser.add_argument(
        "-p", "--password", type=str, required=True, help="TestRail password or API key"
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        default=False,
        help="Verbose mode with API response outputs enabled",
    )
    parser.add_argument(
        "-P",
        "--project",
        type=str,
        default="GLCP",  # GLCP set as Default Project.
        help="TestRail Project Name",
    )
    args = parser.parse_args()
    return args


# Functions to read and process CSV data
def read_csv(csvFilePath, fields):
    """
    Reads CSV file and converts it into a dictionary.

    Args:
        csvFilePath: Path to the csv file.
        fields: A list of fields (columns) in the csv file.

    Returns:
        A dictionary where keys are the ID and values are dictionaries with each property.
    """
    data = {}
    # Open a csv reader called DictReader
    with open(csvFilePath, encoding="utf-8-sig") as csv_file:
        next(csv_file)
        csvReader = csv.DictReader(csv_file, fieldnames=fields)
        # Convert each row into a dictionary and add it to data
        for row in csvReader:
            key = row["ID"]
            data[key] = dict(row)
    return data


def csv_header_processor(csvFilePath):
    """
    Processes the CSV file's header and handles any duplicate headers.

    Args:
        csvFilePath: Path to the csv file.

    Returns:
        A list of unique header names.
    """
    fields = []
    with open(csvFilePath, "r", encoding="utf-8-sig") as csv_file:
        reader = csv.reader(csv_file)
        for header in next(reader):
            if header not in fields:
                fields.append(header)
            else:
                fields.append(header + "+")
        return fields


def map_dict_keys(init_dict, map_dict):
    """
    Maps the keys of a dictionary based on a mapping dictionary.

    Args:
        init_dict: The initial dictionary.
        map_dict: The mapping dictionary.

    Returns:
        A new dictionary with mapped keys.
    """
    res_dict = {}
    for k, v in init_dict.items():
        if isinstance(v, dict):
            v = map_dict_keys(v, map_dict[k])
        elif k in map_dict.keys():
            k = str(map_dict[k])
        if k == "ID":
            res_dict["id"] = int(v[1:])
        res_dict[k] = v or None
    return res_dict


# Function to convert CSV data to API payload format
def csv_to_api_payload_format(csvData, fields_map):
    """
    Converts the CSV data into the format required for the API payload.

    Args:
        csvData: The CSV data as a dictionary.
        fields_map: The mapping of CSV data fields to API payload fields.

    Returns:
        A dictionary representing the API payload.
    """
    api_payload_format = {}
    for key, value in csvData.items():
        api_payload_format[key] = map_dict_keys(value, fields_map)
    return api_payload_format


def get_fields_map(case_fields):
    """
    Generates a mapping of TestRail API fields based on the provided case fields.

    Args:
        case_fields (list): A list of dictionaries representing custom fields.

    Returns:
        dict: A dictionary mapping TestRail API fields to their corresponding values.
    """
    # Base field properties (excluding custom properties)
    fields_map = {
        # 'ID': 'id', # not used as 'id' mapping handled in map_dict_keys() function
        "Section": "section_id",  # requires project ID and suite_id of perticular tc to implement mapping
        "Title": "title",
        "Template": "template_id",  # requires project ID of perticular tc to implement mapping
        "Type": "type_id",
        "Priority": "priority_id",
        "Estimate": "estimate",
        "Forecast": "estimate_forecast",
        "References": "refs",
        "Suite ID": "suite_id",  # requires project ID of perticular tc to implement mapping
        "Steps+": "custom_steps_separated",  # Not implementing because having same label (Steps) as 'custom_steps' causing conflicts
    }

    # Generate custom fields from API
    custom_fields_map = get_custom_fields_map(case_fields)
    fields_map.update(custom_fields_map)

    # Exclude fields that require additional implementation
    excluded_fields = [
        "Template",  # requires project ID of perticular tc to implement
        "Suite ID",  # requires project ID of perticular tc to implement
        "Section",  # requires project ID and suite_id of perticular tc to implement
        "Steps+",  # has same label as 'custom_steps'
        # 'Priority', # Mapping implemented
        # 'Type', # Mapping implemented
        # 'References', # No mapping required
        # 'Estimate', # No mapping required
        # 'Forecast', # No mapping required
        "Automation ID",  # not yet implemented
        # 'Automation Path', # No mapping required
        # 'Automation Status', # Mapping Implemented
        "Automation Type",  # not implemented yet
        "Automation-Owner",  # not implemented yet
        "CFD Testcase",  # not implemented yet
        "Execution Type",  # not implemented yet
        # 'Expected Result', # No mapping required
        "Goals",  # not implemented yet
        "Mission",  # not implemented yet
        # 'Preconditions', # No mapping required
        # 'Steps' # No mapping required
    ]
    for key in excluded_fields:
        del fields_map[key]

    return fields_map


def main():
    # Process command line arguments
    args = args_processor()
    testrail_host = args.host
    file = args.file
    username = args.username
    password = args.password
    verbose = args.verbose
    project = args.project

    # Initialize TestRail API client
    client = APIClient(testrail_host)
    client.user = username
    client.password = password

    # API Calls for mappings
    active_projects = client.send_get("get_projects&is_completed=0")
    priorities = client.send_get("get_priorities")
    case_fields = client.send_get("get_case_fields")
    case_types = client.send_get("get_case_types")

    # Generate fields_map
    fields_map = get_fields_map(case_fields)
    if verbose:
        print("The following fields will be updated by the tool: ")
        pprint.pprint(fields_map, sort_dicts=False)

    # Generate mapping dictionaries
    # TODO: Implement retreival of project ID for each testcase to get automation_status_map
    project_id_map = get_project_id_map(active_projects)
    project_id = project_id_map[project]
    priority_id_map = get_priority_map(priorities)
    case_type_map = get_case_type_map(case_types)
    automation_status_map = get_custom_automation_status_map(case_fields, project_id)

    # Read test cases from CSV file and convert to API payload format
    testcases = read_csv(file, csv_header_processor(file))
    tcs = csv_to_api_payload_format(testcases, fields_map)

    # Iterate over test cases and update them via TestRail API
    for tc, tc_properties in tcs.items():
        # Apply custom mappings to test case properties
        if "priority_id" in tc_properties:
            tc_properties["priority_id"] = priority_id_map[tc_properties["priority_id"]]
        if "custom_automation_status" in tc_properties:
            tc_properties["custom_automation_status"] = automation_status_map[
                tc_properties["custom_automation_status"]
            ]
        if "type_id" in tc_properties:
            tc_properties["type_id"] = case_type_map[tc_properties["type_id"]]
        # Prepare payload with properties different compared to existing values
        payload = {}
        test_case_id = tc_properties["id"]
        print(f"Processing testcase C{test_case_id}:")
        test_case_existing = client.send_get(f"get_case/{test_case_id}")
        for property, value in tc_properties.items():
            if property in test_case_existing:
                api_value = test_case_existing[property]
                if type(api_value) == str:
                    api_value = api_value.replace("\r", "")
                if value != api_value:
                    payload.update({property: value})
        if payload:
            result = client.send_post(f"update_case/{test_case_id}", payload)
            print(f"Testcase C{test_case_id} updated.")
            if verbose:
                pprint.pprint(f"Changes made: {payload}")
                pprint.pprint(result)
        else:
            print("No values changed for testcase.")


if __name__ == "__main__":
    main()
