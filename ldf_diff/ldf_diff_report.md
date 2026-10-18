# LIN Description File (LDF) Semantic Change Report

- **OLD BASE FILE:** SFB_BMS2-5682.ldf
- **NEW TARGET FILE:** Upfitter-6x_LIN_20260722_v1.0.0 1.ldf

## 1. Network Node Updates

- **[+] Added Slave Node:** USP_1
- **[-] Removed Slave Node:** BMS
- **[-] Removed Slave Node:** BMS2
- **[-] Removed Slave Node:** UCIM_UCIM2

## 2. Frame Architecture & Nested Signals Map

### ➕ Added Frames

#### frame: **CIM_1**
- **Frame ID:** 1 | **Size:** 6 Bytes | **Publisher:** CIM_1
- **Nested Signals Layout Matrix:**
  | Signal Variable Target | Bit Offset | Length |
  | --- | --- | --- |
  | CIM_SW1_LED_Rq | 0 | 3 bits |
  | CIM_SW2_LED_Rq | 3 | 3 bits |
  | CIM_SW3_LED_Rq | 6 | 3 bits |
  | CIM_SW4_LED_Rq | 9 | 3 bits |
  | CIM_SW5_LED_Rq | 12 | 3 bits |
  | CIM_SW6_LED_Rq | 15 | 3 bits |
  | CIM_FET1_Rq | 18 | 1 bits |
  | CIM_FET2_Rq | 19 | 1 bits |
  | CIM_FET3_Rq | 20 | 1 bits |
  | CIM_FET4_Rq | 21 | 1 bits |
  | CIM_FET5_Rq | 22 | 1 bits |
  | CIM_FET6_Rq | 23 | 1 bits |
  | CIM_FET7_Rq | 24 | 1 bits |
  | LIN_Dimming_Level | 25 | 8 bits |
  | LIN_Litval | 33 | 8 bits |
  | CIM_Reserved_7bit | 41 | 7 bits |

#### frame: **USP1PartNum**
- **Frame ID:** 6 | **Size:** 8 Bytes | **Publisher:** USP_1
- **Nested Signals Layout Matrix:**
  | Signal Variable Target | Bit Offset | Length |
  | --- | --- | --- |
  | USP1_APINFO_0 | 0 | 1 bits |
  | USP1_APINFO_1 | 1 | 1 bits |
  | USP1_APINFO_2 | 2 | 1 bits |
  | USP1_APINFO_3 | 3 | 1 bits |
  | USP1_APINFO_4 | 4 | 1 bits |
  | USP1_LINStatus | 5 | 3 bits |
  | USP1PartNumIndex | 8 | 8 bits |
  | USP1PartNumData0 | 16 | 8 bits |
  | USP1PartNumData1 | 24 | 8 bits |
  | USP1PartNumData2 | 32 | 8 bits |
  | USP1PartNumData3 | 40 | 8 bits |
  | USP1PartNumData4 | 48 | 8 bits |
  | USP1PartNumData5 | 56 | 8 bits |

#### frame: **USP1SerialNum**
- **Frame ID:** 7 | **Size:** 8 Bytes | **Publisher:** USP_1
- **Nested Signals Layout Matrix:**
  | Signal Variable Target | Bit Offset | Length |
  | --- | --- | --- |
  | USP1_APINFO_0 | 0 | 1 bits |
  | USP1_APINFO_1 | 1 | 1 bits |
  | USP1_APINFO_2 | 2 | 1 bits |
  | USP1_APINFO_3 | 3 | 1 bits |
  | USP1_APINFO_4 | 4 | 1 bits |
  | USP1_LINStatus | 5 | 3 bits |
  | USP1SrNrDigit00 | 8 | 4 bits |
  | USP1SrNrDigit01 | 12 | 4 bits |
  | USP1SrNrDigit02 | 16 | 4 bits |
  | USP1SrNrDigit03 | 20 | 4 bits |
  | USP1SrNrDigit04 | 24 | 4 bits |
  | USP1SrNrDigit05 | 28 | 4 bits |
  | USP1SrNrDigit06 | 32 | 4 bits |
  | USP1SrNrDigit07 | 36 | 4 bits |
  | USP1SrNrDigit08 | 40 | 4 bits |
  | USP1SrNrDigit09 | 44 | 4 bits |
  | USP1SrNrDigit10 | 48 | 4 bits |
  | USP1SrNrDigit11 | 52 | 4 bits |
  | USP1SrNrDigit12 | 56 | 4 bits |
  | USP1SrNrDigit13 | 60 | 4 bits |

