from collections.abc import Sequence
from itertools import pairwise
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
import numpy as np 
from netCDF4 import Dataset
import xarray as xr
import argparse
import traceback

def standardize(da: xr.Dataset | xr.DataArray, minlon, maxlon, minlat, maxlat) -> xr.Dataset | xr.DataArray:
    da = da.squeeze()
    if "ULONG" in da.coords:
        from xarray.groupers import BinGrouper
        da = da.reset_coords("z_t", drop=True)
        lat_bins = np.arange(minlat, maxlat + 1, 1)
        lat_centers = (lat_bins[1:] + lat_bins[:-1]) / 2
        lon_bins = np.arange(minlon, maxlon + 1, 1)
        lon_centers = (lon_bins[1:] + lon_bins[:-1]) / 2
        from xarray.groupers import BinGrouper
        da = da.groupby(ULONG=BinGrouper(lon_bins, labels=lon_centers), ULAT=BinGrouper(lat_bins, labels=lat_centers)).mean().rename({"ULONG_bins": "lon", "ULAT_bins": "lat"})
        da = da.assign_coords(lon=(((da.lon + 180) % 360) - 180))
        da = da.sortby("lon")
    elif (da.lon.max() > 180) and (da.lon.min() >= 0): # we prefer longitude to go from -180 to +180 rather than 0 to 360
        da = da.assign_coords(lon=(((da.lon + 180) % 360) - 180))
        da = da.sortby("lon")
    if "lat" in da.coords and np.diff(da.lat.values)[0] < 0: # and increasing latitudes
        da = da.reindex(lat=da.lat[::-1])
    return (
        da
        .sel(lon=slice(minlon, maxlon))
        .sel(lat=slice(minlat, maxlat))
    )

# modify from here
varname = ""
frequency = ""
token = ""
component = "" # for land variables like RAIN, "atm" for atmospheric variables like wind, and "ocn" for ocean variables
forcing_variant = "cmip6" # other option is "smbb", which stands for "SMoothed Biomass Burning"
out_path = Path("")
minlon, maxlon, minlat, maxlat = -175, -165, -15, -5
levels = None
# yearbounds need to be multiples of 10 years, starting from 1850 for past, and 2015 for future
yearbounds = {
    "past": [1990, 2010],
    "future": [2085, 2095],
}
n_members = 10
# to here

n_workers = 4
experiment_dict = {
    "past": f"BHIST{forcing_variant}",
    "future": f"BSSP370{forcing_variant}",
}

all_yearbounds = {
    "past": np.arange(1850, 2021, 10),
    "future": np.arange(2015, 2106, 10)
}
for key, val in all_yearbounds.items():
    all_yearbounds[key][-1] = val[-1] - 5
if component != "ocn":
    all_timebounds = {key: [f"{year1}0101-{year2 - 1}1231" for year1, year2 in pairwise(val)] for key, val in all_yearbounds.items()}
else:
    def beg(year, frequency):
        if frequency == "month_1":
            return f"{year}01"
        elif frequency == "day_1":
            return f"{year}0101" if year in (1850, 2015) else f"{year}0102"
    def end_(year, frequency):
        if frequency == "month_1":
            return f"{year - 1}12"
        if year == 2015:
            return f"{year - 1}1231"
        elif year == 2100:
            return f"{year}1231"
        return f"{year}0101"
    all_timebounds = {key: [f"{beg(year1, frequency)}-{end_(year2, frequency)}" for year1, year2 in pairwise(val)] for key, val in all_yearbounds.items()}
    
timebounds = {key: np.asarray(val)[(yearbounds[key][0] <= all_yearbounds[key][:-1]) & (yearbounds[key][1] >= all_yearbounds[key][:-1])] for key, val in all_timebounds.items()}

members = [f"{year}.{str(number).zfill(3)}" for year, number in zip(range(1001, 1201, 20), range(1, 11))]
for startyear in [1231, 1251, 1281, 1301]:
    members.extend(f"{startyear}.{str(number).zfill(3)}" for number in range(1, 11))
members = members[:n_members]

def get_url(varname: str, period: str, member: str, timebounds: str):
    experiment = experiment_dict[period]
    # 6 for 3D variables, 1 for 2D. Expand this list at will
    h = 6 if varname in ["U", "V", "T", "Z"] else 1 # anything that has several pressure levels
    h = ".nday1" if (component == "ocn" and frequency == "day_1") else h # weird rules for ocean
    h = "" if (component == "ocn" and frequency == "month_1") else h
    pop_or_cam = "cam" if component == "atm" else "pop" # weird rules for ocean

    return fr"https://tds.ucar.edu/thredds/fileServer/datazone/campaign/cgd/cesm/CESM2-LE/{component}/proc/tseries/{frequency}/{varname}/b.e21.{experiment}.f09_g17.LE2-{member}.{pop_or_cam}.h{h}.{varname}.{timebounds}.nc?api-token={token}#mode=bytes"


def downloader(period: str, member: str, timebounds: str, odir: Path | str):
    global varname
    opath = Path(odir).joinpath(f"{member}-{timebounds}.nc")
    if opath.is_file():
        return f"{member}, {timebounds} already existed"
    ds = xr.open_dataset(
        get_url(varname, period, member, timebounds), engine="h5netcdf"
    )[varname]
    if component == "ocn":
        "Error probably here, you need to regrid to a regular lon-lat grid using xesmf"
    ds = standardize(ds, (180 + minlon) % 360, (180 + maxlon) % 360, minlat, maxlat).chunk("auto")
    ds = ds.load()
    ds = ds.astype(np.float32)
    ds = ds.to_netcdf(opath)
    return f"Retrieved {member}, {timebounds}"


def main():
    out_path.mkdir(exist_ok=True)

    with ThreadPoolExecutor(max_workers=n_workers) as executor:
        futures = [
            executor.submit(downloader, period, member, timebounds_, out_path)
            for period in ["past", "future"]
            for member in members
            for timebounds_ in timebounds[period]
        ]
        for f in as_completed(futures):
            try:
                print(f.result())
            except Exception as e:
                print(traceback.format_exc())
                print("could not retrieve")


if __name__ == "__main__":
    main()
