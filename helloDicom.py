import pydicom
from matplotlib import pyplot as plt
import numpy as np
from pathlib import Path

# github/lebedov/ct_win.py
def window_scale(data, wl, ww, dtype, out_range):
    """
    Scale pixel intensity data using specified window level, width, and intensity range.
    """
    data_new = np.empty(data.shape, dtype=np.double)
    data_new.fill(out_range[1] - 1)

    data_new[data <= (wl - ww / 2.0)] = out_range[0]
    data_new[(data > (wl - ww / 2.0)) & (data <= (wl + ww / 2.0))] = \
        ((data[(data > (wl - ww / 2.0)) & (data <= (wl + ww / 2.0))] - (wl - 0.5)) / (ww - 1.0) + 0.5) * (
                    out_range[1] - out_range[0]) + out_range[0]
    data_new[data > (wl + ww / 2.0)] = out_range[1] - 1
    return data_new.astype(dtype)


def ct_windowed(dcm_ds, wl, ww, dtype, out_range):
    """
    Scale CT image represented as a `pydicom.dataset.FileDataset` instance.
    """
    # Convert pixel data from Houndsfield units to intensity:
    intercept = int(dcm_ds.RescaleIntercept)
    slope = int(dcm_ds.RescaleSlope)
    data = slope * dcm_ds.pixel_array + intercept
    # Scale intensity:
    return window_scale(data, wl, ww, dtype, out_range)


# filename = Path('/Volumes/dataMac/測試用dcm/5B3F22C1')
filename = Path('/Volumes/dataMac/測試用dcm/IM-0008-0035.dcm')
ds = pydicom.dcmread(str(filename))
default_wl = float(ds.WindowCenter)
default_ww = float(ds.WindowWidth)
im = ct_windowed(ds, default_wl, default_ww, np.uint8, (0, 255))
plt.imshow(im, cmap='gray')
plt.show()