#### frame: **USP_1**
- **Frame ID:** 0 | **Size:** 8 Bytes | **Publisher:** USP_1
- **Nested Signals Layout Matrix:**
  | Signal Variable Target | Bit Offset | Length |
  | --- | --- | --- |
  | USP1_APINFO_0 | 0 | 1 bits |
  | USP1_APINFO_1 | 1 | 1 bits |
  | USP1_APINFO_2 | 2 | 1 bits |
  | USP1_APINFO_3 | 3 | 1 bits |
  | USP1_APINFO_4 | 4 | 1 bits |
  | USP1_LINStatus | 5 | 3 bits |
  | USP1_SW1A_Switch_State | 8 | 2 bits |
  | USP1_SW1B_Switch_State | 10 | 2 bits |
  | USP1_SW2_Switch_State | 12 | 2 bits |
  | USP1_SW3_Switch_State | 14 | 2 bits |
  | USP1_SW4_Switch_State | 16 | 2 bits |
  | USP1_SW5_Switch_State | 18 | 2 bits |
  | USP1_SW6_Switch_State | 20 | 2 bits |
  | USP1_FET1_State | 22 | 2 bits |
  | USP1_FET2_State | 24 | 2 bits |
  | USP1_FET3_State | 26 | 2 bits |
  | USP1_FET4_State | 28 | 2 bits |
  | USP1_FET5_State | 30 | 2 bits |
  | USP1_FET6_State | 32 | 2 bits |
  | USP1_FET7_State | 34 | 2 bits |
  | USP1_SW1_LED_State | 36 | 3 bits |
  | USP1_SW2_LED_State | 39 | 3 bits |
  | USP1_SW3_LED_State | 42 | 3 bits |
  | USP1_SW4_LED_State | 45 | 3 bits |
  | USP1_SW5_LED_State | 48 | 3 bits |
  | USP1_SW6_LED_State | 51 | 3 bits |
  | USP1_Reserved1_2bits | 54 | 2 bits |
  | USP1_Reserved2_8bits | 56 | 8 bits |

### ➖ Removed Frames

#### frame: **BCM_D_BMS2_FrP12**
- **Frame ID:** 0x06 | **Size:** 8 Bytes
- **Nested Signals Matrix:**
  | Signal Variable Target | Bit Offset | Length |
  | --- | --- | --- |
  | IgnKeyPosition_BMS2 | 0 | N/A bits |
  | BSDiagReset_BMS2 | 2 | N/A bits |
  | AutoStopCurrentEst_BMS2 | 3 | N/A bits |
  | SleepMode_BMS2 | 10 | N/A bits |
  | POI_SOC_Cal_BMS2 | 11 | N/A bits |
  | StarterResistanceCCC_BMS2 | 16 | N/A bits |
  | StarterResistanceWCC_BMS2 | 24 | N/A bits |
  | StarterResistanceIQD_BMS2 | 32 | N/A bits |
  | SOCWakeUpValue_BMS2 | 40 | N/A bits |

#### frame: **BCM_D_BMS2_FrP13**
- **Frame ID:** 0x07 | **Size:** 8 Bytes
- **Nested Signals Matrix:**
  | Signal Variable Target | Bit Offset | Length |
  | --- | --- | --- |
  | Battery2BCMTableNumber | 0 | N/A bits |
  | Battery2Size | 9 | N/A bits |
  | Battery2Design | 14 | N/A bits |
  | Battery2CCA | 17 | N/A bits |
  | Battery2Capacity | 27 | N/A bits |
  | Battery2UC0max | 35 | N/A bits |
  | Battery2NormAcidCapacity | 48 | N/A bits |

