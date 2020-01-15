import pandas as pd
from datetime import date
import PyWhatsapp


wish_cal=pd.read_excel('contacts.xlsx')
lookups=pd.read_excel('lookups.xlsx')
def extract_message(wish_cal,lookups, event_type):
    """
    Inputs
    wish_cal: contact event calendar df
    lookups: wishes df
    type: type of wish
    """
    drop_null=wish_cal.dropna(subset=[event_type])
    dob_wish=drop_null[drop_null[event_type].map(lambda x: x.strftime('%m-%d'))==date.today().strftime('%m-%d')]
    joined_df=pd.merge(dob_wish,lookups[lookups.Event==event_type],how='left', left_on='Type', right_on='Type').fillna({'Message':lookups[(lookups.Event==event_type) & (lookups.Type=='Default')].iloc[0]['Message']})
    drop_nan=joined_df.dropna(subset=['Whatsapp_name'])[['Whatsapp_name','Message']]
    map_msg=drop_nan.to_dict('records')
    return {x['Whatsapp_name']:x['Message'] for x in map_msg}
    
msg_map=extract_message(wish_cal,lookups, 'DOB')
PyWhatsapp.execute(msg_map)