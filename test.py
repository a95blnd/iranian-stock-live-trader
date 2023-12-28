from network.api.instrument_data import update_contract_info
from services.instrument_data import extract_instrument_ids



list_ids = extract_instrument_ids()
for index, id in enumerate(list_ids):
    update_contract_info(id)
    print(index, id)