#### frame: **BCM_D_BMS2_FrP14**
- **Frame ID:** 0x08 | **Size:** 8 Bytes
- **Nested Signals Matrix:**
  | Signal Variable Target | Bit Offset | Length |
  | --- | --- | --- |
  | Ri_25C_95_Battery2 | 0 | N/A bits |
  | Ri_25C_75_Battery2 | 8 | N/A bits |
  | Ri_25C_55_Battery2 | 16 | N/A bits |
  | Ri_25C_45_Battery2 | 24 | N/A bits |
  | Ri_25C_35_Battery2 | 32 | N/A bits |
  | Ri_25C_25_Battery2 | 40 | N/A bits |
  | Ri_25C_15_Battery2 | 48 | N/A bits |

#### frame: **BCM_D_BMS2_FrP15**
- **Frame ID:** 0x09 | **Size:** 8 Bytes
- **Nested Signals Matrix:**
  | Signal Variable Target | Bit Offset | Length |
  | --- | --- | --- |
  | CurrentLoadMagnitude_BMS2 | 0 | N/A bits |
  | CurrentLoadDuration_BMS2 | 10 | N/A bits |

#### frame: **BCM_D_FrP12**
- **Frame ID:** 0x02 | **Size:** 8 Bytes
- **Nested Signals Matrix:**
  | Signal Variable Target | Bit Offset | Length |
  | --- | --- | --- |
  | IgnKeyPosition | 0 | N/A bits |
  | BSDiagReset | 2 | N/A bits |
  | AutoStopCurrentEst | 3 | N/A bits |
  | SleepMode | 10 | N/A bits |
  | POI_SOC_Cal | 11 | N/A bits |
  | StarterResistanceCCC | 16 | N/A bits |
  | StarterResistanceWCC | 24 | N/A bits |
  | StarterResistanceIQD | 32 | N/A bits |
  | SOCWakeUpValue | 40 | N/A bits |

#### frame: **BCM_D_FrP13**
- **Frame ID:** 0x03 | **Size:** 8 Bytes
- **Nested Signals Matrix:**
  | Signal Variable Target | Bit Offset | Length |
  | --- | --- | --- |
  | BatteryBCMTableNumber | 0 | N/A bits |
  | BatterySize | 9 | N/A bits |
  | BatteryDesign | 14 | N/A bits |
  | BatteryCCA | 17 | N/A bits |
  | BatteryCapacity | 27 | N/A bits |
  | BatteryUC0max | 35 | N/A bits |
  | BatteryNormAcidCapacity | 48 | N/A bits |

#### frame: **BCM_D_FrP14**
- **Frame ID:** 0x04 | **Size:** 8 Bytes
- **Nested Signals Matrix:**
  | Signal Variable Target | Bit Offset | Length |
  | --- | --- | --- |
  | Ri_25C_95 | 0 | N/A bits |
  | Ri_25C_75 | 8 | N/A bits |
  | Ri_25C_55 | 16 | N/A bits |
  | Ri_25C_45 | 24 | N/A bits |
  | Ri_25C_35 | 32 | N/A bits |
  | Ri_25C_25 | 40 | N/A bits |
  | Ri_25C_15 | 48 | N/A bits |

#### frame: **BCM_D_FrP15**
- **Frame ID:** 0x05 | **Size:** 8 Bytes
- **Nested Signals Matrix:**
  | Signal Variable Target | Bit Offset | Length |
  | --- | --- | --- |
  | CurrentLoadMagnitude | 0 | N/A bits |
  | CurrentLoadDuration | 10 | N/A bits |

#### frame: **BMS2_D_FrP00**
- **Frame ID:** 0x11 | **Size:** 8 Bytes
- **Nested Signals Matrix:**
  | Signal Variable Target | Bit Offset | Length |
  | --- | --- | --- |
  | BMS2LINStatus | 0 | N/A bits |
  | BSBatt2Voltage | 8 | N/A bits |
  | BS2FaultLIN | 23 | N/A bits |
  | BSBatt2Current | 24 | N/A bits |
  | BS2CurrentLoadResponse | 48 | N/A bits |
  | BSBatt2SOC_EEM_Function | 56 | N/A bits |

