# coding: utf-8
from sqlalchemy import Column, Date, DateTime, ForeignKey, Integer, String, TIMESTAMP, text
from sqlalchemy.dialects.mysql import TINYINT, VARCHAR
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class CellOperator(Base):
    __tablename__ = 'Cell_operator'

    id = Column(Integer, primary_key=True)
    name = Column(String(60, 'utf8mb3_unicode_ci'), nullable=False)


class GlobalLogging(Base):
    __tablename__ = 'global_logging'

    id = Column(Integer, primary_key=True)
    section_type = Column(String(50, 'utf8mb3_unicode_ci'), nullable=False)
    edit_id = Column(Integer, nullable=False)
    field = Column(String(50, 'utf8mb3_unicode_ci'), nullable=False)
    old_value = Column(String(255, 'utf8mb3_unicode_ci'))
    new_value = Column(String(255, 'utf8mb3_unicode_ci'))
    change_time = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
    sys_id = Column(Integer)
    action = Column(String(100, 'utf8mb3_unicode_ci'))


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
    status = Column(VARCHAR(50))
    abon_bool = Column(TINYINT(1), nullable=False, comment='На абонентке или нет')


class Contragent(Base):
    __tablename__ = 'Contragents'

    ca_id = Column(Integer, primary_key=True)
    ca_holding_id = Column(ForeignKey('holdings.holding_id'), index=True, comment='ID холдинга')
    ca_name = Column(VARCHAR(255), comment='Название контрагента')
    ca_shortname = Column(String(250, 'utf8mb3_unicode_ci'))
    ca_inn = Column(VARCHAR(60), comment='ИНН контрагента')
    ca_kpp = Column(VARCHAR(60), comment='КПП контрагента')
    ca_bill_account_num = Column(VARCHAR(60), comment='Расчетный счет')
    ca_bill_account_bank_name = Column(VARCHAR(60), comment='Наименование банка')
    ca_bill_account_ogrn = Column(VARCHAR(60), comment='ОГРН')
    ca_edo_connect = Column(TINYINT(1), comment='Обмен ЭДО')
    ca_field_of_activity = Column(VARCHAR(260), comment='Сфера деятельности')
    ca_type = Column(VARCHAR(60), comment='тип компании')
    unique_onec_id = Column(VARCHAR(100), comment='уникальный id в 1С контрагента ')
    registration_date = Column(Date, comment='Дата регистрации в 1С')
    key_manager = Column(VARCHAR(200), comment='Основной менеджер ')
    actual_address = Column(VARCHAR(300), comment='Фактический адрес ')
    registered_office = Column(VARCHAR(300), comment='Юридический адрес ')
    phone = Column(VARCHAR(200), comment='Телефон ')

    ca_holding = relationship('Holding')


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
    owner_contragent = Column(VARCHAR(200), comment='Хозяин контрагент')
    owner_user = Column(VARCHAR(255), comment='Хозяин юзер')
    imei = Column(VARCHAR(100), comment='идентификатор терминала')
    updated = Column(DateTime, comment='Когда изменён')
    object_created = Column(DateTime, comment='Дата создания в системе мониторинга ')
    parent_id_sys = Column(VARCHAR(200), comment='Id клиента в системе мониторинга')

    object_status1 = relationship('ObjectStatus')
    sys_mon = relationship('MonitoringSystem')


class LoginUser(Base):
    __tablename__ = 'Login_users'

    id = Column(Integer, primary_key=True)
    client_name = Column(VARCHAR(200))
    login = Column(VARCHAR(60))
    email = Column(VARCHAR(60))
    password = Column(VARCHAR(60))
    date_create = Column(Date)
    system_id = Column(ForeignKey('monitoring_system.mon_sys_id', ondelete='RESTRICT', onupdate='RESTRICT'), index=True)
    contragent_id = Column(ForeignKey('Contragents.ca_id', ondelete='SET NULL', onupdate='RESTRICT'), index=True, comment='ID контрагента')
    comment_field = Column(String(270, 'utf8mb3_unicode_ci'), comment='Поле с комментариями')

    contragent = relationship('Contragent')
    system = relationship('MonitoringSystem')


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
    contract_type = Column(VARCHAR(50), comment='Тип договора')
    contract_num_prefix = Column(VARCHAR(50), comment='Префикс номера договора')
    contract_num = Column(VARCHAR(50), comment='Номер договора')
    contract_payment_term = Column(VARCHAR(50), comment='условия оплаты')
    contract_payment_period = Column(VARCHAR(50), comment='Период оплаты')
    contract_start_date = Column(Date, comment='Дата заключения договора')
    contract_expired_date = Column(Date, comment='Дата завершения договора')

    ca = relationship('Contragent')


