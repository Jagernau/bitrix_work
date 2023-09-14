| Contragents | CREATE TABLE `Contragents` (
  `ca_id` int NOT NULL COMMENT 'ID компании',
  `ca_holding_id` int DEFAULT NULL COMMENT 'ID холдинга',
  `ca_name` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL COMMENT 'Название контрагента',
  `ca_inn` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL COMMENT 'ИНН контрагента',
  `ca_kpp` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL COMMENT 'КПП контрагента',
  `ca_bill_account_num` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL COMMENT 'Расчетный счет',
  `ca_bill_account_bank_name` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL COMMENT 'Наименование банка',
  `ca_bill_account_ogrn` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL COMMENT 'ОГРН',
  `ca_edo_connect` tinyint(1) DEFAULT NULL COMMENT 'Обмен ЭДО',
  `ca_field_of_activity` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL COMMENT 'Сфера деятельности',
  `ca_type` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL COMMENT 'тип компании',
  PRIMARY KEY (`ca_id`),
  KEY `fk_ca_holding_id` (`ca_holding_id`),
  CONSTRAINT `fk_ca_holding_id` FOREIGN KEY (`ca_holding_id`) REFERENCES `holdings` (`holding_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_unicode_ci |

| ca_contacts | CREATE TABLE `ca_contacts` (
  `ca_contact_id` int NOT NULL AUTO_INCREMENT,
  `ca_id` int DEFAULT NULL COMMENT 'id компании',
  `ca_contact_name` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL COMMENT 'Имя контактного лица',
  `ca_contact_surname` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL COMMENT 'Фамилия контактного лица',
  `ca_contact_middlename` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL COMMENT 'Отчество контактного лица',
  `ca_contact_cell_num` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL COMMENT 'Сотовый телефон контакт. лица',
  `ca_contact_work_num` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL COMMENT 'Рабочий телефон к.л.',
  `ca_contact_email` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL COMMENT 'Электр.почт. к.л',
  `ca_contact_position` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL COMMENT 'Должность к.л.',
  PRIMARY KEY (`ca_contact_id`),
  KEY `ca_id` (`ca_id`),
  CONSTRAINT `ca_contacts_ibfk_1` FOREIGN KEY (`ca_id`) REFERENCES `Contragents` (`ca_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_unicode_ci |

| ca_contracts | CREATE TABLE `ca_contracts` (
  `contract_id` int NOT NULL AUTO_INCREMENT,
  `ca_id` int DEFAULT NULL COMMENT 'ID контрагента',
  `contract_type` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL COMMENT 'Тип договора',
  `contract_num_prefix` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL COMMENT 'Префикс номера договора',
  `contract_num` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL COMMENT 'Номер договора',
  `contract_payment_term` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL COMMENT 'условия оплаты',
  `contract_payment_period` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL COMMENT 'Период оплаты',
  `contract_start_date` date DEFAULT NULL COMMENT 'Дата заключения договора',
  `contract_expired_date` date DEFAULT NULL COMMENT 'Дата завершения договора',
  PRIMARY KEY (`contract_id`),
  KEY `ca_id` (`ca_id`),
  CONSTRAINT `ca_contracts_ibfk_1` FOREIGN KEY (`ca_id`) REFERENCES `Contragents` (`ca_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_unicode_ci |

| ca_objects | CREATE TABLE `ca_objects` (
  `ca_object_id` int NOT NULL AUTO_INCREMENT,
  `ca_id` int DEFAULT NULL COMMENT 'ID компании кому пренадлежит',
  `ca_object_sm_id` int DEFAULT NULL COMMENT 'ID системы мониторинга',
  `ca_object_sm_object_id` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL COMMENT 'ID объекта в системе мониторинга',
  `ca_object_name` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL COMMENT 'Название объекта',
  `ca_object_status` int DEFAULT NULL COMMENT 'Статус объекта ссылается к статусам',
  `ca_object_add_date` datetime DEFAULT NULL COMMENT 'Дата добавления объекта',
  `ca_object_last_message` datetime DEFAULT NULL COMMENT 'Дата последнего сообщения',
  `ca_object_margin` int DEFAULT NULL COMMENT 'Надбавка к базовой цене объекта',
  PRIMARY KEY (`ca_object_id`),
  KEY `ca_id` (`ca_id`),
  KEY `mon_sys_idfk_2` (`ca_object_sm_id`),
  KEY `status_idfk_3` (`ca_object_status`),
  CONSTRAINT `ca_objects_ibfk_1` FOREIGN KEY (`ca_id`) REFERENCES `Contragents` (`ca_id`),
  CONSTRAINT `mon_sys_idfk_2` FOREIGN KEY (`ca_object_sm_id`) REFERENCES `monitoring_system` (`mon_sys_id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `status_idfk_3` FOREIGN KEY (`ca_object_status`) REFERENCES `object_statuses` (`status_id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_unicode_ci |

| devices | CREATE TABLE `devices` (
  `device_id` int NOT NULL AUTO_INCREMENT,
  `device_ca_id` int DEFAULT NULL COMMENT 'ID контрагента',
  `device_object_id` int DEFAULT NULL COMMENT 'ID объекта',
  `device_name` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL COMMENT 'Название устройства',
  `device_vendor_name` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL COMMENT 'Наименоваине производителя устройства',
  `device_vendor_model` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL COMMENT 'Модель устройства',
  `device_vendor_id` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL COMMENT 'ID устройства производителя',
  `device_imei` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL COMMENT 'IMEI устройства',
  `device_serial` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL COMMENT 'Серийный номер устройства',
  `device_guarantee_term_id` int DEFAULT NULL COMMENT 'ID гарантийных условий',
  `device_sale_date` date DEFAULT NULL COMMENT 'Дата продажи устройства',
  PRIMARY KEY (`device_id`),
  KEY `device_ca_id` (`device_ca_id`),
  KEY `device_object_id` (`device_object_id`),
  CONSTRAINT `devices_ibfk_1` FOREIGN KEY (`device_ca_id`) REFERENCES `Contragents` (`ca_id`),
  CONSTRAINT `devices_ibfk_2` FOREIGN KEY (`device_object_id`) REFERENCES `ca_objects` (`ca_object_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_unicode_ci |

| guarantee_terms | CREATE TABLE `guarantee_terms` (
  `gt_id` int NOT NULL AUTO_INCREMENT COMMENT 'ID гарантийного срока',
  `gt_term` int DEFAULT NULL COMMENT 'Срок гарантии (дней)',
  `gt_type` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL COMMENT 'Тип гарантии',
  PRIMARY KEY (`gt_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_unicode_ci |

| holdings | CREATE TABLE `holdings` (
  `holding_id` int NOT NULL AUTO_INCREMENT,
  `holding_name` varchar(255) COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`holding_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_unicode_ci |

| monitoring_system | CREATE TABLE `monitoring_system` (
  `mon_sys_id` int NOT NULL AUTO_INCREMENT,
  `pu_sm_id` int DEFAULT NULL COMMENT 'ID системы мониторинга в ПУ',
  `mon_sys_name` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL COMMENT 'Название системы мониторинга',
  `mon_sys_obj_price_suntel` int DEFAULT NULL COMMENT 'Стоимость объекта для Сантел',
  `mon_sys_ca_obj_price_default` int DEFAULT NULL COMMENT 'Базовая стоимость объекта для Контрагента',
  PRIMARY KEY (`mon_sys_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_unicode_ci |

| object_custom_fields | CREATE TABLE `object_custom_fields` (
  `custom_field_id` int NOT NULL AUTO_INCREMENT,
  `custom_field_object_id` int DEFAULT NULL,
  `custom_text` varchar(255) COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`custom_field_id`),
  KEY `custom_field_object_id` (`custom_field_object_id`),
  CONSTRAINT `object_custom_fields_ibfk_1` FOREIGN KEY (`custom_field_object_id`) REFERENCES `ca_objects` (`ca_object_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_unicode_ci |

| object_retranslators | CREATE TABLE `object_retranslators` (
  `retranslator_id` int NOT NULL AUTO_INCREMENT,
  `retranslator_name` varchar(255) COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `retranslator_suntel_price` int DEFAULT NULL,
  `retranslator_ca_price` int DEFAULT NULL,
  `retr_object_id` int DEFAULT NULL,
  PRIMARY KEY (`retranslator_id`),
  KEY `retr_object_id` (`retr_object_id`),
  CONSTRAINT `object_retranslators_ibfk_1` FOREIGN KEY (`retr_object_id`) REFERENCES `ca_objects` (`ca_object_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_unicode_ci |

| object_sensors | CREATE TABLE `object_sensors` (
  `sensor_id` int NOT NULL AUTO_INCREMENT,
  `sensor_object_id` int DEFAULT NULL,
  `sensor_name` varchar(255) COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `sensor_type` varchar(255) COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `sensor_vendor` varchar(255) COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `sensor_vendor_model` varchar(255) COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `sensor_serial` varchar(255) COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `sensor_mac_address` varchar(255) COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `sensor_technology` varchar(255) COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `sensor_connect_type` varchar(255) COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`sensor_id`),
  KEY `sensor_object_id` (`sensor_object_id`),
  CONSTRAINT `object_sensors_ibfk_1` FOREIGN KEY (`sensor_object_id`) REFERENCES `ca_objects` (`ca_object_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_unicode_ci |

| object_statuses | CREATE TABLE `object_statuses` (
  `status_id` int NOT NULL AUTO_INCREMENT,
  `status` varchar(255) COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`status_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_unicode_ci |

| object_vehicles | CREATE TABLE `object_vehicles` (
  `vehicle_id` int NOT NULL AUTO_INCREMENT,
  `vehicle_object_id` int DEFAULT NULL,
  `vehicle_ca_id` int DEFAULT NULL,
  `vehicle_vendor_name` varchar(255) COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `vehicle_vendor_model` varchar(255) COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `vehicle_year_of_manufacture` varchar(255) COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `vehicle_gos_nomer` varchar(255) COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `vehicle_gos_nomer_region` varchar(255) COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `vehicle_type` varchar(255) COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `vehicle_vin` varchar(255) COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`vehicle_id`),
  KEY `vehicle_object_id` (`vehicle_object_id`),
  KEY `vehicle_ca_id` (`vehicle_ca_id`),
  CONSTRAINT `object_vehicles_ibfk_1` FOREIGN KEY (`vehicle_object_id`) REFERENCES `ca_objects` (`ca_object_id`),
  CONSTRAINT `object_vehicles_ibfk_2` FOREIGN KEY (`vehicle_ca_id`) REFERENCES `Contragents` (`ca_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_unicode_ci |

| sim_cards | CREATE TABLE `sim_cards` (
  `sim_id` int NOT NULL AUTO_INCREMENT,
  `sim_device_id` int DEFAULT NULL,
  `sim_ca_id` int DEFAULT NULL,
  `sim_cell_operator` varchar(255) COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `sim_tel_number` varchar(255) COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `sim_owner` varchar(255) COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `sim_iccid` varchar(255) COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `sim_ca_price` int DEFAULT NULL,
  `sim_suntel_price` int DEFAULT NULL,
  PRIMARY KEY (`sim_id`),
  KEY `sim_device_id` (`sim_device_id`),
  KEY `sim_ca_id` (`sim_ca_id`),
  CONSTRAINT `sim_cards_ibfk_1` FOREIGN KEY (`sim_device_id`) REFERENCES `devices` (`device_id`),
  CONSTRAINT `sim_cards_ibfk_2` FOREIGN KEY (`sim_ca_id`) REFERENCES `Contragents` (`ca_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_unicode_ci |