#### frame: **BMS2_D_FrP01**
- **Frame ID:** 0x12 | **Size:** 8 Bytes
- **Nested Signals Matrix:**
  | Signal Variable Target | Bit Offset | Length |
  | --- | --- | --- |
  | BMS2LINStatus | 0 | N/A bits |
  | BSBatt2Temp | 8 | N/A bits |
  | BSBatt2SensorTemp | 16 | N/A bits |
  | BSBatt2RiTNom | 24 | N/A bits |
  | BSBatt2RiTNomStatus | 33 | N/A bits |
  | BS2AutoDiagResetCounter | 35 | N/A bits |
  | BSBatt2Ri | 40 | N/A bits |
  | BSBatt2RiStatus | 49 | N/A bits |
  | BSBatt2OCV | 51 | N/A bits |

#### frame: **BMS2_D_FrP02**
- **Frame ID:** 0x13 | **Size:** 8 Bytes
- **Nested Signals Matrix:**
  | Signal Variable Target | Bit Offset | Length |
  | --- | --- | --- |
  | BMS2LINStatus | 0 | N/A bits |
  | BSBatt2QCapAhLIN | 8 | N/A bits |
  | BSBatt2QCapAhTNom | 15 | N/A bits |
  | BSBatt2SOHLAM | 22 | N/A bits |
  | BSBatt2SOHLAMStatus | 29 | N/A bits |
  | BSBatt2SOHSUL | 31 | N/A bits |
  | BSBatt2SOHSULStatus | 38 | N/A bits |
  | BSBatt2Uc0minAged | 40 | N/A bits |
  | BSBatt2Uc0maxAged | 52 | N/A bits |

#### frame: **BMS2_D_FrP03**
- **Frame ID:** 0x14 | **Size:** 8 Bytes
- **Nested Signals Matrix:**
  | Signal Variable Target | Bit Offset | Length |
  | --- | --- | --- |
  | BMS2LINStatus | 0 | N/A bits |
  | BSBatt2SOC_Actual | 8 | N/A bits |
  | BSBatt2SOC_EEM_Function | 15 | N/A bits |
  | BSBatt2SOCStatus | 22 | N/A bits |
  | BSBatt2LastSOCRecal | 24 | N/A bits |
  | BSBatt2SOCRecalUsed | 32 | N/A bits |
  | BSBatt2SOC_AhFlag | 34 | N/A bits |
  | BSBatt2SOC_ConsistencyFlag | 35 | N/A bits |
  | BSBatt2SOC_BlindChargeFlag | 36 | N/A bits |
  | BSBatt2SOC_PORFlag | 37 | N/A bits |
  | BSBatt2SOC_BSFaultFlag | 38 | N/A bits |
  | BSBatt2SOC_BatteryParameters | 39 | N/A bits |
  | BSBatt2SOC_BSDiagResetFlag | 40 | N/A bits |
  | BSBatt2SOC_TransportFlag | 41 | N/A bits |
  | BS2Stratification | 42 | N/A bits |
  | BS2Icing | 43 | N/A bits |
  | BS2ConsistencyFault | 44 | N/A bits |
  | BS2PowerOnJustOccured | 45 | N/A bits |
  | BSBatt2FullChargeDetected | 46 | N/A bits |
  | BS2Mode | 47 | N/A bits |
  | BSBatt2TimeInService | 48 | N/A bits |

#### frame: **BMS2_D_FrP04**
- **Frame ID:** 0x15 | **Size:** 8 Bytes
- **Nested Signals Matrix:**
  | Signal Variable Target | Bit Offset | Length |
  | --- | --- | --- |
  | BMS2LINStatus | 0 | N/A bits |
  | BSBatt2_Ah_QD_Timer | 8 | N/A bits |
  | BSBatt2TSOFQD | 24 | N/A bits |
  | BSBatt2TSOHQD | 32 | N/A bits |
  | BSBatt2_I_QD | 40 | N/A bits |
  | BSBatt2_Ah_QD | 49 | N/A bits |
  | BSBatt2_Ah_QD_TB | 62 | N/A bits |
  | BS2BlindChargeFlag | 63 | N/A bits |

#### frame: **BMS2_D_FrP05**
- **Frame ID:** 0x16 | **Size:** 8 Bytes
- **Nested Signals Matrix:**
  | Signal Variable Target | Bit Offset | Length |
  | --- | --- | --- |
  | BMS2LINStatus | 0 | N/A bits |
  | BSBatt2VSOFCCC | 8 | N/A bits |
  | BSBatt2TSOFWCC | 16 | N/A bits |

