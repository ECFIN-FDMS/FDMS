.. _tutorial3:

Tutorial 3: Extend input variables for RATS backward to 1960
============================================================

In this tutorial we will add the calculations to extend input variables for RATS backward to 1960.
Please check out `Tutorial 1<tutorial1>` and `Tutorial 2<tutorial2>`, we will follow the same steps:

1. Read the source algorithm and determine what input variables we need and what output variables we need to calculate.
2. Check where the input data comes from (source data from the country, source databases -ameco_h, output_gap, etc.- or data calculated in previous steps or in this one) and
   Prepare the necessary input dataframes. In order to easily identify what variables we get in each step, we export .txt and .xls files with the results at the end.
3. Create the class to perform the calculations, and call it from tests/test_country_calculation.py


**1. Determine inputs and outputs**

  This is our source algorithm (we have removed the unnecessary lines, which are about metadata, not calculations):

    ``Group: Variable in RATS Input variables, to be extended backward to 1960``

        ``If Variable <> 'OIGT.1.1.0.0', 'OVGD.1.1.0.0', 'OVGD.6.1.0.0'``
            ``Then``
                ``If NOT IsEmpty({Country}|{Variable}[t])``
                    ``Then``
                        ``{Country}|{Variable}[t] = ratiosplice({Country}|{Variable}[t], AMECO!{Country}|{Variable}[t], MsSpliceDirection.Backward)``

                    ``Else``

            ``Else``

            ``{Country}|OVGD.6.0.0.0[t] = pch({Country}|OVGD.1.0.0.0[t])``

    ``Group: Variable = 'OIGT.1.0.0.0', 'OVGD.1.0.0.0'``

    ``If NOT IsEmpty({Country}|{Variable}[t])``
        ``Then``
            ``{Country}|{Variable}[t] = ratiosplice({Country}|{Variable}[t], AMECO!{Country}|{Variable}[t], MsSpliceDirection.Backward)``

        ``Else``

    ``// exception for ME: when the base year was 2005, there was not enough historical data for ME therefore exceptional calculations were put in place for that country replacing the two groups above with the following branch``

    ``If Country <> 'ME'``
        ``Then``
            ``Group: Variable in RATS Input variables, to be extended backward to 1960``
                ``If Variable <> 'OIGT.1.1.0.0', 'OVGD.1.1.0.0', 'OVGD.6.1.0.0'``
                    ``Then``
                        ``If NOT IsEmpty({Country}|{Variable}[t])``
                            ``Then``
                                ``{Country}|{Variable}[t] = ratiosplice({Country}|{Variable}[t], AMECO!{Country}|{Variable}[t], MsSpliceDirection.Backward)``

                            ``Else``

                    ``Else``

                ``{Country}|OVGD.6.0.0.0[t] = pch({Country}|OVGD.1.0.0.0[t])``

            ``Group: Variable = 'OIGT.1.0.0.0', 'OVGD.1.0.0.0'``
                ``If NOT IsEmpty({Country}|{Variable}[t])``
                    ``Then``
                        ``{Country}|{Variable}[t] = ratiosplice({Country}|{Variable}[t], AMECO!{Country}|{Variable}[t], MsSpliceDirection.Backward)``

                    ``Else``

            ``{Country}|OVGD.6.0.0.0[t] = pch({Country}|OVGD.1.0.0.0[t])``

        ``Else``

  .. note::
        The last part of the algorithm is commented out, we do not need to consider the exception for ME anymore, we only care about the first part, until the comment:

        ``// exception for ME: when the base year was 2005, there was not enough historical data for ME therefore exceptional calculations were put in place for that country replacing the two groups above with the following branch``.


  **Inputs**:
    The input variables are those in the corresponding variable group (``Group: Variable in RATS Input variables, to be extended backward to 1960``) and ``Group: Variable = 'OIGT.1.0.0.0', 'OVGD.1.0.0.0'``. we can check the variable groups in the source file ``fdms/config/variable_groups.py`` or in the python shell:

    >>> from fdms.config.variable_groups import *
    >>> RI_TBEBT1960
    ['NPTD.1.0.0.0', 'NPAN.1.0.0.0', 'NPAN1.1.0.0.0', 'NLTN.1.0.0.0', 'NLCN.1.0.0.0', 'NECN.1.0.0.0',
    'NUTN.1.0.0.0',   'ZUTN.1.0.0.0', 'NETN.1.0.0.0', 'NETD.1.0.0.0', 'OIGT.1.1.0.0', 'OVGD.1.1.0.0',
    'OVGD.6.1.0.0', 'NLHA.1.0.0.0', 'OVGDT.1.0.0.0', 'PLCD.3.1.0.0', 'OKND.1.0.0.0', 'HWCDW.1.0.0.0',
    'UIGT.1.0.0.0', 'UVGD.1.0.0.0', 'UWCD.1.0.0.0', 'ZVGDFA3.3.0.0.0']

  **Outputs**:
    The outputs in this case are the same as the inputs, we are extending these series with AMECO data

2. Check where the input data come from and prepare the necessary input dataframes.