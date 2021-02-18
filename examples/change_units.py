"""
=====================================
Example for changing units in dataset
=====================================

This is an example of how to change
units in the xarray dataset.

"""

import act
import numpy as np

def print_summary(obj, variables):
    for var_name in variables:
        print(f"{var_name}: mean={np.nanmean(obj[var_name].values)} "
              f"units={obj[var_name].attrs['units']}")
    print()

variables = ['first_cbh', 'second_cbh', 'alt']

# Read in some example data
obj = act.io.armfiles.read_netcdf(act.tests.sample_files.EXAMPLE_CEIL1)

#Print the variable name, mean of values and units
print('Variables in read data')
print_summary(obj, variables)

# Change units of one varible from m to km
obj.utils.change_units(variables='first_cbh', desired_unit='km')
print('Variables with one changed to km')
print_summary(obj, variables)

# Change units of more than one varible from to km
obj.utils.change_units(variables=variables, desired_unit='km')
print('Variables with both changed to km')
print_summary(obj, variables)

# Can change all data variables in the dataset that are units of length by not providing
# a list of variables. Here we are changing back to orginal meters.
# Also, because it needs to loop over all variables and try to convert, will take
# longer if we keep the QC variables. Faseter if we exclude them.
# The method will return a dataset. In this case the dataset returned is the same
# dataset.
skip_variables = [ii for ii in obj.data_vars if ii.startswith('qc_')]
new_obj = obj.utils.change_units(variables=None, desired_unit='m', skip_variables=skip_variables)
print('Variables changed back to m by looping over all variables in dataset')
print('Orginal dataset is same as retured dataset:', obj is new_obj)
print_summary(new_obj, variables)

# For coordinate variables need to explicitly give coordinage variable name and use
# the returned dataset. The xarray method used to change values on coordinate
# values requries returning a new updated dataet.
var_name = 'range'
variables.append(var_name)
new_obj = obj.utils.change_units(variables=variables, desired_unit='km')
print('Variables and coordinate variable values changed to km')
print('Orginal dataset is same as retured dataset:', obj is new_obj)
print_summary(new_obj, variables)
