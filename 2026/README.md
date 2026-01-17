# 2026 Air & Sound Pollution

## Devices

1. Circuit Playground Express (3333)
2. Circuit Playground Express (3333)
3. Circuit Playground Bluefruit (4333)

### 1. Circuit Playground Bluefruit

* nRF52840 Cortex M4
* 64 MHz Cortex M4 with FPU
* 256 KB RAM
* Bootloader: 0.9.2
* CircuitPython 10.1.0-beta-1
* Device 3 is a CPB.

### 2. Circuit Playground Express

* ATSAMD21 ARM Cortex M0
* 48 MHz Cortex M0
* 32 KB RAM
* Bootloader: 3.16.0
* CircuitPython 10.1.0-beta-a
* Devices 1 and 2 are CPEs.

## Sensors

### Adafruit ENS161 MOX Gas Sensor (6431)

* https://www.sciosense.com/intuitive-air-quality-insights-ens161/
* https://www.adafruit.com/product/6431

**Data**

* Air Quality Index
* TVOC
* CO2 (eCO2)

**Documentation**

* [Guide](https://learn.adafruit.com/adafruit-ens161-mox-gas-sensor/circuitpython-and-python)
* [API & Usage](https://docs.circuitpython.org/projects/ens160/en/latest/)


### Adafruit PMSA0031 Air Quality Breakout (4632)

* https://www.adafruit.com/product/4632

**Data**

* PM 1.0, 2.5, 10.0

**Documentation**

* [Guide](https://learn.adafruit.com/adafruit-ens161-mox-gas-sensor/circuitpython-and-python)
* [API & Usage](https://docs.circuitpython.org/projects/pm25/en/latest/)

## Pollutant Info
### 1. PMs (Particulate Matter)
PMs are small particles like dust or ash that can get deep into the lungs and cause mild to severe health problems.  
PMs are devided into four categories: PM10s, which are smaller than 10 μm and don't go as deep into the lungs, PM2.5s, which are smaller than 2.5 μm and burrow deeper than PM10s, PM1.0s, which are smaller than 1 μm and go very deep into the lungs, and UFPs (Ultra-fine Particles), which are smaller than 1/10μm (100nm).
### 2. VOCs (Volatile Organic Compounds)
VOCs are human-made chemicals used and produced in the manufacture of things like paints, pharmaceuticals, and refrigerants. VOCs are often components of fuels, paint thinners, and dry cleaning agents, and are emitted as gases from some solids and liquids, such as permanent markers.
### 3. The AQI (Air Quality Index)
The AQI is a system that takes pollution density and turns it into an index, for easy classification of how dangerous the pollution in the area is. To find the AQI in your area, go to [airnow.gov](https://www.airnow.gov).  
The AQI rankings are as follows:
|Index |Ranking  |
|------|---------|
|0-50|Good     |
|51-100|Moderate|
|101-150|Sensitive|
|151-200|Unhealthy|
|201-300|Very Unhealthy|
|301+|Hazardous|

---
##### By Patrick and Christopher Canfield
