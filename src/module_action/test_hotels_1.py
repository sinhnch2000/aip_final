from DM import Dialogue_Manager

# TEST
domain = "HOTELS_1"
intent_schema = {
        "ReserveHotel": {
            "Reserve a selected hotel for given dates": [
                "hotel_name",
                "check_in_date",
                "number_of_days",
                "destination",
                "number_of_rooms"
            ]
        },
        "SearchHotel": {
            "Find a hotel at a given location": [
                "destination"
            ]
        }
    }
main_slot = "hotel_name"
offer_slots = ["hotel_name", "star_rating"]
ontology = {
        "location of the hotel": [
            "destination"
        ],
        "number of rooms in the reservation": [
            "number_of_rooms"
        ],
        "start date for the reservation": [
            "check_in_date"
        ],
        "number of days in the reservation": [
            "number_of_days"
        ],
        "star rating of the hotel": [
            "star_rating"
        ],
        "name of the hotel": [
            "hotel_name"
        ],
        "address of the hotel": [
            "street_address"
        ],
        "phone number of the hotel": [
            "phone_number"
        ],
        "price per night for the reservation": [
            "price_per_night"
        ],
        "boolean flag indicating if the hotel has wifi": [
            "has_wifi"
        ]
    }
db_slots = ["hotel_name", "destination", "star_rating", "street_address", "phone_number", "price_per_night", "has_wifi", "number_of_rooms_available"]

