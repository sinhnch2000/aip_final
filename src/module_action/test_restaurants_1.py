from DM import Dialogue_Manager

# TEST
domain = "RESTAURANTS_1"
intent_schema = {
        "ReserveRestaurant": {
            "Reserve a table at a restaurant": [
                "restaurant_name",
                "city",
                "time"
            ]
        },
        "FindRestaurants": {
            "Find a restaurant of a particular cuisine in a city": [
                "cuisine",
                "city"
            ]
        }
    }
main_slot = "restaurant_name"
offer_slots = ["restaurant_name"]
ontology = {
        "name of the restaurant": [
            "restaurant_name"
        ],
        "date for the reservation or to find availability": [
            "date"
        ],
        "time for the reservation or to find availability": [
            "time"
        ],
        "boolean flag indicating if the restaurant serves alcohol": [
            "serves_alcohol"
        ],
        "boolean flag indicating if the restaurant has live music": [
            "has_live_music"
        ],
        "phone number of the restaurant": [
            "phone_number"
        ],
        "address of the restaurant": [
            "street_address"
        ],
        "party size for a reservation": [
            "party_size"
        ],
        "price range for the restaurant": [
            "price_range"
        ],
        "city in which the restaurant is located": [
            "city"
        ],
        "cuisine of food served in the restaurant": [
            "cuisine"
        ]
    }
db_slots = ["restaurant_name", "serves_alcohol", "has_live_music", "phone_number", "street_address", "price_range", "city", "cuisine", "number_of_tables_available"]
before_output_dst = ["RESTAURANTS_1:[inform_intent(FindRestaurants)]",
                     "RESTAURANTS_1:[inform(slot8=moderate) and inform(slot10=Brasserie)]",
                     "RESTAURANTS_1:[inform(slot9=HoChiMinh)]",
                     "RESTAURANTS_1:[request(slot6) and request(slot5)]",
                     "RESTAURANTS_1:[select]",
                     "RESTAURANTS_1:[inform(slot7=4) and affirm_intent]",
                     "RESTAURANTS_1:[inform(slot7=1) and inform(slot2=1:15 pm)]",
                     "RESTAURANTS_1:[affirm]",
                     "RESTAURANTS_1:[thank_you and goodbye]"]
path_db = r"C:\ALL\FPT\AIP\aip_final\src\module_action\db_restaurants_1\restaurants_1.db"
dm = Dialogue_Manager(intent_schema, main_slot, ontology, offer_slots, db_slots, path_db, domain)
for i in before_output_dst:
    dm.convert_output_dst(i)
    dm.transform_action()
    print("user:  ", dm.after_output_dst)
    print("system:",dm.policy.output_system_action)
    print("\n")