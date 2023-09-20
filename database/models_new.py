# coding: utf-8
from sqlalchemy import Column, Date, DateTime, ForeignKey, Integer, String
from sqlalchemy.dialects.mysql import TINYINT, VARCHAR
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class GuaranteeTerm(Base):
    __tablename__ = 'guarantee_terms'

    gt_id = Column(Integer, primary_key=True, comment='ID гарантийного срока')
    gt_term = Column(Integer, comment='Срок гарантии (дней)')
    gt_type = Column(VARCHAR(255), comment='Тип гарантии')


class Holding(Base):
    __tablename__ = 'holdings'

    holding_id = Column(Integer, primary_key=True)
    holding_name = Column(String(255, 'utf8mb3_unicode_ci'))


class MonitoringSystem(Base):
    __tablename__ = 'monitoring_system'

    mon_sys_id = Column(Integer, primary_key=True)
    mon_sys_name = Column(VARCHAR(60), comment='Название системы мониторинга')
    mon_sys_obj_price_suntel = Column(Integer, comment='Стоимость объекта для Сантел')
    mon_sys_ca_obj_price_default = Column(Integer, comment='Базовая стоимость объекта для Контрагента')


class ObjectStatus(Base):
    __tablename__ = 'object_statuses'

    status_id = Column(Integer, primary_key=True)
    status = Column(String(255, 'utf8mb3_unicode_ci'))


class Contragent(Base):
    __tablename__ = 'Contragents'

    ca_id = Column(Integer, primary_key=True, comment='ID компании')
    ca_holding_id = Column(ForeignKey('holdings.holding_id'), index=True, comment='ID холдинга')
    ca_name = Column(VARCHAR(255), comment='Название контрагента')
    ca_inn = Column(VARCHAR(255), comment='ИНН контрагента')
    ca_kpp = Column(VARCHAR(255), comment='КПП контрагента')
    ca_bill_account_num = Column(VARCHAR(255), comment='Расчетный счет')
    ca_bill_account_bank_name = Column(VARCHAR(255), comment='Наименование банка')
    ca_bill_account_ogrn = Column(VARCHAR(255), comment='ОГРН')
    ca_edo_connect = Column(TINYINT(1), comment='Обмен ЭДО')
    ca_field_of_activity = Column(VARCHAR(255), comment='Сфера деятельности')
    ca_type = Column(VARCHAR(255), comment='тип компании')

    ca_holding = relationship('Holding')


class LoginUser(Base):
    __tablename__ = 'Login_users'

    id = Column(Integer, primary_key=True)
    client_name = Column(VARCHAR(60))
    login = Column(VARCHAR(60), unique=True)
    email = Column(VARCHAR(60))
    password = Column(VARCHAR(60))
    date_create = Column(Date)
    system_id = Column(ForeignKey('monitoring_system.mon_sys_id', ondelete='RESTRICT', onupdate='RESTRICT'), index=True)

    system = relationship('MonitoringSystem')


class CaObject(Base):
    __tablename__ = 'ca_objects'

    id = Column(Integer, primary_key=True)
    sys_mon_id = Column(ForeignKey('monitoring_system.mon_sys_id', ondelete='RESTRICT', onupdate='RESTRICT'), index=True, comment='ID системы мониторинга')
    sys_mon_object_id = Column(VARCHAR(50), comment='ID объекта в системе мониторинга')
    object_name = Column(VARCHAR(70), comment='Название объекта')
    object_status = Column(ForeignKey('object_statuses.status_id', ondelete='RESTRICT', onupdate='RESTRICT'), index=True, comment='Статус объекта ссылается к статусам')
    object_add_date = Column(DateTime, comment='Дата добавления объекта')
    object_last_message = Column(DateTime, comment='Дата последнего сообщения')
    object_margin = Column(Integer, comment='Надбавка к базовой цене объекта')
    owner_contragent = Column(VARCHAR(70), comment='Хозяин контрагент')
    owner_user = Column(String(25, 'utf8mb3_unicode_ci'), comment='Хозяин юзер')
    imei = Column(VARCHAR(30), comment='идентификатор терминала')
    updated = Column(DateTime, comment='Когда изменён')

    object_status1 = relationship('ObjectStatus')
    sys_mon = relationship('MonitoringSystem')


class CaContact(Base):
    __tablename__ = 'ca_contacts'

    ca_contact_id = Column(Integer, primary_key=True)
    ca_id = Column(ForeignKey('Contragents.ca_id'), index=True, comment='id компании')
    ca_contact_name = Column(VARCHAR(255), comment='Имя контактного лица')
    ca_contact_surname = Column(VARCHAR(255), comment='Фамилия контактного лица')
    ca_contact_middlename = Column(VARCHAR(255), comment='Отчество контактного лица')
    ca_contact_cell_num = Column(VARCHAR(255), comment='Сотовый телефон контакт. лица')
    ca_contact_work_num = Column(VARCHAR(255), comment='Рабочий телефон к.л.')
    ca_contact_email = Column(VARCHAR(255), comment='Электр.почт. к.л')
    ca_contact_position = Column(VARCHAR(255), comment='Должность к.л.')

    ca = relationship('Contragent')


