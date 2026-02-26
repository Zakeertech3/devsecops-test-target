import os
from pathlib import Path
from datasets import load_dataset
from dotenv import load_dotenv

def main():
    load_dotenv()
    
    
    dataset_name = os.getenv("HF_DATASET_PATH", "hao-li/AIDev")
    
    print(f"Downloading dataset: {dataset_name}...")
    
    try:
        
        dataset = load_dataset(dataset_name, split="train")
        
        
        print("Selecting 5,000 records for the test dataset...")
        subset = dataset.select(range(5000))
        
        
        output_dir = Path("./data")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        
        output_file = output_dir / "all_pull_request.parquet"
        print(f"Saving dataset to {output_file}...")
        
        df = subset.to_pandas()
        df.to_parquet(output_file, index=False)
        
        print("Download and save complete! Your data is ready for Elastic.")
        
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()