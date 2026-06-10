import os
os.environ["MAVLINK20"] = "1"
os.environ.pop("MAV_IGNORE_CRC", None)

from pymavlink import mavutil
import threading
from config import RECV_TIMEOUT_S, RECONNECT_DELAY_S

# odb_mavlink_v1.py — copié depuis le repo ODB (commit: 24/05/26)
# Mettre à jour si le dialecte MAVLink change
import odb_mavlink_v1 as mavlink_dialect

mavutil.mavlink = mavlink_dialect
mavutil.current_dialect = "odb_mavlink_v1"


def _connect(serial_port, baud_rate, source_system):
    # Laisse pymavlink gérer la nature du port (série ou UDP)
    master = mavutil.mavlink_connection(
            serial_port,
            baud=baud_rate,
            source_system=source_system,
        )
    # On active uniquement le parsing robuste sur l'instance générée automatiquement
    master.mav.robust_parsing = True
    return master


def _close(master):
    try:
        if master is not None:
            master.close()
    except Exception:
        pass


def run_receiver(serial_port, source_system, baud_rate, data_queue, stop_event = None):
    if stop_event is None:
        stop_event = threading.Event()

    print(f"Station Sol active sur {serial_port}")

    while not stop_event.is_set():
        master = None
        try:
            master = _connect(serial_port, baud_rate, source_system)
            print(f"Station au sol connectée sur {serial_port}")

            while not stop_event.is_set():
                msg = master.recv_match(blocking=True, timeout=RECV_TIMEOUT_S)

                if not msg:
                    continue

                msg_type = msg.get_type()
                sys_id = msg.get_srcSystem()

                if msg_type == "BAD_DATA":
                    raw_payload = msg.get_msgbuf()
                    # print(f"\n\033[91m[ERREUR CRC/FORMAT]\033[0m Reçu : {raw_payload.hex(' ')}")
                    continue

                if msg_type == "ROCKET_TELEMETRY":
                    data_queue.put(msg)
                    continue

                print(f"\n[RAW] Type non géré : {msg_type} (Source ID: {sys_id})")
                print(f"  Contenu : {msg.to_dict()}")

        except KeyboardInterrupt:
            print("\nArrêt de la station sol, interruption clavier.")
            stop_event.set()

        except (OSError, IOError) as exc:
            print(f"\nLiaison perdue {exc}")
            print(f"Reconnexion dans {RECONNECT_DELAY_S} s")

        except Exception as exc:
            print(f"\n[ERREUR FATALE] {exc}")
            print(f"Reconnexion dans {RECONNECT_DELAY_S} s")

        finally:
            _close(master)
        
        # Tentative de reconnexion
        stop_event.wait(RECONNECT_DELAY_S)

    print("Station au sol arrêtée correctement")
