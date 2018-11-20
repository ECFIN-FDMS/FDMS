.. _tutorial1:

Tutorial 1: Adding new country calculations
=============================================

We are using TDD, and currently we are focused on implementing all the country calculations for annual data. We are using tests/test_country_calculation.py for development and testing.
Adding a new step consists on writing the new class and call it from tests/country_calculation.py with the correct set of input dataframes.
In order to add more calculations and maintain the same structure it is convenient to follow these steps:

1. Read the source algorithm and determine what input variables we need and what output variables we need to calculate.
2. Check where the input data comes from (source data from the country, source databases -ameco_h, output_gap, etc.- or data calculated in previous steps or in this one.
   Prepare the necessary input dataframes. In order to easily identify what variables we get in each step, we export .txt and .xls files with the results at the end.
3. Create the class to perform the calculations, and call it from tests/test_country_calculation.py

For this tutorial we will create a new step Household Sector. This is our source algorithm, if the formulas are too long they can be open with a double-click.

.. image:: img/tutorial1.PNG

1. Determine inputs and outputs
    The lines with the word "Source" can be ignored, i.e. :code:`{Country}|UYOH.1.0.0.0.Source[t]`.
    In this case, it's easy to determine the input and the outputs (if there are too many you can use a script):

        Household Sector

            1. {Country}|UYOH.1.0.0.0[t] = buttsplice(AMECO Historical!{Country}|UYOH.1.0.0.0[t], ignoremissingsum({Country}|UOGH.1.0.0.0[t], {Country}|UYNH.1.0.0.0[t]), MsSpliceDirection.Forward)
            2. {Country}|UYOH.1.0.0.0.Source[t] = merge({Country}|UOGH.1.0.0.0.Source[t], {Country}|UYNH.1.0.0.0.Source[t]), (Now-5)-(Now+5)
            3. {Country}|UVGH.1.0.0.0[t] = buttsplice(AMECO Historical!{Country}|UVGH.1.0.0.0[t], ignoremissingsum({Country}|UWCH.1.0.0.0[t], {Country}|UYOH.1.0.0.0[t], {Country}|UCTRH.1.0.0.0[t], -{Country}|UTYH.1.0.0.0[t], -{Country}|UCTPH.1.0.0.0[t]), MsSpliceDirecti
            4. {Country}|UVGHA.1.0.0.0[t] = buttsplice({Country}|UVGHA.1.0.0.0[t], ignoremissingsum({Country}|UVGH.1.0.0.0[t], {Country}|UEHH.1.0.0.0[t]), MsSpliceDirection.Forward)
            5. {Country}|OVGHA.3.0.0.0[t] = rebase({Country}|UVGHA.1.0.0.0[t] / {Country}|PCPH.3.1.0.0[t], {BasePeriod}) / 100 * {Country}|UVGHA.1.0.0.0[{BasePeriod}]
            6. {Country}|USGH.1.0.0.0[t] = buttsplice(AMECO Historical!{Country}|USGH.1.0.0.0[t], ignoremissingsum({Country}|UWCH.1.0.0.0[t], {Country}|UOGH.1.0.0.0[t], {Country}|UYNH.1.0.0.0[t], {Country}|UCTRH.1.0.0.0[t], -{Country}|UTYH.1.0.0.0[t], -{Country}|UCTPH.1
            7. {Country}|ASGH.1.0.0.0[t] = buttsplice(AMECO Historical!{Country}|ASGH.1.0.0.0[t], {Country}|USGH.1.0.0.0[t] / {Country}|UVGHA.1.0.0.0[t] * 100, MsSpliceDirection.Forward)
            8. {Country}|UBLH.1.0.0.0[t] = buttsplice(AMECO Historical!{Country}|UBLH.1.0.0.0[t], ignoremissingsubtract({Country}|USGH.1.0.0.0[t], {Country}|UITH.1.0.0.0[t], {Country}|UKOH.1.0.0.0[t]), MsSpliceDirection.Forward)

    **Inputs**:
        UYOH.1.0.0.0, UOGH.1.0.0.0, UYNH.1.0.0.0, UVGH.1.0.0.0, UWCH.1.0.0.0, UCTRH.1.0.0.0, UTYH.1.0.0.0, UCTPH.1.0.0.0, UVGHA.1.0.0.0, UEHH.1.0.0.0, PCPH.3.1.0.0, USGH.1.0.0.0, ASGH.1.0.0.0, UBLH.1.0.0.0, UITH.1.0.0.0, UKOH.1.0.0.0

    **Outputs**:
        UYOH.1.0.0.0, UVGH.1.0.0.0, UVGHA.1.0.0.0, OVGHA.3.0.0.0, USGH.1.0.0.0, ASGH.1.0.0.0, UBLH.1.0.0.0

2. Check where the input data come from and prepare the necessary input dataframes.
    We need to find out where the input data comes from. Possible sources:

    - Input databases (ameco_h, ameco_db, output_gap...). If it comes from one of these, it will be specified in the formula (i.e. **AMECO Historical!** {Country}|UYOH.1.0.0.0[t]).
    - Value calculated in previous steps. (We have to search in the output/ directory, if it has been calculated previously, it should be in at least one of those files. We should take the last series in case it has been recalculated more than once).
      We can use a tool like grep or ack.
    - Value calculated previously in this same step. In this case we would get the data from self.result.
    - Input from the country forecast. If it has not been calculated in previous steps, it can be in the source data provided by the country.

    In this case we can see that some of the variables are calculated in this same step, other variables are calculated in step1 (we will get those data from CountryCalculation().result_1), and we will also need the ameco_h database

    .. code-block:: console

        $ for item in UYOH.1.0.0.0 UOGH.1.0.0.0 UYNH.1.0.0.0 UVGH.1.0.0.0 UWCH.1.0.0.0 \
        UCTRH.1.0.0.0 UTYH.1.0.0.0 UCTPH.1.0.0.0 UVGHA.1.0.0.0 UEHH.1.0.0.0 \
        PCPH.3.1.0.0 USGH.1.0.0.0 ASGH.1.0.0.0 UBLH.1.0.0.0 UITH.1.0.0.0 UKOH.1.0.0.0;
        do ack $item output/;
        done
        output/outputall.txt
        113:UOGH.1.0.0.0

        **output/outputvars1.txt**
        116:UOGH.1.0.0.0
        output/outputall.txt
        209:UYNH.1.0.0.0

        output/outputvars1.txt
        214:UYNH.1.0.0.0
        output/outputall.txt
        191:UWCH.1.0.0.0

        output/outputvars1.txt
        196:UWCH.1.0.0.0
        output/outputall.txt
        62:UCTRH.1.0.0.0

        output/outputvars1.txt
        62:UCTRH.1.0.0.0
        output/outputall.txt
        177:UTYH.1.0.0.0

        output/outputvars1.txt
        180:UTYH.1.0.0.0
        output/outputall.txt
        58:UCTPH.1.0.0.0

        output/outputvars1.txt
        58:UCTPH.1.0.0.0
        output/outputall.txt
        75:UEHH.1.0.0.0

        output/outputvars1.txt
        76:UEHH.1.0.0.0
        output/outputall.txt
        388:PCPH.3.1.0.0

        **output/outputvars7.txt**
        3:PCPH.3.1.0.0
        output/outputall.txt
        94:UITH.1.0.0.0

        output/outputvars1.txt
        96:UITH.1.0.0.0
        output/outputall.txt
        102:UKOH.1.0.0.0

        output/outputvars1.txt
        104:UKOH.1.0.0.0

3. Therefore, the parameters needed for this step are result_1, result_7 and ameco_h.
    In this step we observe that all lines except numbers 5 and 7 are combining butt_splice and ignoremissingsum / ignoremissingsubtract.
    Since this type of calculation appears multiple times, we have a mixin to simplify those called :ref:`fdms.utils.mixins.SumAndSpliceMixin<stepmixin>`.

    We will create the file computation/country/annual/household_sector.py and call the method :meth:`perform_computation` of the corresponding class in tests/country_calculation.py.


    .. code-block:: python

        # tests/test_country_calculation.py
        ...
        from fdms.computation.country.annual.household_sector import HouseholdSector
        ...

        # STEP 14
        step_14 = HouseholdSector(scales=self.scales)
        result_14 = step_14.perform_computation(self.result_1, result_7, self.ameco_df)
        variables = ['UYOH.1.0.0.0', 'UOGH.1.0.0.0', 'UYNH.1.0.0.0', 'UVGH.1.0.0.0', 'UWCH.1.0.0.0', 'UCTRH.1.0.0.0',
                     'UTYH.1.0.0.0', 'UCTPH.1.0.0.0', 'UVGHA.1.0.0.0', 'UEHH.1.0.0.0', 'PCPH.3.1.0.0', 'USGH.1.0.0.0',
                     'ASGH.1.0.0.0', 'UBLH.1.0.0.0', 'UITH.1.0.0.0', 'UKOH.1.0.0.0']
        missing_vars = [v for v in variables if v not in list(result_14.loc[self.country].index)]
        self.assertFalse(missing_vars)


    For now, we will create computation/country/annual/household_sector.py the following contents:

    .. code-block:: python

        # computation/country/annual/household_sector.py
        import pandas as pd

        from fdms.utils.mixins import SumAndSpliceMixin
        from fdms.utils.splicer import Splicer
        from fdms.utils.operators import Operators
        from fdms.utils.series import export_to_excel


        # STEP 14
        class HouseholdSector(SumAndSpliceMixin):
            def perform_computation(self, df, ameco_h_df):
                splicer = Splicer()
                operators = Operators()
                import pdb;pdb.set_trace()

    This will cause the test to stop at this point and display the Python prompt. We can then check that we have all the data in the interactive session and test our calculations.

    .. note::
        First will use the _sum_and_splice method from SumAndSpliceMixin to calculate
        UYOH.1.0.0.0, UVGH.1.0.0.0, UVGHA.1.0.0.0, USGH.1.0.0.0 and UBLH.1.0.0.0
        and then we will calculate ASGH.1.0.0.0 and OVGHA.3.0.0.0, because we need UVGHA.1.0.0.0 and USGH.1.0.0.0 for these two

        SumAndSpliceMixin has a method that allows you to pass it a dictionary {variable_key: series_list, other_variable: other_list...} and it performs the operation:

        - variable_key_series = buttsplice(variable_key_ameco_h_series, ignoremissingsum(series_list))

        So, it takes a variable and extends the same series taken from ameco_h with the sum of the list of series for the corresponding key, taking into account the sign.

        In this case we cannot calculate them all in one go, because for each one we need the result of the previous one, so we have to do it one by one.

    The first formula would be:

    - {Country}|UYOH.1.0.0.0[t] = buttsplice(AMECO Historical!{Country}|UYOH.1.0.0.0[t], ignoremissingsum({Country}|UOGH.1.0.0.0[t], {Country}|UYNH.1.0.0.0[t]), MsSpliceDirection.Forward)

    So, the variable to calculate (and the variable to read from ameco_h) is UYOH.1.0.0.0.

    The variables needed to extend the series from ameco_h are: :code:`"UOGH.1.0.0.0"` and :code:`"UYNH.1.0.0.0"`.

    .. code-block:: console

        bamarco@D02DI1536268ECF MINGW64 /c/marcos/w/fdms (FDMSSTAR-60__sphinx_docs_1)
        $ ack UOGH.1.0.0.0 output/
        output/outputvars1.txt
        116:UOGH.1.0.0.0

        bamarco@D02DI1536268ECF MINGW64 /c/marcos/w/fdms (FDMSSTAR-60__sphinx_docs_1)
        $ ack UYNH.1.0.0.0 output/
        output/outputvars1.txt
        214:UYNH.1.0.0.0


    The dictionary to pass would be: :code:`addends = {'UYOH.1.0.0.0': ['UOGH.1.0.0.0', 'UYNH.1.0.0.0']}`

    We can see by searching those strings in the output/ directory that those series have been calculated in step1. Let's use the interactive interpreter to make sure we have the correct data.

    We run the tests and check that we have all the input data we need to calculate the new series:

    .. code-block:: console

        $ pytest fdms -s
        (venvs) C:\marcos\w\FDMS>pytest --cov fdms -s
        ========================= test session starts ================================
        platform win32 -- Python 3.6.5, pytest-3.9.2, py-1.7.0, pluggy-0.8.0
        rootdir: C:\marcos\w\FDMS, inifile:
        plugins: profiling-1.3.0, cov-2.6.0
        collected 2 items

        fdms\tests\test_country_calculations.py Python 3.6.5 |Anaconda, Inc.| (default, Mar 29 2018, 13:32:41) [MSC v.1900 64 bit (AMD64)] on win32
        Type "help", "copyright", "credits" or "license" for more information.
        (InteractiveConsole)
        >>> self.get_data(result_1, 'UOGH.1.0.0.0')
        1993    3.127220e+10
        1994    3.279720e+10
        1995    3.224370e+10
        1996    3.292340e+10
        1997    3.424580e+10
        1998    3.533020e+10
        1999    3.604350e+10
        2000    3.792600e+10
        2001    3.889480e+10
        2002    3.830680e+10
        2003    3.894230e+10
        2004    3.956500e+10
        2005    4.138640e+10
        2006    4.373910e+10
        2007    4.570000e+10
        2008    4.681970e+10
        2009    4.527670e+10
        2010    4.591670e+10
        2011    4.682300e+10
        2012    4.741440e+10
        2013    4.734450e+10
        2014    4.891970e+10
        2015    4.965520e+10
        2016    5.011410e+10
        2017    5.154680e+10
        2018    3.778680e+09
        2019    3.778680e+09
        Name: (BE, UOGH.1.0.0.0), dtype: float64
        >>> self.get_data(result_1, 'UYNH.1.0.0.0')
        1993    2.076710e+10
        1994    2.148770e+10
        1995    2.821620e+10
        1996    2.642520e+10
        1997    2.623920e+10
        1998    2.775890e+10
        1999    2.640220e+10
        2000    2.926940e+10
        2001    3.032300e+10
        2002    2.796950e+10
        2003    2.671820e+10
        2004    2.702540e+10
        2005    2.736450e+10
        2006    2.833880e+10
        2007    3.026600e+10
        2008    3.397260e+10
        2009    3.263500e+10
        2010    3.286720e+10
        2011    3.084590e+10
        2012    2.916880e+10
        2013    2.922730e+10
        2014    2.774440e+10
        2015    2.705550e+10
        2016    2.625330e+10
        2017    2.764950e+10
        2018    5.390221e+09
        2019    5.747389e+09
        Name: (BE, UYNH.1.0.0.0), dtype: float64
        >>>

    Great!, we have all the data we need. To check that the data we have is correct, we can check the file sample_data/BE_expected_scale.xlsx. The data in this case is correct. If it were not, that would mean that there's an error in a previous calculation that needs to be fixed.

    We will edit computation/country/annual/household_sector.py and add the following contents:

    .. code-block:: python
        :emphasize-lines: 15,16

        # computation/country/annual/household_sector.py
        import pandas as pd

        from fdms.utils.mixins import SumAndSpliceMixin
        from fdms.utils.splicer import Splicer
        from fdms.utils.operators import Operators
        from fdms.utils.series import export_to_excel


        # STEP 14
        class HouseholdSector(SumAndSpliceMixin):
            def perform_computation(self, result_1, result_7, ameco_h_df):
                splicer = Splicer()
                operators = Operators()
                addends = {'UYOH.1.0.0.0': ['UOGH.1.0.0.0', 'UYNH.1.0.0.0']}
                self._sum_and_splice(addends, result_1, ameco_h_df, splice=False)
                import pdb;pdb.set_trace()

    This will cause the test to stop at this point and display the Python prompt. We can then check that we have all the data in the interactive session and test our calculations.

    .. code-block:: bash

        >>> (venvs) C:\marcos\w\FDMS>pytest --cov fdms -s
        ========================= test session starts ================================
        platform win32 -- Python 3.6.5, pytest-3.9.2, py-1.7.0, pluggy-0.8.0
        rootdir: C:\marcos\w\FDMS, inifile:
        plugins: profiling-1.3.0, cov-2.6.0
        collected 2 items

        fdms\tests\test_country_calculations.py Python 3.6.5 |Anaconda, Inc.| (default, Mar 29 2018, 13:32:41) [MSC v.1900 64 bit (AMD64)] on win32
        Type "help", "copyright", "credits" or "license" for more information.
        (InteractiveConsole)
        >>> self.result
          Country Ameco Variable Code Frequency  Scale          1993          1994          1995          1996          1997      ...               2011          2012          2013          2014          2015          2016          2017          2018          2019
        0            BE  UYOH.1.0.0.0    Annual  Units  5.203930e+10  5.428490e+10  6.045990e+10  5.934860e+10  6.048500e+10      ...       7.766890e+10  7.658320e+10  7.657180e+10  7.666410e+10  7.671070e+10  7.636740e+10  7.919630e+10  9.168901e+09  9.526069e+09

        [1 rows x 31 columns]
        >>>

    We have our first series. Now, because we will need this new series to calculate the next one, we will create a new dataframe concatenating this one and result_1, so that the dataframe we pass to _sum_and_splice has all the necessary data.

    As explained in :ref:`Overview of dataframe structures used<data_structures>`, the current result where we are adding the new data hasn't got a MultiIndex (it's the only one), so we'll create a copy with a MultiIndex to be able to concatenate it with result_1

    .. code-block:: python
        :emphasize-lines: 17-37

        # computation/country/annual/household_sector.py
        import pandas as pd

        from fdms.utils.mixins import SumAndSpliceMixin
        from fdms.utils.splicer import Splicer
        from fdms.utils.operators import Operators
        from fdms.utils.series import export_to_excel


        # STEP 14
        class HouseholdSector(SumAndSpliceMixin):
            def perform_computation(self, result_1, result_7, ameco_h_df):
                splicer = Splicer()
                operators = Operators()
                addends = {'UYOH.1.0.0.0': ['UOGH.1.0.0.0', 'UYNH.1.0.0.0']}
                self._sum_and_splice(addends, result_1, ameco_h_df, splice=False)

                new_input_df = self.result.set_index(['Country Ameco', 'Variable Code'], drop=True)
                new_input_df = pd.concat([new_input_df, result_1], sort=True)
                addends = {'UVGH.1.0.0.0': ['UWCH.1.0.0.0', 'UYOH.1.0.0.0', 'UCTRH.1.0.0.0', '-UTYH.1.0.0.0', '-UCTPH.1.0.0.0']}
                self._sum_and_splice(addends, new_input_df, ameco_h_df, splice=False)

                new_input_df = self.result.set_index(['Country Ameco', 'Variable Code'], drop=True)
                new_input_df = pd.concat([new_input_df, result_1], sort=True)
                addends = {'UVGHA.1.0.0.0': ['UVGH.1.0.0.0', 'UEHH.1.0.0.0']}
                self._sum_and_splice(addends, new_input_df, ameco_h_df, splice=False)

                addends = {'USGH.1.0.0.0': ['UWCH.1.0.0.0', 'UOGH.1.0.0.0', 'UYNH.1.0.0.0', 'UCTRH.1.0.0.0', '-UTYH.1.0.0.0', '-UCTPH.1.0.0.0', 'UEHH.1.0.0.0', '-UCPH0.1.0.0.0']}
                self._sum_and_splice(addends, new_input_df, ameco_h_df, splice=False)

                # Since this formula is using *ignoremissingsubtract* instead of *ignoremissingsum*,
                # we change the sign of all but the first variables in the list
                new_input_df = self.result.set_index(['Country Ameco', 'Variable Code'], drop=True)
                new_input_df = pd.concat([new_input_df, result_1], sort=True)
                addends = {'UBLH.1.0.0.0': ['USGH.1.0.0.0', '-UITH.1.0.0.0', '-UKOH.1.0.0.0']}
                self._sum_and_splice(addends, new_input_df, ameco_h_df, splice=False)

                import pdb;pdb.set_trace()

    And we can check that the new series are being calculated:

    .. code-block:: bash

        (venvs) C:\marcos\w\FDMS>pytest --cov fdms -s
        ========================================================================================================================== test session starts ===========================================================================================================================
        platform win32 -- Python 3.6.5, pytest-3.9.2, py-1.7.0, pluggy-0.8.0
        rootdir: C:\marcos\w\FDMS, inifile:
        plugins: profiling-1.3.0, cov-2.6.0
        collected 2 items

        fdms\tests\test_country_calculations.py Python 3.6.5 |Anaconda, Inc.| (default, Mar 29 2018, 13:32:41) [MSC v.1900 64 bit (AMD64)] on win32
        Type "help", "copyright", "credits" or "license" for more information.
        (InteractiveConsole)
        >>> self.result
          Country Ameco Variable Code Frequency  Scale          1993          1994          1995          1996          1997      ...               2011          2012          2013          2014          2015          2016          2017          2018          2019
        0            BE  UYOH.1.0.0.0    Annual  Units  5.203930e+10  5.428490e+10  6.045990e+10  5.934860e+10  6.048500e+10      ...       7.766890e+10  7.658320e+10  7.657180e+10  7.666410e+10  7.671070e+10  7.636740e+10  7.919630e+10  9.168901e+09  9.526069e+09
        1            BE  UVGH.1.0.0.0    Annual  Units  1.279338e+11  1.324030e+11  1.396412e+11  1.402694e+11  1.435605e+11      ...       2.238218e+11  2.281629e+11  2.307986e+11  2.333724e+11  2.355313e+11  2.410091e+11  2.496097e+11  2.780952e+10  2.926091e+10

        [2 rows x 31 columns]
        >>>

    Now, we will calculate OVGHA.3.0.0.0 and ASGH.1.0.0.0. These are the formulas:

    - {Country}|OVGHA.3.0.0.0[t] = rebase({Country}|UVGHA.1.0.0.0[t] / {Country}|PCPH.3.1.0.0[t], {BasePeriod}) / 100 * {Country}|UVGHA.1.0.0.0[{BasePeriod}]
    - {Country}|ASGH.1.0.0.0[t] = buttsplice(AMECO Historical!{Country}|ASGH.1.0.0.0[t], {Country}|USGH.1.0.0.0[t] / {Country}|UVGHA.1.0.0.0[t] * 100, MsSpliceDirection.Forward)


