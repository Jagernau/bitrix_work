from sqlalchemy import Column, Integer, String, BigInteger, DateTime, Float, MetaData, Table, Boolean
from typing import List

metadata = MetaData()


contragents = Table(
    'Contragents',
    metadata,
    Column('ca_id', Integer, primary_key=True),
    Column('ca_holding_id', Integer),
    Column('ca_name', String(255)),
    Column('ca_inn', String(255)),
    Column('ca_kpp', String(255)),
    Column('ca_bill_account_num', String(255)),
    Column('ca_bill_account_bank_name', String(255)),
    Column('ca_bill_account_ogrn', String(255)),
    Column('ca_edo_connect', Boolean),
    Column('ca_field_of_activity', String(255)),
    Column('ca_type', String(255)),

)

ca_contacts = Table(
    'ca_contacts',
    metadata,
    Column('ca_contact_id', Integer, primary_key=True, autoincrement=True),
    Column('ca_id', Integer),
    Column('ca_contact_name', String(255)),
    Column('ca_contact_surname', String(255)),
    Column('ca_contact_middlename', String(255)),
    Column('ca_contact_cell_num', String(255)),
    Column('ca_contact_work_num', String(255)),
    Column('ca_contact_email', String(255)),
    Column('ca_contact_position', String(255)),
)

ca_objects = Table(
    'ca_objects',
    metadata,
    Column('ca_object_id', Integer, primary_key=True, autoincrement=True),
    Column('ca_id', Integer),
    Column('ca_object_sm_id', Integer),
    Column('ca_object_sm_object_id', String(255)),
    Column('ca_object_name', String(255)),
    Column('ca_object_status', String(255)),
    Column('ca_object_add_date', DateTime),
    Column('ca_object_last_message', DateTime),
    Column('ca_object_margin', Integer),
)

object_sensors = Table(
    'object_sensors',
    metadata,
    Column('sensor_id', Integer, primary_key=True, autoincrement=True),
    Column('sensor_object_id', Integer),
    Column('sensor_name', String(255)),
    Column('sensor_type', String(255)),
    Column('sensor_vendor', String(255)),
    Column('sensor_vendor_model', String(255)),
    Column('sensor_serial', String(255)),
    Column('sensor_mac_address', String(255)),
    Column('sensor_technology', String(255)),
    Column('sensor_connect_type', String(255)),
)

ca_contracts = Table(
    'ca_contracts',
    metadata,
    Column('contract_id', Integer, primary_key=True, autoincrement=True),
    Column('ca_id', Integer),
    Column('contract_type', String(255)),
    Column('contract_num_prefix', String(255)),
    Column('contract_num', String(255)),
    Column('contract_payment_term', String(255)),
    Column('contract_payment_period', String(255)),
    Column('contract_start_date', DateTime),
    Column('contract_expired_date', DateTime),
)

holdings = Table(
    'holdings',
    metadata,
    Column('holding_id', Integer, primary_key=True, autoincrement=True),
    Column('holding_name', String(255)),
)

object_statuses = Table(
    'object_statuses',
    metadata,
    Column('status_id', Integer, primary_key=True, autoincrement=True),
    Column('status', String(255)),
)


sim_cards = Table(
    'sim_cards',
    metadata,
    Column('sim_id', Integer, primary_key=True, autoincrement=True),
    Column('sim_device_id', Integer),
    Column('sim_ca_id', Integer),
    Column('sim_cell_operator', String(255)),
    Column('sim_tel_number', String(255)),
    Column('sim_owner', String(255)),
    Column('sim_iccid', String(255)),
    Column('sim_ca_price', Integer),
    Column('sim_suntel_price', Integer),
)

object_custom_fields = Table(
    'object_custom_fields',
    metadata,
    Column('custom_field_id', Integer, primary_key=True, autoincrement=True),
    Column('custom_field_object_id', Integer),
    Column('custom_text', String(255)),
)

object_retranslators = Table(
    'object_retranslators',
    metadata,
    Column('retranslator_id', Integer, primary_key=True, autoincrement=True),
    Column('retranslator_name', String(255)),
    Column('retranslator_suntel_price', Integer),
    Column('retranslator_ca_price', Integer),
    Column('retr_object_id', Integer),
)

monitoring_system = Table(
    'monitoring_system',
    metadata,
    Column('mon_sys_id', Integer, primary_key=True, autoincrement=True),
    Column('pu_sm_id', Integer),
    Column('mon_sys_name', String(255)),
    Column('mon_sys_obj_price_suntel', Integer),
    Column('mon_sys_ca_obj_price_default', Integer),
)


devices = Table(
    'devices',
    metadata,
    Column('device_id', Integer, primary_key=True, autoincrement=True),
    Column('device_ca_id', Integer),
    Column('device_object_id', Integer),
    Column('device_name', String(255)),
    Column('device_vendor_name', String(255)),
    Column('device_vendor_model', String(255)),
    Column('device_vendor_id', String(255)),
    Column('device_imei', String(255)),
    Column('device_serial', String(255)),
)

object_vehicles = Table(
    'object_vehicles',
    metadata,
    Column('vehicle_id', Integer, primary_key=True, autoincrement=True),
    Column('vehicle_object_id', Integer),
    Column('vehicle_ca_id', Integer),
    Column('vehicle_vendor_name', String(255)),
    Column('vehicle_vendor_model', String(255)),
    Column('vehicle_year_of_manufacture', String(255)),
    Column('vehicle_gos_nomer', String(255)),
    Column('vehicle_gos_nomer_region', String(255)),
    Column('vehicle_type', String(255)),
    Column('vehicle_vin', String(255)),

)
