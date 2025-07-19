import os
import re
import cv2
import argparse
import logging
import pandas as pd
from pathlib import Path
from dotenv import load_dotenv
from psycopg2 import connect
from psycopg2.extras import execute_values
from ultralytics import YOLO

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def detect_and_annotate_images(root_image_dir, annotated_output_dir, model):
    all_detections = []

    root_path = Path(root_image_dir)
    annotated_output_dir = Path(annotated_output_dir)
    annotated_output_dir.mkdir(parents=True, exist_ok=True)

    image_files = list(root_path.rglob("*.jpg")) + list(root_path.rglob("*.png"))
    logging.info(f"Found {len(image_files)} image(s) to process...")

    for image_path in image_files:
        try:
            img = cv2.imread(str(image_path))
            if img is None:
                logging.warning(f"Failed to load image: {image_path}")
                continue

            results = model.predict(source=str(image_path), save=False, conf=0.25)
            result = results[0]
            annotated_img = result.plot()

            output_path = annotated_output_dir / image_path.name
            cv2.imwrite(str(output_path), annotated_img)  # ⚠️ This will overwrite if exists

            df = result.to_df()
            df["image_name"] = image_path.name

            # Extract numeric message_id from filename
            matches = re.findall(r"\d+", image_path.stem)
            if matches:
                df["message_id"] = int(matches[0])
                all_detections.append(df)
            else:
                logging.warning(f"Skipping {image_path.name}: No numeric message_id found in filename.")

        except Exception as e:
            logging.error(f"Error processing {image_path.name}: {e}")

    if all_detections:
        detections_df = pd.concat(all_detections, ignore_index=True)
        logging.info(f"Detection complete. Total rows: {len(detections_df)}")
        return detections_df
    else:
        logging.warning("No valid detections.")
        return pd.DataFrame()

def push_to_postgres(df, table_name, db_params):
    if df.empty:
        logging.warning("DataFrame is empty. Nothing to insert.")
        return

    try:
        with connect(**db_params) as conn:
            with conn.cursor() as cur:
                insert_query = f"""
                    INSERT INTO {table_name} (message_id, detected_object_class, confidence_score)
                    VALUES %s
                """
                values = [
                    (
                        int(row["message_id"]),
                        row["name"],
                        row["confidence"]
                    )
                    for _, row in df.iterrows()
                ]
                logging.info(f"Inserting {len(values)} rows into {table_name}")
                execute_values(cur, insert_query, values)
                conn.commit()
    except Exception as e:
        logging.error(f"PostgreSQL insertion failed: {e}")

def main():
    parser = argparse.ArgumentParser(description="YOLOv8 image detection + PostgreSQL ingestion")
    parser.add_argument("--images_folder", type=str, default="data/raw/media/2025-07-09", help="Input image folder")
    parser.add_argument("--annotated_output", type=str, default="object_detection/annotated", help="Where to save annotated images")
    parser.add_argument("--env_file", type=str, default=".env", help="Path to .env file")
    parser.add_argument("--table_name", type=str, default="analytics.fct_image_detections", help="Full PostgreSQL table name")

    args = parser.parse_args()

    # Load DB credentials
    load_dotenv(args.env_file)
    db_params = {
        "host": os.getenv("PGHOST"),
        "port": os.getenv("PGPORT"),
        "dbname": os.getenv("PGDATABASE"),
        "user": os.getenv("PGUSER"),
        "password": os.getenv("PGPASSWORD"),
    }

    # Load model
    model = YOLO("yolov8n.pt")
    logging.info("YOLOv8 model loaded.")

    # Detect and annotate
    df = detect_and_annotate_images(args.images_folder, args.annotated_output, model)

    # Save to CSV for debugging
    if not df.empty:
        logging.info("Sample detections:\n%s", df.head())
        df.to_csv("debug_detection_output.csv", index=False)
        push_to_postgres(df, args.table_name, db_params)
    else:
        logging.warning("No detections to insert.")

if __name__ == "__main__":
    main()