#### frame: **BMS2_D_FrP06**
- **Frame ID:** 0x17 | **Size:** 8 Bytes
- **Nested Signals Matrix:**
  | Signal Variable Target | Bit Offset | Length |
  | --- | --- | --- |
  | BMS2LINStatus | 0 | N/A bits |
  | BSBatt2QChaRideCN | 8 | N/A bits |
  | BSBatt2QDchRideCn | 24 | N/A bits |
  | BSBatt2QDeltaRideAhLIN | 40 | N/A bits |

#### frame: **BMS2_D_FrP07**
- **Frame ID:** 0x18 | **Size:** 8 Bytes
- **Nested Signals Matrix:**
  | Signal Variable Target | Bit Offset | Length |
  | --- | --- | --- |
  | BMS2LINStatus | 0 | N/A bits |
  | BSBatt2QDchQDCn | 8 | N/A bits |
  | BSBatt2QDchActCn | 24 | N/A bits |
  | BSBatt2VSOHCCC | 40 | N/A bits |
  | BSBatt2VSOHCCC_50 | 48 | N/A bits |
  | BSBatt2TSOHWCC | 56 | N/A bits |

#### frame: **BMS2_D_FrP08**
- **Frame ID:** 0x19 | **Size:** 8 Bytes
- **Nested Signals Matrix:**
  | Signal Variable Target | Bit Offset | Length |
  | --- | --- | --- |
  | BMS2LINStatus | 0 | N/A bits |
  | BSBatt2CurrentECOS | 8 | N/A bits |
  | BSBatt2VoltageECOS | 24 | N/A bits |

#### frame: **BMS2_D_FrP09**
- **Frame ID:** 0x1A | **Size:** 8 Bytes
- **Nested Signals Matrix:**
  | Signal Variable Target | Bit Offset | Length |
  | --- | --- | --- |
  | BMS2LINStatus | 0 | N/A bits |
  | BS2GassingRate | 8 | N/A bits |
  | BS2ShortedCell | 20 | N/A bits |
  | BS2WaterLoss | 21 | N/A bits |
  | BSBatt2Ri_25C | 31 | N/A bits |

#### frame: **BMS2_D_FrP10**
- **Frame ID:** 0x1B | **Size:** 8 Bytes
- **Nested Signals Matrix:**
  | Signal Variable Target | Bit Offset | Length |
  | --- | --- | --- |
  | BSBatt2KoLCurrent | 0 | N/A bits |

#### frame: **BMS2_D_FrP11**
- **Frame ID:** 0x1C | **Size:** 8 Bytes
- **Nested Signals Matrix:**
  | Signal Variable Target | Bit Offset | Length |
  | --- | --- | --- |
  | BMS2LINStatus | 0 | N/A bits |
  | BMS2PartNumIndex | 8 | N/A bits |
  | BMS2PartNumData0 | 16 | N/A bits |
  | BMS2PartNumData1 | 24 | N/A bits |
  | BMS2PartNumData2 | 32 | N/A bits |
  | BMS2PartNumData3 | 40 | N/A bits |
  | BMS2PartNumData4 | 48 | N/A bits |
  | BMS2PartNumData5 | 56 | N/A bits |

#### frame: **BMS2_D_FrP12**
- **Frame ID:** 0x1D | **Size:** 8 Bytes
- **Nested Signals Matrix:**
  | Signal Variable Target | Bit Offset | Length |
  | --- | --- | --- |
  | BMS2LINStatus | 0 | N/A bits |
  | BSBatt2SOF_V_WCC | 8 | N/A bits |
  | BSBatt2SOF_I_WCC | 16 | N/A bits |
  | BS2CrankVoltage | 27 | N/A bits |
  | BS2CrankTimer | 40 | N/A bits |
  | BS2CrankCurrent | 48 | N/A bits |

#### frame: **BMS_D_FrASIL_001**
- **Frame ID:** 0x2E | **Size:** 8 Bytes
- **Nested Signals Matrix:**
  | Signal Variable Target | Bit Offset | Length |
  | --- | --- | --- |
  | BMSLINStatus | 0 | 8 bits |
  | BSBatt_Voltage_ASIL | 8 | N/A bits |
  | BSBatt_Batt_Off_ASIL | 23 | N/A bits |
  | BSBatt_Current_ASIL | 24 | N/A bits |
  | BS_ASIL_Frame_Counter1 | 48 | N/A bits |
  | BS_ASIL_CRC1 | 56 | N/A bits |