class ClientsInSystemMonitor(Base):
    __tablename__ = 'clients_in_system_monitor'

    id = Column(Integer, primary_key=True)
    id_in_system_monitor = Column(VARCHAR(200), comment='Id клиента в системе мониторинга')
    name_in_system_monitor = Column(VARCHAR(200), comment='Имя клиента в системе мониторинга ')
    owner_id_sys_mon = Column(VARCHAR(200), comment='Id хозяина в системе мониторинга')
    system_monitor_id = Column(ForeignKey('monitoring_system.mon_sys_id', ondelete='RESTRICT', onupdate='RESTRICT'), index=True, comment='Id системы мониторинга ')
    client_id = Column(ForeignKey('Contragents.ca_id', ondelete='RESTRICT', onupdate='RESTRICT'), index=True, comment='id клиента')

    client = relationship('Contragent')
    system_monitor = relationship('MonitoringSystem')


class Device(Base):
    __tablename__ = 'devices'

    device_id = Column(Integer, primary_key=True)
    device_name = Column(VARCHAR(60), comment='Название устройства')
    device_vendor_model = Column(VARCHAR(255), comment='Модель устройства')
    device_imei = Column(VARCHAR(60), nullable=False, unique=True, comment='IMEI устройства')
    device_serial = Column(VARCHAR(60), unique=True, comment='Серийный номер устройства')
    device_ca_id = Column(ForeignKey('Contragents.ca_id'), index=True, comment='ID контрагента')
    sys_mon_id = Column(ForeignKey('monitoring_system.mon_sys_id', ondelete='RESTRICT', onupdate='RESTRICT'), index=True, comment='ID системы мониторинга')

    device_ca = relationship('Contragent')
    sys_mon = relationship('MonitoringSystem')


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
    sensor_object_id = Column(ForeignKey('ca_objects.id'), index=True, comment='На каком объекте стоит по ID объекта')
    sensor_name = Column(VARCHAR(255), comment='Имя датчика в СМ')
    sensor_type = Column(VARCHAR(255), comment='Тип датчика(ДУТ, Температуры, наклона)')
    sensor_vendor = Column(VARCHAR(255), comment='производитель')
    sensor_vendor_model = Column(VARCHAR(255), comment='Модель датчика')
    sensor_serial = Column(VARCHAR(255), comment='Серийный номер датчика')
    sensor_mac_address = Column(VARCHAR(255), comment='Мак адрес датчика')
    sensor_technology = Column(VARCHAR(255), comment='Подтип датчика(аналоговый, цифровой, частотный)')
    sensor_connect_type = Column(VARCHAR(255), comment='Тип подключения')

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
    sim_iccid = Column(VARCHAR(40), comment='ICCID')
    sim_tel_number = Column(VARCHAR(40), comment='телефонный номер сим')
    client_name = Column(VARCHAR(270), comment='Имя клиента')
    sim_cell_operator = Column(ForeignKey('Cell_operator.id', ondelete='RESTRICT', onupdate='RESTRICT'), index=True, comment='Сотовый оператор(надо по ID)')
    sim_owner = Column(TINYINT(1), comment='Владелец сим (мы или клиент)')
    sim_ca_price = Column(Integer, comment='Стоимость сим для клиента')
    sim_suntel_price = Column(Integer, comment='Стоимость сим для Сантел(закупочная)')
    sim_device_id = Column(ForeignKey('devices.device_id'), index=True, comment='ID к девайсам(devices)')
    sim_ca_id = Column(ForeignKey('Contragents.ca_id'), index=True, comment='ID контрагента')
    sim_date = Column(DateTime, comment='Дата регистрации сим')
    name_it = Column(VARCHAR(100), comment='Имя активировавшего')
    status = Column(Integer, comment='Активность симки')
    terminal_imei = Column(String(25, 'utf8mb3_unicode_ci'), comment='IMEI терминала в который вставлена симка')
    contragent_id = Column(ForeignKey('Contragents.ca_id', ondelete='SET NULL', onupdate='SET NULL'), index=True, comment='ID контрагента')

    contragent = relationship('Contragent', primaryjoin='SimCard.contragent_id == Contragent.ca_id')
    sim_ca = relationship('Contragent', primaryjoin='SimCard.sim_ca_id == Contragent.ca_id')
    Cell_operator = relationship('CellOperator')
    sim_device = relationship('Device')
