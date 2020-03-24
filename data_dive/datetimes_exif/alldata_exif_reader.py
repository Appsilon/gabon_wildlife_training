import pandas as pd

alldata_raw = pd.read_csv("allDatOut.csv", names=["fullPath", "exif"])
alldata_raw.head()
alldata_raw.exif[0]
alldata_raw["exif_datetime"] = alldata_raw["exif"].str.extract("'EXIF DateTimeOriginal': \(.*\) ASCII=([\d\:]*\s[\d\:]*)\s", expand=True)
alldata_raw.head()
alldata_df = alldata_raw[["fullPath","exif_datetime"]]
alldata_df.head()
len(alldata_df)
alldata_df.to_csv("allDataDatetime.csv")

a=100010
list(alldata_df.exif_datetime[a:a+100])
