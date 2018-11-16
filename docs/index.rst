Welcome to FDMS STAR's documentation!
=====================================


.. _overview:

:ref:`FDMS STAR - Overview <overview>`
--------------------------------------

FDMS STAR will be the new system used to perform the calculations necessary to produce the periodic economic forecasts in the European Commission. It's still in its early development phase. The system will read input data from a number of databases and from the forecasts produced by each country and perform the calculations / aggregations and produce the results.

|     The system will work with annual and quarterly data and transform the data in different ways. For now, we are only working with annual data and we are implementing the first part of the process, called "Country Calculation", in which we are processing the forecast data produced by each country and combine it with data coming from various databases to calculate the required data series.

The databases involved, besides the forecast data from each country, are:

- AMECO Historical db
- AMECO db
- Output Gap db
- XR-IR db
- Cyclical Adjustment db

For now, we are reading these data from excel files. There are helper functions in utils/interfaces.py to read all these files.

----------------------------

We are trying to maintain the same structure than the old system. In order to do this, we are creating a class for each of the steps and calculate the same group of variables.

All these classes inherit from:: utils.mixins.StepMixin, and there are two more mixins that provide extra functionality.

`Project Setup <_overview>`_
----------------------------
`Project Setup <_overview>`_
`Project Setup <_overview>`_

:ref:`Adding new calculations <_country_calc>`
----------------------------------------------

`Overview <_overview>`_
-----------------------

.. toctree::
   :maxdepth: 2
      abc <overview.rst>
