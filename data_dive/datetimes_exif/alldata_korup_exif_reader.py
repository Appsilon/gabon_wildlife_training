import pandas as pd

korup_raw = pd.read_csv("ApsillonKorup.csv")#, names=["fullPath", "exif"])
korup_raw.head()
# alldata_raw.exif[0]
# alldata_raw["exif_datetime"] = alldata_raw["exif"].str.extract("'EXIF DateTimeOriginal': \(.*\) ASCII=([\d\:]*\s[\d\:]*)\s", expand=True)
# alldata_raw.head()
korup_raw["fullPath"] = korup_raw.uniqueName.apply(lambda x: "D:\\allData\\" + x)
korup_df = korup_raw[["fullPath","Date","Time"]]
korup_df.head()
len(korup_df)
korup_df.to_csv("allData_korup_Datetime.csv")

# a=100010
# list(korup_df.exif_datetime[a:a+100])
