CONN_URL = 'eastus2.api.cognitive.microsoft.com'
SCHEMA = "https://schema.cognitiveservices.azure.com/formrecognizer/2021-03-01/labels.json"

APPLICATION_TYPE = {
    'PDF': 'application/pdf',
    'TIFF': 'image/tiff',
    'PNG': 'image/png'
}

TMP_LABEL_LIST = [
    {
        "label": "Patient Name",
        "key": None,
        "value": [
            {
                "page": 1,
                "text": "Ted",
                "boundingBoxes": [
                    [
                        0.15509411764705883,
                        0.3451272727272727,
                        0.18398823529411765,
                        0.3451272727272727,
                        0.18398823529411765,
                        0.3558909090909091,
                        0.15509411764705883,
                        0.3558909090909091
                    ]
                ]
            },
            {
                "page": 1,
                "text": "Jones",
                "boundingBoxes": [
                    [
                        0.1907764705882353,
                        0.34517272727272724,
                        0.2401294117647059,
                        0.34517272727272724,
                        0.2401294117647059,
                        0.3559,
                        0.1907764705882353,
                        0.3559
                    ]
                ]
            }
        ]
    },
    {
        "label": "Patient DOB",
        "key": None,
        "value": [
            {
                "page": 1,
                "text": "01/01/1900",
                "boundingBoxes": [
                    [
                        0.6127764705882353,
                        0.4704636363636363,
                        0.7058470588235294,
                        0.4704636363636363,
                        0.7058470588235294,
                        0.48119090909090906,
                        0.6127764705882353,
                        0.48119090909090906
                    ]
                ]
            }
        ]
    },
    {
        "label": "Requestor Org.",
        "key": None,
        "value": [
            {
                "page": 1,
                "text": "ENABLE",
                "boundingBoxes": [
                    [
                        0.6022470588235295,
                        0.36935454545454544,
                        0.6657294117647058,
                        0.3697909090909091,
                        0.665164705882353,
                        0.38064545454545456,
                        0.6022470588235295,
                        0.38107272727272723
                    ]
                ]
            },
            {
                "page": 1,
                "text": "COMP",
                "boundingBoxes": [
                    [
                        0.6696588235294118,
                        0.3697909090909091,
                        0.7168588235294118,
                        0.36935454545454544,
                        0.7162941176470587,
                        0.38064545454545456,
                        0.6696588235294118,
                        0.38064545454545456
                    ]
                ]
            }
        ]
    },
    {
        "label": "Requester Address",
        "key": None,
        "value": [
            {
                "page": 1,
                "text": "206",
                "boundingBoxes": [
                    [
                        0.6028117647058824,
                        0.39496363636363635,
                        0.6264,
                        0.3945272727272728,
                        0.6264,
                        0.40581818181818186,
                        0.6033764705882353,
                        0.40581818181818186
                    ]
                ]
            },
            {
                "page": 1,
                "text": "Gothic",
                "boundingBoxes": [
                    [
                        0.6292117647058824,
                        0.3945272727272728,
                        0.6758470588235294,
                        0.39496363636363635,
                        0.6758470588235294,
                        0.4062545454545454,
                        0.6297764705882354,
                        0.40581818181818186
                    ]
                ]
            },
            {
                "page": 1,
                "text": "Court",
                "boundingBoxes": [
                    [
                        0.6786470588235295,
                        0.39496363636363635,
                        0.7196588235294117,
                        0.39540000000000003,
                        0.7191058823529412,
                        0.40581818181818186,
                        0.6786470588235295,
                        0.4062545454545454
                    ]
                ]
            },
            {
                "page": 1,
                "text": "Suite",
                "boundingBoxes": [
                    [
                        0.6292117647058824,
                        0.4188363636363636,
                        0.6629176470588236,
                        0.4192727272727273,
                        0.6629176470588236,
                        0.43011818181818184,
                        0.6292117647058824,
                        0.43055454545454547
                    ]
                ]
            },
            {
                "page": 1,
                "text": "308",
                "boundingBoxes": [
                    [
                        0.6657294117647058,
                        0.4192727272727273,
                        0.6910117647058823,
                        0.4188363636363636,
                        0.6915764705882353,
                        0.4296909090909091,
                        0.6662941176470588,
                        0.43011818181818184
                    ]
                ]
            },
            {
                "page": 1,
                "text": "Franklin,",
                "boundingBoxes": [
                    [
                        0.5955058823529411,
                        0.4440090909090909,
                        0.6550588235294117,
                        0.4440090909090909,
                        0.6544941176470589,
                        0.4557272727272727,
                        0.5949411764705883,
                        0.4561636363636364
                    ]
                ]
            },
            {
                "page": 1,
                "text": "TN",
                "boundingBoxes": [
                    [
                        0.6578705882352941,
                        0.4440090909090909,
                        0.6769647058823529,
                        0.44357272727272723,
                        0.6764,
                        0.4557272727272727,
                        0.6578705882352941,
                        0.4557272727272727
                    ]
                ]
            },
            {
                "page": 1,
                "text": "37067",
                "boundingBoxes": [
                    [
                        0.6842705882352941,
                        0.44357272727272723,
                        0.7264,
                        0.44357272727272723,
                        0.7264,
                        0.45529090909090913,
                        0.6842705882352941,
                        0.4557272727272727
                    ]
                ]
            }
        ]
    },
    {
        "label": "Request Date",
        "key": None,
        "value": [
            {
                "page": 1,
                "text": "8/17/2020",
                "boundingBoxes": [
                    [
                        0.8264,
                        0.8441818181818181,
                        0.8904470588235295,
                        0.8446181818181819,
                        0.8910117647058824,
                        0.8550363636363637,
                        0.8264,
                        0.8554727272727273
                    ]
                ]
            }
        ]
    }
]
