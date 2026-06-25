FEATURE_NAMES = [
    "having_IP_Address",
    "URL_Length",
    "Shortining_Service",
    "having_At_Symbol",
    "double_slash_redirecting",
    "Prefix_Suffix",
    "having_Sub_Domain",
    "SSLfinal_State",
    "Domain_registeration_length",
    "Favicon",
    "port",
    "HTTPS_token",
    "Request_URL",
    "URL_of_Anchor",
    "Links_in_tags",
    "SFH",
    "Submitting_to_email",
    "Abnormal_URL",
    "Redirect",
    "on_mouseover",
    "RightClick",
    "popUpWidnow",
    "Iframe",
    "age_of_domain",
    "DNSRecord",
    "web_traffic",
    "Page_Rank",
    "Google_Index",
    "Links_pointing_to_page",
    "Statistical_report",
]

FEATURE_GROUPS = {
    "URL Structure": [
        "having_IP_Address",
        "URL_Length",
        "Shortining_Service",
        "having_At_Symbol",
        "double_slash_redirecting",
        "Prefix_Suffix",
        "having_Sub_Domain",
        "Abnormal_URL",
        "Redirect",
    ],
    "Security Signals": [
        "SSLfinal_State",
        "Domain_registeration_length",
        "HTTPS_token",
        "Submitting_to_email",
        "age_of_domain",
        "DNSRecord",
        "Google_Index",
        "Statistical_report",
    ],
    "Page Behavior": [
        "Favicon",
        "port",
        "Request_URL",
        "URL_of_Anchor",
        "Links_in_tags",
        "SFH",
        "on_mouseover",
        "RightClick",
        "popUpWidnow",
        "Iframe",
        "web_traffic",
        "Page_Rank",
        "Links_pointing_to_page",
    ],
}

FEATURE_OPTIONS = {
    "having_IP_Address": {-1: "No IP address", 1: "IP address present"},
    "URL_Length": {-1: "Suspicious length", 0: "Moderate length", 1: "Normal length"},
    "Shortining_Service": {-1: "Shortener used", 1: "No shortener"},
    "having_At_Symbol": {-1: "@ symbol present", 1: "No @ symbol"},
    "double_slash_redirecting": {-1: "Redirect pattern present", 1: "No redirect pattern"},
    "Prefix_Suffix": {-1: "Hyphenated domain", 1: "No hyphenation"},
    "having_Sub_Domain": {-1: "Many subdomains", 0: "Some subdomains", 1: "Normal subdomain"},
    "SSLfinal_State": {-1: "Invalid SSL", 0: "Untrusted SSL", 1: "Trusted SSL"},
    "Domain_registeration_length": {-1: "Short registration", 1: "Long registration"},
    "Favicon": {-1: "External favicon", 1: "Local favicon"},
    "port": {-1: "Non-standard port", 1: "Standard port"},
    "HTTPS_token": {-1: "HTTPS token in domain", 1: "No HTTPS token abuse"},
    "Request_URL": {-1: "External requests high", 1: "External requests low"},
    "URL_of_Anchor": {-1: "Unsafe anchors", 0: "Mixed anchors", 1: "Safe anchors"},
    "Links_in_tags": {-1: "Suspicious tag links", 0: "Mixed tag links", 1: "Normal tag links"},
    "SFH": {-1: "Suspicious form handler", 0: "Empty form handler", 1: "Safe form handler"},
    "Submitting_to_email": {-1: "Submits to email", 1: "No email submission"},
    "Abnormal_URL": {-1: "Abnormal URL", 1: "Normal URL"},
    "Redirect": {0: "No redirect", 1: "One redirect"},
    "on_mouseover": {-1: "Status bar change", 1: "No status bar change"},
    "RightClick": {-1: "Right-click disabled", 1: "Right-click enabled"},
    "popUpWidnow": {-1: "Popup present", 1: "No popup"},
    "Iframe": {-1: "Iframe present", 1: "No iframe"},
    "age_of_domain": {-1: "Young domain", 1: "Established domain"},
    "DNSRecord": {-1: "No DNS record", 1: "DNS record found"},
    "web_traffic": {-1: "Low traffic", 0: "Moderate traffic", 1: "High traffic"},
    "Page_Rank": {-1: "Low page rank", 1: "Strong page rank"},
    "Google_Index": {-1: "Not indexed", 1: "Indexed"},
    "Links_pointing_to_page": {-1: "Few backlinks", 0: "Some backlinks", 1: "Many backlinks"},
    "Statistical_report": {-1: "Reported suspicious", 1: "No suspicious report"},
}

DEFAULT_FEATURE_VALUES = {
    name: 1 if 1 in FEATURE_OPTIONS.get(name, {}) else 0 for name in FEATURE_NAMES
}


def label_for_prediction(prediction):
    return "Normal" if int(prediction) == 1 else "Attack"


def risk_for_prediction(prediction):
    return "Low" if int(prediction) == 1 else "High"