list_test_case = {
    "0": [
        "HOTELS_1:[inform_intent(SearchHotel) and inform(slot0=District 1)]",
        "{'offer': {'slot4': 4, 'slot5': 'CayXanh'}}"
    ],
    "01": [
        "HOTELS_1:[inform_intent(SearchHotel) and inform(slot0=District 1)]",
        "HOTELS_1:[inform_intent(ReserveHotel)]",
        "{'request': {'slot2': 'none', 'slot3': 'none', 'slot1': 'none'}}"
    ],
    "011": [
        "HOTELS_1:[inform_intent(SearchHotel) and inform(slot0=District 1)]",
        "HOTELS_1:[inform_intent(ReserveHotel)]",
        "HOTELS_1:[inform(slot3=two) and inform(slot2=the 3rd) and inform(slot1=1)]",
        "{'confirm': {'slot5': 'CayXanh', 'slot2': 'the 3rd', 'slot3': 2, 'slot0': 'District 1', 'slot1': 1}}"
    ],
    "0111": [
        "HOTELS_1:[inform_intent(SearchHotel) and inform(slot0=District 1)]",
        "HOTELS_1:[inform_intent(ReserveHotel)]",
        "HOTELS_1:[inform(slot3=two) and inform(slot2=the 3rd) and inform(slot1=1)]",
        "HOTELS_1:[negate]",
        "{'request': {'slot5': 'none', 'slot2': 'none', 'slot3': 'none', 'slot0': 'none', 'slot1': 'none'}}"
    ],
    "01111": [
        "HOTELS_1:[inform_intent(SearchHotel) and inform(slot0=District 1)]",
        "HOTELS_1:[inform_intent(ReserveHotel)]",
        "HOTELS_1:[inform(slot3=two) and inform(slot2=the 3rd) and inform(slot1=1)]",
        "HOTELS_1:[negate]",
        "HOTELS_1:[inform(slot3=three)]",
        "{'confirm': {'slot5': 'CayXanh', 'slot2': 'the 3rd', 'slot3': 3, 'slot0': 'District 1', 'slot1': 1}}"
    ],
    "011111": [
        "HOTELS_1:[inform_intent(SearchHotel) and inform(slot0=District 1)]",
        "HOTELS_1:[inform_intent(ReserveHotel)]",
        "HOTELS_1:[inform(slot3=two) and inform(slot2=the 3rd) and inform(slot1=1)]",
        "HOTELS_1:[negate]",
        "HOTELS_1:[inform(slot3=three)]",
        "HOTELS_1:[affirm]",
        "{'notify_success': {'none': 'none'}, 'req_more': {'none': 'none'}}"
    ],
    "0111111": [
        "HOTELS_1:[inform_intent(SearchHotel) and inform(slot0=District 1)]",
        "HOTELS_1:[inform_intent(ReserveHotel)]",
        "HOTELS_1:[inform(slot3=two) and inform(slot2=the 3rd) and inform(slot1=1)]",
        "HOTELS_1:[negate]",
        "HOTELS_1:[inform(slot3=three)]",
        "HOTELS_1:[affirm]",
        "HOTELS_1:[negate]",
        "{'goodbye': {'none': 'none'}}"
    ],
    "0111112": [
        "HOTELS_1:[inform_intent(SearchHotel) and inform(slot0=District 1)]",
        "HOTELS_1:[inform_intent(ReserveHotel)]",
        "HOTELS_1:[inform(slot3=two) and inform(slot2=the 3rd) and inform(slot1=1)]",
        "HOTELS_1:[negate]",
        "HOTELS_1:[inform(slot3=three)]",
        "HOTELS_1:[affirm]",
        "HOTELS_1:[negate and thank_you]",
        "{'goodbye': {'none': 'none'}}"
    ],
    "011112": [
        "HOTELS_1:[inform_intent(SearchHotel) and inform(slot0=District 1)]",
        "HOTELS_1:[inform_intent(ReserveHotel)]",
        "HOTELS_1:[inform(slot3=two) and inform(slot2=the 3rd) and inform(slot1=1)]",
        "HOTELS_1:[negate]",
        "HOTELS_1:[inform(slot3=three)]",
        "HOTELS_1:[negate]",
        "{'request': {'slot5': 'none', 'slot2': 'none', 'slot3': 'none', 'slot0': 'none', 'slot1': 'none'}}"
    ],
    "0111121": [
        "HOTELS_1:[inform_intent(SearchHotel) and inform(slot0=District 1)]",
        "HOTELS_1:[inform_intent(ReserveHotel)]",
        "HOTELS_1:[inform(slot3=two) and inform(slot2=the 3rd) and inform(slot1=1)]",
        "HOTELS_1:[negate]",
        "HOTELS_1:[inform(slot3=three)]",
        "HOTELS_1:[negate]",
        "HOTELS_1:[inform(slot1=2)]",
        "{'confirm': {'slot5': 'CayXanh', 'slot2': 'the 3rd', 'slot3': 3, 'slot0': 'District 1', 'slot1': 2}}"
    ],
    "01111211": [
        "HOTELS_1:[inform_intent(SearchHotel) and inform(slot0=District 1)]",
        "HOTELS_1:[inform_intent(ReserveHotel)]",
        "HOTELS_1:[inform(slot3=two) and inform(slot2=the 3rd) and inform(slot1=1)]",
        "HOTELS_1:[negate]",
        "HOTELS_1:[inform(slot3=three)]",
        "HOTELS_1:[negate]",
        "HOTELS_1:[inform(slot1=2)]",
        "HOTELS_1:[affirm]",
        "{'notify_success': {'none': 'none'}, 'req_more': {'none': 'none'}}"
    ],"011112111": [
        "HOTELS_1:[inform_intent(SearchHotel) and inform(slot0=District 1)]",
        "HOTELS_1:[inform_intent(ReserveHotel)]",
        "HOTELS_1:[inform(slot3=two) and inform(slot2=the 3rd) and inform(slot1=1)]",
        "HOTELS_1:[negate]",
        "HOTELS_1:[inform(slot3=three)]",
        "HOTELS_1:[negate]",
        "HOTELS_1:[inform(slot1=2)]",
        "HOTELS_1:[affirm]",
        "HOTELS_1:[negate and thank_you]",
        "{'goodbye': {'none': 'none'}}"
    ],"011112112": [
        "HOTELS_1:[inform_intent(SearchHotel) and inform(slot0=District 1)]",
        "HOTELS_1:[inform_intent(ReserveHotel)]",
        "HOTELS_1:[inform(slot3=two) and inform(slot2=the 3rd) and inform(slot1=1)]",
        "HOTELS_1:[negate]",
        "HOTELS_1:[inform(slot3=three)]",
        "HOTELS_1:[negate]",
        "HOTELS_1:[inform(slot1=2)]",
        "HOTELS_1:[affirm]",
        "HOTELS_1:[negate]",
        "{'goodbye': {'none': 'none'}}"
    ],
    "0112": [
        "HOTELS_1:[inform_intent(SearchHotel) and inform(slot0=District 1)]",
        "HOTELS_1:[inform_intent(ReserveHotel)]",
        "HOTELS_1:[inform(slot3=two) and inform(slot2=the 3rd) and inform(slot1=1)]",
        "HOTELS_1:[affirm]",
        "{'notify_success': {'none': 'none'}, 'req_more': {'none': 'none'}}"
    ],
    "012": [
        "HOTELS_1:[inform_intent(SearchHotel) and inform(slot0=District 1)]",
        "HOTELS_1:[inform_intent(ReserveHotel)]",
        "HOTELS_1:[inform(slot2=the 3rd)]",
        "{'request': {'slot3': 'none', 'slot1': 'none'}}"
    ],
    "0121": [
        "HOTELS_1:[inform_intent(SearchHotel) and inform(slot0=District 1)]",
        "HOTELS_1:[inform_intent(ReserveHotel)]",
        "HOTELS_1:[inform(slot2=the 3rd)]",
        "HOTELS_1:[inform(slot3=two) and inform(slot1=1)]",
        "{'confirm': {'slot5': 'CayXanh', 'slot2': 'the 3rd', 'slot3': 2, 'slot0': 'District 1', 'slot1': 1}}"
    ],
    "0122": [
        "HOTELS_1:[inform_intent(SearchHotel) and inform(slot0=District 1)]",
        "HOTELS_1:[inform_intent(ReserveHotel)]",
        "HOTELS_1:[inform(slot2=the 3rd)]",
        "HOTELS_1:[inform(slot1=1)]",
        "{'request': {'slot3': 'none'}}"
    ],
    "0123": [
        "HOTELS_1:[inform_intent(SearchHotel) and inform(slot0=District 1)]",
        "HOTELS_1:[inform_intent(ReserveHotel)]",
        "HOTELS_1:[inform(slot2=the 3rd)]",
        "HOTELS_1:[request(slot9)]",
        "{'inform': {'slot9': 'True'}}"
    ],
    "0124": [
        "HOTELS_1:[inform_intent(SearchHotel) and inform(slot0=District 1)]",
        "HOTELS_1:[inform_intent(ReserveHotel)]",
        "HOTELS_1:[inform(slot2=the 3rd)]",
        "HOTELS_1:[chitchat]",
        "{'asking': {'none': 'none'}}"
    ],
    "0125": [
        "HOTELS_1:[inform_intent(SearchHotel) and inform(slot0=District 1)]",
        "HOTELS_1:[inform_intent(ReserveHotel)]",
        "HOTELS_1:[inform(slot2=the 3rd)]",
        "HOTELS_1:[inform(slot5=CayVang)]",
        "{'offer_intent': {'intent': 'ReserveHotel'}}"
    ],
    "01251": [
        "HOTELS_1:[inform_intent(SearchHotel) and inform(slot0=District 1)]",
        "HOTELS_1:[inform_intent(ReserveHotel)]",
        "HOTELS_1:[inform(slot2=the 3rd)]",
        "HOTELS_1:[inform(slot5=CayVang)]",
        "HOTELS_1:[affirm_intent]",
        "{'request': {'slot3': 'none', 'slot1': 'none'}}"
    ],
    "012511": [
        "HOTELS_1:[inform_intent(SearchHotel) and inform(slot0=District 1)]",
        "HOTELS_1:[inform_intent(ReserveHotel)]",
        "HOTELS_1:[inform(slot2=the 3rd)]",
        "HOTELS_1:[inform(slot5=CayVang)]",
        "HOTELS_1:[affirm_intent]",
        "HOTELS_1:[inform(slot3=two) and inform(slot1=1)]",
        "{'confirm': {'slot5': 'CayVang', 'slot2': 'the 3rd', 'slot3': 2, 'slot0': 'District 3', 'slot1': 1}}"
    ],
    "0125111": [
        "HOTELS_1:[inform_intent(SearchHotel) and inform(slot0=District 1)]",
        "HOTELS_1:[inform_intent(ReserveHotel)]",
        "HOTELS_1:[inform(slot2=the 3rd)]",
        "HOTELS_1:[inform(slot5=CayVang)]",
        "HOTELS_1:[affirm_intent]",
        "HOTELS_1:[inform(slot3=two) and inform(slot1=1)]",
        "HOTELS_1:[affirm]",
        "{'notify_success': {'none': 'none'}, 'req_more': {'none': 'none'}}"
    ],
    "01251111": [
        "HOTELS_1:[inform_intent(SearchHotel) and inform(slot0=District 1)]",
        "HOTELS_1:[inform_intent(ReserveHotel)]",
        "HOTELS_1:[inform(slot2=the 3rd)]",
        "HOTELS_1:[inform(slot5=CayVang)]",
        "HOTELS_1:[affirm_intent]",
        "HOTELS_1:[inform(slot3=two) and inform(slot1=1)]",
        "HOTELS_1:[affirm]",
        "HOTELS_1:[negate]",
        "{'goodbye': {'none': 'none'}}"
    ],
    "0125112": [
        "HOTELS_1:[inform_intent(SearchHotel) and inform(slot0=District 1)]",
        "HOTELS_1:[inform_intent(ReserveHotel)]",
        "HOTELS_1:[inform(slot2=the 3rd)]",
        "HOTELS_1:[inform(slot5=CayVang)]",
        "HOTELS_1:[affirm_intent]",
        "HOTELS_1:[inform(slot3=two) and inform(slot1=1)]",
        "HOTELS_1:[affirm]",
        "HOTELS_1:[inform(slot0=District 1)]",
        "{'offer_intent': {'intent': 'SearchHotel'}}"
    ],
    "01251121": [
        "HOTELS_1:[inform_intent(SearchHotel) and inform(slot0=District 1)]",
        "HOTELS_1:[inform_intent(ReserveHotel)]",
        "HOTELS_1:[inform(slot2=the 3rd)]",
        "HOTELS_1:[inform(slot5=CayVang)]",
        "HOTELS_1:[affirm_intent]",
        "HOTELS_1:[inform(slot3=two) and inform(slot1=1)]",
        "HOTELS_1:[affirm]",
        "HOTELS_1:[inform(slot0=District 1)]",
        "HOTELS_1:[affirm_intent]",
        "HOTELS_1:[inform_intent(ReserveHotel)]",
        "{'request': {'slot2': 'none', 'slot3': 'none', 'slot1': 'none'}}"
    ],
    "0125113": [
        "HOTELS_1:[inform_intent(SearchHotel) and inform(slot0=District 1)]",
        "HOTELS_1:[inform_intent(ReserveHotel)]",
        "HOTELS_1:[inform(slot2=the 3rd)]",
        "HOTELS_1:[inform(slot5=CayVang)]",
        "HOTELS_1:[affirm_intent]",
        "HOTELS_1:[inform(slot3=two) and inform(slot1=1)]",
        "HOTELS_1:[affirm]",
        "HOTELS_1:[goodbye]",
        "{'goodbye': {'none': 'none'}}"
    ],
    "013": [
        "HOTELS_1:[inform_intent(SearchHotel) and inform(slot0=District 1)]",
        "HOTELS_1:[inform_intent(ReserveHotel)]",
        "HOTELS_1:[chitchat]",
        "{'asking': {'none': 'none'}}"
    ],
    "014": [
        "HOTELS_1:[inform_intent(SearchHotel) and inform(slot0=District 1)]",
        "HOTELS_1:[inform_intent(ReserveHotel)]",
        "HOTELS_1:[request(slot9)]",
        "HOTELS_1:[inform(slot3=two)]",
        "{'request': {'slot2': 'none', 'slot1': 'none'}}"
    ],
    "015": [
        "HOTELS_1:[inform_intent(SearchHotel) and inform(slot0=District 1)]",
        "HOTELS_1:[inform_intent(ReserveHotel)]",
        "HOTELS_1:[inform(slot3=two) and inform(slot2=the 3rd) and inform(slot1=1)]",
        "{'confirm': {'slot5': 'CayXanh', 'slot2': 'the 3rd', 'slot3': 2, 'slot0': 'District 1', 'slot1': 1}}"
    ],
    "02": [
        "HOTELS_1:[inform_intent(SearchHotel) and inform(slot0=District 1)]",
        "HOTELS_1:[select]",
        "{'offer_intent': {'intent': 'ReserveHotel'}}"
    ],
    "03": [
        "HOTELS_1:[inform_intent(SearchHotel) and inform(slot0=District 1)]",
        "HOTELS_1:[request_alts]",
        "{'offer': {'slot4': 5, 'slot5': 'CayHong'}}"
    ],
    "031": [
        "HOTELS_1:[inform_intent(SearchHotel) and inform(slot0=District 1)]",
        "HOTELS_1:[request_alts]",
        "HOTELS_1:[inform(slot5=CayTrang)]",
        "{'offer': {'slot4': 5, 'slot5': 'CayHong'}}"
    ],
    "04": [
        "HOTELS_1:[inform_intent(SearchHotel) and inform(slot0=District 1)]",
        "HOTELS_1:[request(slot9)]",
        "{'inform': {'slot9': 'True'}}"
    ],
    "05": [
        "HOTELS_1:[inform_intent(SearchHotel) and inform(slot0=District 1)]",
        "HOTELS_1:[inform(slot0=District 3)]",
        "{'offer': {'slot4': 3, 'slot5': 'CayVang'}}"
    ],
    "06": [
        "HOTELS_1:[inform_intent(SearchHotel) and inform(slot0=District 1)]",
        "HOTELS_1:[inform(slot4=5)]",
        "{'offer': {'slot4': 5, 'slot5': 'CayHong'}}"
    ],
    "07": [
        "HOTELS_1:[inform_intent(SearchHotel) and inform(slot0=District 1)]",
        "HOTELS_1:[inform(slot5=CayVang)]",
        "{'offer_intent': {'intent': 'ReserveHotel'}}"
    ],
    "08": [
        "HOTELS_1:[inform_intent(SearchHotel) and inform(slot0=District 1)]",
        "HOTELS_1:[inform(slot5=CayVang) and inform_intent(ReserveHotel)]",
        "{'request': {'slot2': 'none', 'slot3': 'none', 'slot1': 'none'}}"
    ],
    "09": [
        "HOTELS_1:[inform_intent(SearchHotel) and inform(slot0=District 1)]",
        "HOTELS_1:[inform(slot5=CayTrang)]",
        "{'offer': {'slot4': 4, 'slot5': 'CayXanh'}}"
    ],
    "091": [
        "HOTELS_1:[inform_intent(SearchHotel) and inform(slot0=District 1)]",
        "HOTELS_1:[inform(slot5=CayTrang)]",
        "HOTELS_1:[select]",
        "{'offer_intent': {'intent': 'ReserveHotel'}}"
    ],
    "092": [
        "HOTELS_1:[inform_intent(SearchHotel) and inform(slot0=District 1)]",
        "HOTELS_1:[inform(slot5=CayTrang)]",
        "HOTELS_1:[request_alts]",
        "{'offer': {'slot4': 5, 'slot5': 'CayHong'}}"
    ],
    "0921": [
        "HOTELS_1:[inform_intent(SearchHotel) and inform(slot0=District 1)]",
        "HOTELS_1:[inform(slot5=CayTrang)]",
        "HOTELS_1:[request_alts]",
        "HOTELS_1:[select]",
        "{'offer_intent': {'intent': 'ReserveHotel'}}"
    ],
    "0A": [
        "HOTELS_1:[inform_intent(SearchHotel) and inform(slot0=District 1)]",
        "HOTELS_1:[inform(slot5=CayHong)]",
        "{'offer_intent': {'intent': 'ReserveHotel'}}"
    ],
    "1": [
        "HOTELS_1:[inform_intent(ReserveHotel) and inform(slot0=District 1)]",
        "{'offer': {'slot4': 4, 'slot5': 'CayXanh'}}"
    ],
    "11": [
        "HOTELS_1:[inform_intent(ReserveHotel) and inform(slot0=District 1)]",
        "HOTELS_1:[inform(slot0=District 3)]",
        "{'offer': {'slot4': 3, 'slot5': 'CayVang'}}"
    ],
    "111": [
        "HOTELS_1:[inform_intent(ReserveHotel) and inform(slot0=District 1)]",
        "HOTELS_1:[inform(slot0=District 3)]",
        "HOTELS_1:[select]",
        "{'request': {'slot2': 'none', 'slot3': 'none', 'slot1': 'none'}}"
    ],
    "1111": [
        "HOTELS_1:[inform_intent(ReserveHotel) and inform(slot0=District 1)]",
        "HOTELS_1:[inform(slot0=District 3)]",
        "HOTELS_1:[select]",
        "HOTELS_1:[inform(slot3=two) and inform(slot2=the 3rd) and inform(slot1=1)]",
        "{'confirm': {'slot5': 'CayVang', 'slot2': 'the 3rd', 'slot3': 2, 'slot0': 'District 3', 'slot1': 1}}"
    ],
    "11111": [
        "HOTELS_1:[inform_intent(ReserveHotel) and inform(slot0=District 1)]",
        "HOTELS_1:[inform(slot0=District 3)]",
        "HOTELS_1:[select]",
        "HOTELS_1:[inform(slot3=two) and inform(slot2=the 3rd) and inform(slot1=1)]",
        "HOTELS_1:[negate]",
        "{'request': {'slot5': 'none', 'slot2': 'none', 'slot3': 'none', 'slot0': 'none', 'slot1': 'none'}}"
    ],
    "11112": [
        "HOTELS_1:[inform_intent(ReserveHotel) and inform(slot0=District 1)]",
        "HOTELS_1:[inform(slot0=District 3)]",
        "HOTELS_1:[select]",
        "HOTELS_1:[inform(slot3=two) and inform(slot2=the 3rd) and inform(slot1=1)]",
        "HOTELS_1:[affirm]",
        "{'notify_success': {'none': 'none'}, 'req_more': {'none': 'none'}}"
    ],
    "2": [
        "HOTELS_1:[inform_intent(SearchHotel) and inform(slot0=District 1) and inform(slot4=4)]",
        "{'offer': {'slot4': 4, 'slot5': 'CayXanh'}}"
    ],
    "21": [
        "HOTELS_1:[inform_intent(SearchHotel) and inform(slot0=District 1) and inform(slot4=4)]",
        "HOTELS_1:[select]",
        "{'offer_intent': {'intent': 'ReserveHotel'}}"
    ],
    "211": [
        "HOTELS_1:[inform_intent(SearchHotel) and inform(slot0=District 1) and inform(slot4=4)]",
        "HOTELS_1:[select]",
        "HOTELS_1:[affirm_intent]",
        "{'request': {'slot2': 'none', 'slot3': 'none', 'slot1': 'none'}}"
    ],
    "2111": [
        "HOTELS_1:[inform_intent(SearchHotel) and inform(slot0=District 1) and inform(slot4=4)]",
        "HOTELS_1:[select]",
        "HOTELS_1:[affirm_intent]",
        "HOTELS_1:[inform(slot3=two) and inform(slot2=the 3rd) and inform(slot1=1)]",
        "{'confirm': {'slot5': 'CayXanh', 'slot2': 'the 3rd', 'slot3': 2, 'slot0': 'District 1', 'slot1': 1}}"
    ],
    "21111": [
        "HOTELS_1:[inform_intent(SearchHotel) and inform(slot0=District 1) and inform(slot4=4)]",
        "HOTELS_1:[select]",
        "HOTELS_1:[affirm_intent]",
        "HOTELS_1:[inform(slot3=two) and inform(slot2=the 3rd) and inform(slot1=1)]",
        "HOTELS_1:[negate]",
        "{'request': {'slot5': 'none', 'slot2': 'none', 'slot3': 'none', 'slot0': 'none', 'slot1': 'none'}}"
    ],
    "21112": [
        "HOTELS_1:[inform_intent(SearchHotel) and inform(slot0=District 1) and inform(slot4=4)]",
        "HOTELS_1:[select]",
        "HOTELS_1:[affirm_intent]",
        "HOTELS_1:[inform(slot3=two) and inform(slot2=the 3rd) and inform(slot1=1)]",
        "HOTELS_1:[affirm]",
        "{'notify_success': {'none': 'none'}, 'req_more': {'none': 'none'}}"
    ],
    "3": [
        "HOTELS_1:[inform_intent(ReserveHotel) and inform(slot0=District 1) and inform(slot4=4)]",
        "{'offer': {'slot4': 4, 'slot5': 'CayXanh'}}"
    ],
    "31": [
        "HOTELS_1:[inform_intent(ReserveHotel) and inform(slot0=District 1) and inform(slot4=4)]",
        "HOTELS_1:[select]",
        "{'request': {'slot2': 'none', 'slot3': 'none', 'slot1': 'none'}}"
    ],
    "311": [
        "HOTELS_1:[inform_intent(ReserveHotel) and inform(slot0=District 1) and inform(slot4=4)]",
        "HOTELS_1:[select]",
        "HOTELS_1:[inform(slot3=two) and inform(slot2=the 3rd) and inform(slot1=1)]",
        "{'confirm': {'slot5': 'CayXanh', 'slot2': 'the 3rd', 'slot3': 2, 'slot0': 'District 1', 'slot1': 1}}"
    ],
    "3111": [
        "HOTELS_1:[inform_intent(ReserveHotel) and inform(slot0=District 1) and inform(slot4=4)]",
        "HOTELS_1:[select]",
        "HOTELS_1:[inform(slot3=two) and inform(slot2=the 3rd) and inform(slot1=1)]",
        "HOTELS_1:[negate]",
        "{'request': {'slot5': 'none', 'slot2': 'none', 'slot3': 'none', 'slot0': 'none', 'slot1': 'none'}}"
    ],
    "3112": [
        "HOTELS_1:[inform_intent(ReserveHotel) and inform(slot0=District 1) and inform(slot4=4)]",
        "HOTELS_1:[select]",
        "HOTELS_1:[inform(slot3=two) and inform(slot2=the 3rd) and inform(slot1=1)]",
        "HOTELS_1:[affirm]",
        "{'notify_success': {'none': 'none'}, 'req_more': {'none': 'none'}}"
    ],
    "4": [
        "HOTELS_1:[inform_intent(ReserveHotel) and inform(slot5=CayXanh)]",
        "{'request': {'slot2': 'none', 'slot3': 'none', 'slot1': 'none'}}"
    ],
    "5": [
        "HOTELS_1:[inform(slot4=4)]",
        "{'offer_intent': {'intent': 'SearchHotel'}}"
    ],
    "6": [
        "HOTELS_1:[inform(slot0=District 1)]",
        "{'offer_intent': {'intent': 'SearchHotel'}}"
    ],
    "7": [
        "HOTELS_1:[inform(slot0=District 1) and inform(slot5=CayXanh)]",
        "{'offer_intent': {'intent': 'ReserveHotel'}}"
    ],
    "8": [
        "HOTELS_1:[inform(slot0=District 1) and inform(slot5=CayXanh) and inform_intent(ReserveHotel)]",
        "{'request': {'slot2': 'none', 'slot3': 'none', 'slot1': 'none'}}"
    ],
    "9": [
        "HOTELS_1:[inform(slot0=District 1) and inform(slot5=CayVang)]",
        "{'inform': {'slot5': 'CayVang', 'slot0': 'District 3'}, 'offer_intent': {'intent': 'ReserveHotel'}}"
    ],
    "A": [
        "HOTELS_1:[inform(slot0=District 1) and inform(slot5=CayVang) and inform_intent(ReserveHotel)]",
        "{'inform': {'slot5': 'CayVang', 'slot0': 'District 3'}, 'request': {'slot2': 'none', 'slot3': 'none', 'slot1': 'none'}}"
    ],
    "B": [
        "HOTELS_1:[inform(slot0=District 1) and inform(slot4=4)]",
        "{'offer_intent': {'intent': 'SearchHotel'}}"
    ],
    "C": [
        "HOTELS_1:[inform(slot5=CayXanh)]",
        "{'offer_intent': {'intent': 'ReserveHotel'}}"
    ],
    "D": [
        "HOTELS_1:[request(slot9)]",
        "{'offer_intent': {'intent': 'SearchHotel'}}"
    ],
    "E": [
        "chitchat",
        "{'asking': {'none': 'none'}}"
    ],
    "E1": [
        "chitchat",
        "HOTELS_1:[inform(slot0=District 1) and inform(slot4=4)]",
        "{'offer_intent': {'intent': 'SearchHotel'}}"
    ],
    "E11": [
        "chitchat",
        "HOTELS_1:[inform(slot0=District 1) and inform(slot4=4)]",
        "HOTELS_1:[inform(slot5=CayTrang)]",
        "{'request': {'slot5': 'none'}}"
    ],
    "E111": [
        "chitchat",
        "HOTELS_1:[inform(slot0=District 1) and inform(slot4=4)]",
        "HOTELS_1:[inform(slot5=CayTrang)]",
        "HOTELS_1:[affirm_intent]",
        "{'offer': {'slot4': 4, 'slot5': 'CayXanh'}}"
    ],
    "E112": [
        "chitchat",
        "HOTELS_1:[inform(slot0=District 1) and inform(slot4=4)]",
        "HOTELS_1:[inform(slot5=CayTrang)]",
        "HOTELS_1:[inform(slot5=CayXanh)]",
        "{'offer_intent': {'intent': 'ReserveHotel'}}"
    ],
    "FINAL": [
        "HOTELS_1:[inform_intent(SearchHotel)]",
        "HOTELS_1:[inform(slot5=CayTrang)]",
        "HOTELS_1:[inform(slot5=CayXanh)]",
        "HOTELS_1:[affirm_intent]",
        "HOTELS_1:[inform(slot3=two) and inform(slot2=the 3rd) and inform(slot1=1)]",
        "HOTELS_1:[negate]",
        "HOTELS_1:[inform(slot3=two)]",
        "HOTELS_1:[affirm]",
        "HOTELS_1:[inform(slot4=5)]",
        "HOTELS_1:[inform_intent(SearchHotel)]",
        "HOTELS_1:[inform(slot0=District 1)]",
        "HOTELS_1:[request_alts]",
        "HOTELS_1:[select]",
        "HOTELS_1:[negate_intent]",
        ""
    ]
}

path_db = r"C:\ALL\FPT\AIP\aip_final\src\module_action\db_hotels_1\hotels_1.db"
for title, case in list_test_case.items():
    dm = Dialogue_Manager(intent_schema, main_slot, ontology, offer_slots, db_slots, path_db, domain)
    for index, turn in enumerate(case[:-1]):
        dm.convert_output_dst(turn, "")
        dm.transform_action()
        if index == len(case[:-2]):
            if str(dm.policy.output_system_action) != case[-1]:
                print("CASE:", title)
                dm = Dialogue_Manager(intent_schema, main_slot, ontology, offer_slots, db_slots, path_db, domain)
                for turn in case[:-1]:
                    dm.convert_output_dst(turn, "")
                    dm.transform_action()
                    print("user:  ", dm.after_output_dst)
                    print("system:",dm.policy.output_system_action)
                print("LABEL: ", case[-1])
                print("--------------------------------------------------------------------------------------------------------------------------------------------------------------")
                break