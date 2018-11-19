Welcome to FDMS STAR's documentation!
=====================================


.. _overview:

:ref:`FDMS STAR - Overview <overview>`
--------------------------------------

FDMS STAR will be the new system used to perform the calculations necessary to produce the periodic economic forecasts in the European Commission. It's still in its early development phase. The system will read input data from a number of databases and from the forecasts produced by each country and perform the calculations / aggregations and produce the results.

|     The system will work with annual and quarterly data and transform the data in different ways. For now, we are only working with annual data and we are implementing the first part of the process, called "Country Calculation", in which we are processing the forecast data produced by each country and combining it with data coming from various databases to calculate the required data series.

The databases involved, besides the forecast data from each country, are:

- AMECO Historical db
- AMECO db
- Output Gap db
- XR-IR db
- Cyclical Adjustment db

For now, we are reading these data from excel files. There are helper functions in utils/interfaces.py to read all these files.

----------------------------

We are trying to maintain the same structure than the old system. In order to do this, we are creating a class for each of the steps and calculating the same group of variables.

All these classes inherit from:: :ref:`utils.mixins.StepMixin <stepmixin>`, and there are two more mixins that provide extra functionality.

:ref:`Development Environment <development_environment>`
-----------------------------------------------------------
1. :ref:`Development environment<development_environment>`
2. :ref:`Anaconda installation<anaconda>`
3. :ref:`PyCharm <pycharm>`
4. :ref:`Git <git>`

:ref:`Project setup <project_setup>`
------------------------------------


:ref:`Tutorial: adding new country calculations <tutorial1>`
----------------------------------------------

.. toctree::
   :maxdepth: 2
      abc <overview.rst>
