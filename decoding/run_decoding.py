from pathlib import Path



if __name__ in "__main__":
    path = Path(__file__).parent

    data_path = path / "data"
    outpath = path / "results"

    # create output directory if it doesn't exist
    if not outpath.exists():
        outpath.mkdir()
    
    subjects = ["0108", "0109", "0110", "0111", "0112", "0113", "0114", "0115"]
    

    