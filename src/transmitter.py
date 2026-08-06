import os
os.environ["MAVLINK20"] = "1"

import time
from pymavlink import mavutil
import odb_mavlink_v1 as mavlink_dialect

# --- CONFIGURATION ---
#SERIAL_PORT = 'COM15'
SERIAL_PORT = 'udpout:127.0.0.1:14550'
BAUD_RATE = 115200
BOOSTER_SYSTEM_ID = 2
SUSTAINER_SYSTEM_ID = 3

def run_transmitter():
    master = mavutil.mavlink_connection(SERIAL_PORT, baud=BAUD_RATE)
    
    # Instances MAVLink séparées pour chaque airframe.
    booster_mav = mavlink_dialect.MAVLink(master, srcSystem=BOOSTER_SYSTEM_ID, srcComponent=1)
    sustainer_mav = mavlink_dialect.MAVLink(master, srcSystem=SUSTAINER_SYSTEM_ID, srcComponent=1)

    print(f"Transmission lancée sur {SERIAL_PORT}...")    
    start_time = time.time()

    while True:
        current_ms = int((time.time() - start_time) * 1000)
        
        # --- ENVOI BOOSTER (ID 1) ---
        booster_mav.rocket_telemetry_send(
            time_boot_ms=current_ms,
            system_states=0xFFFF,
            event_states=0x01,
            mission_state=1,
            battery_mv=12400,
            roll=int(5.00 * 100.0),          # 5 deg -> 500 cdeg
            pitch=int(10.00 * 100.0),        # 10 deg -> 1000 cdeg
            yaw=int(45.00 * 100.0),          # 45 deg -> 4500 cdeg
            imu_acc_x=int(0.00 * 100.0),     # 0 m/s2 -> 0 cm/s2
            imu_acc_y=int(0.00 * 100.0),
            imu_acc_z=int(9.81 * 100.0),     # 9.81 m/s2 -> 981 cm/s2
            imu_gyro_x=int(0.10 * 100.0),    # 0.10 deg/s -> 10 cdeg/s
            imu_gyro_y=int(0.20 * 100.0),
            imu_gyro_z=int(0.30 * 100.0),
            imu_mag_x=int(12.3 * 100.0),     # 12.3 uT -> 1230 cuT
            imu_mag_y=int(45.6 * 100.0),
            imu_mag_z=int(78.9 * 100.0),
            altitude_msl_cm=int(1200.0 * 100.0),
            pressure_pa=int(101325),    
            temp_celsius=int(25.0 * 100.0),      # 25 C -> 2500 cdegC
            highg_acc_x=int(0.00 * 100.0),
            highg_acc_y=int(0.00 * 100.0),
            highg_acc_z=int(98.10 * 100.0),
            gps_fix=1,
            lat=465000000,
            lon=66000000,
            gps_alt=1200000,
            vel=150,
            cog=350,
            satellites_nb=12,
            imu_acc_vertical=int(9.81 * 100.0),
            highg_acc_vertical=int(98.10 * 100.0),
            kalman_z=int(1198.4 * 100.0),
            kalman_v=int(0.0 * 100.0)
        )
        print(f"[{current_ms}ms] Packet envoyé : BOOSTER (ID {BOOSTER_SYSTEM_ID})")

        time.sleep(0.10)

        # --- ENVOI SUSTAINER (ID 2) ---
        sustainer_mav.rocket_telemetry_send(
            time_boot_ms=current_ms,
            system_states=0x0F,
            event_states=0x02,
            mission_state=2,
            battery_mv=11800,
            roll=int(0.00 * 100.0),
            pitch=int(89.00 * 100.0),
            yaw=int(0.00 * 100.0),
            imu_acc_x=int(0.00 * 100.0),
            imu_acc_y=int(0.00 * 100.0),
            imu_acc_z=int(4.50 * 100.0),
            imu_gyro_x=int(0.50 * 100.0),
            imu_gyro_y=int(0.50 * 100.0),
            imu_gyro_z=int(5.00 * 100.0),
            imu_mag_x=int(13.0 * 100.0),
            imu_mag_y=int(46.0 * 100.0),
            imu_mag_z=int(79.0 * 100.0),
            altitude_msl_cm=int(8500.0 * 100.0),
            pressure_pa=int(75500),
            temp_celsius=int(18.0 * 100.0),
            highg_acc_x=int(0.00 * 100.0),
            highg_acc_y=int(0.00 * 100.0),
            highg_acc_z=int(45.00 * 100.0),
            gps_fix=1,
            lat=465010000,
            lon=66005000,
            gps_alt=8500000,
            vel=45000,
            cog=0,
            satellites_nb=10,
            imu_acc_vertical=int(4.50 * 100.0),
            highg_acc_vertical=int(45.00 * 100.0),
            kalman_z=int(8498.7 * 100.0),
            kalman_v=int(-12.3 * 100.0)
        )
        print(f"[{current_ms}ms] Packet envoyé : SUSTAINER (ID {SUSTAINER_SYSTEM_ID})")
        time.sleep(0.40)

if __name__ == "__main__":
    run_transmitter()