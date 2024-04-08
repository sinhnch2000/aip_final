from DM import Dialogue_Manager

intent_schema = {
        "SearchHouse": {
            "Find a house at a given location": [
                "where_to"
            ]
        },
        "BookHouse": {
            "Book the selected house for given dates and number of adults": [
                "where_to",
                "number_of_adults",
                "check_in_date",
                "check_out_date"
            ]
        }
    }
main_slot = "address"
offer_slots = ["address", "rating"]
ontology = {
        "location of the house": [
            "where_to"
        ],
        "number of people for the reservation": [
            "number_of_adults"
        ],
        "start date for the reservation or to find the house": [
            "check_in_date"
        ],
        "end date for the reservation or to find the house": [
            "check_out_date"
        ],
        "review rating of the house": [
            "rating"
        ],
        "address of the house": [
            "address"
        ],
        "phone number of the house": [
            "phone_number"
        ],
        "price per night of the house": [
            "total_price"
        ],
        "boolean flag indicating if the house has laundry service": [
            "has_laundry_service"
        ]
    }
db_slots = ["where_to", "rating", "address", "phone_number", "total_price", "has_laundry_service", "number_of_rooms_available"]
before_output_dst = ["HOTELS_2:[inform_intent(SearchHouse)]",
                     "HOTELS_2:[inform(slot0=District 1)]",
                     "HOTELS_2:[select]",
                     "HOTELS_2:[affirm_intent]",
                     "HOTELS_2:[inform(slot1=1) and inform(slot3=2nd of march) and affirm]",
                     "HOTELS_2:[affirm]",
                     "HOTELS_2:[thank_you and goodbye]"]

dm = Dialogue_Manager(intent_schema, main_slot, ontology, offer_slots, db_slots)
for i in before_output_dst:
    dm.convert_output_dst(i)
    dm.transform_action()
    print("user:  ", dm.after_output_dst)
    print("system:",dm.policy.output_system_action)
    print("\n")