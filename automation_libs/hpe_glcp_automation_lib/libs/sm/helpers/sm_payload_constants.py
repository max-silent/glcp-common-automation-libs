import logging

from hpe_glcp_automation_lib.libs.commons.utils.random_gens import RandomGenUtils

log = logging.getLogger(__name__)


class SmInputPayload:
    @staticmethod
    def get_pce_supported_skus():
        return ["S2D64AAE"]

    @staticmethod
    def get_sdwan_supported_skus():
        return ["S2M87AAS"]

    @staticmethod
    def combined_iap_sw_gw_subs():
        null = None
        combined_subs_networking = {
            "reason": "Creation",
            "quote": "CMEUPAPS10",
            "contract": "CMEUPAPS10",
            "smcCode": "E",
            "customer": {
                "MDM": "CMEUPAPS10",
                "phone": "50179505",
                "postal_code": "164 40",
                "address": "Torshamnsgatan 21-23",
                "city": "Kista",
                "country": "SE",
                "state": "",
                "company_name": "ERICSSON AB EAB",
                "email": "goran.matovic@ericsson.com",
            },
            "activate": {
                "soldTo": "Kronborgsgränd 7 Kista SE",
                "soldToName": "ARROW ECS SWEDEN AB",
                "soldToEmail": "ap.ecs.dk@arrow.com",
                "shipTo": "Torshamnsgatan 21-23 Kista SE",
                "shipToName": "ERICSSON AB EAB",
                "shipToEmail": "ptp.incident.management@ericsson.com",
                "endUser": "Torshamnsgatan 21-23 Kista SE",
                "endUserName": "Florence Sprint6 CMEUPAPS02",
                "endUserEmail": "goran.matovic@ericsson.com",
                "reseller": "Kronborgsgränd 1 Kista SE",
                "resellerName": "ATEA SVERIGE AB",
                "resellerEmail": "levresk@atea.se",
                "po": "ARSW_TST4",
                "resellerPo": "",
                "endUserPo": "",
                "orderClass": "ZBRIM",
                "party": {
                    "id": "CMEUPAPS10",
                    "countryId": "120771848",
                    "globalId": "120771846",
                },
                "parties": [
                    {
                        "function": "AG",
                        "id": "CMEUPAPS10",
                        "countryId": "121140995",
                        "globalId": "121140994",
                    },
                    {
                        "function": "WE",
                        "id": "CMEUPAPS10",
                        "countryId": "120771848",
                        "globalId": "120771846",
                    },
                    {
                        "function": "RE",
                        "id": "CMEUPAPS10",
                        "countryId": "121140995",
                        "globalId": "121140994",
                    },
                    {
                        "function": "RG",
                        "id": "CMEUPAPS10",
                        "countryId": "121140995",
                        "globalId": "121140994",
                    },
                    {
                        "function": "Z1",
                        "id": "CMEUPAPS10",
                        "countryId": "121148324",
                        "globalId": "121148323",
                    },
                    {
                        "function": "ZC",
                        "id": "CMEUPAPS10",
                        "countryId": "120771848",
                        "globalId": "120771846",
                    },
                    {
                        "function": "ZE",
                        "id": "CMEUPAPS10",
                        "countryId": "120771848",
                        "globalId": "120771846",
                    },
                    {
                        "function": "ZL",
                        "id": "CMEUPAPS10",
                        "countryId": "120771848",
                        "globalId": "120771846",
                    },
                ],
                "contacts": [
                    {
                        "function": "ZG",
                        "id": "9000202677",
                        "countryId": null,
                        "globalId": null,
                    }
                ],
            },
            "entitlements": [
                {
                    "lineItem": "0000000010",
                    "quote": "CMEUPAPS10",
                    "contract": "CMEUPAPS10",
                    "total_qty": "2.000",
                    "available_qty": "0.00",
                    "product": {
                        "sku": "JN001AAS",
                        "legacy": "",
                        "description": "Aruba Central AP Fnd 3yr Sub SaaS",
                        "attributes": [
                            {
                                "name": "BILL_FREQ",
                                "value": "UP",
                                "valueDisplay": "Paid Upfront",
                                "nameDisplay": "Billing Frequency",
                            },
                            {
                                "name": "TERM_IN_MONTHS",
                                "value": "36",
                                "valueDisplay": "36",
                                "nameDisplay": "Term In Months",
                            },
                            {
                                "name": "TERM_IN_MONTHS_MAX_2",
                                "value": "36",
                                "valueDisplay": "36",
                                "nameDisplay": "Term in months maximum",
                            },
                            {
                                "name": "TIER",
                                "value": "FO",
                                "valueDisplay": "Foundation",
                                "nameDisplay": "Tier",
                            },
                            {
                                "name": "HIDE_CHAR",
                                "value": "COMMITMENT_VALUE1|FIXED_COMMITMENT|PREPAID_AMT|PRICING_MODEL",
                                "valueDisplay": "COMMITMENT_VALUE1|FIXED_COMMITMENT|PREPAID_AMT|PRICING_MODEL",
                                "nameDisplay": "Characteristic Name",
                            },
                            {
                                "name": "INVOICING_MODEL",
                                "value": "UP",
                                "valueDisplay": "Paid Upfront",
                                "nameDisplay": "Invoicing Model",
                            },
                            {
                                "name": "TERM_UOM",
                                "value": "Y",
                                "valueDisplay": "Year(s)",
                                "nameDisplay": "Term Unit of Measure",
                            },
                            {
                                "name": "TERM_IN_MONTHS_MIN_2",
                                "value": "12",
                                "valueDisplay": "12",
                                "nameDisplay": "Term in months minimum",
                            },
                            {
                                "name": "TERM",
                                "value": "3",
                                "valueDisplay": "3",
                                "nameDisplay": "Term",
                            },
                            {
                                "name": "TIER_AP",
                                "value": "FO",
                                "valueDisplay": "Foundation",
                                "nameDisplay": "Access Point Tier",
                            },
                        ],
                    },
                    "support": [
                        {
                            "name": "CS_TCS_CONTRACT_TYPE",
                            "value": "FC",
                            "valueDisplay": "Foundation Care",
                            "nameDisplay": "Contract Type",
                        },
                        {
                            "name": "SUPPORT_TIER",
                            "value": "FC",
                            "valueDisplay": "Foundation Care",
                            "nameDisplay": "Support Tier",
                        },
                        {
                            "name": "CS_TCS_TECH_SUPPORT",
                            "value": "Y",
                            "valueDisplay": "Year(s)",
                            "nameDisplay": "Technical Support",
                        },
                        {
                            "name": "CS_TCS_TECH_GUIDANCE",
                            "value": "Y",
                            "valueDisplay": "Year(s)",
                            "nameDisplay": "General Technical Guidance",
                        },
                        {
                            "name": "TERM_UOM",
                            "value": "Y",
                            "valueDisplay": "Year(s)",
                            "nameDisplay": "Term Unit of Measure",
                        },
                        {
                            "name": "CS_TCS_RESPONSE_TIME",
                            "value": "2HR",
                            "valueDisplay": "2 Hours",
                            "nameDisplay": "Response Time",
                        },
                        {
                            "name": "CS_TERM_UOM",
                            "value": "Y",
                            "valueDisplay": "Year(s)",
                            "nameDisplay": "Term Unit Of Measure",
                        },
                        {
                            "name": "CS_TCS_COV_WINDOW7",
                            "value": "24",
                            "valueDisplay": "24 Hours",
                            "nameDisplay": "Coverage Window 24x7",
                        },
                        {
                            "name": "TERM",
                            "value": "3",
                            "valueDisplay": "3",
                            "nameDisplay": "Term",
                        },
                        {
                            "name": "CS_TCS_COLLAB_SUPPORT",
                            "value": "Y",
                            "valueDisplay": "Year(s)",
                            "nameDisplay": "Collaborative Supp and Assist",
                        },
                        {
                            "name": "CS_TCS_SERVICE_LEVEL",
                            "value": "ESS",
                            "valueDisplay": "Essential",
                            "nameDisplay": "Service Level",
                        },
                        {
                            "name": "CS_TERM",
                            "value": "3",
                            "valueDisplay": "3",
                            "nameDisplay": "Term",
                        },
                    ],
                    "licenses": [
                        {
                            "id": "CTHSTDTESTCMEUPAPS10",
                            "qty": "2.000",
                            "devices": [],
                            "customer": {},
                            "appointments": {
                                "subscriptionStart": "05.05.2023 00:00:00",
                                "subscriptionEnd": "05.05.2036 00:00:00",
                                "suspensionDate": null,
                                "cancellationDate": null,
                                "reactivationDate": null,
                                "activationDate": "05.05.2023 12:26:59",
                                "duration": "3",
                                "delayedActivation": null,
                                "autoRenewalDate": null,
                            },
                        }
                    ],
                },
                {
                    "lineItem": "0000000020",
                    "quote": "6000257227",
                    "contract": "2000046487",
                    "total_qty": "2.000",
                    "available_qty": "0.00",
                    "product": {
                        "sku": "JN002AAS",
                        "legacy": "",
                        "description": "Aruba Central 62XX Foundation Year(s) SUB SaaS",
                        "attributes": [
                            {
                                "name": "TERM_IN_MONTHS",
                                "value": "12",
                                "valueDisplay": "12",
                                "nameDisplay": "Term In Months",
                            },
                            {
                                "name": "TIER",
                                "value": "FO",
                                "valueDisplay": "Foundation",
                                "nameDisplay": "Tier",
                            },
                            {
                                "name": "HIDE_CHAR",
                                "value": "COMMITMENT_VALUE1|EVERGREEN|FIXED_COMMITMENT|PRICING_MODEL",
                                "valueDisplay": "COMMITMENT_VALUE1|EVERGREEN|FIXED_COMMITMENT|PRICING_MODEL",
                                "nameDisplay": "HIDE CHARACTERISTICS",
                            },
                            {
                                "name": "TERM_UOM",
                                "value": "Y",
                                "valueDisplay": "Year(s)",
                                "nameDisplay": "Term Unit of Measure",
                            },
                            {
                                "name": "TERM_IN_MONTHS_MIN_2",
                                "value": "0",
                                "valueDisplay": "0",
                                "nameDisplay": "Term in months minimum",
                            },
                            {
                                "name": "PRODUCT_ID",
                                "value": "JN002AAS",
                                "valueDisplay": "JN002AAS",
                                "nameDisplay": "Product ID",
                            },
                            {
                                "name": "SW_FAMILY",
                                "value": "62XX",
                                "valueDisplay": "62XX",
                                "nameDisplay": "Switch Family",
                            },
                            {
                                "name": "BILL_FREQ",
                                "value": "M",
                                "valueDisplay": "Monthly",
                                "nameDisplay": "BILLING FREQUENCY",
                            },
                            {
                                "name": "TIER_SW",
                                "value": "FO",
                                "valueDisplay": "Foundation",
                                "nameDisplay": "Switch Tier",
                            },
                            {
                                "name": "SP_HIDE_CHAR1",
                                "value": "TERM",
                                "valueDisplay": "TERM",
                                "nameDisplay": "Characteristic Name",
                            },
                            {
                                "name": "QUANTITY_2",
                                "value": "10",
                                "valueDisplay": "10",
                                "nameDisplay": "CRM: Order Quantity",
                            },
                            {
                                "name": "SP_HIDE_CHAR2",
                                "value": "TERM_UOM",
                                "valueDisplay": "TERM_UOM",
                                "nameDisplay": "Characteristic Name",
                            },
                            {
                                "name": "TERM_IN_MONTHS_MAX_2",
                                "value": "12",
                                "valueDisplay": "12",
                                "nameDisplay": "Term in months maximum",
                            },
                            {
                                "name": "INVOICING_MODEL",
                                "value": "SU",
                                "valueDisplay": "Subscription",
                                "nameDisplay": "INVOICING MODEL",
                            },
                            {
                                "name": "PRODUCT_CC",
                                "value": "CENTRAL_SW",
                                "valueDisplay": "Central_SW",
                                "nameDisplay": "Product ID for CC",
                            },
                            {
                                "name": "CS_TERM_UOM",
                                "value": "Y",
                                "valueDisplay": "Year(s)",
                                "nameDisplay": "Term Unit Of Measure",
                            },
                            {
                                "name": "CS_TERM",
                                "value": "1",
                                "valueDisplay": "1",
                                "nameDisplay": "Term",
                            },
                        ],
                    },
                    "support": [
                        {
                            "name": "SUPPORT_TIER",
                            "value": "FC",
                            "valueDisplay": "Foundation Care",
                            "nameDisplay": "Support Tier",
                        },
                        {
                            "name": "CS_TCS_TECH_SUPPORT",
                            "value": "Y",
                            "valueDisplay": "年",
                            "nameDisplay": "Technical Support",
                        },
                        {
                            "name": "SP_HIDE_CHAR1",
                            "value": "TERM",
                            "valueDisplay": "TERM",
                            "nameDisplay": "Characteristic Name",
                        },
                        {
                            "name": "CS_TCS_TECH_GUIDANCE",
                            "value": "Y",
                            "valueDisplay": "年",
                            "nameDisplay": "General Technical Guidance",
                        },
                        {
                            "name": "SP_HIDE_CHAR2",
                            "value": "TERM_UOM",
                            "valueDisplay": "TERM_UOM",
                            "nameDisplay": "Characteristic Name",
                        },
                        {
                            "name": "TERM_UOM",
                            "value": "Y",
                            "valueDisplay": "Year(s)",
                            "nameDisplay": "Term Unit of Measure",
                        },
                        {
                            "name": "CS_TERM_UOM",
                            "value": "Y",
                            "valueDisplay": "Year(s)",
                            "nameDisplay": "Term Unit Of Measure",
                        },
                        {
                            "name": "CS_TCS_COV_WINDOW7",
                            "value": "24",
                            "valueDisplay": "24 Hours",
                            "nameDisplay": "Coverage Window 24x7",
                        },
                        {
                            "name": "CS_TCS_COLLAB_SUPPORT",
                            "value": "Y",
                            "valueDisplay": "年",
                            "nameDisplay": "Collaborative Supp and Assist",
                        },
                        {
                            "name": "CS_TERM",
                            "value": "1",
                            "valueDisplay": "1",
                            "nameDisplay": "Term",
                        },
                    ],
                    "licenses": [
                        {
                            "id": "PAYGUE3A659YA5",
                            "qty": "2.000",
                            "devices": [],
                            "customer": {},
                            "appointments": {
                                "subscriptionStart": "17.05.2023 00:00:00",
                                "subscriptionEnd": "17.05.2034 00:00:00",
                                "suspensionDate": null,
                                "cancellationDate": null,
                                "reactivationDate": null,
                                "activationDate": "17.05.2023 06:57:03",
                                "duration": "1",
                                "delayedActivation": null,
                                "autoRenewalDate": null,
                            },
                        }
                    ],
                },
                {
                    "lineItem": "0000000030",
                    "quote": "6000203085",
                    "contract": "2000045651",
                    "total_qty": "2.000",
                    "available_qty": "0.00",
                    "product": {
                        "sku": "JN003AAS",
                        "legacy": "",
                        "description": "Aruba Central SDWAN 7005 GW Foundation Year(s) SUB Saas",
                        "attributes": [
                            {
                                "name": "TERM_IN_MONTHS",
                                "value": "12",
                                "valueDisplay": "12",
                                "nameDisplay": "Term In Months",
                            },
                            {
                                "name": "TIER",
                                "value": "FO",
                                "valueDisplay": "Foundation",
                                "nameDisplay": "Tier",
                            },
                            {
                                "name": "HIDE_CHAR",
                                "value": "COMMITMENT_VALUE1|EVERGREEN|FIXED_COMMITMENT|PRICING_MODEL|TERM|TERM_UOM|TIER_GW",
                                "valueDisplay": "COMMITMENT_VALUE1|EVERGREEN|FIXED_COMMITMENT|PRICING_MODEL|TERM|TERM_UOM|TIER_GW",
                                "nameDisplay": "HIDE CHARACTERISTICS",
                            },
                            {
                                "name": "TERM_UOM",
                                "value": "Y",
                                "valueDisplay": "Year(s)",
                                "nameDisplay": "Term Unit of Measure",
                            },
                            {
                                "name": "TERM_IN_MONTHS_MIN_2",
                                "value": "0",
                                "valueDisplay": "0",
                                "nameDisplay": "Term in months minimum",
                            },
                            {
                                "name": "PRODUCT_ID",
                                "value": "JN003AAS",
                                "valueDisplay": "JN003AAS",
                                "nameDisplay": "Product ID",
                            },
                            {
                                "name": "GW_FAMILY",
                                "value": "7005",
                                "valueDisplay": "7005",
                                "nameDisplay": "Gateway Family",
                            },
                            {
                                "name": "BILL_FREQ",
                                "value": "M",
                                "valueDisplay": "Monthly",
                                "nameDisplay": "BILLING FREQUENCY",
                            },
                            {
                                "name": "SP_HIDE_CHAR1",
                                "value": "TERM",
                                "valueDisplay": "TERM",
                                "nameDisplay": "Characteristic Name",
                            },
                            {
                                "name": "QUANTITY_2",
                                "value": "1",
                                "valueDisplay": "1",
                                "nameDisplay": "CRM: Order Quantity",
                            },
                            {
                                "name": "SP_HIDE_CHAR2",
                                "value": "TERM_UOM",
                                "valueDisplay": "TERM_UOM",
                                "nameDisplay": "Characteristic Name",
                            },
                            {
                                "name": "TERM_IN_MONTHS_MAX_2",
                                "value": "12",
                                "valueDisplay": "12",
                                "nameDisplay": "Term in months maximum",
                            },
                            {
                                "name": "INVOICING_MODEL",
                                "value": "SU",
                                "valueDisplay": "Subscription",
                                "nameDisplay": "INVOICING MODEL",
                            },
                            {
                                "name": "PRODUCT_CC",
                                "value": "CENTRAL_GW",
                                "valueDisplay": "Central_GW",
                                "nameDisplay": "Product ID for CC",
                            },
                            {
                                "name": "CS_TERM_UOM",
                                "value": "Y",
                                "valueDisplay": "Year(s)",
                                "nameDisplay": "Term Unit Of Measure",
                            },
                            {
                                "name": "GW_TYPE",
                                "value": "SDWAN",
                                "valueDisplay": "SDWAN",
                                "nameDisplay": "Gateway Type",
                            },
                            {
                                "name": "CS_TERM",
                                "value": "1",
                                "valueDisplay": "1",
                                "nameDisplay": "Term",
                            },
                        ],
                    },
                    "support": [
                        {
                            "name": "CS_TCS_CONTRACT_TYPE",
                            "value": "TC",
                            "valueDisplay": "TechCare",
                            "nameDisplay": "Contract Type",
                        },
                        {
                            "name": "SUPPORT_TIER",
                            "value": "FC",
                            "valueDisplay": "Foundation Care",
                            "nameDisplay": "Support Tier",
                        },
                        {
                            "name": "CS_TCS_TECH_SUPPORT",
                            "value": "Y",
                            "valueDisplay": "Year(s)",
                            "nameDisplay": "Technical Support",
                        },
                        {
                            "name": "SP_HIDE_CHAR1",
                            "value": "TERM",
                            "valueDisplay": "TERM",
                            "nameDisplay": "Characteristic Name",
                        },
                        {
                            "name": "CS_TCS_TECH_GUIDANCE",
                            "value": "Y",
                            "valueDisplay": "Year(s)",
                            "nameDisplay": "General Technical Guidance",
                        },
                        {
                            "name": "SP_HIDE_CHAR2",
                            "value": "TERM_UOM",
                            "valueDisplay": "TERM_UOM",
                            "nameDisplay": "Characteristic Name",
                        },
                        {
                            "name": "CS_TCS_RESPONSE_TIME",
                            "value": "2HR",
                            "valueDisplay": "2 Hours",
                            "nameDisplay": "Response Time",
                        },
                        {
                            "name": "CS_TERM_UOM",
                            "value": "Y",
                            "valueDisplay": "Year(s)",
                            "nameDisplay": "Term Unit Of Measure",
                        },
                        {
                            "name": "CS_TCS_COV_WINDOW7",
                            "value": "24",
                            "valueDisplay": "24 Hours",
                            "nameDisplay": "Coverage Window 24x7",
                        },
                        {
                            "name": "CS_TCS_COLLAB_SUPPORT",
                            "value": "Y",
                            "valueDisplay": "Year(s)",
                            "nameDisplay": "Collaborative Supp and Assist",
                        },
                        {
                            "name": "CS_TCS_SERVICE_LEVEL",
                            "value": "ESS",
                            "valueDisplay": "Essential",
                            "nameDisplay": "Service Level",
                        },
                        {
                            "name": "CS_TERM",
                            "value": "1",
                            "valueDisplay": "1",
                            "nameDisplay": "Term",
                        },
                    ],
                    "licenses": [
                        {
                            "id": "PAYGHEUDY5A9D7",
                            "qty": "2.000",
                            "devices": [],
                            "customer": {},
                            "appointments": {
                                "subscriptionStart": "27.04.2023 00:00:00",
                                "subscriptionEnd": "27.04.2034 00:00:00",
                                "suspensionDate": null,
                                "cancellationDate": null,
                                "reactivationDate": null,
                                "activationDate": "26.04.2023 00:02:02",
                                "duration": "1",
                                "delayedActivation": null,
                                "autoRenewalDate": null,
                            },
                        }
                    ],
                },
            ],
        }
        return combined_subs_networking

    @staticmethod
    def subs_storage_baas():
        null = None
        sub_storage_baas = {
            "reason": "Creation",
            "quote": "6000116190",
            "contract": "2000046674",
            "smcCode": "E",
            "customer": {
                "MDM": "1000003242",
                "phone": "147526000",
                "postal_code": "92500",
                "address": "1 AVENUE DE BOIS PREAU",
                "city": "RUEIL MALMAISON",
                "country": "FR",
                "state": "IDF",
                "company_name": "IFP ENERGIES NOUVELLES",
                "email": "marina.destouches@ifp.fr",
            },
            "activate": {
                "soldTo": "1 AVENUE DE BOIS PREAU RUEIL MALMAISON FR",
                "soldToName": "IFP ENERGIES NOUVELLES",
                "soldToEmail": "",
                "shipTo": "1 AVENUE DE BOIS PREAU RUEIL MALMAISON FR",
                "shipToName": "IFP ENERGIES NOUVELLES",
                "shipToEmail": "",
                "endUser": "1 AVENUE DE BOIS PREAU RUEIL MALMAISON FR",
                "endUserName": "IFP ENERGIES NOUVELLES",
                "endUserEmail": "marina.destouches@ifp.fr",
                "po": "18octOMandP",
                "resellerPo": "",
                "endUserPo": "",
                "orderClass": "ZBRIM",
                "party": {
                    "id": "1000003242",
                    "countryId": "121390111",
                    "globalId": "121390108",
                },
                "parties": [
                    {
                        "function": "AG",
                        "id": "1000003242",
                        "countryId": "121390111",
                        "globalId": "121390108",
                    },
                    {
                        "function": "WE",
                        "id": "1000003242",
                        "countryId": "121390111",
                        "globalId": "121390108",
                    },
                    {
                        "function": "RE",
                        "id": "1000003242",
                        "countryId": "121390111",
                        "globalId": "121390108",
                    },
                    {
                        "function": "RG",
                        "id": "1000003242",
                        "countryId": "121390111",
                        "globalId": "121390108",
                    },
                    {
                        "function": "ZC",
                        "id": "1000003242",
                        "countryId": "121390111",
                        "globalId": "121390108",
                    },
                    {
                        "function": "ZE",
                        "id": "1000003242",
                        "countryId": "121390111",
                        "globalId": "121390108",
                    },
                    {
                        "function": "ZL",
                        "id": "1000003242",
                        "countryId": "121390111",
                        "globalId": "121390108",
                    },
                ],
                "contacts": [
                    {
                        "function": "ZG",
                        "id": "9000188775",
                        "countryId": null,
                        "globalId": null,
                    }
                ],
            },
            "entitlements": [
                {
                    "lineItem": "0000000010",
                    "quote": "6000116190",
                    "contract": "2000046674",
                    "total_qty": "1.000",
                    "available_qty": "0.00",
                    "product": {
                        "sku": "R9T02AAE",
                        "legacy": "",
                        "description": "HPE GreenLake for Block Storage 3 Year(s) Consumption+Subscription",
                        "attributes": [
                            {
                                "name": "CS_INVOICING_MODEL",
                                "value": "CO_SU",
                                "valueDisplay": "Consumption+Subscription",
                                "nameDisplay": "Invoicing Model",
                            },
                            {
                                "name": "CS_TERM_IN_MONTHS_MAX_2",
                                "value": "60",
                                "valueDisplay": "60",
                                "nameDisplay": "Term in months maximum",
                            },
                            {
                                "name": "CS_HW_SUPPORT_TYPE",
                                "value": "TES",
                                "valueDisplay": "Tech Care Essential",
                                "nameDisplay": "HW Support Type",
                            },
                            {
                                "name": "CS_RACK_SIZE",
                                "value": "RACKLESS",
                                "valueDisplay": "Rackless",
                                "nameDisplay": "Rack Size",
                            },
                            {
                                "name": "CS_BILL_FREQ",
                                "value": "M",
                                "valueDisplay": "Monthly",
                                "nameDisplay": "Billing Frequency",
                            },
                            {
                                "name": "CS_CAGE_LEVEL_REDUNDANCY",
                                "value": "Y",
                                "valueDisplay": "Yes",
                                "nameDisplay": "Cage Level Reduandancy",
                            },
                            {
                                "name": "CS_PERFORMANCE",
                                "value": "P",
                                "valueDisplay": "Performance Up To 1M IOPs",
                                "nameDisplay": "Performance Requirement",
                            },
                            {
                                "name": "CS_ENCRYPTION_REQUIRED",
                                "value": "N",
                                "valueDisplay": "No",
                                "nameDisplay": "Encryption Required",
                            },
                            {
                                "name": "CS_3RD_PARTY_SW",
                                "value": "N",
                                "valueDisplay": "No",
                                "nameDisplay": "3rd Party SW",
                            },
                            {
                                "name": "CS_BASIC_CHOICES2",
                                "value": "XXX",
                                "valueDisplay": "Empty",
                                "nameDisplay": "Basic Choices2",
                            },
                            {
                                "name": "CS_TERM_IN_MONTHS",
                                "value": "36",
                                "valueDisplay": "36",
                                "nameDisplay": "Term in months",
                            },
                            {
                                "name": "CS_WRKLOAD",
                                "value": "MC",
                                "valueDisplay": "Mission Critical 100% avail.",
                                "nameDisplay": "Workload Requirement",
                            },
                            {
                                "name": "CS_PRODUCT_ID",
                                "value": "R9T02AAE",
                                "valueDisplay": "R9T02AAE",
                                "nameDisplay": "Base Product ID",
                            },
                            {
                                "name": "CS_SCREEN_DEP_INVISIBLE",
                                "value": "CS_3RD_PARTY_SW|CS_BASIC_CHOICES|CS_BASIC_CHOICES2|CS_DRIVE_RETENTION|CS_FACTOR_QTY|CS_FIXED_COMMITMENT|CS_HW_LED_MANDATORY_SAAS|CS_INSTALLATION_PRODUCT|CS_POWER_INFRASTRUCTURE|CS_PRICING_MODEL|CS_PRODUCT_CC|CS_PRODUCT_ID|CS_RACK_SERVICE_POWER|CS_RACK_SIZE|CS_RANGE|CS_SALES_BOM_NUMBER|CS_SCREEN_DEP_INVISIBLE|CS_SDCOM_VKOND|CS_SDCOM_VKOND_SINGLE1|CS_SWSC_AAS_HANDLING|CS_TABLE_INDEX|CS_TERM_IN_MONTHS|CS_TERM_IN_MONTHS_MAX_2|CS_TERM_IN_MONTHS_MIN_2",
                                "valueDisplay": "CS_3RD_PARTY_SW|CS_BASIC_CHOICES|CS_BASIC_CHOICES2|CS_DRIVE_RETENTION|CS_FACTOR_QTY|CS_FIXED_COMMITMENT|CS_HW_LED_MANDATORY_SAAS|CS_INSTALLATION_PRODUCT|CS_POWER_INFRASTRUCTURE|CS_PRICING_MODEL|CS_PRODUCT_CC|CS_PRODUCT_ID|CS_RACK_SERVICE_POWER|CS_RACK_SIZE|CS_RANGE|CS_SALES_BOM_NUMBER|CS_SCREEN_DEP_INVISIBLE|CS_SDCOM_VKOND|CS_SDCOM_VKOND_SINGLE1|CS_SWSC_AAS_HANDLING|CS_TABLE_INDEX|CS_TERM_IN_MONTHS|CS_TERM_IN_MONTHS_MAX_2|CS_TERM_IN_MONTHS_MIN_2",
                                "nameDisplay": "Screen Dep Invisible",
                            },
                            {
                                "name": "CS_TIER",
                                "value": "MCP",
                                "valueDisplay": "Mission Critical Performance",
                                "nameDisplay": "Tier",
                            },
                            {
                                "name": "CS_INSTALLATION_PROVIDER",
                                "value": "HPE",
                                "valueDisplay": "HPE",
                                "nameDisplay": "Installation Provider",
                            },
                            {
                                "name": "CS_COMMITMENT_VALUE2",
                                "value": "132000",
                                "valueDisplay": "132000",
                                "nameDisplay": "Commitment UoM2 Value",
                            },
                            {
                                "name": "CS_INSTALLATION_TYPE",
                                "value": "ISS",
                                "valueDisplay": "Installation and Start Up",
                                "nameDisplay": "Installation Type",
                            },
                            {
                                "name": "CS_NET_INT",
                                "value": "ET10GBE",
                                "valueDisplay": "Ethernet - 10 GbE",
                                "nameDisplay": "Network Interface",
                            },
                            {
                                "name": "CS_PRODUCT_CC",
                                "value": "BLST",
                                "valueDisplay": "Block Storage",
                                "nameDisplay": "Product ID for CC",
                            },
                            {
                                "name": "CS_TERM_UOM",
                                "value": "Y",
                                "valueDisplay": "Year(s)",
                                "nameDisplay": "Term Unit Of Measure",
                            },
                            {
                                "name": "CS_SWSC_AAS_HANDLING",
                                "value": "DEV",
                                "valueDisplay": "Device",
                                "nameDisplay": "Software SupChain aaS Handling",
                            },
                            {
                                "name": "CS_RANGE",
                                "value": "STO",
                                "valueDisplay": "Storage",
                                "nameDisplay": "Range",
                            },
                            {
                                "name": "CS_TERM",
                                "value": "3",
                                "valueDisplay": "3",
                                "nameDisplay": "Term",
                            },
                            {
                                "name": "CS_INSTALLATION",
                                "value": "N",
                                "valueDisplay": "No",
                                "nameDisplay": "Installation Required",
                            },
                            {
                                "name": "CS_FIXED_COMMITMENT",
                                "value": "Y",
                                "valueDisplay": "Yes",
                                "nameDisplay": "Fixed Commitment",
                            },
                            {
                                "name": "CS_HW_LED_MANDATORY_SAAS",
                                "value": "N",
                                "valueDisplay": "No",
                                "nameDisplay": "HW Led Mandatory SaaS Flag",
                            },
                            {
                                "name": "CS_TERM_IN_MONTHS_MIN_2",
                                "value": "36",
                                "valueDisplay": "36",
                                "nameDisplay": "Term in months minimum",
                            },
                            {
                                "name": "CS_POWER_INFRASTRUCTURE",
                                "value": "AC",
                                "valueDisplay": "AC",
                                "nameDisplay": "Power Infrastructure",
                            },
                            {
                                "name": "CS_FAN",
                                "value": "FAN4400000",
                                "valueDisplay": "FAN4400000",
                                "nameDisplay": "Fan Number",
                            },
                            {
                                "name": "CS_USAGE_UOM2",
                                "value": "GB",
                                "valueDisplay": "GB",
                                "nameDisplay": "Unit Of Measure 2",
                            },
                            {
                                "name": "CS_PRICING_MODEL",
                                "value": "TIER",
                                "valueDisplay": "Tier",
                                "nameDisplay": "Pricing Model",
                            },
                        ],
                    },
                    "support": [],
                    "licenses": [
                        {
                            "id": "YGUEJYT9E93U",
                            "qty": "1.000",
                            "devices": [],
                            "customer": {},
                            "appointments": {
                                "subscriptionStart": "24.05.2023 00:00:00",
                                "subscriptionEnd": "18.10.2045 00:00:00",
                                "suspensionDate": null,
                                "cancellationDate": null,
                                "reactivationDate": null,
                                "activationDate": "24.05.2023 09:33:48",
                                "duration": "3",
                                "delayedActivation": null,
                                "autoRenewalDate": null,
                            },
                        }
                    ],
                }
            ],
        }
        return sub_storage_baas

    @staticmethod
    def subs_data_default():
        subs_data_payload_default = {
            "reason": "Creation",
            "quote": "string",
            "contract": "string",
            "entitlements": [
                {
                    "lineItem": "string",
                    "quote": "string",
                    "contract": "string",
                    "licenses": [
                        {
                            "id": "string",
                            "customer": {
                                "id": "string",
                                "phone": "string",
                                "postal_code": "string",
                                "address": "string",
                                "city": "string",
                                "state": "str",
                                "country": "str",
                                "company_name": "string",
                                "email": "string",
                            },
                            "qty": "string",
                            "available_qty": "string",
                            "appointments": {
                                "subscriptionStart": "string",
                                "subscriptionEnd": "string",
                                "executionDate": "string",
                                "suspensionDate": "string",
                                "cancellationDate": "string",
                                "reactivationDate": "string",
                                "duration": "string",
                                "activationDate": "string",
                                "delayedActivation": "string",
                                "autoRenewalDate": "string",
                            },
                            "devices": [{"serial": "string", "material": "string"}],
                        }
                    ],
                    "product": {
                        "sku": "string",
                        "legacy": "string",
                        "description": "string",
                        "attributes": [
                            {
                                "name": "string",
                                "value": "string",
                                "nameDisplay": "string",
                                "valueDisplay": "string",
                            }
                        ],
                    },
                    "support": [{"name": "string", "value": "string"}],
                }
            ],
            "activate": {
                "soldTo": "string",
                "soldToName": "string",
                "soldToEmail": "string",
                "shipTo": "string",
                "shipToName": "string",
                "shipToEmail": "string",
                "endUser": "string",
                "endUserName": "string",
                "endUserEmail": "string",
                "reseller": "string",
                "resellerName": "string",
                "resellerEmail": "string",
                "po": "string",
                "resellerPo": "string",
                "endUserPo": "string",
                "orderClass": "string",
                "party": {
                    "id": "string",
                    "function": "AG",
                    "country_id": "string",
                    "global_id": "string",
                },
                "parties": [
                    {
                        "id": "string",
                        "function": "AG",
                        "country_id": "string",
                        "global_id": "string",
                    }
                ],
                "contacts": [{"id": "string", "function": "SM"}],
            },
            "customer": {
                "phone": "string",
                "postal_code": "string",
                "address": "string",
                "city": "string",
                "state": "str",
                "country": "str",
                "company_name": "string",
                "email": "string",
                "mdm": "string",
                "MDM": "string",
            },
            "smcCode": "string",
            "aasType": "IAAS",
        }
        return subs_data_payload_default

    @staticmethod
    def subs_data_ap():
        subs_data_ap_payload = {
            "reason": "Creation",
            "future": False,
            "quote": "3100000453",
            "contract": "5100000111",
            "smcCode": "E",
            "customer": {
                "MDM": "1000937777",
                "phone": "50179505",
                "postal_code": "164 40",
                "address": "Torshamnsgatan 21-23",
                "city": "Kista",
                "country": "SE",
                "state": "",
                "company_name": "ERICSSON AB EAB",
                "email": "goran.matovic@ericsson.com",
            },
            "activate": {
                "soldTo": "Kronborgsgränd 7 Kista SE",
                "soldToName": "ARROW ECS SWEDEN AB",
                "soldToEmail": "ap.ecs.dk@arrow.com",
                "shipTo": "Torshamnsgatan 21-23 Kista SE",
                "shipToName": "ERICSSON AB EAB",
                "shipToEmail": "ptp.incident.management@ericsson.com",
                "endUser": "txpsojc",
                "endUserName": "txpsojc",
                "endUserEmail": "goran.matovic@ericsson.com",
                "reseller": "Kronborgsgränd 1 Kista SE",
                "resellerName": "ATEA SVERIGE AB",
                "resellerEmail": "levresk@atea.se",
                "po": "ARSW_TST4",
                "resellerPo": "",
                "endUserPo": "",
                "orderClass": "ZBRIM",
                "party": {
                    "id": "1000937777",
                    "countryId": "120771848",
                    "globalId": "120771846",
                },
                "parties": [
                    {
                        "function": "AG",
                        "id": "1000831628",
                        "countryId": "121140995",
                        "globalId": "121140994",
                    },
                    {
                        "function": "WE",
                        "id": "1000937777",
                        "countryId": "120771848",
                        "globalId": "120771846",
                    },
                    {
                        "function": "RE",
                        "id": "1000831628",
                        "countryId": "121140995",
                        "globalId": "121140994",
                    },
                    {
                        "function": "RG",
                        "id": "1000831628",
                        "countryId": "121140995",
                        "globalId": "121140994",
                    },
                    {
                        "function": "Z1",
                        "id": "1001063567",
                        "countryId": "121148324",
                        "globalId": "121148323",
                    },
                    {
                        "function": "ZC",
                        "id": "1000937777",
                        "countryId": "120771848",
                        "globalId": "120771846",
                    },
                    {
                        "function": "ZE",
                        "id": "1000937777",
                        "countryId": "120771848",
                        "globalId": "120771846",
                    },
                    {
                        "function": "ZL",
                        "id": "1000937777",
                        "countryId": "120771848",
                        "globalId": "120771846",
                    },
                ],
                "contacts": [
                    {
                        "function": "ZG",
                        "id": "9000202677",
                        "countryId": None,
                        "globalId": None,
                    }
                ],
            },
            "entitlements": [
                {
                    "lineItem": "0000000030",
                    "quote": "3100000453",
                    "contract": "5100000111",
                    "total_qty": "100.000",
                    "available_qty": "0.00",
                    "product": {
                        "sku": "Q9Y59AAS",
                        "legacy": "",
                        "description": "Aruba Central AP Fnd 3yr Sub SaaS",
                        "attributes": [
                            {
                                "name": "BILL_FREQ",
                                "value": "UP",
                                "valueDisplay": "Paid Upfront",
                                "nameDisplay": "Billing Frequency",
                            },
                            {
                                "name": "TERM_IN_MONTHS",
                                "value": "36",
                                "valueDisplay": "36",
                                "nameDisplay": "Term In Months",
                            },
                            {
                                "name": "TERM_IN_MONTHS_MAX_2",
                                "value": "36",
                                "valueDisplay": "36",
                                "nameDisplay": "Term in months maximum",
                            },
                            {
                                "name": "TIER",
                                "value": "FO",
                                "valueDisplay": "Foundation",
                                "nameDisplay": "Tier",
                            },
                            {
                                "name": "HIDE_CHAR",
                                "value": "COMMITMENT_VALUE1|FIXED_COMMITMENT|PREPAID_AMT|PRICING_MODEL",
                                "valueDisplay": "COMMITMENT_VALUE1|FIXED_COMMITMENT|PREPAID_AMT|PRICING_MODEL",
                                "nameDisplay": "Characteristic Name",
                            },
                            {
                                "name": "INVOICING_MODEL",
                                "value": "UP",
                                "valueDisplay": "Paid Upfront",
                                "nameDisplay": "Invoicing Model",
                            },
                            {
                                "name": "TERM_UOM",
                                "value": "Y",
                                "valueDisplay": "Year(s)",
                                "nameDisplay": "Term Unit of Measure",
                            },
                            {
                                "name": "TERM_IN_MONTHS_MIN_2",
                                "value": "12",
                                "valueDisplay": "12",
                                "nameDisplay": "Term in months minimum",
                            },
                            {
                                "name": "TERM",
                                "value": "3",
                                "valueDisplay": "3",
                                "nameDisplay": "Term",
                            },
                            {
                                "name": "TIER_AP",
                                "value": "FO",
                                "valueDisplay": "Foundation",
                                "nameDisplay": "Access Point Tier",
                            },
                        ],
                    },
                    "support": [
                        {
                            "name": "CS_TCS_CONTRACT_TYPE",
                            "value": "FC",
                            "valueDisplay": "Foundation Care",
                            "nameDisplay": "Contract Type",
                        },
                        {
                            "name": "SUPPORT_TIER",
                            "value": "FC",
                            "valueDisplay": "Foundation Care",
                            "nameDisplay": "Support Tier",
                        },
                        {
                            "name": "CS_TCS_TECH_SUPPORT",
                            "value": "Y",
                            "valueDisplay": "Year(s)",
                            "nameDisplay": "Technical Support",
                        },
                        {
                            "name": "CS_TCS_TECH_GUIDANCE",
                            "value": "Y",
                            "valueDisplay": "Year(s)",
                            "nameDisplay": "General Technical Guidance",
                        },
                        {
                            "name": "TERM_UOM",
                            "value": "Y",
                            "valueDisplay": "Year(s)",
                            "nameDisplay": "Term Unit of Measure",
                        },
                        {
                            "name": "CS_TCS_RESPONSE_TIME",
                            "value": "2HR",
                            "valueDisplay": "2 Hours",
                            "nameDisplay": "Response Time",
                        },
                        {
                            "name": "CS_TERM_UOM",
                            "value": "Y",
                            "valueDisplay": "Year(s)",
                            "nameDisplay": "Term Unit Of Measure",
                        },
                        {
                            "name": "CS_TCS_COV_WINDOW7",
                            "value": "24",
                            "valueDisplay": "24 Hours",
                            "nameDisplay": "Coverage Window 24x7",
                        },
                        {
                            "name": "TERM",
                            "value": "3",
                            "valueDisplay": "3",
                            "nameDisplay": "Term",
                        },
                        {
                            "name": "CS_TCS_COLLAB_SUPPORT",
                            "value": "Y",
                            "valueDisplay": "Year(s)",
                            "nameDisplay": "Collaborative Supp and Assist",
                        },
                        {
                            "name": "CS_TCS_SERVICE_LEVEL",
                            "value": "ESS",
                            "valueDisplay": "Essential",
                            "nameDisplay": "Service Level",
                        },
                        {
                            "name": "CS_TERM",
                            "value": "3",
                            "valueDisplay": "3",
                            "nameDisplay": "Term",
                        },
                    ],
                    "licenses": [
                        {
                            "id": "PAYGHCUECD6U66",
                            "qty": "100.000",
                            "devices": [],
                            "customer": {},
                            "appointments": {
                                "subscriptionStart": "04.01.2023 00:00:00",
                                "subscriptionEnd": "04.01.2026 00:00:00",
                                "suspensionDate": None,
                                "cancellationDate": None,
                                "reactivationDate": None,
                                "activationDate": "04.01.2023 14:26:59",
                                "duration": "3",
                                "delayedActivation": None,
                                "autoRenewalDate": None,
                            },
                        }
                    ],
                }
            ],
        }
        return subs_data_ap_payload

    @staticmethod
    def subs_data_sw_6200():
        null = None
        subs_data_sw_6200_payload = {
            "reason": "Creation",
            "future": False,
            "quote": "6000210273",
            "contract": "2000043261",
            "smcCode": "E",
            "customer": {
                "MDM": "1000023264",
                "phone": "",
                "postal_code": "33760-3155",
                "address": "5350 Tech Data Dr",
                "city": "Clearwater",
                "country": "US",
                "state": "",
                "company_name": "TECH DATA CORPORATION",
                "email": "Simha@gmail.com",
            },
            "activate": {
                "soldTo": "44201 Nobel Drive FREMONT US",
                "soldToName": "TD SYNNEX CORPORATION",
                "soldToEmail": "narahari.n@hpe.com",
                "shipTo": "5350 Tech Data Dr Clearwater US",
                "shipToName": "TECH DATA CORPORATION",
                "shipToEmail": "",
                "endUser": "5350 Tech Data Dr Clearwater US",
                "endUserName": "TECH DATA CORPORATION",
                "endUserEmail": "Simha@gmail.com",
                "reseller": "300 Spectrum Center Dr Ste 100 Irvine US",
                "resellerName": "ENTERPRISE COMPUTING SOLUTIONS, INC.",
                "resellerEmail": "kollisetti@hpe.com",
                "po": "TEST-341RAMP",
                "resellerPo": "",
                "endUserPo": "",
                "orderClass": "ZBRIM",
                "party": {
                    "id": "1000023264",
                    "countryId": "121482897",
                    "globalId": "121105452",
                },
                "parties": [
                    {
                        "function": "AG",
                        "id": "1000939629",
                        "countryId": "121482897",
                        "globalId": "121105452",
                    },
                    {
                        "function": "WE",
                        "id": "2002082346",
                        "countryId": null,
                        "globalId": null,
                    },
                    {
                        "function": "RE",
                        "id": "1000939629",
                        "countryId": "121482897",
                        "globalId": "121105452",
                    },
                    {
                        "function": "RG",
                        "id": "1000939629",
                        "countryId": "121482897",
                        "globalId": "121105452",
                    },
                    {
                        "function": "Z1",
                        "id": "1000023046",
                        "countryId": "120424886",
                        "globalId": "120424885",
                    },
                    {
                        "function": "ZC",
                        "id": "1000023264",
                        "countryId": "121482897",
                        "globalId": "121105452",
                    },
                    {
                        "function": "ZE",
                        "id": "1000023264",
                        "countryId": "121482897",
                        "globalId": "121105452",
                    },
                    {
                        "function": "ZL",
                        "id": "1000023264",
                        "countryId": "121482897",
                        "globalId": "121105452",
                    },
                ],
                "contacts": [
                    {
                        "function": "CS",
                        "id": "9000975555",
                        "countryId": null,
                        "globalId": null,
                    },
                    {
                        "function": "RT",
                        "id": "9001139386",
                        "countryId": null,
                        "globalId": null,
                    },
                    {
                        "function": "ZG",
                        "id": "9000125290",
                        "countryId": null,
                        "globalId": null,
                    },
                ],
            },
            "entitlements": [
                {
                    "lineItem": "0000000010",
                    "quote": "6000210273",
                    "contract": "2000043261",
                    "total_qty": "1.000",
                    "available_qty": "0.00",
                    "product": {
                        "sku": "Q9Y76AAS",
                        "legacy": "",
                        "description": "Aruba Central 62/29xx F 7y SaaS",
                        "attributes": [
                            {
                                "name": "BILL_FREQ",
                                "value": "UP",
                                "valueDisplay": "Paid Upfront",
                                "nameDisplay": "BILLING FREQUENCY",
                            },
                            {
                                "name": "TERM_IN_MONTHS",
                                "value": "84",
                                "valueDisplay": "84",
                                "nameDisplay": "Term In Months",
                            },
                            {
                                "name": "TERM_IN_MONTHS_MAX_2",
                                "value": "84",
                                "valueDisplay": "84",
                                "nameDisplay": "Term in months maximum",
                            },
                            {
                                "name": "TIER",
                                "value": "FO",
                                "valueDisplay": "Foundation",
                                "nameDisplay": "Tier",
                            },
                            {
                                "name": "HIDE_CHAR",
                                "value": "COMMITMENT_VALUE1|FIXED_COMMITMENT|PRICING_MODEL",
                                "valueDisplay": "COMMITMENT_VALUE1|FIXED_COMMITMENT|PRICING_MODEL",
                                "nameDisplay": "HIDE CHARACTERISTICS",
                            },
                            {
                                "name": "INVOICING_MODEL",
                                "value": "UP",
                                "valueDisplay": "Paid Upfront",
                                "nameDisplay": "INVOICING MODEL",
                            },
                            {
                                "name": "PRODUCT_CC",
                                "value": "CENTRAL_SW",
                                "valueDisplay": "Central_SW",
                                "nameDisplay": "Product ID for CC",
                            },
                            {
                                "name": "TERM_UOM",
                                "value": "Y",
                                "valueDisplay": "Year(s)",
                                "nameDisplay": "Term Unit of Measure",
                            },
                            {
                                "name": "TERM_IN_MONTHS_MIN_2",
                                "value": "60",
                                "valueDisplay": "60",
                                "nameDisplay": "Term in months minimum",
                            },
                            {
                                "name": "TERM",
                                "value": "7",
                                "valueDisplay": "7",
                                "nameDisplay": "Term",
                            },
                            {
                                "name": "PRODUCT_ID",
                                "value": "JN002AAS",
                                "valueDisplay": "JN002AAS",
                                "nameDisplay": "Product ID",
                            },
                            {
                                "name": "SW_FAMILY",
                                "value": "62XX",
                                "valueDisplay": "62XX",
                                "nameDisplay": "Switch Family",
                            },
                        ],
                    },
                    "support": [
                        {
                            "name": "SUPPORT_TIER",
                            "value": "FC",
                            "valueDisplay": "Foundation Care",
                            "nameDisplay": "Support Tier",
                        },
                        {
                            "name": "TERM_UOM",
                            "value": "Y",
                            "valueDisplay": "Year(s)",
                            "nameDisplay": "Term Unit of Measure",
                        },
                        {
                            "name": "TERM",
                            "value": "7",
                            "valueDisplay": "7",
                            "nameDisplay": "Term",
                        },
                    ],
                    "licenses": [
                        {
                            "id": "PAYGHUYHH5AHC6",
                            "qty": "1.000",
                            "devices": [],
                            "customer": {},
                            "appointments": {
                                "subscriptionStart": "21.03.2023 00:00:00",
                                "subscriptionEnd": "21.03.2030 00:00:00",
                                "suspensionDate": null,
                                "cancellationDate": null,
                                "reactivationDate": null,
                                "activationDate": "07.03.2023 08:25:40",
                                "duration": "7",
                                "delayedActivation": null,
                                "autoRenewalDate": null,
                            },
                        }
                    ],
                }
            ],
        }
        return subs_data_sw_6200_payload

    @staticmethod
    def subs_data_sw_6300():
        null = None
        subs_data_sw_6300_payload = {
            "reason": "Creation",
            "future": False,
            "quote": "6000212238",
            "contract": "2000043706",
            "smcCode": "E",
            "aasType": "IAAS",
            "customer": {
                "MDM": "1013199818",
                "phone": "",
                "postal_code": "70124",
                "address": "8000 Lakeshore Dr",
                "city": "New Orleans",
                "country": "US",
                "state": "LA",
                "company_name": "LANDRYS",
                "email": "kevin.balmaceda@hpe.com",
            },
            "activate": {
                "soldTo": "8000 Lakeshore Dr New Orleans US",
                "soldToName": "LANDRYS",
                "soldToEmail": "",
                "shipTo": "8000 Lakeshore Dr New Orleans US",
                "shipToName": "LANDRYS",
                "shipToEmail": "alma.ber.garcia-soto@hpe.com",
                "endUser": "8000 Lakeshore Dr New Orleans US",
                "endUserName": "LANDRYS",
                "endUserEmail": "kevin.balmaceda@hpe.com",
                "po": "end2end27_03",
                "resellerPo": "",
                "endUserPo": "",
                "orderClass": "ZBRIM",
                "party": {"id": "1013199818", "countryId": null, "globalId": null},
                "parties": [
                    {
                        "function": "AG",
                        "id": "1013199818",
                        "countryId": null,
                        "globalId": null,
                    },
                    {
                        "function": "WE",
                        "id": "1013199818",
                        "countryId": null,
                        "globalId": null,
                    },
                    {
                        "function": "RE",
                        "id": "1013199818",
                        "countryId": null,
                        "globalId": null,
                    },
                    {
                        "function": "RG",
                        "id": "1013199818",
                        "countryId": null,
                        "globalId": null,
                    },
                    {
                        "function": "ZC",
                        "id": "1013199818",
                        "countryId": null,
                        "globalId": null,
                    },
                    {
                        "function": "ZE",
                        "id": "1013199818",
                        "countryId": null,
                        "globalId": null,
                    },
                    {
                        "function": "ZL",
                        "id": "1013199818",
                        "countryId": null,
                        "globalId": null,
                    },
                ],
                "contacts": [
                    {
                        "function": "ZG",
                        "id": "9000990693",
                        "countryId": null,
                        "globalId": null,
                    }
                ],
            },
            "entitlements": [
                {
                    "lineItem": "0000000070",
                    "quote": "6000212238",
                    "contract": "2000043706",
                    "total_qty": "1.000",
                    "available_qty": "0.00",
                    "product": {
                        "sku": "FSB_ARUBA_AGG",
                        "legacy": "",
                        "description": "FSB ARUBA AGG",
                        "attributes": [
                            {
                                "name": "CS_AGG_CORE_HW",
                                "value": "JL662A",
                                "valueDisplay": "JL662A 24G CL4 PoE 4SFP56",
                                "nameDisplay": "Aruba Agg Switch HW",
                            },
                            {
                                "name": "CS_INVOICING_MODEL",
                                "value": "SU",
                                "valueDisplay": "Subscription",
                                "nameDisplay": "Invoicing Model",
                            },
                            {
                                "name": "CS_NET_TIER",
                                "value": "FO",
                                "valueDisplay": "Foundation",
                                "nameDisplay": "Aruba Tier Values",
                            },
                            {
                                "name": "TERM_IN_MONTHS",
                                "value": "36",
                                "valueDisplay": "36",
                                "nameDisplay": "Term In Months",
                            },
                            {
                                "name": "CS_BILL_FREQ",
                                "value": "M",
                                "valueDisplay": "Monthly",
                                "nameDisplay": "Billing Frequency",
                            },
                            {
                                "name": "TIER",
                                "value": "FO",
                                "valueDisplay": "Foundation",
                                "nameDisplay": "Tier",
                            },
                            {
                                "name": "HIDE_CHAR",
                                "value": "BILL_FREQ|CS_PRODUCT_ID|EVERGREEN|HP_BASIC_CHOICES|HP_STD_COMPONENT|INVOICING_MODEL|NO_OF_SW|SDCOM_VKOND|TIER",
                                "valueDisplay": "BILL_FREQ|CS_PRODUCT_ID|EVERGREEN|HP_BASIC_CHOICES|HP_STD_COMPONENT|INVOICING_MODEL|NO_OF_SW|SDCOM_VKOND|TIER",
                                "nameDisplay": "HIDE CHARACTERISTICS",
                            },
                            {
                                "name": "TERM_IN_MONTHS_MIN_2",
                                "value": "12",
                                "valueDisplay": "12",
                                "nameDisplay": "Term in months minimum",
                            },
                            {
                                "name": "SW_FAMILY",
                                "value": "63XX",
                                "valueDisplay": "63XX",
                                "nameDisplay": "Switch Family",
                            },
                            {
                                "name": "BILL_FREQ",
                                "value": "M",
                                "valueDisplay": "Monthly",
                                "nameDisplay": "BILLING FREQUENCY",
                            },
                            {
                                "name": "CS_NET_HW_VAR",
                                "value": "JL086A-1#ABA",
                                "valueDisplay": "JL086A-1#ABA",
                                "nameDisplay": "Concatenate of Loc./Reg. Opt.",
                            },
                            {
                                "name": "CS_WIRE_POWER_SUPPLY",
                                "value": "JL086A-1",
                                "valueDisplay": "680W AC",
                                "nameDisplay": "Power Supply Options",
                            },
                            {
                                "name": "TERM_IN_MONTHS_MAX_2",
                                "value": "36",
                                "valueDisplay": "36",
                                "nameDisplay": "Term in months maximum",
                            },
                            {
                                "name": "CS_TERM_ALPHANUM",
                                "value": "_36",
                                "valueDisplay": "_36",
                                "nameDisplay": "Alphanumeric Value for Term",
                            },
                            {
                                "name": "INVOICING_MODEL",
                                "value": "SU",
                                "valueDisplay": "Subscription",
                                "nameDisplay": "INVOICING MODEL",
                            },
                            {
                                "name": "CS_NET_PWR_CORD",
                                "value": "#ABA",
                                "valueDisplay": "US",
                                "nameDisplay": "Aruba Localizations",
                            },
                            {
                                "name": "CS_TERM_UOM",
                                "value": "Y",
                                "valueDisplay": "Year(s)",
                                "nameDisplay": "Term Unit Of Measure",
                            },
                            {
                                "name": "HP_STD_COMPONENT",
                                "value": "1",
                                "valueDisplay": "1",
                                "nameDisplay": "STD COMP FOR PLANNING",
                            },
                            {
                                "name": "CS_FOUND_CARE_SUPPORT",
                                "value": "NBDEXHW",
                                "valueDisplay": "Next Business Day HW Exchange",
                                "nameDisplay": "Foundation Care Support",
                            },
                            {
                                "name": "CS_TERM",
                                "value": "3",
                                "valueDisplay": "3",
                                "nameDisplay": "Term",
                            },
                        ],
                    },
                    "support": [],
                    "licenses": [
                        {
                            "id": "IAASYGHUUU43UU66",
                            "qty": "1.000",
                            "devices": [{"serial": "AB7812009668", "material": "R3V49A"}],
                            "customer": {},
                            "appointments": {
                                "subscriptionStart": "16.03.2023 00:00:00",
                                "subscriptionEnd": "16.03.2026 00:00:00",
                                "suspensionDate": null,
                                "cancellationDate": null,
                                "reactivationDate": null,
                                "activationDate": "15.03.2023 12:58:11",
                                "duration": "3",
                                "delayedActivation": null,
                                "autoRenewalDate": null,
                            },
                        }
                    ],
                }
            ],
        }
        return subs_data_sw_6300_payload

    @staticmethod
    def subs_data_gw_70xx():
        null = None
        subs_data_gw_70xx_payload = {
            "reason": "Creation",
            "future": False,
            "quote": "6000203085",
            "contract": "2000045651",
            "smcCode": "E",
            "customer": {
                "MDM": "1000283737",
                "phone": "7709324084",
                "postal_code": "30024-3634",
                "address": "3055 Shawnee Industrial Way",
                "city": "Suwanee",
                "country": "US",
                "state": "GA",
                "company_name": "TECH DATA CORPORATION LTD",
                "email": "mani@gmail.com",
            },
            "activate": {
                "soldTo": "2525 N 7TH ST HARRISBURG US",
                "soldToName": "D&H DISTRIBUTING CO.",
                "soldToEmail": "",
                "shipTo": "3055 Shawnee Industrial Way Suwanee US",
                "shipToName": "TECH DATA CORPORATION LTD",
                "shipToEmail": "",
                "endUser": "3055 Shawnee Industrial Way Suwanee US",
                "endUserName": "TECH DATA CORPORATION SMTEST ONLY",
                "endUserEmail": "mani@gmail.com",
                "reseller": "770 The City Dr S Ste 5300 Orange US",
                "resellerName": "CB TECHNOLOGIES, INC.",
                "resellerEmail": "",
                "po": "6000203085",
                "resellerPo": "",
                "endUserPo": "",
                "orderClass": "ZBRIM",
                "party": {
                    "id": "1000283737",
                    "countryId": "121482897",
                    "globalId": "121105452",
                },
                "parties": [
                    {
                        "function": "AG",
                        "id": "1000748499",
                        "countryId": "121481984",
                        "globalId": "121468769",
                    },
                    {
                        "function": "WE",
                        "id": "1000283737",
                        "countryId": "121482897",
                        "globalId": "121105452",
                    },
                    {
                        "function": "RE",
                        "id": "1000283737",
                        "countryId": "121482897",
                        "globalId": "121105452",
                    },
                    {
                        "function": "RG",
                        "id": "1000748499",
                        "countryId": "121481984",
                        "globalId": "121468769",
                    },
                    {
                        "function": "Z1",
                        "id": "1000004938",
                        "countryId": "121573676",
                        "globalId": "121573675",
                    },
                    {
                        "function": "ZC",
                        "id": "1000283737",
                        "countryId": "121482897",
                        "globalId": "121105452",
                    },
                    {
                        "function": "ZE",
                        "id": "1000748499",
                        "countryId": "121481984",
                        "globalId": "121468769",
                    },
                    {
                        "function": "ZL",
                        "id": "1000283737",
                        "countryId": "121482897",
                        "globalId": "121105452",
                    },
                ],
                "contacts": [
                    {
                        "function": "ZG",
                        "id": "9000219135",
                        "countryId": null,
                        "globalId": null,
                    }
                ],
            },
            "entitlements": [
                {
                    "lineItem": "0000000030",
                    "quote": "6000203085",
                    "contract": "2000045651",
                    "total_qty": "1.000",
                    "available_qty": "0.00",
                    "product": {
                        "sku": "JN003AAS",
                        "legacy": "",
                        "description": "Aruba Central SDWAN 7005 GW Foundation Year(s) SUB Saas",
                        "attributes": [
                            {
                                "name": "TERM_IN_MONTHS",
                                "value": "12",
                                "valueDisplay": "12",
                                "nameDisplay": "Term In Months",
                            },
                            {
                                "name": "TIER",
                                "value": "FO",
                                "valueDisplay": "Foundation",
                                "nameDisplay": "Tier",
                            },
                            {
                                "name": "HIDE_CHAR",
                                "value": "COMMITMENT_VALUE1|EVERGREEN|FIXED_COMMITMENT|PRICING_MODEL|TERM|TERM_UOM|TIER_GW",
                                "valueDisplay": "COMMITMENT_VALUE1|EVERGREEN|FIXED_COMMITMENT|PRICING_MODEL|TERM|TERM_UOM|TIER_GW",
                                "nameDisplay": "HIDE CHARACTERISTICS",
                            },
                            {
                                "name": "TERM_UOM",
                                "value": "Y",
                                "valueDisplay": "Year(s)",
                                "nameDisplay": "Term Unit of Measure",
                            },
                            {
                                "name": "TERM_IN_MONTHS_MIN_2",
                                "value": "0",
                                "valueDisplay": "0",
                                "nameDisplay": "Term in months minimum",
                            },
                            {
                                "name": "PRODUCT_ID",
                                "value": "JN003AAS",
                                "valueDisplay": "JN003AAS",
                                "nameDisplay": "Product ID",
                            },
                            {
                                "name": "GW_FAMILY",
                                "value": "7005",
                                "valueDisplay": "7005",
                                "nameDisplay": "Gateway Family",
                            },
                            {
                                "name": "BILL_FREQ",
                                "value": "M",
                                "valueDisplay": "Monthly",
                                "nameDisplay": "BILLING FREQUENCY",
                            },
                            {
                                "name": "SP_HIDE_CHAR1",
                                "value": "TERM",
                                "valueDisplay": "TERM",
                                "nameDisplay": "Characteristic Name",
                            },
                            {
                                "name": "QUANTITY_2",
                                "value": "1",
                                "valueDisplay": "1",
                                "nameDisplay": "CRM: Order Quantity",
                            },
                            {
                                "name": "SP_HIDE_CHAR2",
                                "value": "TERM_UOM",
                                "valueDisplay": "TERM_UOM",
                                "nameDisplay": "Characteristic Name",
                            },
                            {
                                "name": "TERM_IN_MONTHS_MAX_2",
                                "value": "12",
                                "valueDisplay": "12",
                                "nameDisplay": "Term in months maximum",
                            },
                            {
                                "name": "INVOICING_MODEL",
                                "value": "SU",
                                "valueDisplay": "Subscription",
                                "nameDisplay": "INVOICING MODEL",
                            },
                            {
                                "name": "PRODUCT_CC",
                                "value": "CENTRAL_GW",
                                "valueDisplay": "Central_GW",
                                "nameDisplay": "Product ID for CC",
                            },
                            {
                                "name": "CS_TERM_UOM",
                                "value": "Y",
                                "valueDisplay": "Year(s)",
                                "nameDisplay": "Term Unit Of Measure",
                            },
                            {
                                "name": "GW_TYPE",
                                "value": "SDWAN",
                                "valueDisplay": "SDWAN",
                                "nameDisplay": "Gateway Type",
                            },
                            {
                                "name": "CS_TERM",
                                "value": "1",
                                "valueDisplay": "1",
                                "nameDisplay": "Term",
                            },
                        ],
                    },
                    "support": [
                        {
                            "name": "CS_TCS_CONTRACT_TYPE",
                            "value": "TC",
                            "valueDisplay": "TechCare",
                            "nameDisplay": "Contract Type",
                        },
                        {
                            "name": "SUPPORT_TIER",
                            "value": "FC",
                            "valueDisplay": "Foundation Care",
                            "nameDisplay": "Support Tier",
                        },
                        {
                            "name": "CS_TCS_TECH_SUPPORT",
                            "value": "Y",
                            "valueDisplay": "Year(s)",
                            "nameDisplay": "Technical Support",
                        },
                        {
                            "name": "SP_HIDE_CHAR1",
                            "value": "TERM",
                            "valueDisplay": "TERM",
                            "nameDisplay": "Characteristic Name",
                        },
                        {
                            "name": "CS_TCS_TECH_GUIDANCE",
                            "value": "Y",
                            "valueDisplay": "Year(s)",
                            "nameDisplay": "General Technical Guidance",
                        },
                        {
                            "name": "SP_HIDE_CHAR2",
                            "value": "TERM_UOM",
                            "valueDisplay": "TERM_UOM",
                            "nameDisplay": "Characteristic Name",
                        },
                        {
                            "name": "CS_TCS_RESPONSE_TIME",
                            "value": "2HR",
                            "valueDisplay": "2 Hours",
                            "nameDisplay": "Response Time",
                        },
                        {
                            "name": "CS_TERM_UOM",
                            "value": "Y",
                            "valueDisplay": "Year(s)",
                            "nameDisplay": "Term Unit Of Measure",
                        },
                        {
                            "name": "CS_TCS_COV_WINDOW7",
                            "value": "24",
                            "valueDisplay": "24 Hours",
                            "nameDisplay": "Coverage Window 24x7",
                        },
                        {
                            "name": "CS_TCS_COLLAB_SUPPORT",
                            "value": "Y",
                            "valueDisplay": "Year(s)",
                            "nameDisplay": "Collaborative Supp and Assist",
                        },
                        {
                            "name": "CS_TCS_SERVICE_LEVEL",
                            "value": "ESS",
                            "valueDisplay": "Essential",
                            "nameDisplay": "Service Level",
                        },
                        {
                            "name": "CS_TERM",
                            "value": "1",
                            "valueDisplay": "1",
                            "nameDisplay": "Term",
                        },
                    ],
                    "licenses": [
                        {
                            "id": "PAYGHEUDY5A9D7",
                            "qty": "1.000",
                            "devices": [],
                            "customer": {},
                            "appointments": {
                                "subscriptionStart": "27.04.2023 00:00:00",
                                "subscriptionEnd": "27.04.2034 00:00:00",
                                "suspensionDate": null,
                                "cancellationDate": null,
                                "reactivationDate": null,
                                "activationDate": "26.04.2023 00:02:02",
                                "duration": "1",
                                "delayedActivation": "27.04.2023 00:00:00",
                                "autoRenewalDate": null,
                            },
                        }
                    ],
                }
            ],
        }
        return subs_data_gw_70xx_payload

    @staticmethod
    def subs_data_gw_72xx():
        null = None
        subs_data_gw_72xx_payload = {
            "reason": "Creation",
            "future": False,
            "quote": "6000216574",
            "contract": "2000044016",
            "smcCode": "E",
            "customer": {
                "MDM": "1013199818",
                "phone": "",
                "postal_code": "70124",
                "address": "8000 Lakeshore Dr",
                "city": "New Orleans",
                "country": "US",
                "state": "LA",
                "company_name": "LANDRYS",
                "email": "kevin.balmaceda@hpe.com",
            },
            "activate": {
                "soldTo": "8000 Lakeshore Dr New Orleans US",
                "soldToName": "LANDRYS",
                "soldToEmail": "",
                "shipTo": "8000 Lakeshore Dr New Orleans US",
                "shipToName": "LANDRYS",
                "shipToEmail": "alma.ber.garcia-soto@hpe.com",
                "endUser": "8000 Lakeshore Dr New Orleans US",
                "endUserName": "LANDRYS",
                "endUserEmail": "kevin.balmaceda@hpe.com",
                "po": "6000216574",
                "resellerPo": "",
                "endUserPo": "",
                "orderClass": "ZBRIM",
                "party": {"id": "1013199818", "countryId": null, "globalId": null},
                "parties": [
                    {
                        "function": "AG",
                        "id": "1013199818",
                        "countryId": null,
                        "globalId": null,
                    },
                    {
                        "function": "WE",
                        "id": "1013199818",
                        "countryId": null,
                        "globalId": null,
                    },
                    {
                        "function": "RE",
                        "id": "1013199818",
                        "countryId": null,
                        "globalId": null,
                    },
                    {
                        "function": "RG",
                        "id": "1013199818",
                        "countryId": null,
                        "globalId": null,
                    },
                    {
                        "function": "ZC",
                        "id": "1013199818",
                        "countryId": null,
                        "globalId": null,
                    },
                    {
                        "function": "ZE",
                        "id": "1013199818",
                        "countryId": null,
                        "globalId": null,
                    },
                    {
                        "function": "ZL",
                        "id": "1013199818",
                        "countryId": null,
                        "globalId": null,
                    },
                ],
                "contacts": [
                    {
                        "function": "ZG",
                        "id": "9000990693",
                        "countryId": null,
                        "globalId": null,
                    }
                ],
            },
            "entitlements": [
                {
                    "lineItem": "0000000010",
                    "quote": "6000216574",
                    "contract": "2000044016",
                    "total_qty": "1.000",
                    "available_qty": "0.00",
                    "product": {
                        "sku": "JZ198AAS",
                        "legacy": "",
                        "description": "Aruba72xxGatewayAdv1yrSubSaaS",
                        "attributes": [
                            {
                                "name": "TERM_IN_MONTHS",
                                "value": "12",
                                "valueDisplay": "12",
                                "nameDisplay": "Term In Months",
                            },
                            {
                                "name": "TIER",
                                "value": "AD",
                                "valueDisplay": "Advanced",
                                "nameDisplay": "Tier",
                            },
                            {
                                "name": "HIDE_CHAR",
                                "value": "COMMITMENT_VALUE1|EVERGREEN|FIXED_COMMITMENT|PRICING_MODEL",
                                "valueDisplay": "COMMITMENT_VALUE1|EVERGREEN|FIXED_COMMITMENT|PRICING_MODEL",
                                "nameDisplay": "HIDE CHARACTERISTICS",
                            },
                            {
                                "name": "TERM_UOM",
                                "value": "Y",
                                "valueDisplay": "Year(s)",
                                "nameDisplay": "Term Unit of Measure",
                            },
                            {
                                "name": "TERM_IN_MONTHS_MIN_2",
                                "value": "0",
                                "valueDisplay": "0",
                                "nameDisplay": "Term in months minimum",
                            },
                            {
                                "name": "TERM",
                                "value": "1",
                                "valueDisplay": "1",
                                "nameDisplay": "Term",
                            },
                            {
                                "name": "PRODUCT_ID",
                                "value": "JN003AAS",
                                "valueDisplay": "JN003AAS",
                                "nameDisplay": "Product ID",
                            },
                            {
                                "name": "GW_FAMILY",
                                "value": "7200",
                                "valueDisplay": "7200",
                                "nameDisplay": "Gateway Family",
                            },
                            {
                                "name": "BILL_FREQ",
                                "value": "UP",
                                "valueDisplay": "Upfront",
                                "nameDisplay": "BILLING FREQUENCY",
                            },
                            {
                                "name": "SP_HIDE_CHAR1",
                                "value": "TERM",
                                "valueDisplay": "TERM",
                                "nameDisplay": "Characteristic Name",
                            },
                            {
                                "name": "SP_HIDE_CHAR2",
                                "value": "TERM_UOM",
                                "valueDisplay": "TERM_UOM",
                                "nameDisplay": "Characteristic Name",
                            },
                            {
                                "name": "TERM_IN_MONTHS_MAX_2",
                                "value": "12",
                                "valueDisplay": "12",
                                "nameDisplay": "Term in months maximum",
                            },
                            {
                                "name": "INVOICING_MODEL",
                                "value": "UP",
                                "valueDisplay": "Upfront",
                                "nameDisplay": "INVOICING MODEL",
                            },
                            {
                                "name": "PRODUCT_CC",
                                "value": "CENTRAL_GW",
                                "valueDisplay": "Central_GW",
                                "nameDisplay": "Product ID for CC",
                            },
                            {
                                "name": "CS_TERM_UOM",
                                "value": "Y",
                                "valueDisplay": "Year(s)",
                                "nameDisplay": "Term Unit Of Measure",
                            },
                            {
                                "name": "GW_TYPE",
                                "value": "SDWAN",
                                "valueDisplay": "SDWAN",
                                "nameDisplay": "Gateway Type",
                            },
                            {
                                "name": "TIER_GW",
                                "value": "AD",
                                "valueDisplay": "Advanced",
                                "nameDisplay": "Gateway Tier",
                            },
                            {
                                "name": "CS_TERM",
                                "value": "1",
                                "valueDisplay": "1",
                                "nameDisplay": "Term",
                            },
                        ],
                    },
                    "support": [
                        {
                            "name": "SUPPORT_TIER",
                            "value": "FC",
                            "valueDisplay": "Foundation Care",
                            "nameDisplay": "Support Tier",
                        },
                        {
                            "name": "TERM_UOM",
                            "value": "Y",
                            "valueDisplay": "Year(s)",
                            "nameDisplay": "Term Unit of Measure",
                        },
                        {
                            "name": "CS_TERM_UOM",
                            "value": "Y",
                            "valueDisplay": "Year(s)",
                            "nameDisplay": "Term Unit Of Measure",
                        },
                        {
                            "name": "TERM",
                            "value": "1",
                            "valueDisplay": "1",
                            "nameDisplay": "Term",
                        },
                        {
                            "name": "CS_TERM",
                            "value": "1",
                            "valueDisplay": "1",
                            "nameDisplay": "Term",
                        },
                    ],
                    "licenses": [
                        {
                            "id": "PAYGHJ3U3E4HTE",
                            "qty": "1.000",
                            "devices": [],
                            "customer": {},
                            "appointments": {
                                "subscriptionStart": "21.03.2023 00:00:00",
                                "subscriptionEnd": "21.03.2024 00:00:00",
                                "suspensionDate": null,
                                "cancellationDate": null,
                                "reactivationDate": null,
                                "activationDate": "21.03.2023 07:24:52",
                                "duration": "1",
                                "delayedActivation": null,
                                "autoRenewalDate": null,
                            },
                        }
                    ],
                }
            ],
        }
        return subs_data_gw_72xx_payload

    @staticmethod
    def subs_data_vgw_500():
        null = None
        subs_data_vgw_500_payload = {
            "reason": "Creation",
            "quote": "6000207485",
            "contract": "2000042707",
            "smcCode": "E",
            "customer": {
                "MDM": "1037086683",
                "phone": "",
                "postal_code": "49412-1812",
                "address": "502 CONNIE AVE",
                "city": "FREMONT",
                "country": "US",
                "state": "MI",
                "company_name": "DURA AUTOMOTIVE SYSTEMS",
                "email": "maria-s@hpe.com",
            },
            "activate": {
                "soldTo": "502 CONNIE AVE FREMONT US",
                "soldToName": "DURA AUTOMOTIVE SYSTEMS",
                "soldToEmail": "danut-alexandru.iordache@hpe.com",
                "shipTo": "502 CONNIE AVE FREMONT US",
                "shipToName": "DURA AUTOMOTIVE SYSTEMS",
                "shipToEmail": "danut-alexandru.iordache@hpe.com",
                "endUser": "502 CONNIE AVE FREMONT US",
                "endUserName": "DURA AUTOMOTIVE SYSTEMS",
                "endUserEmail": "maria-s@hpe.com",
                "po": "SPID828372817",
                "resellerPo": "",
                "endUserPo": "",
                "orderClass": "ZBRIM",
                "party": {
                    "id": "1037086683",
                    "countryId": "121450124",
                    "globalId": "121450117",
                },
                "parties": [
                    {
                        "function": "AG",
                        "id": "1037086683",
                        "countryId": "121450124",
                        "globalId": "121450117",
                    },
                    {
                        "function": "WE",
                        "id": "1037086683",
                        "countryId": "121450124",
                        "globalId": "121450117",
                    },
                    {
                        "function": "RE",
                        "id": "1037086683",
                        "countryId": "121450124",
                        "globalId": "121450117",
                    },
                    {
                        "function": "RG",
                        "id": "1037086683",
                        "countryId": "121450124",
                        "globalId": "121450117",
                    },
                    {
                        "function": "ZC",
                        "id": "1037086683",
                        "countryId": "121450124",
                        "globalId": "121450117",
                    },
                    {
                        "function": "ZE",
                        "id": "1037086683",
                        "countryId": "121450124",
                        "globalId": "121450117",
                    },
                    {
                        "function": "ZL",
                        "id": "1037086683",
                        "countryId": "121450124",
                        "globalId": "121450117",
                    },
                    {
                        "function": "ZW",
                        "id": "1037086683",
                        "countryId": "121450124",
                        "globalId": "121450117",
                    },
                ],
                "contacts": [
                    {
                        "function": "ZG",
                        "id": "9001140868",
                        "countryId": null,
                        "globalId": null,
                    }
                ],
            },
            "entitlements": [
                {
                    "lineItem": "0000000010",
                    "quote": "6000207485",
                    "contract": "2000042707",
                    "total_qty": "2.000",
                    "available_qty": "0.00",
                    "product": {
                        "sku": "JN004AAS",
                        "legacy": "",
                        "description": "Aruba Central Virtual GW 500Mbps Foundation Year(s) SUB SaaS",
                        "attributes": [
                            {
                                "name": "TERM_IN_MONTHS",
                                "value": "36",
                                "valueDisplay": "36",
                                "nameDisplay": "Term In Months",
                            },
                            {
                                "name": "TIER",
                                "value": "FO",
                                "valueDisplay": "Foundation",
                                "nameDisplay": "Tier",
                            },
                            {
                                "name": "HIDE_CHAR",
                                "value": "COMMITMENT_VALUE1|EVERGREEN|FIXED_COMMITMENT|TIER",
                                "valueDisplay": "COMMITMENT_VALUE1|EVERGREEN|FIXED_COMMITMENT|Tier",
                                "nameDisplay": "HIDE CHARACTERISTICS",
                            },
                            {
                                "name": "TERM_UOM",
                                "value": "Y",
                                "valueDisplay": "Year(s)",
                                "nameDisplay": "Term Unit of Measure",
                            },
                            {
                                "name": "TERM_IN_MONTHS_MIN_2",
                                "value": "12",
                                "valueDisplay": "12",
                                "nameDisplay": "Term in months minimum",
                            },
                            {
                                "name": "PRODUCT_ID",
                                "value": "JN004AAS",
                                "valueDisplay": "JN004AAS",
                                "nameDisplay": "Product ID",
                            },
                            {
                                "name": "BILL_FREQ",
                                "value": "M",
                                "valueDisplay": "Monthly",
                                "nameDisplay": "BILLING FREQUENCY",
                            },
                            {
                                "name": "PRICING_MODEL",
                                "value": "TIER",
                                "valueDisplay": "Tier",
                                "nameDisplay": "Pricing Model",
                            },
                            {
                                "name": "SP_HIDE_CHAR1",
                                "value": "TERM",
                                "valueDisplay": "TERM",
                                "nameDisplay": "Characteristic Name",
                            },
                            {
                                "name": "QUANTITY_2",
                                "value": "1",
                                "valueDisplay": "1",
                                "nameDisplay": "CRM: Order Quantity",
                            },
                            {
                                "name": "SP_HIDE_CHAR2",
                                "value": "TERM_UOM",
                                "valueDisplay": "TERM_UOM",
                                "nameDisplay": "Characteristic Name",
                            },
                            {
                                "name": "TERM_IN_MONTHS_MAX_2",
                                "value": "36",
                                "valueDisplay": "36",
                                "nameDisplay": "Term in months maximum",
                            },
                            {
                                "name": "INVOICING_MODEL",
                                "value": "CO_SU",
                                "valueDisplay": "Consumption+Subscription",
                                "nameDisplay": "INVOICING MODEL",
                            },
                            {
                                "name": "PRODUCT_CC",
                                "value": "CENTRAL_VGW",
                                "valueDisplay": "Central_VGW",
                                "nameDisplay": "Product ID for CC",
                            },
                            {
                                "name": "CS_TERM_UOM",
                                "value": "Y",
                                "valueDisplay": "Year(s)",
                                "nameDisplay": "Term Unit Of Measure",
                            },
                            {
                                "name": "BANDWIDTH",
                                "value": "VGW_500",
                                "valueDisplay": "Virtual GW 500Mbps",
                                "nameDisplay": "Bandwidth",
                            },
                            {
                                "name": "CS_TERM",
                                "value": "3",
                                "valueDisplay": "3",
                                "nameDisplay": "Term",
                            },
                        ],
                    },
                    "support": [
                        {
                            "name": "SUPPORT_TIER",
                            "value": "FC",
                            "valueDisplay": "Foundation Care",
                            "nameDisplay": "Support Tier",
                        },
                        {
                            "name": "CS_TCS_TECH_SUPPORT",
                            "value": "Y",
                            "valueDisplay": "Yes",
                            "nameDisplay": "Technical Support",
                        },
                        {
                            "name": "CS_TCS_TECH_GUIDANCE",
                            "value": "Y",
                            "valueDisplay": "Yes",
                            "nameDisplay": "General Technical Guidance",
                        },
                        {
                            "name": "TERM_UOM",
                            "value": "Y",
                            "valueDisplay": "Year(s)",
                            "nameDisplay": "Term Unit of Measure",
                        },
                        {
                            "name": "CS_TCS_RESPONSE_TIME",
                            "value": "2HR",
                            "valueDisplay": "2 Hours",
                            "nameDisplay": "Response Time",
                        },
                        {
                            "name": "CS_TCS_COV_WINDOW7",
                            "value": "24",
                            "valueDisplay": "24 Hours",
                            "nameDisplay": "Coverage Window 24x7",
                        },
                        {
                            "name": "CS_TCS_CONTRACT_TYPE",
                            "value": "TC",
                            "valueDisplay": "TechCare",
                            "nameDisplay": "Contract Type",
                        },
                        {
                            "name": "SP_HIDE_CHAR1",
                            "value": "TERM",
                            "valueDisplay": "TERM",
                            "nameDisplay": "Characteristic Name",
                        },
                        {
                            "name": "SP_HIDE_CHAR2",
                            "value": "TERM_UOM",
                            "valueDisplay": "TERM_UOM",
                            "nameDisplay": "Characteristic Name",
                        },
                        {
                            "name": "CS_TERM_UOM",
                            "value": "Y",
                            "valueDisplay": "Year(s)",
                            "nameDisplay": "Term Unit Of Measure",
                        },
                        {
                            "name": "CS_TCS_COLLAB_SUPPORT",
                            "value": "Y",
                            "valueDisplay": "Yes",
                            "nameDisplay": "Collaborative Supp and Assist",
                        },
                        {
                            "name": "CS_TCS_SERVICE_LEVEL",
                            "value": "ESS",
                            "valueDisplay": "Essential",
                            "nameDisplay": "Service Level",
                        },
                        {
                            "name": "CS_TERM",
                            "value": "3",
                            "valueDisplay": "3",
                            "nameDisplay": "Term",
                        },
                    ],
                    "licenses": [
                        {
                            "id": "PAYGHHA7TCYEAG",
                            "qty": "2.000",
                            "devices": [],
                            "customer": {},
                            "appointments": {
                                "subscriptionStart": "22.02.2023 00:00:00",
                                "subscriptionEnd": "22.02.2036 00:00:00",
                                "suspensionDate": null,
                                "cancellationDate": null,
                                "reactivationDate": null,
                                "activationDate": "22.02.2023 14:14:01",
                                "duration": "3",
                                "delayedActivation": null,
                                "autoRenewalDate": null,
                            },
                        }
                    ],
                }
            ],
        }
        return subs_data_vgw_500_payload

    @staticmethod
    def vm_bakcup():
        null = None
        vm_backup_order = {
            "reason": "Creation",
            "quote": "SERTEST007",
            "contract": "SERTEST007",
            "trial": True,
            "smcCode": "code",
            "customer": {
                "MDM": "SERTEST007",
                "phone": "3747702",
                "postal_code": "109841",
                "address": "1 Depot Close",
                "city": "Singapore",
                "country": "SG",
                "state": "ca",
                "company_name": "HEWLETT-PACKARD ASIA PACIFIC PTE.",
                "email": "jeremy.lee@hpe.com",
            },
            "activate": {
                "soldTo": "51 Tai Seng Avenue #05-01 Pixe Singapore SG",
                "soldToName": "HEWLETT-PACKARD SINGAPORE(SALES)PTE",
                "soldToEmail": "default@gmail.com",
                "shipTo": "1 Depot Close Singapore SG",
                "shipToName": "HEWLETT-PACKARD ASIA PACIFIC PTE. LTD.",
                "shipToEmail": "default@gmail.com",
                "endUser": "1 Depot Close Singapore SG",
                "endUserName": "FLORENCE SPRINT6 SM TEST1",
                "endUserEmail": "jeremy.lee@hpe.com",
                "po": "PONUMCCS_09_170120_SERTEST007",
                "resellerPo": "SERTEST007",
                "endUserPo": "SERTEST007",
                "orderClass": "ZBRIM",
                "party": {
                    "id": "SERTEST007",
                    "countryId": "122394339",
                    "globalId": "122394308",
                },
                "parties": [
                    {
                        "function": "AG",
                        "id": "SERTEST007",
                        "countryId": null,
                        "globalId": null,
                    },
                    {
                        "function": "WE",
                        "id": "SERTEST007",
                        "countryId": "122394339",
                        "globalId": "122394308",
                    },
                    {
                        "function": "RE",
                        "id": "SERTEST007",
                        "countryId": null,
                        "globalId": null,
                    },
                    {
                        "function": "RG",
                        "id": "SERTEST007",
                        "countryId": null,
                        "globalId": null,
                    },
                    {
                        "function": "ZC",
                        "id": "SERTEST007",
                        "countryId": "122394339",
                        "globalId": "122394308",
                    },
                    {
                        "function": "ZE",
                        "id": "SERTEST007",
                        "countryId": "122394339",
                        "globalId": "122394308",
                    },
                    {
                        "function": "ZL",
                        "id": "SERTEST007",
                        "countryId": "122394339",
                        "globalId": "122394308",
                    },
                ],
                "contacts": [
                    {
                        "function": "ZG",
                        "id": "SERTEST007",
                        "countryId": null,
                        "globalId": null,
                    }
                ],
            },
            "entitlements": [
                {
                    "lineItem": "0000000010",
                    "quote": "SERTEST007",
                    "contract": "SERTEST007",
                    "total_qty": "1.000",
                    "available_qty": "0.00",
                    "product": {
                        "sku": "R7A23AAE",
                        "legacy": null,
                        "description": "HPE GreenLake for Backup and Recovery 90 Day(s) Evaluation SaaS",
                        "attributes": [
                            {
                                "name": "CS_INVOICING_MODEL",
                                "value": "EVAL",
                                "valueDisplay": "Evaluation",
                                "nameDisplay": "Invoicing Model",
                            },
                            {
                                "name": "CS_CCM_MULTIV_UOM_CONC",
                                "value": "EBS,0|EC2,0|GB,0|VM,0",
                                "valueDisplay": "EBS,0|EC2,0|GB,0|VM,0",
                                "nameDisplay": "Concatenate UOM with Commit",
                            },
                            {
                                "name": "CS_BILL_FREQ",
                                "value": "M",
                                "valueDisplay": "Monthly",
                                "nameDisplay": "Billing Frequency",
                            },
                            {
                                "name": "EVERGREEN",
                                "value": "NO",
                                "valueDisplay": "NO",
                                "nameDisplay": "EVERGREEN",
                            },
                            {
                                "name": "CS_READ_ITM_TYPE",
                                "value": "ZQPV",
                                "valueDisplay": "ZQPV",
                                "nameDisplay": "Item Category",
                            },
                            {
                                "name": "CS_FIXED_COMMITMENT",
                                "value": "N",
                                "valueDisplay": "No",
                                "nameDisplay": "Fixed Commitment",
                            },
                            {
                                "name": "CS_CCM_MULTIV_UOM",
                                "value": "EBS|EC2|GB|VM",
                                "valueDisplay": "EBS|EC2|GB|VM",
                                "nameDisplay": "List of product unit of measur",
                            },
                            {
                                "name": "CS_USAGE_UOM1",
                                "value": "VM",
                                "valueDisplay": "VM",
                                "nameDisplay": "Unit Of Measure 1",
                            },
                            {
                                "name": "CS_PRODUCT_ID",
                                "value": "R7A23AAE",
                                "valueDisplay": "R7A23AAE",
                                "nameDisplay": "Base Product ID",
                            },
                            {
                                "name": "CS_SCREEN_DEP_INVISIBLE",
                                "value": "CS_CCM_EBS|CS_CCM_EC2|CS_CCM_GB|CS_CCM_MULTIV_UOM|CS_CCM_MULTIV_UOM_CONC|CS_CCM_VM|CS_CLASSIC_PREPAID|CS_COMMITMENT_VALUE1|CS_COMMITMENT_VALUE2|CS_HW_LED_MANDATORY_SAAS|CS_PLATFORM|CS_PRICING_MODEL|CS_PRODUCT_CC|CS_PRODUCT_ID|CS_RANGE|CS_SWSC_AAS_HANDLING|CS_TERM_IN_MONTHS|CS_TERM_IN_MONTHS_MAX_2|CS_TERM_IN_MONTHS_MIN_2|CS_TIER|CS_USAGE_UOM1|CS_USAGE_UOM2|EVERGREEN",
                                "valueDisplay": "CS_CCM_EBS|CS_CCM_EC2|CS_CCM_GB|CS_CCM_MULTIV_UOM|CS_CCM_MULTIV_UOM_CONC|CS_CCM_VM|CS_CLASSIC_PREPAID|CS_COMMITMENT_VALUE1|CS_COMMITMENT_VALUE2|CS_HW_LED_MANDATORY_SAAS|CS_PLATFORM|CS_PRICING_MODEL|CS_PRODUCT_CC|CS_PRODUCT_ID|CS_RANGE|CS_SWSC_AAS_HANDLING|CS_TERM_IN_MONTHS|CS_TERM_IN_MONTHS_MAX_2|CS_TERM_IN_MONTHS_MIN_2|CS_TIER|CS_USAGE_UOM1|CS_USAGE_UOM2|EVERGREEN",
                                "nameDisplay": "Characteristic Name",
                            },
                            {
                                "name": "CS_TIER",
                                "value": "FN",
                                "valueDisplay": "Foundation",
                                "nameDisplay": "Tier",
                            },
                            {
                                "name": "CS_PRODUCT_CC",
                                "value": "VM_BACKUP",
                                "valueDisplay": "VM Backup",
                                "nameDisplay": "Product ID for CC",
                            },
                            {
                                "name": "CS_USAGE_UOM2",
                                "value": "GB",
                                "valueDisplay": "GB",
                                "nameDisplay": "Unit Of Measure 2",
                            },
                            {
                                "name": "CS_TERM_UOM",
                                "value": "D",
                                "valueDisplay": "Day(s)",
                                "nameDisplay": "Term Unit Of Measure",
                            },
                            {
                                "name": "CS_SWSC_AAS_HANDLING",
                                "value": "SVC",
                                "valueDisplay": "Service",
                                "nameDisplay": "Software SupChain aaS Handling",
                            },
                            {
                                "name": "CS_RANGE",
                                "value": "STO",
                                "valueDisplay": "Storage",
                                "nameDisplay": "Range",
                            },
                            {
                                "name": "CS_CONFIG_TYPE",
                                "value": "001",
                                "valueDisplay": "EVAL Configuration",
                                "nameDisplay": "Configuration Type",
                            },
                            {
                                "name": "CS_PRICING_MODEL",
                                "value": "TIER",
                                "valueDisplay": "Tier",
                                "nameDisplay": "Pricing Model",
                            },
                            {
                                "name": "CS_TERM",
                                "value": "90",
                                "valueDisplay": "90",
                                "nameDisplay": "Term",
                            },
                        ],
                    },
                    "support": [],
                    "licenses": [
                        {
                            "id": "SERTEST007GUAGY",
                            "qty": "1.000",
                            "devices": [],
                            "customer": {},
                            "appointments": {
                                "subscriptionStart": "10.03.2023 00:00:00",
                                "subscriptionEnd": "08.06.2023 00:00:00",
                                "suspensionDate": null,
                                "cancellationDate": null,
                                "reactivationDate": null,
                                "activationDate": "10.03.2023 20:39:06",
                                "duration": "90",
                                "delayedActivation": null,
                                "autoRenewalDate": null,
                            },
                        }
                    ],
                }
            ],
        }
        return vm_backup_order

    @staticmethod
    def svc_dis_recovery_zerto():
        null = None
        dis_recovery_order = {
            "reason": "Creation",
            "quote": "6001998187",
            "contract": "6001998187",
            "smcCode": "E",
            "customer": {
                "MDM": "1010858407",
                "phone": "3054366718",
                "postal_code": "33172-2525",
                "address": "2100 NW 102ND Pl",
                "city": "DORAL",
                "country": "US",
                "state": "FL",
                "company_name": "WESTHAM TRADE COMPANY LIMITED",
                "email": "kvazquez@hpe.com",
            },
            "activate": {
                "soldTo": "2100 NW 102ND Pl DORAL US",
                "soldToName": "WESTHAM TRADE COMPANY LIMITED",
                "soldToEmail": "lkategaru@deloitte.com",
                "shipTo": "2100 NW 102ND Pl DORAL US",
                "shipToName": "WESTHAM TRADE COMPANY LIMITED",
                "shipToEmail": "lkategaru@deloitte.com",
                "endUser": "2100 NW 102ND Pl DORAL US",
                "endUserName": "Zerto ABC LIMITED",
                "endUserEmail": "kvazquez@hpe.com",
                "po": "zerto_test_01",
                "resellerPo": "",
                "endUserPo": "",
                "orderClass": "ZBRIM",
                "party": {
                    "id": "6001998187",
                    "countryId": "6001998187",
                    "globalId": "6001998187",
                },
                "parties": [
                    {
                        "function": "AG",
                        "id": "1010858407",
                        "countryId": "120703851",
                        "globalId": "120703323",
                    },
                    {
                        "function": "WE",
                        "id": "1010858407",
                        "countryId": "120703851",
                        "globalId": "120703323",
                    },
                    {
                        "function": "RE",
                        "id": "1010858407",
                        "countryId": "120703851",
                        "globalId": "120703323",
                    },
                    {
                        "function": "RG",
                        "id": "1010858407",
                        "countryId": "120703851",
                        "globalId": "120703323",
                    },
                    {
                        "function": "ZC",
                        "id": "1010858407",
                        "countryId": "120703851",
                        "globalId": "120703323",
                    },
                    {
                        "function": "ZE",
                        "id": "6001998187",
                        "countryId": "6001998187",
                        "globalId": "6001998187",
                    },
                    {
                        "function": "ZL",
                        "id": "1010858407",
                        "countryId": "120703851",
                        "globalId": "120703323",
                    },
                    {
                        "function": "ZW",
                        "id": "1010858407",
                        "countryId": "120703851",
                        "globalId": "120703323",
                    },
                ],
                "contacts": [
                    {
                        "function": "ZG",
                        "id": "9000166419",
                        "countryId": null,
                        "globalId": null,
                    }
                ],
            },
            "entitlements": [
                {
                    "lineItem": "0000000010",
                    "quote": "6001998187",
                    "contract": "6001998187",
                    "total_qty": "1.000",
                    "available_qty": "0.00",
                    "product": {
                        "sku": "S1S62AAE",
                        "legacy": "",
                        "description": "HPE GreenLake Disaster Recovery Sub Foundation 3 Year(s) Monthly SaaS",
                        "attributes": [
                            {
                                "name": "CS_INVOICING_MODEL",
                                "value": "SU",
                                "valueDisplay": "Subscription",
                                "nameDisplay": "Invoicing Model",
                            },
                            {
                                "name": "CS_CCM_MULTIV_UOM_CONC",
                                "value": "VM,00",
                                "valueDisplay": "VM,00",
                                "nameDisplay": "Concatenate UOM with Commit",
                            },
                            {
                                "name": "CS_BILL_FREQ",
                                "value": "M",
                                "valueDisplay": "Monthly",
                                "nameDisplay": "Billing Frequency",
                            },
                            {
                                "name": "CS_HW_LED_MANDATORY_SAAS",
                                "value": "N",
                                "valueDisplay": "NO",
                                "nameDisplay": "HW Led Mandatory SaaS Flag",
                            },
                            {
                                "name": "CS_CCM_MULTIV_UOM",
                                "value": "VM",
                                "valueDisplay": "VM",
                                "nameDisplay": "List of product unit of measur",
                            },
                            {
                                "name": "CS_PRODUCT_ID",
                                "value": "S1S62AAE",
                                "valueDisplay": "S1S62AAE",
                                "nameDisplay": "Base Product ID",
                            },
                            {
                                "name": "CS_SCREEN_DEP_INVISIBLE",
                                "value": "CS_CCM_MULTIV_UOM_CONC|CS_HW_LED_MANDATORY_SAAS|CS_PRICING_MODEL|CS_PRODUCT_ID|CS_RANGE|CS_SCREEN_DEP_INVISIBLE|CS_SDCOM_VKOND|CS_SWSC_AAS_HANDLING|CS_TIER",
                                "valueDisplay": "CS_CCM_MULTIV_UOM_CONC|CS_HW_LED_MANDATORY_SAAS|CS_PRICING_MODEL|CS_PRODUCT_ID|CS_RANGE|CS_SCREEN_DEP_INVISIBLE|CS_SDCOM_VKOND|CS_SWSC_AAS_HANDLING|CS_TIER",
                                "nameDisplay": "Screen Dep Invisible",
                            },
                            {
                                "name": "CS_TIER",
                                "value": "FN",
                                "valueDisplay": "Foundation",
                                "nameDisplay": "Tier",
                            },
                            {
                                "name": "CS_TERM_UOM",
                                "value": "Y",
                                "valueDisplay": "Year(s)",
                                "nameDisplay": "Term Unit Of Measure",
                            },
                            {
                                "name": "CS_CCM_VM",
                                "value": "UP TO 100",
                                "valueDisplay": "UP TO 100",
                                "nameDisplay": "Commit Value VM",
                            },
                            {
                                "name": "CS_SWSC_AAS_HANDLING",
                                "value": "SVC",
                                "valueDisplay": "Service",
                                "nameDisplay": "Software SupChain aaS Handling",
                            },
                            {
                                "name": "CS_RANGE",
                                "value": "STO",
                                "valueDisplay": "Storage",
                                "nameDisplay": "Range",
                            },
                            {
                                "name": "CS_CONFIG_TYPE",
                                "value": "002",
                                "valueDisplay": "NON EVAL Configuration",
                                "nameDisplay": "Configuration Type",
                            },
                            {
                                "name": "CS_PRICING_MODEL",
                                "value": "TIER",
                                "valueDisplay": "Tier",
                                "nameDisplay": "Pricing Model",
                            },
                            {
                                "name": "CS_TERM",
                                "value": "3",
                                "valueDisplay": "3",
                                "nameDisplay": "Term",
                            },
                        ],
                    },
                    "support": [],
                    "licenses": [
                        {
                            "id": "YGGZERTO6UTT",
                            "qty": "1.000",
                            "devices": [],
                            "customer": {},
                            "appointments": {
                                "subscriptionStart": "20.10.2022 00:00:00",
                                "subscriptionEnd": "20.10.2025 00:00:00",
                                "suspensionDate": null,
                                "cancellationDate": null,
                                "reactivationDate": null,
                                "activationDate": "20.10.2022 20:48:19",
                                "duration": "3",
                                "delayedActivation": null,
                                "autoRenewalDate": null,
                            },
                        }
                    ],
                }
            ],
        }
        return dis_recovery_order

    @staticmethod
    def subs_compute_iaas():
        null = None
        sub_compute_iaas = {
            "reason": "Creation",
            "quote": "COMPRO0001",
            "contract": "COMPRO0001",
            "smcCode": "E",
            "customer": {
                "MDM": "COMPRO0001",
                "phone": "2078430200",
                "postal_code": "LS12 6EH",
                "address": "7 Brown Lane West",
                "city": "LEEDS",
                "country": "GB",
                "state": "",
                "company_name": "NG BAILEY IT SERVICES LIMITED",
                "email": "shreyast@gmail.com",
            },
            "activate": {
                "soldTo": "REDWOOD 2, CROCKFORD LANE CHIN BASINGSTOKE GB",
                "soldToName": "TECH DATA LIMITED",
                "soldToEmail": "suresh.bhojani@cibc.co.uk",
                "shipTo": "7 Brown Lane West LEEDS GB",
                "shipToName": "NG BAILEY IT SERVICES LIMITED",
                "shipToEmail": "",
                "endUser": "7 Brown Lane West LEEDS GB",
                "endUserName": "FLORENCE SPRINT6 SM TEST1",
                "endUserEmail": "shreyast@gmail.com",
                "reseller": "ADMINISTRATION CENTRE HATFIELD HATFIELD GB",
                "resellerName": "COMPUTACENTER (UK) LIMITED",
                "resellerEmail": "Ashokkumar.Thangavelu@telefonica.com",
                "po": "16152_PO_COMPRO0001",
                "resellerPo": "",
                "endUserPo": "",
                "orderClass": "ZBRIM",
                "party": {
                    "id": "COMPRO0001",
                    "countryId": "120243194",
                    "globalId": "120243012",
                },
                "parties": [
                    {
                        "function": "AG",
                        "id": "COMPRO0001",
                        "countryId": "121109504",
                        "globalId": "121109503",
                    },
                    {
                        "function": "WE",
                        "id": "COMPRO0001",
                        "countryId": null,
                        "globalId": null,
                    },
                    {
                        "function": "RE",
                        "id": "COMPRO0001",
                        "countryId": "121109504",
                        "globalId": "121109503",
                    },
                    {
                        "function": "RG",
                        "id": "COMPRO0001",
                        "countryId": "121109504",
                        "globalId": "121109503",
                    },
                    {
                        "function": "Z1",
                        "id": "COMPRO0001",
                        "countryId": "120762923",
                        "globalId": "120762922",
                    },
                    {
                        "function": "ZC",
                        "id": "COMPRO0001",
                        "countryId": "120243194",
                        "globalId": "120243012",
                    },
                    {
                        "function": "ZE",
                        "id": "COMPRO0001",
                        "countryId": "120243194",
                        "globalId": "120243012",
                    },
                    {
                        "function": "ZL",
                        "id": "COMPRO0001",
                        "countryId": "120243194",
                        "globalId": "120243012",
                    },
                ],
                "contacts": [
                    {
                        "function": "CS",
                        "id": "COMPRO0001",
                        "countryId": null,
                        "globalId": null,
                    },
                    {
                        "function": "RT",
                        "id": "COMPRO0001",
                        "countryId": null,
                        "globalId": null,
                    },
                    {
                        "function": "ZG",
                        "id": "COMPRO0001",
                        "countryId": null,
                        "globalId": null,
                    },
                ],
            },
            "entitlements": [
                {
                    "lineItem": "0000000010",
                    "quote": "COMPRO0001",
                    "contract": "COMPRO0001",
                    "total_qty": "1.000",
                    "available_qty": "0.00",
                    "product": {
                        "sku": "R6Z88AAE",
                        "legacy": "",
                        "description": "HPE GreenLake COM St 1y Up ProLiant aaS",
                        "attributes": [
                            {
                                "name": "CS_INVOICING_MODEL",
                                "value": "UP",
                                "valueDisplay": "Upfront",
                                "nameDisplay": "Invoicing Model",
                            },
                            {
                                "name": "CS_TERM_IN_MONTHS_MAX_2",
                                "value": "12",
                                "valueDisplay": "12",
                                "nameDisplay": "Term in months maximum",
                            },
                            {
                                "name": "CS_BILL_FREQ",
                                "value": "UP",
                                "valueDisplay": "Upfront",
                                "nameDisplay": "Billing Frequency",
                            },
                            {
                                "name": "CS_HW_LED_SAAS",
                                "value": "N",
                                "valueDisplay": "NO",
                                "nameDisplay": "HW Led Mandatory SaaS Flag",
                            },
                            {
                                "name": "CS_HW_LED_MANDATORY_SAAS",
                                "value": "N",
                                "valueDisplay": "NO",
                                "nameDisplay": "HW Led Mandatory SaaS Flag",
                            },
                            {
                                "name": "CS_TERM_IN_MONTHS_MIN_2",
                                "value": "0",
                                "valueDisplay": "0",
                                "nameDisplay": "Term in months minimum",
                            },
                            {
                                "name": "CS_TERM_IN_MONTHS",
                                "value": "12",
                                "valueDisplay": "12",
                                "nameDisplay": "Term in months",
                            },
                            {
                                "name": "CS_PLATFORM",
                                "value": "PROLIANT",
                                "valueDisplay": "ProLiant",
                                "nameDisplay": "Platform",
                            },
                            {
                                "name": "CS_PRODUCT_ID",
                                "value": "R6Z73AAE",
                                "valueDisplay": "R6Z73AAE",
                                "nameDisplay": "Base Product ID",
                            },
                            {
                                "name": "CS_SCREEN_DEP_INVISIBLE",
                                "value": "CS_HW_LED_MANDATORY_SAAS|CS_PRODUCT_ID|CS_RANGE|CS_SWSC_AAS_HANDLING|CS_TERM_IN_MONTHS|CS_TERM_IN_MONTHS_MAX_2|CS_TERM_IN_MONTHS_MIN_2",
                                "valueDisplay": "CS_HW_LED_MANDATORY_SAAS|CS_PRODUCT_ID|CS_RANGE|CS_SWSC_AAS_HANDLING|CS_TERM_IN_MONTHS|CS_TERM_IN_MONTHS_MAX_2|CS_TERM_IN_MONTHS_MIN_2",
                                "nameDisplay": "Screen Dep Invisible",
                            },
                            {
                                "name": "CS_TIER",
                                "value": "ST",
                                "valueDisplay": "Standard",
                                "nameDisplay": "Tier",
                            },
                            {
                                "name": "CS_TERM_UOM",
                                "value": "Y",
                                "valueDisplay": "Year(s)",
                                "nameDisplay": "Term Unit Of Measure",
                            },
                            {
                                "name": "CS_SWSC_AAS_HANDLING",
                                "value": "DEV",
                                "valueDisplay": "Device",
                                "nameDisplay": "Software SupChain aaS Handling",
                            },
                            {
                                "name": "CS_RANGE",
                                "value": "COM",
                                "valueDisplay": "Compute",
                                "nameDisplay": "Range",
                            },
                            {
                                "name": "CS_CONFIG_TYPE",
                                "value": "002",
                                "valueDisplay": "NON EVAL Configuration",
                                "nameDisplay": "Configuration Type",
                            },
                            {
                                "name": "CS_TIER_POSITANO",
                                "value": "ST",
                                "valueDisplay": "Standard",
                                "nameDisplay": "Tier for Positano",
                            },
                            {
                                "name": "CS_TERM",
                                "value": "1",
                                "valueDisplay": "1",
                                "nameDisplay": "Term",
                            },
                        ],
                    },
                    "support": [
                        {
                            "name": "CS_TCS_CONTRACT_TYPE",
                            "value": "TC",
                            "valueDisplay": "TechCare",
                            "nameDisplay": "Contract Type",
                        },
                        {
                            "name": "CS_TCS_TECH_SUPPORT",
                            "value": "Y",
                            "valueDisplay": "Yes",
                            "nameDisplay": "Technical Support",
                        },
                        {
                            "name": "CS_TCS_TECH_GUIDANCE",
                            "value": "Y",
                            "valueDisplay": "Yes",
                            "nameDisplay": "General Technical Guidance",
                        },
                        {
                            "name": "CS_SUPPORT_TIER",
                            "value": "FC",
                            "valueDisplay": "Foundation Care 24x7",
                            "nameDisplay": "Support Tier",
                        },
                        {
                            "name": "CS_TCS_RESPONSE_TIME",
                            "value": "2HR",
                            "valueDisplay": "2 Hours",
                            "nameDisplay": "Response Time",
                        },
                        {
                            "name": "CS_TERM_UOM",
                            "value": "Y",
                            "valueDisplay": "Year(s)",
                            "nameDisplay": "Term Unit Of Measure",
                        },
                        {
                            "name": "CS_TCS_COV_WINDOW7",
                            "value": "24",
                            "valueDisplay": "24 Hours",
                            "nameDisplay": "Coverage Window 24x7",
                        },
                        {
                            "name": "CS_TCS_COLLAB_SUPPORT",
                            "value": "Y",
                            "valueDisplay": "Yes",
                            "nameDisplay": "Collaborative Supp and Assist",
                        },
                        {
                            "name": "CS_TCS_SERVICE_LEVEL",
                            "value": "ESS",
                            "valueDisplay": "Essential",
                            "nameDisplay": "Service Level",
                        },
                        {
                            "name": "CS_TERM",
                            "value": "1",
                            "valueDisplay": "1",
                            "nameDisplay": "Term",
                        },
                    ],
                    "licenses": [
                        {
                            "id": "COMPRO0001J73UC26",
                            "qty": "1.000",
                            "devices": [],
                            "customer": {},
                            "appointments": {
                                "subscriptionStart": "16.03.2023 00:00:00",
                                "subscriptionEnd": "16.03.2024 00:00:00",
                                "suspensionDate": null,
                                "cancellationDate": null,
                                "reactivationDate": null,
                                "activationDate": "16.03.2023 00:00:00",
                                "duration": "1",
                                "delayedActivation": null,
                                "autoRenewalDate": null,
                            },
                        }
                    ],
                }
            ],
        }

        return sub_compute_iaas

    @staticmethod
    def subs_compute_gecko_iaas():
        null = None
        sub_compute_gecko_iaas = {
            "reason": "Creation",
            "quote": "6000204811",
            "contract": "2000042213",
            "smcCode": "E",
            "aasType": "IAAS",
            "customer": {
                "MDM": "1001763858",
                "phone": "7248508677",
                "postal_code": "15601-7647",
                "address": "1638 ROSEYTOWN RD STE 8",
                "city": "GREENSBURG",
                "country": "US",
                "state": "PA",
                "company_name": "ACCUTECH DATA SUPPLIES, INC.",
                "email": "vijaian.c@gmaaail.om",
            },
            "activate": {
                "soldTo": "1638 ROSEYTOWN RD STE 8 GREENSBURG US",
                "soldToName": "ACCUTECH DATA SUPPLIES, INC.",
                "soldToEmail": "rajatyagi@deloitte.com",
                "shipTo": "1638 ROSEYTOWN RD STE 8 GREENSBURG US",
                "shipToName": "ACCUTECH DATA SUPPLIES, INC.",
                "shipToEmail": "rajatyagi@deloitte.com",
                "endUser": "1638 ROSEYTOWN RD STE 8 GREENSBURG US",
                "endUserName": "ACCUTECH DATA SUPPLIES, INC.",
                "endUserEmail": "vijaian.c@gmaaail.om",
                "po": "6000204811",
                "resellerPo": "",
                "endUserPo": "",
                "orderClass": "ZBRIM",
                "party": {
                    "id": "1001763858",
                    "countryId": "120790310",
                    "globalId": "120790309",
                },
                "parties": [
                    {
                        "function": "AG",
                        "id": "1001763858",
                        "countryId": "120790310",
                        "globalId": "120790309",
                    },
                    {
                        "function": "WE",
                        "id": "1001763858",
                        "countryId": "120790310",
                        "globalId": "120790309",
                    },
                    {
                        "function": "RE",
                        "id": "1001763858",
                        "countryId": "120790310",
                        "globalId": "120790309",
                    },
                    {
                        "function": "RG",
                        "id": "1001763858",
                        "countryId": "120790310",
                        "globalId": "120790309",
                    },
                    {
                        "function": "ZC",
                        "id": "1001763858",
                        "countryId": "120790310",
                        "globalId": "120790309",
                    },
                    {
                        "function": "ZE",
                        "id": "1001763858",
                        "countryId": "120790310",
                        "globalId": "120790309",
                    },
                    {
                        "function": "ZL",
                        "id": "1001763858",
                        "countryId": "120790310",
                        "globalId": "120790309",
                    },
                    {
                        "function": "ZW",
                        "id": "1001763858",
                        "countryId": "120790310",
                        "globalId": "120790309",
                    },
                ],
                "contacts": [
                    {
                        "function": "ZG",
                        "id": "9000129525",
                        "countryId": null,
                        "globalId": null,
                    }
                ],
            },
            "entitlements": [
                {
                    "lineItem": "0000000010",
                    "quote": "6000204811",
                    "contract": "2000042213",
                    "total_qty": "1.000",
                    "available_qty": "0.00",
                    "product": {
                        "sku": "S0B80AAE",
                        "legacy": "",
                        "description": "HPE GreenLake Bare Metal Compute IaaS",
                        "attributes": [
                            {
                                "name": "CS_INVOICING_MODEL",
                                "value": "SU",
                                "valueDisplay": "Subscription",
                                "nameDisplay": "Invoicing Model",
                            },
                            {
                                "name": "CS_TERM_IN_MONTHS_MAX_2",
                                "value": "36",
                                "valueDisplay": "36",
                                "nameDisplay": "Term in months maximum",
                            },
                            {
                                "name": "CS_BILL_FREQ",
                                "value": "M",
                                "valueDisplay": "Monthly",
                                "nameDisplay": "Billing Frequency",
                            },
                            {
                                "name": "CS_INSTALLATION",
                                "value": "M",
                                "valueDisplay": "Monthly",
                                "nameDisplay": "Installation Required",
                            },
                            {
                                "name": "CS_HBA",
                                "value": "FC",
                                "valueDisplay": "16 Gb Dual Port Fibre Channel",
                                "nameDisplay": "Host Bus Adapter",
                            },
                            {
                                "name": "CS_HW_LED_MANDATORY_SAAS",
                                "value": "N",
                                "valueDisplay": "NO",
                                "nameDisplay": "HW Led Mandatory SaaS Flag",
                            },
                            {
                                "name": "CS_NIC",
                                "value": "100GBE",
                                "valueDisplay": "100 GbE",
                                "nameDisplay": "Network Interface Card",
                            },
                            {
                                "name": "CS_TERM_IN_MONTHS_MIN_2",
                                "value": "24",
                                "valueDisplay": "24",
                                "nameDisplay": "Term in months minimum",
                            },
                            {
                                "name": "CS_TERM_IN_MONTHS",
                                "value": "36",
                                "valueDisplay": "36",
                                "nameDisplay": "Term in months",
                            },
                            {
                                "name": "CS_WRKLOAD",
                                "value": "CO-G",
                                "valueDisplay": "Compute Optimized",
                                "nameDisplay": "Workload Requirement",
                            },
                            {
                                "name": "CS_PLATFORM",
                                "value": "PROLIANT",
                                "valueDisplay": "ProLiant",
                                "nameDisplay": "Platform",
                            },
                            {
                                "name": "CS_PRODUCT_ID",
                                "value": "S0B80AAE",
                                "valueDisplay": "S0B80AAE",
                                "nameDisplay": "Base Product ID",
                            },
                            {
                                "name": "CS_SCREEN_DEP_INVISIBLE",
                                "value": "CS_HW_LED_MANDATORY_SAAS|CS_INSTALLATION_TYPE|CS_PRODUCT_ID|CS_RANGE|CS_SCREEN_DEP_INVISIBLE|CS_SDCOM_VKOND|CS_SDCOM_VKOND_SINGLE1|CS_SWSC_AAS_HANDLING|CS_TERM_IN_MONTHS|CS_TERM_IN_MONTHS_MAX_2|CS_TERM_IN_MONTHS_MIN_2|CS_TIER",
                                "valueDisplay": "CS_HW_LED_MANDATORY_SAAS|CS_INSTALLATION_TYPE|CS_PRODUCT_ID|CS_RANGE|CS_SCREEN_DEP_INVISIBLE|CS_SDCOM_VKOND|CS_SDCOM_VKOND_SINGLE1|CS_SWSC_AAS_HANDLING|CS_TERM_IN_MONTHS|CS_TERM_IN_MONTHS_MAX_2|CS_TERM_IN_MONTHS_MIN_2|CS_TIER",
                                "nameDisplay": "Screen Dep Invisible",
                            },
                            {
                                "name": "CS_TIER",
                                "value": "EN",
                                "valueDisplay": "Enhanced",
                                "nameDisplay": "Tier",
                            },
                            {
                                "name": "CS_SIZE",
                                "value": "M",
                                "valueDisplay": "Monthly",
                                "nameDisplay": "Size",
                            },
                            {
                                "name": "CS_TERM_UOM",
                                "value": "Y",
                                "valueDisplay": "Year(s)",
                                "nameDisplay": "Term Unit Of Measure",
                            },
                            {
                                "name": "CS_FORM_FACTOR",
                                "value": "1U",
                                "valueDisplay": "1U",
                                "nameDisplay": "Form Factor",
                            },
                            {
                                "name": "CS_ADD_HBA",
                                "value": "Y",
                                "valueDisplay": "年",
                                "nameDisplay": "Add Host Bus Adapter",
                            },
                            {
                                "name": "CS_SWSC_AAS_HANDLING",
                                "value": "DEV",
                                "valueDisplay": "Device",
                                "nameDisplay": "Software SupChain aaS Handling",
                            },
                            {
                                "name": "CS_RANGE",
                                "value": "COM",
                                "valueDisplay": "Compute",
                                "nameDisplay": "Range",
                            },
                            {
                                "name": "CS_TERM",
                                "value": "3",
                                "valueDisplay": "3",
                                "nameDisplay": "Term",
                            },
                        ],
                    },
                    "support": [],
                    "licenses": [
                        {
                            "id": "YGHT9DDDE7HG",
                            "qty": "1.000",
                            "devices": [
                                {"serial": "SMCMPTGCKO01", "material": "P28948-B21"}
                            ],
                            "customer": {},
                            "appointments": {
                                "subscriptionStart": "21.11.2022 00:00:00",
                                "subscriptionEnd": "21.11.2025 00:00:00",
                                "suspensionDate": null,
                                "cancellationDate": null,
                                "reactivationDate": null,
                                "activationDate": "09.02.2023 09:15:58",
                                "duration": "3",
                                "delayedActivation": null,
                                "autoRenewalDate": null,
                            },
                        }
                    ],
                }
            ],
        }

        return sub_compute_gecko_iaas

    @staticmethod
    def subs_compute_alletra_4k():
        null = None
        sub_compute_alletra_4k = {
            "reason": "Creation",
            "quote": "3100005591",
            "contract": "5100001420",
            "smcCode": "E",
            "customer": {
                "MDM": "1000791811",
                "phone": "2124107500",
                "postal_code": "34418",
                "address": "NO:65 YESILCE MAHALLESI ESKI",
                "city": "Istanbul (Europe)",
                "country": "TR",
                "state": "",
                "company_name": "MEDIA MARKT TURKEY TICARET LIMITED",
                "email": "mozdemir@mediamarkt.com.tr",
            },
            "activate": {
                "soldTo": "ANEL IS MERKEZI NO:5 KAT:8 SAR Istanbul TR",
                "soldToName": "TECH DATA BILGISAYAR SISTEMLERI ANONIM SIRKETI",
                "soldToEmail": "",
                "shipTo": "NO:65 YESILCE MAHALLESI ESKI Istanbul (Europe) TR",
                "shipToName": "MEDIA MARKT TURKEY TICARET LIMITED SIRKETI",
                "shipToEmail": "rohit.reddy@hpe.com",
                "endUser": "NO:65 YESILCE MAHALLESI ESKI Istanbul (Europe) TR",
                "endUserName": "MEDIA MARKT TURKEY TICARET LIMITED SIRKETI",
                "endUserEmail": "mozdemir@mediamarkt.com.tr",
                "reseller": "Nil Tic Merkezi, Yesilce Mah., Istanbul (Europe) TR",
                "resellerName": "DESTEK BILG ILET OTOM SIST VE DAN HIZLERI YAZ SAN VE TIC LTD STI",
                "resellerEmail": "",
                "po": "123_TR",
                "resellerPo": "",
                "endUserPo": "",
                "orderClass": "ZBRIM",
                "party": {
                    "id": "1000791811",
                    "countryId": "121414137",
                    "globalId": "121414120",
                },
                "parties": [
                    {
                        "function": "AG",
                        "id": "1000823619",
                        "countryId": "121414147",
                        "globalId": "120774498",
                    },
                    {
                        "function": "WE",
                        "id": "1000791811",
                        "countryId": "121414137",
                        "globalId": "121414120",
                    },
                    {
                        "function": "RE",
                        "id": "1000823619",
                        "countryId": "121414147",
                        "globalId": "120774498",
                    },
                    {
                        "function": "RG",
                        "id": "1000823619",
                        "countryId": "121414147",
                        "globalId": "120774498",
                    },
                    {
                        "function": "Z1",
                        "id": "1001698582",
                        "countryId": "120773664",
                        "globalId": "120773663",
                    },
                    {
                        "function": "ZC",
                        "id": "1000791811",
                        "countryId": "121414137",
                        "globalId": "121414120",
                    },
                    {
                        "function": "ZE",
                        "id": "1000791811",
                        "countryId": "121414137",
                        "globalId": "121414120",
                    },
                    {
                        "function": "ZL",
                        "id": "1000791811",
                        "countryId": "121414137",
                        "globalId": "121414120",
                    },
                ],
                "contacts": [
                    {
                        "function": "ZG",
                        "id": "9000642413",
                        "countryId": null,
                        "globalId": null,
                    }
                ],
            },
            "entitlements": [
                {
                    "lineItem": "0000000010",
                    "quote": "3100005591",
                    "contract": "5100001420",
                    "total_qty": "100.000",
                    "available_qty": "0.00",
                    "product": {
                        "sku": "R6Z73AAE",
                        "legacy": "",
                        "description": "HPE GreenLake Cmp Ops Mgm Enhanced 3 Year(s) Monthly Alletra 4000 SaaS",
                        "attributes": [
                            {
                                "name": "CS_INVOICING_MODEL",
                                "value": "SU",
                                "valueDisplay": "Subscription",
                                "nameDisplay": "Invoicing Model",
                            },
                            {
                                "name": "CS_TERM_IN_MONTHS_MAX_2",
                                "value": "60",
                                "valueDisplay": "60",
                                "nameDisplay": "Term in months maximum",
                            },
                            {
                                "name": "CS_BILL_FREQ",
                                "value": "M",
                                "valueDisplay": "Monthly",
                                "nameDisplay": "Billing Frequency",
                            },
                            {
                                "name": "CS_HW_LED_MANDATORY_SAAS",
                                "value": "N",
                                "valueDisplay": "NO",
                                "nameDisplay": "HW Led Mandatory SaaS Flag",
                            },
                            {
                                "name": "CS_TERM_IN_MONTHS_MIN_2",
                                "value": "36",
                                "valueDisplay": "36",
                                "nameDisplay": "Term in months minimum",
                            },
                            {
                                "name": "CS_TERM_IN_MONTHS",
                                "value": "36",
                                "valueDisplay": "36",
                                "nameDisplay": "Term in months",
                            },
                            {
                                "name": "CS_PLATFORM",
                                "value": "ALLETRA_4K",
                                "valueDisplay": "Alletra 4000",
                                "nameDisplay": "Platform",
                            },
                            {
                                "name": "CS_PRODUCT_ID",
                                "value": "R6Z73AAE",
                                "valueDisplay": "R6Z73AAE",
                                "nameDisplay": "Base Product ID",
                            },
                            {
                                "name": "CS_SCREEN_DEP_INVISIBLE",
                                "value": "CS_ERROR_LOG|CS_ERROR_TRGR|CS_HW_LED_MANDATORY_SAAS|CS_PRODUCT_ID|CS_RANGE|CS_SWSC_AAS_HANDLING|CS_TERM_IN_MONTHS|CS_TERM_IN_MONTHS_MAX_2|CS_TERM_IN_MONTHS_MIN_2",
                                "valueDisplay": "CS_ERROR_LOG|CS_ERROR_TRGR|CS_HW_LED_MANDATORY_SAAS|CS_PRODUCT_ID|CS_RANGE|CS_SWSC_AAS_HANDLING|CS_TERM_IN_MONTHS|CS_TERM_IN_MONTHS_MAX_2|CS_TERM_IN_MONTHS_MIN_2",
                                "nameDisplay": "Screen Dep Invisible",
                            },
                            {
                                "name": "CS_TIER",
                                "value": "EN",
                                "valueDisplay": "Enhanced",
                                "nameDisplay": "Tier",
                            },
                            {
                                "name": "CS_TERM_UOM",
                                "value": "Y",
                                "valueDisplay": "Year(s)",
                                "nameDisplay": "Term Unit Of Measure",
                            },
                            {
                                "name": "CS_SWSC_AAS_HANDLING",
                                "value": "DEV",
                                "valueDisplay": "Device",
                                "nameDisplay": "Software SupChain aaS Handling",
                            },
                            {
                                "name": "CS_RANGE",
                                "value": "COM",
                                "valueDisplay": "Compute",
                                "nameDisplay": "Range",
                            },
                            {
                                "name": "CS_CONFIG_TYPE",
                                "value": "002",
                                "valueDisplay": "NON EVAL Configuration",
                                "nameDisplay": "Configuration Type",
                            },
                            {
                                "name": "CS_TERM",
                                "value": "3",
                                "valueDisplay": "3",
                                "nameDisplay": "Term",
                            },
                        ],
                    },
                    "support": [
                        {
                            "name": "CS_TCS_CONTRACT_TYPE",
                            "value": "TC",
                            "valueDisplay": "TechCare",
                            "nameDisplay": "Contract Type",
                        },
                        {
                            "name": "CS_TCS_TECH_SUPPORT",
                            "value": "Y",
                            "valueDisplay": "年",
                            "nameDisplay": "Technical Support",
                        },
                        {
                            "name": "CS_TCS_TECH_GUIDANCE",
                            "value": "Y",
                            "valueDisplay": "年",
                            "nameDisplay": "General Technical Guidance",
                        },
                        {
                            "name": "CS_TCS_RESPONSE_TIME",
                            "value": "2HR",
                            "valueDisplay": "2 Hours",
                            "nameDisplay": "Response Time",
                        },
                        {
                            "name": "CS_TERM_UOM",
                            "value": "Y",
                            "valueDisplay": "Year(s)",
                            "nameDisplay": "Term Unit Of Measure",
                        },
                        {
                            "name": "CS_TCS_COV_WINDOW7",
                            "value": "24",
                            "valueDisplay": "24 Hours",
                            "nameDisplay": "Coverage Window 24x7",
                        },
                        {
                            "name": "CS_TCS_COLLAB_SUPPORT",
                            "value": "Y",
                            "valueDisplay": "年",
                            "nameDisplay": "Collaborative Supp and Assist",
                        },
                        {
                            "name": "CS_TCS_SERVICE_LEVEL",
                            "value": "ESS",
                            "valueDisplay": "Essential",
                            "nameDisplay": "Service Level",
                        },
                        {
                            "name": "CS_TERM",
                            "value": "3",
                            "valueDisplay": "3",
                            "nameDisplay": "Term",
                        },
                    ],
                    "licenses": [
                        {
                            "id": "YGUAYAY3U7H6",
                            "qty": "100.000",
                            "devices": [],
                            "customer": {},
                            "appointments": {
                                "subscriptionStart": "29.03.2023 00:00:00",
                                "subscriptionEnd": "29.03.2026 00:00:00",
                                "suspensionDate": null,
                                "cancellationDate": null,
                                "reactivationDate": null,
                                "activationDate": "29.03.2023 14:50:00",
                                "duration": "3",
                                "delayedActivation": null,
                                "autoRenewalDate": null,
                            },
                        }
                    ],
                }
            ],
        }
        return sub_compute_alletra_4k

    @staticmethod
    def subs_storage_hciaas():
        null = None
        sub_storage_hciaas = {
            "reason": "Creation",
            "quote": "6000212008",
            "contract": "2000044030",
            "smcCode": "E",
            "aasType": "IAAS",
            "customer": {
                "MDM": "1037209181",
                "phone": "",
                "postal_code": "29607-2761",
                "address": "100 Fluor Daniel Dr,Greenville",
                "city": "GREENVILLE",
                "country": "US",
                "state": "SC",
                "company_name": "FLUOR ENTERPRISES INC",
                "email": "ardiel.valentin@hpe.com",
            },
            "activate": {
                "soldTo": "100 Fluor Daniel Dr,Greenville GREENVILLE US",
                "soldToName": "FLUOR ENTERPRISES INC",
                "soldToEmail": "",
                "shipTo": "100 Fluor Daniel Dr,Greenville GREENVILLE US",
                "shipToName": "FLUOR ENTERPRISES INC",
                "shipToEmail": "",
                "endUser": "100 Fluor Daniel Dr,Greenville GREENVILLE US",
                "endUserName": "FLUOR ENTERPRISES INC",
                "endUserEmail": "ardiel.valentin@hpe.com",
                "po": "SPID16299DHANYT1",
                "resellerPo": "",
                "endUserPo": "",
                "orderClass": "ZBRIM",
                "party": {
                    "id": "1037209181",
                    "countryId": "120155625",
                    "globalId": "120155517",
                },
                "parties": [
                    {
                        "function": "AG",
                        "id": "1037209181",
                        "countryId": "120155625",
                        "globalId": "120155517",
                    },
                    {
                        "function": "WE",
                        "id": "1037209181",
                        "countryId": "120155625",
                        "globalId": "120155517",
                    },
                    {
                        "function": "RE",
                        "id": "1037209181",
                        "countryId": "120155625",
                        "globalId": "120155517",
                    },
                    {
                        "function": "RG",
                        "id": "1037209181",
                        "countryId": "120155625",
                        "globalId": "120155517",
                    },
                    {
                        "function": "ZC",
                        "id": "1037209181",
                        "countryId": "120155625",
                        "globalId": "120155517",
                    },
                    {
                        "function": "ZE",
                        "id": "1037209181",
                        "countryId": "120155625",
                        "globalId": "120155517",
                    },
                    {
                        "function": "ZL",
                        "id": "1037209181",
                        "countryId": "120155625",
                        "globalId": "120155517",
                    },
                ],
                "contacts": [
                    {
                        "function": "ZG",
                        "id": "9001141116",
                        "countryId": null,
                        "globalId": null,
                    }
                ],
            },
            "entitlements": [
                {
                    "lineItem": "0000000010",
                    "quote": "6000212008",
                    "contract": "2000044030",
                    "total_qty": "1.000",
                    "available_qty": "0.00",
                    "product": {
                        "sku": "R9Q18AAE",
                        "legacy": "",
                        "description": "HPE GreenLake for HCI IaaS Business Critical Balance 3 Year(s) Consumption+Subscription",
                        "attributes": [
                            {
                                "name": "CS_INVOICING_MODEL",
                                "value": "CO_SU",
                                "valueDisplay": "Consumption+Subscription",
                                "nameDisplay": "Invoicing Model",
                            },
                            {
                                "name": "CS_PDU",
                                "value": "NAJP3P",
                                "valueDisplay": "North America / Japan, 3 Phase",
                                "nameDisplay": "Power Distribution Unit",
                            },
                            {
                                "name": "CS_HW_SUPPORT_TYPE",
                                "value": "TES",
                                "valueDisplay": "Tech Care Essential",
                                "nameDisplay": "HW Support Type",
                            },
                            {
                                "name": "CS_RACK_SIZE",
                                "value": "1075X600MM",
                                "valueDisplay": "1075 x 600mm",
                                "nameDisplay": "Rack Size",
                            },
                            {
                                "name": "CS_BILL_FREQ",
                                "value": "M",
                                "valueDisplay": "Monthly",
                                "nameDisplay": "Billing Frequency",
                            },
                            {
                                "name": "CS_PERFORMANCE",
                                "value": "B",
                                "valueDisplay": "Balanced Up To 600K IOPs",
                                "nameDisplay": "Performance Requirement",
                            },
                            {
                                "name": "CS_ENCRYPTION_REQUIRED",
                                "value": "N",
                                "valueDisplay": "No",
                                "nameDisplay": "Encryption Required",
                            },
                            {
                                "name": "CS_3RD_PARTY_SW",
                                "value": "N",
                                "valueDisplay": "No",
                                "nameDisplay": "3rd Party SW",
                            },
                            {
                                "name": "CS_WRKLOAD",
                                "value": "BC",
                                "valueDisplay": "Bus. Critical 99.9999% avail.",
                                "nameDisplay": "Workload Requirement",
                            },
                            {
                                "name": "CS_PRODUCT_ID",
                                "value": "R9Q18AAE",
                                "valueDisplay": "R9Q18AAE",
                                "nameDisplay": "Base Product ID",
                            },
                            {
                                "name": "CS_SCREEN_DEP_INVISIBLE",
                                "value": "CS_FAN|CS_FIXED_COMMITMENT|CS_HW_LED_MANDATORY_SAAS|CS_POWER_INFRASTRUCTURE|CS_PRICING_MODEL|CS_PRODUCT_CC|CS_PRODUCT_ID|CS_RANGE|CS_SCREEN_DEP_INVISIBLE|CS_SWSC_AAS_HANDLING|CS_TERM_IN_MONTHS|CS_TERM_IN_MONTHS_MAX_2",
                                "valueDisplay": "CS_FAN|CS_FIXED_COMMITMENT|CS_HW_LED_MANDATORY_SAAS|CS_POWER_INFRASTRUCTURE|CS_PRICING_MODEL|CS_PRODUCT_CC|CS_PRODUCT_ID|CS_RANGE|CS_SCREEN_DEP_INVISIBLE|CS_SWSC_AAS_HANDLING|CS_TERM_IN_MONTHS|CS_TERM_IN_MONTHS_MAX_2",
                                "nameDisplay": "Screen Dep Invisible",
                            },
                            {
                                "name": "CS_TIER",
                                "value": "BCB",
                                "valueDisplay": "Business Critical Balance",
                                "nameDisplay": "Tier",
                            },
                            {
                                "name": "CS_INSTALLATION_PROVIDER",
                                "value": "HPE",
                                "valueDisplay": "HPE",
                                "nameDisplay": "Installation Provider",
                            },
                            {
                                "name": "CS_INSTALLATION_TYPE",
                                "value": "ISS",
                                "valueDisplay": "Installation and Start Up",
                                "nameDisplay": "Installation Type",
                            },
                            {
                                "name": "CS_PRODUCT_CC",
                                "value": "HCIAAS",
                                "valueDisplay": "HCIAAS",
                                "nameDisplay": "Product ID for CC",
                            },
                            {
                                "name": "CS_TERM_UOM",
                                "value": "Y",
                                "valueDisplay": "Year(s)",
                                "nameDisplay": "Term Unit Of Measure",
                            },
                            {
                                "name": "CS_CCM_MEMGB",
                                "value": "2458",
                                "valueDisplay": "2,458",
                                "nameDisplay": "Compute Memory in GB",
                            },
                            {
                                "name": "CS_SWSC_AAS_HANDLING",
                                "value": "DEV",
                                "valueDisplay": "Device",
                                "nameDisplay": "Software SupChain aaS Handling",
                            },
                            {
                                "name": "CS_RANGE",
                                "value": "STO",
                                "valueDisplay": "Storage",
                                "nameDisplay": "Range",
                            },
                            {
                                "name": "CS_CCM_CORES",
                                "value": "154",
                                "valueDisplay": "154",
                                "nameDisplay": "Number of CPU cores",
                            },
                            {
                                "name": "CS_TERM",
                                "value": "3",
                                "valueDisplay": "3",
                                "nameDisplay": "Term",
                            },
                            {
                                "name": "CS_CCM_MULTIV_UOM_CONC",
                                "value": "BLKGB,74000|CORES,154|MEMGB,2458",
                                "valueDisplay": "BLKGB,74000|CORES,154|MEMGB,2458",
                                "nameDisplay": "Concatenate UOM with Commit",
                            },
                            {
                                "name": "CS_INSTALLATION_SKU",
                                "value": "H36PHCS",
                                "valueDisplay": "H36PHCS",
                                "nameDisplay": "Installation SKU",
                            },
                            {
                                "name": "CS_CCM_BLKGB",
                                "value": "74",
                                "valueDisplay": "74,000",
                                "nameDisplay": "Block Storage Capacity in GB",
                            },
                            {
                                "name": "CS_DRIVE_RETENTION",
                                "value": "NA",
                                "valueDisplay": "NA",
                                "nameDisplay": "Drive Retention",
                            },
                            {
                                "name": "CS_INSTALLATION",
                                "value": "N",
                                "valueDisplay": "No",
                                "nameDisplay": "Installation Required",
                            },
                            {
                                "name": "CS_FIXED_COMMITMENT",
                                "value": "Y",
                                "valueDisplay": "Year(s)",
                                "nameDisplay": "Fixed Commitment",
                            },
                            {
                                "name": "CS_HW_LED_MANDATORY_SAAS",
                                "value": "N",
                                "valueDisplay": "No",
                                "nameDisplay": "HW Led Mandatory SaaS Flag",
                            },
                            {
                                "name": "CS_CCM_MULTIV_UOM",
                                "value": "BLKGB|CORES|MEMGB",
                                "valueDisplay": "BLKGB|CORES|MEMGB",
                                "nameDisplay": "Unit of measure",
                            },
                            {
                                "name": "CS_POWER_INFRASTRUCTURE",
                                "value": "AC",
                                "valueDisplay": "AC",
                                "nameDisplay": "Power Infrastructure",
                            },
                            {
                                "name": "CS_FAN",
                                "value": "FAN4400000",
                                "valueDisplay": "FAN4400000",
                                "nameDisplay": "Fan Number",
                            },
                            {
                                "name": "CS_PRICING_MODEL",
                                "value": "TIER",
                                "valueDisplay": "Tier",
                                "nameDisplay": "Pricing Model",
                            },
                        ],
                    },
                    "support": [],
                    "licenses": [
                        {
                            "id": "YGHUU3E5HAGA",
                            "qty": "1.000",
                            "devices": [],
                            "customer": {},
                            "appointments": {
                                "subscriptionStart": "15.03.2023 00:00:00",
                                "subscriptionEnd": "15.03.2026 00:00:00",
                                "suspensionDate": null,
                                "cancellationDate": null,
                                "reactivationDate": null,
                                "activationDate": "21.03.2023 00:43:22",
                                "duration": "3",
                                "delayedActivation": null,
                                "autoRenewalDate": null,
                            },
                        }
                    ],
                }
            ],
        }
        return sub_storage_hciaas

    @staticmethod
    def opsramp_eval_order():
        null = None
        opsramp_eval_order = {
            "reason": "Creation",
            "quote": "3100016374",
            "contract": "5100005129",
            "trial": True,
            "smcCode": "",
            "customer": {
                "MDM": "1000485126",
                "phone": "4062520171",
                "postal_code": "59101-3227",
                "address": "1465MonadRd",
                "city": "Billings",
                "country": "US",
                "state": "MT",
                "company_name": "GRAYBARELECTRICCOMPANY,INC.",
                "email": "noel.mejias-hernandez@hpe.com",
            },
            "activate": {
                "soldTo": "6280AmericaCenterDriveSANJOSEUS",
                "soldToName": "HEWLETTPACKARDENTERPRISECOMPANY",
                "soldToEmail": "",
                "shipTo": "1465MonadRdBillingsUS",
                "shipToName": "GRAYBARELECTRICCOMPANY,INC.",
                "shipToEmail": "",
                "endUser": "1465MonadRdBillingsUS",
                "endUserName": "GRAYBARELECTRICCOMPANY,INC.",
                "endUserEmail": "noel.mejias-hernandez@hpe.com",
                "po": "PONUMCCS_09_180827",
                "resellerPo": "",
                "endUserPo": "",
                "orderClass": "ZBRIM",
                "party": {
                    "id": "1000485126",
                    "countryId": "120425365",
                    "globalId": "120425364",
                },
                "parties": [
                    {
                        "function": "AG",
                        "id": "8999299909",
                        "countryId": "121489047",
                        "globalId": "121416014",
                    },
                    {
                        "function": "WE",
                        "id": "1000485126",
                        "countryId": "120425365",
                        "globalId": "120425364",
                    },
                    {
                        "function": "RE",
                        "id": "1000929240",
                        "countryId": "120777987",
                        "globalId": "120777986",
                    },
                    {
                        "function": "RG",
                        "id": "1000929240",
                        "countryId": "120777987",
                        "globalId": "120777986",
                    },
                    {
                        "function": "ZC",
                        "id": "1000485126",
                        "countryId": "120425365",
                        "globalId": "120425364",
                    },
                    {
                        "function": "ZE",
                        "id": "1000485126",
                        "countryId": "120425365",
                        "globalId": "120425364",
                    },
                    {
                        "function": "ZL",
                        "id": "1000485126",
                        "countryId": "120425365",
                        "globalId": "120425364",
                    },
                ],
                "contacts": [
                    {
                        "function": "ZG",
                        "id": "9001094115",
                        "countryId": null,
                        "globalId": null,
                    }
                ],
            },
            "entitlements": [
                {
                    "lineItem": "0000000010",
                    "quote": "3100016374",
                    "contract": "5100005129",
                    "total_qty": "1.000",
                    "available_qty": "0.00",
                    "product": {
                        "sku": "S2E00AAE",
                        "legacy": "",
                        "description": "OpsRampSaaS90Day(s)EvaluationSaaS",
                        "attributes": [
                            {
                                "name": "CS_INVOICING_MODEL",
                                "value": "EVAL",
                                "valueDisplay": "Evaluation",
                                "nameDisplay": "InvoicingModel",
                            },
                            {
                                "name": "CS_CCM_MULTIV_UOM_CONC",
                                "value": "RESOURCES4000",
                                "valueDisplay": "RESOURCES4000",
                                "nameDisplay": "ConcatenateUOMwithCommit",
                            },
                            {
                                "name": "CS_BILL_FREQ",
                                "value": "M",
                                "valueDisplay": "Monthly",
                                "nameDisplay": "BillingFrequency",
                            },
                            {
                                "name": "CS_READ_ITM_TYPE",
                                "value": "ZQPV",
                                "valueDisplay": "ZQPV",
                                "nameDisplay": "ItemCategory",
                            },
                            {
                                "name": "CS_FIXED_COMMITMENT",
                                "value": "Y",
                                "valueDisplay": "Yes",
                                "nameDisplay": "FixedCommitment",
                            },
                            {
                                "name": "CS_HW_LED_MANDATORY_SAAS",
                                "value": "N",
                                "valueDisplay": "NO",
                                "nameDisplay": "HWLedMandatorySaaSFlag",
                            },
                            {
                                "name": "CS_CCM_MULTIV_UOM",
                                "value": "EVENTS_AND_TRANSACTIONS|METRIC_SERIES|RESOURCES",
                                "valueDisplay": "EventsandTransactions|MetricSeries|Resources",
                                "nameDisplay": "UnitofMeasure",
                            },
                            {
                                "name": "CS_CCM_METRICS",
                                "value": "200000",
                                "valueDisplay": "200000",
                                "nameDisplay": "CommitValueMETRICS",
                            },
                            {
                                "name": "CS_CCM_RESOURCES",
                                "value": "4000",
                                "valueDisplay": "4000",
                                "nameDisplay": "CommitValueRESOURCES",
                            },
                            {
                                "name": "CS_PRODUCT_ID",
                                "value": "S2E00AAE",
                                "valueDisplay": "S2E00AAE",
                                "nameDisplay": "BaseProductID",
                            },
                            {
                                "name": "CS_SCREEN_DEP_INVISIBLE",
                                "value": "CS_CCM_EVENTS|CS_CCM_MULTIV_UOM|CS_CCM_MULTIV_UOM_CONC|CS_CCM_SAMPLING|CS_CCM_TRACES|CS_FIXED_COMMITMENT|CS_HW_LED_MANDATORY_SAAS|CS_INSTALLATION|CS_INVOICING_MODEL|CS_PRICING_MODEL|CS_PRODUCT_CC|CS_PRODUCT_ID|CS_RANGE|CS_SWSC_AAS_HANDLING|ZTEST_UOM|ZTEST_UOM_TEMP",
                                "valueDisplay": "CS_CCM_EVENTS|CS_CCM_MULTIV_UOM|CS_CCM_MULTIV_UOM_CONC|CS_CCM_SAMPLING|CS_CCM_TRACES|CS_FIXED_COMMITMENT|CS_HW_LED_MANDATORY_SAAS|CS_INSTALLATION|CS_INVOICING_MODEL|CS_PRICING_MODEL|CS_PRODUCT_CC|CS_PRODUCT_ID|CS_RANGE|CS_SWSC_AAS_HANDLING|ZTEST_UOM|ZTEST_UOM_TEMP",
                                "nameDisplay": "ScreenDepInvisible",
                            },
                            {
                                "name": "CS_CCM_LOGS",
                                "value": "2000",
                                "valueDisplay": "2000",
                                "nameDisplay": "CommitValueLOGS",
                            },
                            {
                                "name": "CS_TIER",
                                "value": "ET",
                                "valueDisplay": "Enterprise",
                                "nameDisplay": "Tier",
                            },
                            {
                                "name": "CS_PRODUCT_CC",
                                "value": "S2E00AAE",
                                "valueDisplay": "S2E00AAE",
                                "nameDisplay": "ProductIDforCC",
                            },
                            {
                                "name": "CS_TERM_UOM",
                                "value": "D",
                                "valueDisplay": "Day(s)",
                                "nameDisplay": "TermUnitOfMeasure",
                            },
                            {
                                "name": "CS_SWSC_AAS_HANDLING",
                                "value": "SVC",
                                "valueDisplay": "Service",
                                "nameDisplay": "SoftwareSupChainaaSHandling",
                            },
                            {
                                "name": "CS_RANGE",
                                "value": "OCTO",
                                "valueDisplay": "OfficeofCTO",
                                "nameDisplay": "Range",
                            },
                            {
                                "name": "CS_CONFIG_TYPE",
                                "value": "001",
                                "valueDisplay": "EVALConfiguration",
                                "nameDisplay": "ConfigurationType",
                            },
                            {
                                "name": "CS_PRICING_MODEL",
                                "value": "TIER",
                                "valueDisplay": "Tier",
                                "nameDisplay": "PricingModel",
                            },
                            {
                                "name": "CS_TERM",
                                "value": "90",
                                "valueDisplay": "90",
                                "nameDisplay": "Term",
                            },
                        ],
                    },
                    "support": [
                        {
                            "name": "CS_TERM_UOM",
                            "value": "D",
                            "valueDisplay": "Day(s)",
                            "nameDisplay": "TermUnitOfMeasure",
                        },
                        {
                            "name": "CS_TERM",
                            "value": "90",
                            "valueDisplay": "90",
                            "nameDisplay": "Term",
                        },
                    ],
                    "licenses": [
                        {
                            "id": "YGUJAY2552U3",
                            "qty": "1.000",
                            "devices": [],
                            "customer": {},
                            "appointments": {
                                "subscriptionStart": "10.07.2023 00:00:00",
                                "subscriptionEnd": "08.10.2099 00:00:00",
                                "suspensionDate": null,
                                "cancellationDate": null,
                                "reactivationDate": null,
                                "activationDate": "10.07.2023 18:09:30",
                                "duration": "90",
                                "delayedActivation": null,
                                "autoRenewalDate": null,
                            },
                        }
                    ],
                }
            ],
        }
        return opsramp_eval_order

    @staticmethod
    def opsramp_non_eval_order():
        null = None
        opsramp_non_eval_order = {
            "reason": "Creation",
            "quote": "3100016374",
            "contract": "5100005129",
            "trial": False,
            "smcCode": "",
            "customer": {
                "MDM": "1000485126",
                "phone": "4062520171",
                "postal_code": "59101-3227",
                "address": "1465MonadRd",
                "city": "Billings",
                "country": "US",
                "state": "MT",
                "company_name": "GRAYBARELECTRICCOMPANY,INC.",
                "email": "noel.mejias-hernandez@hpe.com",
            },
            "activate": {
                "soldTo": "6280AmericaCenterDriveSANJOSEUS",
                "soldToName": "HEWLETTPACKARDENTERPRISECOMPANY",
                "soldToEmail": "",
                "shipTo": "1465MonadRdBillingsUS",
                "shipToName": "GRAYBARELECTRICCOMPANY,INC.",
                "shipToEmail": "",
                "endUser": "1465MonadRdBillingsUS",
                "endUserName": "GRAYBARELECTRICCOMPANY,INC.",
                "endUserEmail": "noel.mejias-hernandez@hpe.com",
                "po": "PONUMCCS_09_180827",
                "resellerPo": "",
                "endUserPo": "",
                "orderClass": "ZBRIM",
                "party": {
                    "id": "1000485126",
                    "countryId": "120425365",
                    "globalId": "120425364",
                },
                "parties": [
                    {
                        "function": "AG",
                        "id": "8999299909",
                        "countryId": "121489047",
                        "globalId": "121416014",
                    },
                    {
                        "function": "WE",
                        "id": "1000485126",
                        "countryId": "120425365",
                        "globalId": "120425364",
                    },
                    {
                        "function": "RE",
                        "id": "1000929240",
                        "countryId": "120777987",
                        "globalId": "120777986",
                    },
                    {
                        "function": "RG",
                        "id": "1000929240",
                        "countryId": "120777987",
                        "globalId": "120777986",
                    },
                    {
                        "function": "ZC",
                        "id": "1000485126",
                        "countryId": "120425365",
                        "globalId": "120425364",
                    },
                    {
                        "function": "ZE",
                        "id": "1000485126",
                        "countryId": "120425365",
                        "globalId": "120425364",
                    },
                    {
                        "function": "ZL",
                        "id": "1000485126",
                        "countryId": "120425365",
                        "globalId": "120425364",
                    },
                ],
                "contacts": [
                    {
                        "function": "ZG",
                        "id": "9001094115",
                        "countryId": null,
                        "globalId": null,
                    }
                ],
            },
            "entitlements": [
                {
                    "lineItem": "0000000010",
                    "quote": "3100016374",
                    "contract": "5100005129",
                    "total_qty": "1.000",
                    "available_qty": "0.00",
                    "product": {
                        "sku": "S2E00AAE",
                        "legacy": "",
                        "description": "OpsRampSaaS90Day(s)EvaluationSaaS",
                        "attributes": [
                            {
                                "name": "CS_CCM_MULTIV_UOM_CONC",
                                "value": "RESOURCES4000",
                                "valueDisplay": "RESOURCES4000",
                                "nameDisplay": "ConcatenateUOMwithCommit",
                            },
                            {
                                "name": "CS_BILL_FREQ",
                                "value": "M",
                                "valueDisplay": "Monthly",
                                "nameDisplay": "BillingFrequency",
                            },
                            {
                                "name": "CS_READ_ITM_TYPE",
                                "value": "ZQPV",
                                "valueDisplay": "ZQPV",
                                "nameDisplay": "ItemCategory",
                            },
                            {
                                "name": "CS_FIXED_COMMITMENT",
                                "value": "Y",
                                "valueDisplay": "Yes",
                                "nameDisplay": "FixedCommitment",
                            },
                            {
                                "name": "CS_HW_LED_MANDATORY_SAAS",
                                "value": "N",
                                "valueDisplay": "NO",
                                "nameDisplay": "HWLedMandatorySaaSFlag",
                            },
                            {
                                "name": "CS_CCM_MULTIV_UOM",
                                "value": "EVENTS_AND_TRANSACTIONS|METRIC_SERIES|RESOURCES",
                                "valueDisplay": "EventsandTransactions|MetricSeries|Resources",
                                "nameDisplay": "UnitofMeasure",
                            },
                            {
                                "name": "CS_CCM_METRICS",
                                "value": "200000",
                                "valueDisplay": "200000",
                                "nameDisplay": "CommitValueMETRICS",
                            },
                            {
                                "name": "CS_CCM_RESOURCES",
                                "value": "4000",
                                "valueDisplay": "4000",
                                "nameDisplay": "CommitValueRESOURCES",
                            },
                            {
                                "name": "CS_PRODUCT_ID",
                                "value": "S2E00AAE",
                                "valueDisplay": "S2E00AAE",
                                "nameDisplay": "BaseProductID",
                            },
                            {
                                "name": "CS_SCREEN_DEP_INVISIBLE",
                                "value": "CS_CCM_EVENTS|CS_CCM_MULTIV_UOM|CS_CCM_MULTIV_UOM_CONC|CS_CCM_SAMPLING|CS_CCM_TRACES|CS_FIXED_COMMITMENT|CS_HW_LED_MANDATORY_SAAS|CS_INSTALLATION|CS_INVOICING_MODEL|CS_PRICING_MODEL|CS_PRODUCT_CC|CS_PRODUCT_ID|CS_RANGE|CS_SWSC_AAS_HANDLING|ZTEST_UOM|ZTEST_UOM_TEMP",
                                "valueDisplay": "CS_CCM_EVENTS|CS_CCM_MULTIV_UOM|CS_CCM_MULTIV_UOM_CONC|CS_CCM_SAMPLING|CS_CCM_TRACES|CS_FIXED_COMMITMENT|CS_HW_LED_MANDATORY_SAAS|CS_INSTALLATION|CS_INVOICING_MODEL|CS_PRICING_MODEL|CS_PRODUCT_CC|CS_PRODUCT_ID|CS_RANGE|CS_SWSC_AAS_HANDLING|ZTEST_UOM|ZTEST_UOM_TEMP",
                                "nameDisplay": "ScreenDepInvisible",
                            },
                            {
                                "name": "CS_CCM_LOGS",
                                "value": "2000",
                                "valueDisplay": "2000",
                                "nameDisplay": "CommitValueLOGS",
                            },
                            {
                                "name": "CS_TIER",
                                "value": "ET",
                                "valueDisplay": "Enterprise",
                                "nameDisplay": "Tier",
                            },
                            {
                                "name": "CS_PRODUCT_CC",
                                "value": "S2E00AAE",
                                "valueDisplay": "S2E00AAE",
                                "nameDisplay": "ProductIDforCC",
                            },
                            {
                                "name": "CS_TERM_UOM",
                                "value": "D",
                                "valueDisplay": "Day(s)",
                                "nameDisplay": "TermUnitOfMeasure",
                            },
                            {
                                "name": "CS_SWSC_AAS_HANDLING",
                                "value": "SVC",
                                "valueDisplay": "Service",
                                "nameDisplay": "SoftwareSupChainaaSHandling",
                            },
                            {
                                "name": "CS_RANGE",
                                "value": "OCTO",
                                "valueDisplay": "OfficeofCTO",
                                "nameDisplay": "Range",
                            },
                            {
                                "name": "CS_CONFIG_TYPE",
                                "value": "001",
                                "valueDisplay": "EVALConfiguration",
                                "nameDisplay": "ConfigurationType",
                            },
                            {
                                "name": "CS_PRICING_MODEL",
                                "value": "TIER",
                                "valueDisplay": "Tier",
                                "nameDisplay": "PricingModel",
                            },
                            {
                                "name": "CS_TERM",
                                "value": "90",
                                "valueDisplay": "90",
                                "nameDisplay": "Term",
                            },
                        ],
                    },
                    "support": [
                        {
                            "name": "CS_TERM_UOM",
                            "value": "D",
                            "valueDisplay": "Day(s)",
                            "nameDisplay": "TermUnitOfMeasure",
                        },
                        {
                            "name": "CS_TERM",
                            "value": "90",
                            "valueDisplay": "90",
                            "nameDisplay": "Term",
                        },
                    ],
                    "licenses": [
                        {
                            "id": "YGUJAY2552U3",
                            "qty": "1.000",
                            "devices": [],
                            "customer": {},
                            "appointments": {
                                "subscriptionStart": "10.07.2023 00:00:00",
                                "subscriptionEnd": "08.10.2099 00:00:00",
                                "suspensionDate": null,
                                "cancellationDate": null,
                                "reactivationDate": null,
                                "activationDate": "10.07.2023 18:09:30",
                                "duration": "90",
                                "delayedActivation": null,
                                "autoRenewalDate": null,
                            },
                        }
                    ],
                }
            ],
        }
        return opsramp_non_eval_order

    @staticmethod
    def subs_pce_iaas_order():
        pce_iaas_order = {
            "reason": "Creation",
            "quote": "3100010815",
            "contract": "3100010815",
            "trial": True,
            "smcCode": "",
            "customer": {
                "MDM": "1000410004",
                "phone": "4062520171",
                "postal_code": "94089",
                "address": "6280 America Center Drive",
                "city": "San Jose",
                "country": "US",
                "state": "CA",
                "company_name": "GLCP Automation HPE, INC.",
                "email": "autoactivatesmpce@hpe.com",
            },
            "activate": {
                "soldTo": "6280 America Center Drive San Jose US",
                "soldToName": "HEWLETT PACKARD ENTERPRISE INC",
                "soldToEmail": "",
                "shipTo": "6280 America Center Drive San Jose US",
                "shipToName": "GLCP Automation HPE, INC.",
                "shipToEmail": "",
                "endUser": "PCE Test endUser",
                "endUserName": "PCE Test endUser",
                "endUserEmail": "endUserTest@pce.com",
                "po": "PONUMCCS_09_100001",
                "resellerPo": "",
                "endUserPo": "",
                "orderClass": "ZBRIM",
                "party": {
                    "id": "1001760815",
                    "countryId": "120790815",
                    "globalId": "120790815",
                },
                "parties": [
                    {
                        "function": "AG",
                        "id": "2000410001",
                        "countryId": "220420001",
                        "globalId": "220430001",
                    },
                    {
                        "function": "WE",
                        "id": "2000410001",
                        "countryId": "220420001",
                        "globalId": "220430001",
                    },
                    {
                        "function": "RE",
                        "id": "2000410001",
                        "countryId": "220420001",
                        "globalId": "220430001",
                    },
                    {
                        "function": "RG",
                        "id": "1000929240",
                        "countryId": "120777987",
                        "globalId": "120777986",
                    },
                    {
                        "function": "ZC",
                        "id": "1000485126",
                        "countryId": "120425365",
                        "globalId": "120425364",
                    },
                    {
                        "function": "ZE",
                        "id": "1001760815",
                        "countryId": "120790815",
                        "globalId": "120790815",
                    },
                    {
                        "function": "ZL",
                        "id": "1000485126",
                        "countryId": "120425365",
                        "globalId": "120425364",
                    },
                ],
                "contacts": [
                    {
                        "function": "ZG",
                        "id": "9001093764",
                        "countryId": None,
                        "globalId": None,
                    }
                ],
            },
            "entitlements": [
                {
                    "lineItem": "0000000010",
                    "quote": "3100010815",
                    "contract": "3100010815",
                    "total_qty": "1.000",
                    "available_qty": "0.00",
                    "POOLED_COMMIT_FLAG": False,
                    "POOLED_COMMIT_TECH_RES": "",
                    "product": {
                        "sku": "SKU",
                        "legacy": "",
                        "description": "HPE GreenLake Private Cloud Enterprise",
                        "attributes": [
                            {
                                "name": "CS_INVOICING_MODEL",
                                "value": "EVAL",
                                "valueDisplay": "Evaluation",
                                "nameDisplay": "Invoicing Model",
                            },
                            {
                                "name": "CS_CCM_MULTIV_UOM_CONC",
                                "value": "SWITCHES, 0",
                                "valueDisplay": "SWITCHES, 0",
                                "nameDisplay": "Concatenate UOM with Commit",
                            },
                            {
                                "name": "CS_BILL_FREQ",
                                "value": "M",
                                "valueDisplay": "Monthly",
                                "nameDisplay": "Billing Frequency",
                            },
                            {
                                "name": "CS_READ_ITM_TYPE",
                                "value": "ZQPV",
                                "valueDisplay": "ZQPV",
                                "nameDisplay": "Item Category",
                            },
                            {
                                "name": "CS_FIXED_COMMITMENT",
                                "value": "Y",
                                "valueDisplay": "Yes",
                                "nameDisplay": "Fixed Commitment",
                            },
                            {
                                "name": "CS_CCM_MULTIV_UOM",
                                "value": "SWITCHES",
                                "valueDisplay": "SWITCHES",
                                "nameDisplay": "Unit of Measure",
                            },
                            {
                                "name": "CS_PRODUCT_ID",
                                "value": "SKU",
                                "valueDisplay": "SKU",
                                "nameDisplay": "Base Product ID",
                            },
                            {
                                "name": "CS_SCREEN_DEP_INVISIBLE",
                                "value": "CS_CCM_MULTIV_UOM_CONC|CS_CCM_NVME|CS_CCM_SWITCHES|CS_FIXED_COMMITMENT|CS_PRICING_MODEL|CS_PRODUCT_CC|CS_PRODUCT_ID|CS_RANGE|CS_READ_ITM_TYPE|CS_SCREEN_DEP_INVISIBLE|CS_SDCOM_VKOND|CS_SWSC_AAS_HANDLING|CS_TIER|EVERGREEN",
                                "valueDisplay": "CS_CCM_MULTIV_UOM_CONC|CS_CCM_NVME|CS_CCM_SWITCHES|CS_FIXED_COMMITMENT|CS_PRICING_MODEL|CS_PRODUCT_CC|CS_PRODUCT_ID|CS_RANGE|CS_READ_ITM_TYPE|CS_SCREEN_DEP_INVISIBLE|CS_SDCOM_VKOND|CS_SWSC_AAS_HANDLING|CS_TIER|EVERGREEN",
                                "nameDisplay": "Screen Dep Invisible",
                            },
                            {
                                "name": "CS_TIER",
                                "value": "FN",
                                "valueDisplay": "Foundation",
                                "nameDisplay": "Tier",
                            },
                            {
                                "name": "CS_PRODUCT_CC",
                                "value": "FABMGMT",
                                "valueDisplay": "Storage Fabric Management",
                                "nameDisplay": "Product ID for CC",
                            },
                            {
                                "name": "CS_TERM_UOM",
                                "value": "D",
                                "valueDisplay": "Day(s)",
                                "nameDisplay": "Term Unit Of Measure",
                            },
                            {
                                "name": "CS_SWSC_AAS_HANDLING",
                                "value": "SVC",
                                "valueDisplay": "Service",
                                "nameDisplay": "Software SupChain aaS Handling",
                            },
                            {
                                "name": "CS_RANGE",
                                "value": "STO",
                                "valueDisplay": "Storage",
                                "nameDisplay": "Range",
                            },
                            {
                                "name": "CS_CONFIG_TYPE",
                                "value": "001",
                                "valueDisplay": "EVAL Configuration",
                                "nameDisplay": "Configuration Type",
                            },
                            {
                                "name": "CS_PRICING_MODEL",
                                "value": "TIER",
                                "valueDisplay": "Tier",
                                "nameDisplay": "Pricing Model",
                            },
                            {
                                "name": "CS_TERM",
                                "value": "180",
                                "valueDisplay": "180",
                                "nameDisplay": "Term",
                            },
                        ],
                    },
                    "support": [],
                    "licenses": [
                        {
                            "id": "SUBKEY",
                            "qty": "1.000",
                            "customer": {},
                            "devices": [],
                            "appointments": {
                                "subscriptionStart": "11.11.2022 00:00:00",
                                "subscriptionEnd": "11.11.2025 00:00:00",
                                "suspensionDate": None,
                                "cancellationDate": None,
                                "reactivationDate": None,
                                "activationDate": None,
                                "duration": "180",
                                "delayedActivation": None,
                                "autoRenewalDate": None,
                            },
                        }
                    ],
                }
            ],
        }

        return pce_iaas_order

    @staticmethod
    def create_pce_iaas_order_payload(
        quote_number=None,
        product_sku=None,
        subscription_key=None,
        end_username=None,
        device_serial=None,
        device_material=None,
    ):
        """
        Helper method to get pce iaas subscription oder
        :param quote_number: Quote number
        :param product_sku: Product SKU
        :param subscription_key: Subscription key
        :param end_username:
        :param device_serial: Device serial
        :param device_material: Device SKU
        :return: Subscription order body request
        """
        pce_iaas_payload = SmInputPayload.subs_pce_iaas_order()

        if quote_number is None:
            quote_number = RandomGenUtils.random_string_of_chars(
                length=10, lowercase=False, uppercase=True, digits=False
            )

        if subscription_key is None:
            subscription_key = RandomGenUtils.random_string_of_chars(
                length=20, lowercase=False, uppercase=False, digits=True
            )

        if device_serial is None:
            device_serial = "SN" + RandomGenUtils.random_string_of_chars(
                length=10, lowercase=False, uppercase=True, digits=True
            )

        if device_material is None:
            device_material = "PN" + RandomGenUtils.random_string_of_chars(
                length=10, lowercase=False, uppercase=True, digits=True
            )

        if end_username is None:
            end_username = RandomGenUtils.random_string_of_chars(
                length=10, lowercase=True, uppercase=False, digits=True
            )

        # device_list = [{"serial": serial, "material": material}]
        device_list = [{"serial": device_serial, "material": device_material}]

        if product_sku not in SmInputPayload.get_pce_supported_skus():
            log.error(
                "Failed to create pce subscription order for key: {}, with quote: {}\n. Product sku {} is not supported".format(
                    subscription_key, quote_number, subscription_key
                )
            )
            return None

        pce_iaas_payload["quote"] = quote_number
        pce_iaas_payload["entitlements"][0]["quote"] = pce_iaas_payload["quote"]

        pce_iaas_payload["contract"] = RandomGenUtils.random_string_of_chars(
            length=10, lowercase=False, uppercase=True, digits=False
        )
        pce_iaas_payload["entitlements"][0]["contract"] = pce_iaas_payload["contract"]
        pce_iaas_payload["activate"]["endUserName"] = (
            "Test_PCE_" + end_username + " Company"
        )

        pce_iaas_payload["customer"]["MDM"] = RandomGenUtils.random_string_of_chars(
            length=10, lowercase=False, uppercase=True, digits=False
        )

        pce_iaas_payload["activate"]["po"] = (
            "PONUMCCS_09_100001_" + pce_iaas_payload["customer"]["MDM"]
        )
        pce_iaas_payload["activate"]["party"]["id"] = pce_iaas_payload["customer"]["MDM"]
        pce_iaas_payload["activate"]["party"]["countryId"] = pce_iaas_payload["customer"][
            "MDM"
        ]
        pce_iaas_payload["activate"]["party"]["globalId"] = pce_iaas_payload["customer"][
            "MDM"
        ]

        for i in range(0, len(pce_iaas_payload["activate"]["parties"])):
            pce_iaas_payload["activate"]["parties"][i]["id"] = pce_iaas_payload[
                "customer"
            ]["MDM"]
            pce_iaas_payload["activate"]["parties"][i]["countryId"] = pce_iaas_payload[
                "customer"
            ]["MDM"]
            pce_iaas_payload["activate"]["parties"][i]["globalId"] = pce_iaas_payload[
                "customer"
            ]["MDM"]

        for i in range(0, len(pce_iaas_payload["activate"]["contacts"])):
            pce_iaas_payload["activate"]["contacts"][i]["id"] = pce_iaas_payload[
                "customer"
            ]["MDM"]
            pce_iaas_payload["activate"]["contacts"][i]["countryId"] = pce_iaas_payload[
                "customer"
            ]["MDM"]
            pce_iaas_payload["activate"]["contacts"][i]["globalId"] = pce_iaas_payload[
                "customer"
            ]["MDM"]

        pce_iaas_payload["entitlements"][0]["licenses"][0]["id"] = subscription_key
        pce_iaas_payload["entitlements"][0]["product"]["sku"] = product_sku

        product_attributes = pce_iaas_payload["entitlements"][0]["product"]["attributes"]

        for i in range(0, len(product_attributes)):
            if product_attributes[i]["name"] == "CS_PRODUCT_ID":
                product_attributes[i]["value"] = product_sku
                product_attributes[i]["valueDisplay"] = product_sku

        # Add pce device serial and material
        for i in range(0, len(device_list)):
            pce_iaas_payload["entitlements"][0]["licenses"][0]["devices"].append(
                device_list[i]
            )

        return pce_iaas_payload

    @staticmethod
    def subs_sdwan_order():
        sdwan_order = {
            "reason": "Creation",
            "quote": "QUOTE",
            "contract": "CONTRACT",
            "smcCode": "E",
            "squid": "ITGa6JzM7ow7WON8KF_QAmVLKFAsZ_hWgPVsaqbDAeKm2k=",
            "customer": {
                "MDM": "1000755838",
                "phone": "8056447100",
                "postal_code": "94089",
                "address": "6280 America Center Drive",
                "city": "San Jose",
                "country": "US",
                "state": "CA",
                "company_name": "GLCP Automation HPE, INC.",
                "email": "autoactivatesmsdwan@hpe.com",
            },
            "activate": {
                "soldTo": "6280 America Center Drive San Jose US",
                "soldToName": "HEWLETT PACKARD ENTERPRISE INC",
                "soldToEmail": "",
                "shipTo": "6280 America Center Drive San Jose US",
                "shipToName": "GLCP Automation HPE, INC.",
                "shipToEmail": "",
                "endUser": "SDWAN Test endUser",
                "endUserName": "SDWAN Test endUser",
                "endUserEmail": "endUserTest@sdwan.com",
                "reseller": "6280 America Center Drive San Jose US",
                "resellerName": "HPE INC.",
                "resellerEmail": "",
                "po": "3100929430",
                "resellerPo": "",
                "endUserPo": "",
                "orderClass": "ZBRIM",
                "party": {
                    "id": "3100929430",
                    "countryId": "3100929430",
                    "globalId": "3100929430",
                },
                "parties": [
                    {
                        "function": "AG",
                        "id": "1000765471",
                        "countryId": "121482897",
                        "globalId": "121105452",
                    },
                    {
                        "function": "WE",
                        "id": "1000755838",
                        "countryId": "120790310",
                        "globalId": "120790309",
                    },
                    {
                        "function": "RE",
                        "id": "1000765471",
                        "countryId": "121482897",
                        "globalId": "121105452",
                    },
                    {
                        "function": "RG",
                        "id": "1000765471",
                        "countryId": "121482897",
                        "globalId": "121105452",
                    },
                    {
                        "function": "Z1",
                        "id": "1000911033",
                        "countryId": "121410855",
                        "globalId": "120773756",
                    },
                    {
                        "function": "ZC",
                        "id": "1000755838",
                        "countryId": "120790310",
                        "globalId": "120790309",
                    },
                    {
                        "function": "ZE",
                        "id": "3100929430",
                        "countryId": "3100929430",
                        "globalId": "3100929430",
                    },
                    {
                        "function": "ZL",
                        "id": "1000755838",
                        "countryId": "120790310",
                        "globalId": "120790309",
                    },
                ],
                "contacts": [
                    {
                        "function": "CS",
                        "id": "9000047270",
                        "countryId": None,
                        "globalId": None,
                    },
                    {
                        "function": "SM",
                        "id": "9000604423",
                        "countryId": None,
                        "globalId": None,
                    },
                    {
                        "function": "ZG",
                        "id": "9000604423",
                        "countryId": None,
                        "globalId": None,
                    },
                ],
            },
            "entitlements": [
                {
                    "lineItem": "0000000010",
                    "quote": "QUOTE",
                    "contract": "CONTRACT",
                    "total_qty": "10.000",
                    "available_qty": "0.00",
                    "product": {
                        "sku": "SKU",
                        "description": "EC_SDWAN_HUB",
                        "attributes": [
                            {
                                "name": "TERM_IN_MONTHS",
                                "value": "36",
                                "valueDisplay": "36",
                                "nameDisplay": "Term In Months",
                            },
                            {
                                "name": "CS_NET_CENTRAL_PLATFORM",
                                "value": "CLOUD",
                                "valueDisplay": "CLOUD",
                                "nameDisplay": "Central platform",
                            },
                            {
                                "name": "EVERGREEN",
                                "value": "NO",
                                "valueDisplay": "NO",
                                "nameDisplay": "EVERGREEN",
                            },
                            {
                                "name": "CS_TIER",
                                "value": "FO",
                                "valueDisplay": "Foundation",
                                "nameDisplay": "Tier",
                            },
                            {
                                "name": "HIDE_CHAR",
                                "value": "COMMITMENT_VALUE1|FIXED_COMMITMENT|TERM|TERM_UOM",
                                "valueDisplay": "COMMITMENT_VALUE1|FIXED_COMMITMENT|TERM|TERM_UOM",
                                "nameDisplay": "HIDE CHARACTERISTICS",
                            },
                            {
                                "name": "TERM_UOM",
                                "value": "Y",
                                "valueDisplay": "Year(s)",
                                "nameDisplay": "Term Unit of Measure",
                            },
                            {
                                "name": "TERM_IN_MONTHS_MIN_2",
                                "value": "12",
                                "valueDisplay": "12",
                                "nameDisplay": "Term in months minimum",
                            },
                            {
                                "name": "TERM",
                                "value": "3",
                                "valueDisplay": "3",
                                "nameDisplay": "Term",
                            },
                            {
                                "name": "PRODUCT_ID",
                                "value": "JN003AAS",
                                "valueDisplay": "JN003AAS",
                                "nameDisplay": "Product ID",
                            },
                            {
                                "name": "GW_FAMILY",
                                "value": "EC_HUB",
                                "valueDisplay": "EC_SDWAN_HUB",
                                "nameDisplay": "Gateway Family",
                            },
                            {
                                "name": "BILL_FREQ",
                                "value": "UP",
                                "valueDisplay": "Upfront",
                                "nameDisplay": "BILLING FREQUENCY",
                            },
                            {
                                "name": "PRICING_MODEL",
                                "value": "TIER",
                                "valueDisplay": "Tier",
                                "nameDisplay": "Pricing Model",
                            },
                            {
                                "name": "TERM_IN_MONTHS_MAX_2",
                                "value": "36",
                                "valueDisplay": "36",
                                "nameDisplay": "Term in months maximum",
                            },
                            {
                                "name": "INVOICING_MODEL",
                                "value": "PR_DR",
                                "valueDisplay": "Prepaid Drawdown",
                                "nameDisplay": "INVOICING MODEL",
                            },
                            {
                                "name": "PRODUCT_CC",
                                "value": "CENTRAL_GW",
                                "valueDisplay": "Central_GW",
                                "nameDisplay": "Product ID for CC",
                            },
                            {
                                "name": "CS_TERM_UOM",
                                "value": "Y",
                                "valueDisplay": "Year(s)",
                                "nameDisplay": "Term Unit Of Measure",
                            },
                            {
                                "name": "CS_SWSC_AAS_HANDLING",
                                "value": "DEV",
                                "valueDisplay": "Device",
                                "nameDisplay": "Software SupChain aaS Handling",
                            },
                            {
                                "name": "GW_TYPE",
                                "value": "SDWAN",
                                "valueDisplay": "SDWAN",
                                "nameDisplay": "Gateway Type",
                            },
                            {
                                "name": "TIER_GW",
                                "value": "FO",
                                "valueDisplay": "Foundation",
                                "nameDisplay": "Gateway Tier",
                            },
                            {
                                "name": "CS_TERM",
                                "value": "3",
                                "valueDisplay": "3",
                                "nameDisplay": "Term",
                            },
                        ],
                    },
                    "support": [
                        {
                            "name": "CS_TCS_TECH_SUPPORT",
                            "value": "Y",
                            "valueDisplay": "Year(s)",
                            "nameDisplay": "Technical Support",
                        },
                        {
                            "name": "CS_TCS_TECH_GUIDANCE",
                            "value": "Y",
                            "valueDisplay": "Year(s)",
                            "nameDisplay": "General Technical Guidance",
                        },
                        {
                            "name": "CS_TCS_RESPONSE_TIME",
                            "value": "2HR",
                            "valueDisplay": "2 Hours",
                            "nameDisplay": "Response Time",
                        },
                        {
                            "name": "CS_TERM_UOM",
                            "value": "Y",
                            "valueDisplay": "Year(s)",
                            "nameDisplay": "Term Unit Of Measure",
                        },
                        {
                            "name": "CS_TCS_COV_WINDOW7",
                            "value": "24",
                            "valueDisplay": "24 Hours",
                            "nameDisplay": "Coverage Window 24x7",
                        },
                        {
                            "name": "CS_TCS_COLLAB_SUPPORT",
                            "value": "Y",
                            "valueDisplay": "Year(s)",
                            "nameDisplay": "Collaborative Supp and Assist",
                        },
                        {
                            "name": "CS_TCS_SERVICE_LEVEL",
                            "value": "ESS",
                            "valueDisplay": "Essential",
                            "nameDisplay": "Service Level",
                        },
                        {
                            "name": "CS_TERM",
                            "value": "3",
                            "valueDisplay": "3",
                            "nameDisplay": "Term",
                        },
                    ],
                    "licenses": [
                        {
                            "id": "KEY",
                            "qty": "10.000",
                            "devices": [],
                            "customer": {},
                            "appointments": {
                                "subscriptionStart": "20.08.2023 00:00:00",
                                "subscriptionEnd": "20.08.2026 00:00:00",
                                "suspensionDate": None,
                                "cancellationDate": None,
                                "reactivationDate": None,
                                "activationDate": "21.08.2023 00:00:00",
                                "duration": "3",
                                "delayedActivation": None,
                                "autoRenewalDate": None,
                            },
                        }
                    ],
                }
            ],
        }

        return sdwan_order

    @staticmethod
    def create_sdwan_order_payload(
        quote_number=None,
        product_sku=None,
        subscription_key=None,
        end_username=None,
        tier="FO",
    ):
        """
        Helper method to create subscription order for SDWAN devices
        :param quote_number: Quote number
        :param product_sku: Product SKU
        :param subscription_key: Subscription key
        :param end_username: End username
        :param tier: Subscription tier foundation, advanced etc
        :return: Subscription order request
        """

        sdwan_payload = SmInputPayload.subs_sdwan_order()

        if quote_number is None:
            quote_number = RandomGenUtils.random_string_of_chars(
                length=10, lowercase=False, uppercase=True, digits=False
            )

        if subscription_key is None:
            subscription_key = RandomGenUtils.random_string_of_chars(
                length=20, lowercase=False, uppercase=False, digits=True
            )

        if product_sku not in SmInputPayload.get_sdwan_supported_skus():
            log.error(
                "Failed to create sdwan subscription order for key: {}, with quote: {}\n. Product sku {} is not "
                "supported".format(subscription_key, quote_number, subscription_key)
            )
            return None

        if end_username is None:
            end_username = RandomGenUtils.random_string_of_chars(
                length=10, lowercase=True, uppercase=False, digits=True
            )

        sdwan_payload["quote"] = quote_number
        sdwan_payload["entitlements"][0]["quote"] = sdwan_payload["quote"]

        sdwan_payload["contract"] = RandomGenUtils.random_string_of_chars(
            length=10, lowercase=False, uppercase=True, digits=False
        )
        sdwan_payload["entitlements"][0]["contract"] = sdwan_payload["contract"]
        sdwan_payload["activate"]["endUserName"] = (
            "Test_SDWAN_" + end_username + " Company"
        )

        sdwan_payload["customer"]["MDM"] = RandomGenUtils.random_string_of_chars(
            length=10, lowercase=False, uppercase=True, digits=False
        )

        sdwan_payload["activate"]["po"] = (
            "PONUMCCS_09_100001_" + sdwan_payload["customer"]["MDM"]
        )
        sdwan_payload["activate"]["party"]["id"] = sdwan_payload["customer"]["MDM"]
        sdwan_payload["activate"]["party"]["countryId"] = sdwan_payload["customer"]["MDM"]
        sdwan_payload["activate"]["party"]["globalId"] = sdwan_payload["customer"]["MDM"]

        for i in range(0, len(sdwan_payload["activate"]["parties"])):
            sdwan_payload["activate"]["parties"][i]["id"] = sdwan_payload["customer"][
                "MDM"
            ]
            sdwan_payload["activate"]["parties"][i]["countryId"] = sdwan_payload[
                "customer"
            ]["MDM"]
            sdwan_payload["activate"]["parties"][i]["globalId"] = sdwan_payload[
                "customer"
            ]["MDM"]

        for i in range(0, len(sdwan_payload["activate"]["contacts"])):
            sdwan_payload["activate"]["contacts"][i]["id"] = sdwan_payload["customer"][
                "MDM"
            ]
            sdwan_payload["activate"]["contacts"][i]["countryId"] = sdwan_payload[
                "customer"
            ]["MDM"]
            sdwan_payload["activate"]["contacts"][i]["globalId"] = sdwan_payload[
                "customer"
            ]["MDM"]

        sdwan_payload["entitlements"][0]["licenses"][0]["id"] = subscription_key
        sdwan_payload["entitlements"][0]["product"]["sku"] = product_sku

        for attribute in sdwan_payload["entitlements"][0]["product"]["attributes"]:
            if attribute["name"] == "PRODUCT_ID":
                attribute["value"] = product_sku
                attribute["valueDisplay"] = product_sku
            if attribute["name"] == "CS_TIER":
                attribute["value"] = tier
                if tier == "FO":
                    attribute["valueDisplay"] = "Foundation"
                else:
                    attribute["valueDisplay"] = "Advanced"

        return sdwan_payload

    @staticmethod
    def create_sensor_order_payload(
        quote_number=None,
        product_sku=None,
        subscription_key=None,
        end_username=None,
        tier="FO",
    ):
        """
        Helper method to create subscription order for SENSOR devices
        :param quote_number: Quote number
        :param product_sku: Product SKU
        :param subscription_key: Subscription key
        :param end_username: End username
        :param tier: Subscription tier foundation, advanced etc
        :return: Subscription order request
        """

        sensor_payload = SmInputPayload.subs_sdwan_order()

        if quote_number is None:
            quote_number = RandomGenUtils.random_string_of_chars(
                length=10, lowercase=False, uppercase=True, digits=False
            )

        if subscription_key is None:
            subscription_key = RandomGenUtils.random_string_of_chars(
                length=20, lowercase=False, uppercase=False, digits=True
            )

        if end_username is None:
            end_username = RandomGenUtils.random_string_of_chars(
                length=10, lowercase=True, uppercase=False, digits=True
            )

        sensor_payload["quote"] = quote_number
        sensor_payload["entitlements"][0]["quote"] = sensor_payload["quote"]

        sensor_payload["contract"] = RandomGenUtils.random_string_of_chars(
            length=10, lowercase=False, uppercase=True, digits=False
        )
        sensor_payload["entitlements"][0]["contract"] = sensor_payload["contract"]
        sensor_payload["activate"]["endUserName"] = (
            "Test_SENSOR_" + end_username + " Company"
        )

        sensor_payload["customer"]["MDM"] = RandomGenUtils.random_string_of_chars(
            length=10, lowercase=False, uppercase=True, digits=False
        )

        sensor_payload["activate"]["po"] = (
            "PONUMCCS_09_100001_" + sensor_payload["customer"]["MDM"]
        )
        sensor_payload["activate"]["party"]["id"] = sensor_payload["customer"]["MDM"]
        sensor_payload["activate"]["party"]["countryId"] = sensor_payload["customer"][
            "MDM"
        ]
        sensor_payload["activate"]["party"]["globalId"] = sensor_payload["customer"][
            "MDM"
        ]

        for i in range(0, len(sensor_payload["activate"]["parties"])):
            sensor_payload["activate"]["parties"][i]["id"] = sensor_payload["customer"][
                "MDM"
            ]
            sensor_payload["activate"]["parties"][i]["countryId"] = sensor_payload[
                "customer"
            ]["MDM"]
            sensor_payload["activate"]["parties"][i]["globalId"] = sensor_payload[
                "customer"
            ]["MDM"]

        for i in range(0, len(sensor_payload["activate"]["contacts"])):
            sensor_payload["activate"]["contacts"][i]["id"] = sensor_payload["customer"][
                "MDM"
            ]
            sensor_payload["activate"]["contacts"][i]["countryId"] = sensor_payload[
                "customer"
            ]["MDM"]
            sensor_payload["activate"]["contacts"][i]["globalId"] = sensor_payload[
                "customer"
            ]["MDM"]

        sensor_payload["entitlements"][0]["licenses"][0]["id"] = subscription_key
        sensor_payload["entitlements"][0]["product"]["sku"] = product_sku

        for attribute in sensor_payload["entitlements"][0]["product"]["attributes"]:
            if attribute["name"] == "PRODUCT_ID":
                attribute["value"] = product_sku
                attribute["valueDisplay"] = product_sku
            if attribute["name"] == "CS_TIER":
                attribute["value"] = tier
                if tier == "FO":
                    attribute["valueDisplay"] = "Foundation"
                else:
                    attribute["valueDisplay"] = "Advanced"

        return sensor_payload
