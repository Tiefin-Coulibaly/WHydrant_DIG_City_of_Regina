PRODUCTION_SDE_CONNECTION_FILE = r"K:\ConnectionFiles\cgisp_gssrc.sde"
# PRODUCTION_SDE_CONNECTION_FILE = r"K:\ConnectionFiles\cgist_gssrc.sde"
FEATURE_DATASET_NAME = "GSSRC.WN_WaterNetwork"

FEATURE_SCHEMA = {
    "AREA_NAME": {
        "type": "TEXT",
    },
    "UPDATE_USER": {
        "type": "TEXT",
        "alias": "Update User",
    },
    "DRAWING_STATUS": {
        "type": "TEXT",
        "alias": "Drawing Status",
        "domain": "GS_DrawingStatus",
    },
    "ASSETID": {
        "type": "LONG",
    },
    "OWNEDBY": {
        "type": "TEXT",
        "default": "City",
        "domain": "WN_OwnedBy",
    },
    "SAC_ANODE": {
        "type": "TEXT",
        "domain": "WN_YesNo",
    },
    "INSTALL_DATE": {
        "type": "DATE",
        "alias": "Installation Date",
    },
    "COMMENTS": {
        "type": "TEXT",
        "alias": "Comments",
    },
    "SURVEY_DATE": {
        "type": "DATE",
        "alias": "Survey Date",
    },
    "GSID": {
        "type": "LONG",
        "alias": "GISID",
    },
    "UPDATE_DATE": {
        "type": "DATE",
        "alias": "Update Date",
    },
    "PROJECT": {
        "type": "TEXT",
        "alias": "Project Number",
    },
    "INSTALLED_BY": {
        "type": "TEXT",
        "alias": "Installed By",
        "domain": "WWE_INSTALLERS",
        "default": "UNKNOWN",
    },
    "MAINTAINED_BY": {
        "type": "TEXT",
        "alias": "Maintained By",
        "domain": "GS_MaintainedBy",
        "default": "C",
    },
    "REFERENCE": {
        "type": "TEXT",
        "alias": "Reference of information ",
    },
    "ENABLED": {
        "type": "TEXT",
        "alias": "Enabled",
        "default": "True",
        "domain": "WN_EnabledDomain",
    },
    "DRAWING_STATUS": {
        "type": "TEXT",
        "alias": "Drawing Status",
        "domain": "GS_DrawingStatus",
    },
    "SYMBOLANGLE": {
        "type": "DOUBLE",
        "alias": "Symbol Angle",
        "default": 0,
    },
}

DOMAINS_TO_CREATE_IN_GDB = {
    "WN_OwnedBy": {
        "field_type": "TEXT",
        "domain_type": "CODED",
        "split_policy": "DEFAULT",
        "merge_policy": "DEFAULT",
        "coded_values": {
            "City": "City",
            "Private": "Private",
            "RM of Sherwood": "RM of Sherwood",
            "Uofr": "Uofr",
        },
    },
    "WN_YesNo": {
        "field_type": "TEXT",
        "domain_type": "CODED",
        "split_policy": "DEFAULT",
        "merge_policy": "DEFAULT",
        "coded_values": {
            "Y": "Yes",
            "N": "No",
            "N/A": "N/A",
        },
    },
}