#### frame: **BMS_D_FrASIL_002**
- **Frame ID:** 0x2F | **Size:** 8 Bytes
- **Nested Signals Matrix:**
  | Signal Variable Target | Bit Offset | Length |
  | --- | --- | --- |
  | BMSLINStatus | 0 | 8 bits |
  | BSBatt_Ri_ASIL | 8 | N/A bits |
  | BSBatt_Ri_Error_ASIL | 20 | N/A bits |
  | BSBatt_SOF_ASIL | 24 | N/A bits |
  | BSBatt_SOF_Error_ASIL | 32 | N/A bits |
  | BS_ASIL_Frame_Counter2 | 48 | N/A bits |
  | BS_ASIL_CRC2 | 56 | N/A bits |

#### frame: **BMS_D_FrP00**
- **Frame ID:** 0x21 | **Size:** 8 Bytes
- **Nested Signals Matrix:**
  | Signal Variable Target | Bit Offset | Length |
  | --- | --- | --- |
  | BMSLINStatus | 0 | 8 bits |
  | BSBattVoltage | 8 | 15 bits |
  | BSFaultLIN | 23 | 1 bits |
  | BSBattCurrent | 24 | 24 bits |
  | BSCurrentLoadResponse | 48 | N/A bits |
  | BSBattSOC_EEM_Function | 56 | N/A bits |

#### frame: **BMS_D_FrP01**
- **Frame ID:** 0x22 | **Size:** 8 Bytes
- **Nested Signals Matrix:**
  | Signal Variable Target | Bit Offset | Length |
  | --- | --- | --- |
  | BMSLINStatus | 0 | 8 bits |
  | BSBattTemp | 8 | N/A bits |
  | BSBattSensorTemp | 16 | N/A bits |
  | BSBattRiTNom | 24 | N/A bits |
  | BSBattRiTNomStatus | 33 | N/A bits |
  | BSAutoDiagResetCounter | 35 | N/A bits |
  | BSBattRi | 40 | N/A bits |
  | BSBattRiStatus | 49 | N/A bits |
  | BSBattOCV | 51 | N/A bits |

#### frame: **BMS_D_FrP02**
- **Frame ID:** 0x23 | **Size:** 8 Bytes
- **Nested Signals Matrix:**
  | Signal Variable Target | Bit Offset | Length |
  | --- | --- | --- |
  | BMSLINStatus | 0 | 8 bits |
  | BSBattQCapAhLIN | 8 | N/A bits |
  | BSBattQCapAhTNom | 15 | N/A bits |
  | BSBattSOHLAM | 22 | N/A bits |
  | BSBattSOHLAMStatus | 29 | N/A bits |
  | BSBattSOHSUL | 31 | N/A bits |
  | BSBattSOHSULStatus | 38 | N/A bits |
  | BSBattUc0minAged | 40 | N/A bits |
  | BSBattUc0maxAged | 52 | N/A bits |

#### frame: **BMS_D_FrP03**
- **Frame ID:** 0x24 | **Size:** 8 Bytes
- **Nested Signals Matrix:**
  | Signal Variable Target | Bit Offset | Length |
  | --- | --- | --- |
  | BMSLINStatus | 0 | 8 bits |
  | BSBattSOC_Actual | 8 | N/A bits |
  | BSBattSOC_EEM_Function | 15 | N/A bits |
  | BSBattSOCStatus | 22 | N/A bits |
  | BSBattLastSOCRecal | 24 | N/A bits |
  | BSBattSOCRecalUsed | 32 | N/A bits |
  | BSBattSOC_AhFlag | 34 | N/A bits |
  | BSBattSOC_ConsistencyFlag | 35 | N/A bits |
  | BSBattSOC_BlindChargeFlag | 36 | N/A bits |
  | BSBattSOC_PORFlag | 37 | N/A bits |
  | BSBattSOC_BSFaultFlag | 38 | N/A bits |
  | BSBattSOC_BatteryParameters | 39 | N/A bits |
  | BSBattSOC_BSDiagResetFlag | 40 | N/A bits |
  | BSBattSOC_TransportFlag | 41 | N/A bits |
  | BSStratification | 42 | N/A bits |
  | BSIcing | 43 | N/A bits |
  | BSConsistencyFault | 44 | N/A bits |
  | BSPowerOnJustOccured | 45 | N/A bits |
  | BSBattFullChargeDetected | 46 | N/A bits |
  | BSMode | 47 | N/A bits |
  | BSBattTimeInService | 48 | N/A bits |

