import json
import pandas as pd
import yaml


def check_sensors():
    # 1. Les innstillinger fra YAML-fil
    with open("config.yml", "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    max_days = config["max_days_since_calibration"]
    output_filename = config["output_file"]

    # 2. Les inn data fra Excel og CSV
    sensors_df = pd.read_excel("sensors.xlsx")
    calibrations_df = pd.read_csv("calibrations.csv")

    # Slå sammen (join) dataene basert på felles nøkkel (f.eks. 'sensor_id')
    merged_df = pd.merge(sensors_df, calibrations_df, on="sensor_id")

    # 3. Filtrer ut sensorer hvor kalibreringstiden har utløpt
    overdue_df = merged_df[merged_df["days_since_calibration"] > max_days]

    # Konverter relevante kolonner til en liste med ordbøker (dictionaries)
    overdue_sensors = overdue_df.to_dict(orient="records")

    # 4. Eksporter til JSON-fil spesifisert i config.yml med indent=2
    with open(output_filename, "w", encoding="utf-8") as f:
        json.dump(overdue_sensors, f, indent=2)

    print(
        f"Sjekk fullført. Fant {len(overdue_sensors)} sensorer som krever ny kalibrering."
    )


if __name__ == "__main__":
    check_sensors()