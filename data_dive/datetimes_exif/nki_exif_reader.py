import pandas as pd

nki_raw = pd.read_csv("NkiOut.csv", names=["fullPath", "exif"])
nki_raw.head()
nki_raw.columns
eval(nki_raw.exif[0])
nki_raw.exif[0]
nki_raw["exif_datetime"] = nki_raw["exif"].str.extract("'EXIF DateTimeOriginal': \(.*\) ASCII=([\d\:]*\s[\d\:]*)\s", expand=True)
nki_raw.head()
nki_df = nki_raw[["fullPath","exif_datetime"]]
nki_df.head()
len(nki_df)
nki_df.to_csv("NkiDatetime.csv")