#### frame: **BMS_D_FrP04**
- **Frame ID:** 0x25 | **Size:** 8 Bytes
- **Nested Signals Matrix:**
  | Signal Variable Target | Bit Offset | Length |
  | --- | --- | --- |
  | BMSLINStatus | 0 | 8 bits |
  | BSBatt_Ah_QD_Timer | 8 | N/A bits |
  | BSBattTSOFQD | 24 | N/A bits |
  | BSBattTSOHQD | 32 | N/A bits |
  | BSBatt_I_QD | 40 | N/A bits |
  | BSBatt_Ah_QD | 49 | N/A bits |
  | BSBatt_Ah_QD_TB | 62 | N/A bits |
  | BSBlindChargeFlag | 63 | N/A bits |

#### frame: **BMS_D_FrP05**
- **Frame ID:** 0x26 | **Size:** 8 Bytes
- **Nested Signals Matrix:**
  | Signal Variable Target | Bit Offset | Length |
  | --- | --- | --- |
  | BMSLINStatus | 0 | 8 bits |
  | BSBattVSOFCCC | 8 | N/A bits |
  | BSBattTSOFWCC | 16 | N/A bits |

#### frame: **BMS_D_FrP06**
- **Frame ID:** 0x27 | **Size:** 8 Bytes
- **Nested Signals Matrix:**
  | Signal Variable Target | Bit Offset | Length |
  | --- | --- | --- |
  | BMSLINStatus | 0 | 8 bits |
  | BSBattQChaRideCN | 8 | N/A bits |
  | BSBattQDchRideCn | 24 | N/A bits |
  | BSBattQDeltaRideAhLIN | 40 | N/A bits |

#### frame: **BMS_D_FrP07**
- **Frame ID:** 0x28 | **Size:** 8 Bytes
- **Nested Signals Matrix:**
  | Signal Variable Target | Bit Offset | Length |
  | --- | --- | --- |
  | BMSLINStatus | 0 | 8 bits |
  | BSBattQDchQDCn | 8 | N/A bits |
  | BSBattQDchActCn | 24 | N/A bits |
  | BSBattVSOHCCC | 40 | N/A bits |
  | BSBattVSOHCCC_50 | 48 | N/A bits |
  | BSBattTSOHWCC | 56 | N/A bits |

#### frame: **BMS_D_FrP08**
- **Frame ID:** 0x29 | **Size:** 8 Bytes
- **Nested Signals Matrix:**
  | Signal Variable Target | Bit Offset | Length |
  | --- | --- | --- |
  | BMSLINStatus | 0 | 8 bits |
  | BSBattCurrentECOS | 8 | N/A bits |
  | BSBattVoltageECOS | 24 | N/A bits |

#### frame: **BMS_D_FrP09**
- **Frame ID:** 0x2A | **Size:** 8 Bytes
- **Nested Signals Matrix:**
  | Signal Variable Target | Bit Offset | Length |
  | --- | --- | --- |
  | BMSLINStatus | 0 | 8 bits |
  | BSGassingRate | 8 | N/A bits |
  | BSShortedCell | 20 | N/A bits |
  | BSWaterLoss | 21 | N/A bits |
  | BSBattRi_25C | 31 | N/A bits |

#### frame: **BMS_D_FrP10**
- **Frame ID:** 0x2B | **Size:** 8 Bytes
- **Nested Signals Matrix:**
  | Signal Variable Target | Bit Offset | Length |
  | --- | --- | --- |
  | BSBattKoLCurrent | 0 | N/A bits |

