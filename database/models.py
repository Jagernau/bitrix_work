from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Contragents(Base):
    __tablename__ = 'Contragents'
    ca_id = Column(Integer, primary_key=True)
    ca_holding_id = Column(Integer, ForeignKey('holdings.holding_id'))
    ca_name = Column(String(255))
    ca_inn = Column(String(255))
    ca_kpp = Column(String(255))
    ca_bill_account_num = Column(String(255))
    ca_bill_account_bank_name = Column(String(255))
    ca_bill_account_ogrn = Column(String(255))
    ca_edo_connect = Column(Boolean)
    ca_field_of_activity = Column(String(255))
    ca_type = Column(String(255))

    # ca_contacts = relationship('ca_contacts', back_populates='contragent')
    # ca_objects = relationship('ca_objects', back_populates='contragent')
    # ca_contracts = relationship('ca_contracts', back_populates='contragent')
    # sim_cards = relationship('sim_cards', back_populates='contragent')
    # object_vehicles = relationship('object_vehicles', back_populates='contragent')
    # holding = relationship('holdings', back_populates='contragent')

class ca_contacts(Base):
    __tablename__ = 'ca_contacts'
    ca_contact_id = Column(Integer, primary_key=True, autoincrement=True)
    ca_id = Column(Integer, ForeignKey('Contragents.ca_id'))
    ca_contact_name = Column(String(255))
    ca_contact_surname = Column(String(255))
    ca_contact_middlename = Column(String(255))
    ca_contact_cell_num = Column(String(255))
    ca_contact_work_num = Column(String(255))
    ca_contact_email = Column(String(255))
    ca_contact_position = Column(String(255))

    # contragent = relationship('Contragents', back_populates='ca_contacts')
    #
class ca_objects(Base):
    __tablename__ = 'ca_objects'
    ca_object_id = Column(Integer, primary_key=True, autoincrement=True)
    ca_id = Column(Integer, ForeignKey('Contragents.ca_id'))
    owner = Column(String(255))
    imei = Column(String(255))
    ca_object_sm_id = Column(Integer, ForeignKey('monitoring_system.mon_sys_id'))
    ca_object_sm_object_id = Column(String(255))
    ca_object_name = Column(String(255))
    ca_object_status = Column(String(255), ForeignKey('object_statuses.status_id'))
    created_date = Column(DateTime)
    ca_object_add_date = Column(DateTime)
    ca_object_last_message = Column(DateTime)
    ca_object_margin = Column(Integer)
    updated = Column(DateTime)
    linked_login = Column(String(255))
    linked_client = Column(String(255))

    # contragent = relationship('Contragents', back_populates='ca_objects')
    # object_sensors = relationship('object_sensors', back_populates='ca_object')
    # object_custom_fields = relationship('object_custom_fields', back_populates='ca_object')
    # object_retranslators = relationship('object_retranslators', back_populates='ca_object')
    # object_status = relationship('object_statuses', back_populates='ca_object')

class object_sensors(Base):
    __tablename__ = 'object_sensors'
    sensor_id = Column(Integer, primary_key=True, autoincrement=True)
    sensor_object_id = Column(Integer, ForeignKey('ca_objects.ca_object_id'))
    sensor_name = Column(String(255))
    sensor_type = Column(String(255))
    sensor_vendor = Column(String(255))
    sensor_vendor_model = Column(String(255))
    sensor_serial = Column(String(255))
    sensor_mac_address = Column(String(255))
    sensor_technology = Column(String(255))
    sensor_connect_type = Column(String(255))

    # ca_object = relationship('ca_objects', back_populates='object_sensors')
    #
class ca_contracts(Base):
    __tablename__ = 'ca_contracts'
    contract_id = Column(Integer, primary_key=True, autoincrement=True)
    ca_id = Column(Integer, ForeignKey('Contragents.ca_id'))
    contract_type = Column(String(255))
    contract_num_prefix = Column(String(255))
    contract_num = Column(String(255))
    contract_payment_term = Column(String(255))
    contract_payment_period = Column(String(255))
    contract_start_date = Column(DateTime)
    contract_expired_date = Column(DateTime)

    # contragent = relationship('Contragents', back_populates='ca_contracts')
    #