class CaContract(Base):
    __tablename__ = 'ca_contracts'

    contract_id = Column(Integer, primary_key=True)
    ca_id = Column(ForeignKey('Contragents.ca_id'), index=True, comment='ID контрагента')
    contract_type = Column(VARCHAR(255), comment='Тип договора')
    contract_num_prefix = Column(VARCHAR(255), comment='Префикс номера договора')
    contract_num = Column(VARCHAR(255), comment='Номер договора')
    contract_payment_term = Column(VARCHAR(255), comment='условия оплаты')
    contract_payment_period = Column(VARCHAR(255), comment='Период оплаты')
    contract_start_date = Column(Date, comment='Дата заключения договора')
    contract_expired_date = Column(Date, comment='Дата завершения договора')

    ca = relationship('Contragent')


class Device(Base):
    __tablename__ = 'devices'

    device_id = Column(Integer, primary_key=True)
    device_ca_id = Column(ForeignKey('Contragents.ca_id'), index=True, comment='ID контрагента')
    device_name = Column(VARCHAR(60), comment='Название устройства')
    device_vendor_name = Column(VARCHAR(255), comment='Наименоваине производителя устройства')
    device_vendor_model = Column(VARCHAR(255), comment='Модель устройства')
    device_imei = Column(VARCHAR(60), nullable=False, unique=True, comment='IMEI устройства')
    device_serial = Column(VARCHAR(60), unique=True, comment='Серийный номер устройства')
    device_guarantee_term_id = Column(Integer, comment='ID гарантийных условий')
    device_sale_date = Column(Date, comment='Дата продажи устройства')

    device_ca = relationship('Contragent')


class ObjectCustomField(Base):
    __tablename__ = 'object_custom_fields'

    custom_field_id = Column(Integer, primary_key=True)
    custom_field_object_id = Column(ForeignKey('ca_objects.id'), index=True)
    custom_text = Column(String(255, 'utf8mb3_unicode_ci'))

    custom_field_object = relationship('CaObject')


class ObjectRetranslator(Base):
    __tablename__ = 'object_retranslators'

    retranslator_id = Column(Integer, primary_key=True)
    retranslator_name = Column(VARCHAR(50))
    retranslator_suntel_price = Column(Integer)
    retranslator_ca_price = Column(Integer)
    retr_object_id = Column(ForeignKey('ca_objects.id'), index=True)

    retr_object = relationship('CaObject')


class ObjectSensor(Base):
    __tablename__ = 'object_sensors'

    sensor_id = Column(Integer, primary_key=True)
    sensor_object_id = Column(ForeignKey('ca_objects.id'), index=True)
    sensor_name = Column(String(255, 'utf8mb3_unicode_ci'))
    sensor_type = Column(String(255, 'utf8mb3_unicode_ci'))
    sensor_vendor = Column(String(255, 'utf8mb3_unicode_ci'))
    sensor_vendor_model = Column(String(255, 'utf8mb3_unicode_ci'))
    sensor_serial = Column(String(255, 'utf8mb3_unicode_ci'))
    sensor_mac_address = Column(String(255, 'utf8mb3_unicode_ci'))
    sensor_technology = Column(String(255, 'utf8mb3_unicode_ci'))
    sensor_connect_type = Column(String(255, 'utf8mb3_unicode_ci'))

    sensor_object = relationship('CaObject')


class ObjectVehicle(Base):
    __tablename__ = 'object_vehicles'

    vehicle_id = Column(Integer, primary_key=True)
    vehicle_object_id = Column(ForeignKey('ca_objects.id'), index=True)
    vehicle_ca_id = Column(ForeignKey('Contragents.ca_id'), index=True)
    vehicle_vendor_name = Column(String(255, 'utf8mb3_unicode_ci'))
    vehicle_vendor_model = Column(String(255, 'utf8mb3_unicode_ci'))
    vehicle_year_of_manufacture = Column(String(255, 'utf8mb3_unicode_ci'))
    vehicle_gos_nomer = Column(String(255, 'utf8mb3_unicode_ci'))
    vehicle_gos_nomer_region = Column(String(255, 'utf8mb3_unicode_ci'))
    vehicle_type = Column(String(255, 'utf8mb3_unicode_ci'))
    vehicle_vin = Column(String(255, 'utf8mb3_unicode_ci'))

    vehicle_ca = relationship('Contragent')
    vehicle_object = relationship('CaObject')


class SimCard(Base):
    __tablename__ = 'sim_cards'

    sim_id = Column(Integer, primary_key=True)
    sim_device_id = Column(ForeignKey('devices.device_id'), index=True)
    sim_ca_id = Column(ForeignKey('Contragents.ca_id'), index=True)
    sim_cell_operator = Column(String(255, 'utf8mb3_unicode_ci'))
    sim_tel_number = Column(String(255, 'utf8mb3_unicode_ci'))
    sim_owner = Column(String(255, 'utf8mb3_unicode_ci'))
    sim_iccid = Column(String(255, 'utf8mb3_unicode_ci'))
    sim_ca_price = Column(Integer)
    sim_suntel_price = Column(Integer)

    sim_ca = relationship('Contragent')
    sim_device = relationship('Device')