#### frame: **BMS_D_FrP11**
- **Frame ID:** 0x2C | **Size:** 8 Bytes
- **Nested Signals Matrix:**
  | Signal Variable Target | Bit Offset | Length |
  | --- | --- | --- |
  | BMSLINStatus | 0 | 8 bits |
  | BMSPartNumIndex | 8 | N/A bits |
  | BMSPartNumData0 | 16 | N/A bits |
  | BMSPartNumData1 | 24 | N/A bits |
  | BMSPartNumData2 | 32 | N/A bits |
  | BMSPartNumData3 | 40 | N/A bits |
  | BMSPartNumData4 | 48 | N/A bits |
  | BMSPartNumData5 | 56 | N/A bits |

#### frame: **BMS_D_FrP12**
- **Frame ID:** 0x2D | **Size:** 8 Bytes
- **Nested Signals Matrix:**
  | Signal Variable Target | Bit Offset | Length |
  | --- | --- | --- |
  | BMSLINStatus | 0 | 8 bits |
  | BSBattSOF_V_WCC | 8 | N/A bits |
  | BSBattSOF_I_WCC | 16 | N/A bits |
  | BSCrankVoltage | 27 | N/A bits |
  | BSCrankTimer | 40 | N/A bits |
  | BSCrankCurrent | 48 | N/A bits |

#### frame: **CIM_SOFT_INPUT**
- **Frame ID:** 0x10 | **Size:** 8 Bytes
- **Nested Signals Matrix:**
  | Signal Variable Target | Bit Offset | Length |
  | --- | --- | --- |
  | Soft_Button1 | 0 | N/A bits |
  | Soft_Button2 | 2 | N/A bits |
  | Soft_Button3 | 4 | N/A bits |
  | Soft_Button4 | 6 | N/A bits |
  | Soft_Button5 | 8 | N/A bits |
  | Soft_Button6 | 10 | N/A bits |
  | Soft_Button7 | 12 | N/A bits |
  | Soft_Button8 | 14 | N/A bits |
  | CTS_Power | 16 | N/A bits |
  | ECRS_Relay | 18 | N/A bits |
  | CCP_Relay | 20 | N/A bits |
  | SFB_Update | 22 | N/A bits |
  | Handbrake | 23 | N/A bits |
  | CamperMode_D_Stat | 24 | N/A bits |
  | LocalEpoch | 32 | N/A bits |

#### frame: **SFB_STATUS**
- **Frame ID:** 0x01 | **Size:** 8 Bytes
- **Nested Signals Matrix:**
  | Signal Variable Target | Bit Offset | Length |
  | --- | --- | --- |
  | FuseState1 | 0 | N/A bits |
  | FuseState2 | 2 | N/A bits |
  | FuseState3 | 4 | N/A bits |
  | FuseState4 | 6 | N/A bits |
  | FuseState5 | 8 | N/A bits |
  | FuseState6 | 10 | N/A bits |
  | FuseState7 | 12 | N/A bits |
  | FuseState8 | 14 | N/A bits |
  | InputPin1 | 16 | N/A bits |
  | InputPin2 | 17 | N/A bits |
  | InputPin3 | 18 | N/A bits |
  | InputPin4 | 19 | N/A bits |
  | InputPin5 | 20 | N/A bits |
  | InputPin6 | 21 | N/A bits |
  | InputPin7 | 22 | N/A bits |
  | InputPin8 | 23 | N/A bits |
  | BatterySocAux1 | 24 | N/A bits |
  | BatterySocAux1Source | 31 | N/A bits |
  | BatterySocAux2 | 32 | N/A bits |
  | BatterySocAux2Source | 39 | N/A bits |
  | EcrmRelayState | 40 | N/A bits |
  | CcpRelayState | 41 | N/A bits |
  | CamperMode_B_RQ | 42 | N/A bits |
  | SplitChargeRule | 56 | N/A bits |

#### frame: **Slave_Error_Response_UCIM_UCIM2**
- **Frame ID:** 0x1E | **Size:** 8 Bytes
- **Nested Signals Matrix:**
  | Signal Variable Target | Bit Offset | Length |
  | --- | --- | --- |
  | UCIM_UCIM2_error_response_camper_st | 0 | N/A bits |

### 🔄 Changed Frames & Inner Signal Configurations

No matching frame packing layouts or internal signal configurations modified.