class holdings(Base):
    __tablename__ = 'holdings'
    holding_id = Column(Integer, primary_key=True, autoincrement=True)
    holding_name = Column(String(255))

    # contragent = relationship('Contragents', back_populates='holding')
    #
class object_statuses(Base):
    __tablename__ = 'object_statuses'
    status_id = Column(Integer, primary_key=True, autoincrement=True)
    status = Column(String(255))

    # ca_object = relationship('ca_objects', back_populates='ca_object_status')
    #
class sim_cards(Base):
    __tablename__ = 'sim_cards'
    sim_id = Column(Integer, primary_key=True, autoincrement=True)
    sim_device_id = Column(Integer, ForeignKey('devices.device_id'))
    sim_ca_id = Column(Integer, ForeignKey('Contragents.ca_id'))
    sim_cell_operator = Column(String(255))
    sim_tel_number = Column(String(255))
    sim_owner = Column(String(255))
    sim_iccid = Column(String(255))
    sim_ca_price = Column(Integer)
    sim_suntel_price = Column(Integer)

    # contragent = relationship('Contragents', back_populates='sim_cards')
    #
class object_custom_fields(Base):
    __tablename__ = 'object_custom_fields'
    custom_field_id = Column(Integer, primary_key=True, autoincrement=True)
    custom_field_object_id = Column(Integer, ForeignKey('ca_objects.ca_object_id'))
    custom_text = Column(String(255))

    # ca_object = relationship('ca_objects', back_populates='object_custom_fields')
    #
class object_retranslators(Base):
    __tablename__ = 'object_retranslators'
    retranslator_id = Column(Integer, primary_key=True, autoincrement=True)
    retranslator_name = Column(String(255))
    retranslator_suntel_price = Column(Integer)
    retranslator_ca_price = Column(Integer)
    retr_object_id = Column(Integer, ForeignKey('ca_objects.ca_object_id'))

    # ca_object = relationship('ca_objects', back_populates='object_retranslators')
    #
class monitoring_system(Base):
    __tablename__ = 'monitoring_system'
    mon_sys_id = Column(Integer, primary_key=True, autoincrement=True)
    pu_sm_id = Column(Integer, unique=True)
    mon_sys_name = Column(String(255))
    mon_sys_obj_price_suntel = Column(Integer)
    mon_sys_ca_obj_price_default = Column(Integer)

    # ca_objects = relationship('ca_objects', back_populates='ca_object_sm_id')
    #
class devices(Base):
    __tablename__ = 'devices'
    device_id = Column(Integer, primary_key=True, autoincrement=True)
    device_ca_id = Column(Integer, ForeignKey('Contragents.ca_id'))
    device_object_id = Column(Integer, ForeignKey('ca_objects.ca_object_id'))
    device_name = Column(String(255))
    device_vendor_name = Column(String(255))
    device_vendor_model = Column(String(255))
    device_vendor_id = Column(String(255))
    device_imei = Column(String(255))
    device_serial = Column(String(255))

    # contragent = relationship('Contragents', back_populates='devices')
    #
class object_vehicles(Base):
    __tablename__ = 'object_vehicles'
    vehicle_id = Column(Integer, primary_key=True, autoincrement=True)
    vehicle_object_id = Column(Integer, ForeignKey('ca_objects.ca_object_id'))
    vehicle_ca_id = Column(Integer, ForeignKey('Contragents.ca_id'))
    vehicle_vendor_name = Column(String(255))
    vehicle_vendor_model = Column(String(255))
    vehicle_year_of_manufacture = Column(String(255))
    vehicle_gos_nomer = Column(String(255))
    vehicle_gos_nomer_region = Column(String(255))
    vehicle_type = Column(String(255))
    vehicle_vin = Column(String(255))

    # contragent = relationship('Contragents', back_populates='object_vehicles')
    #

