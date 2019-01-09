.. _tutorial2:

Tutorial 2: External Sector
=============================================

In this tutorial we will add the calculations for the external sector.
Please check out `Tutorial 1<tutorial1>`, we will follow the same steps:

1. Read the source algorithm and determine what input variables we need and what output variables we need to calculate.
2. Check where the input data comes from (source data from the country, source databases -ameco_h, output_gap, etc.- or data calculated in previous steps or in this one) and
   Prepare the necessary input dataframes. In order to easily identify what variables we get in each step, we export .txt and .xls files with the results at the end.
3. Create the class to perform the calculations, and call it from tests/test_country_calculation.py


**1. Determine inputs and outputs**

  This is our source algorithm (we have removed the unnecessary lines, which are about metadata, not calculations):

    ``External Sector``

	``{Country}|UBYA.1.0.0.0[t] = buttsplice(AMECO Historical!{Country}|UBYA.1.0.0.0[t] sum({Country}|UBRA.1.0.0.0[t] {Country}|UBTA.1.0.0.0[t]) MsSpliceDirection.Forward)``

	``{Country}|UBCA.1.0.0.0[t] = buttsplice(AMECO Historical!{Country}|UBCA.1.0.0.0[t] sum({Country}|UXGS[t] -{Country}|UMGS[t] {Country}|UBYA.1.0.0.0[t]) MsSpliceDirection.Forward)``

	``{Country}|UBLA.1.0.0.0[t] = buttsplice(AMECO Historical!{Country}|UBLA.1.0.0.0[t] sum({Country}|UBCA.1.0.0.0[t] {Country}|UBKA.1.0.0.0[t]) MsSpliceDirection.Forward)``

	``{Country}|DXGT.1.0.0.0[t] = sum({Country}|DXGE.1.0.0.0[t] {Country}|DXGI.1.0.0.0[t])``

	``{Country}|DMGT.1.0.0.0[t] = sum({Country}|DMGE.1.0.0.0[t] {Country}|DMGI.1.0.0.0[t])``

	``{Country}|DBGT.1.0.0.0[t] = {Country}|DXGT.1.0.0.0[t] - {Country}|DMGT.1.0.0.0[t]``

	``{Country}|DBGE.1.0.0.0[t] = {Country}|DXGE.1.0.0.0[t] - {Country}|DMGE.1.0.0.0[t]``

	``{Country}|DBGI.1.0.0.0[t] = {Country}|DXGI.1.0.0.0[t] - {Country}|DMGI.1.0.0.0[t]``

    **Inputs**:
        UYOH.1.0.0.0, UOGH.1.0.0.0, UYNH.1.0.0.0, UVGH.1.0.0.0, UWCH.1.0.0.0, UCTRH.1.0.0.0, UTYH.1.0.0.0, UCTPH.1.0.0.0, UVGHA.1.0.0.0, UEHH.1.0.0.0, PCPH.3.1.0.0, USGH.1.0.0.0, ASGH.1.0.0.0, UBLH.1.0.0.0, UITH.1.0.0.0, UKOH.1.0.0.0

    **Outputs**:
        UYOH.1.0.0.0, UVGH.1.0.0.0, UVGHA.1.0.0.0, OVGHA.3.0.0.0, USGH.1.0.0.0, ASGH.1.0.0.0, UBLH.1.0.0.0

2. Check where the input data come from and prepare the necessary input dataframes.
    We need to find out where the input data comes from. Possible sourcesa`