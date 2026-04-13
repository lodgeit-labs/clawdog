# ATO GST Registration: Logical English Schema

This document defines the Logical English (LE) templates, ontology, and rules governing Australian GST Registration. This schema acts as the syntactic bridge between our SBRM Neurosemantic Graph and the underlying Prolog engine.

## 1. Templates
* *an entity* does not operate for profit.
* *an entity* must register for GST. 
* *an entity* has *a turnover*. 
* *an entity* projected turnover is *a turnover*. 
* the turnover of *an entity* for the current month is *an amount*.    
* the turnover of *an entity* for the previous 11 months is *an amount*. 
* the turnover of *an entity* for the next 11 months is *an amount*.
* *an amount* is the total business income. 
* *an amount* is the GST included in sales to your customers.
* *an amount* is sales to associates that are not for payment and are not taxable. 
* *an amount* is sales not connected with an enterprise you run. 
* *an amount* is input-taxed sales you make.
* *an amount* is sales not connected with Australia (export sales). 
* *an amount* is sales of goods or services within Australia that are sales to third parties.
* *an amount* is the GST Turnover. 

## 2. Ontology
* sporting club is an entity.
* charity is an entity.
* community group is an entity.
* professional association is an entity.
* Uber driver is a ride-sourcing service.   

**Classification Override:**
* an entity is a not-for-profit if the entity does not operate for profit.

## 3. Knowledge Base Rules
1. **Ride-Sourcing Rule:** an entity must register for GST if the entity is of a service and the service is a ride-sourcing service. 
2. **NFP Rule:** an entity must register for GST if the entity is a not-for-profit AND (the entity has a turnover >= 150000 OR the entity projected turnover >= 150000).
3. **For-Profit Rule:** an entity must register for GST if it is *not* the case that the entity is a not-for-profit AND (the entity has a turnover >= 75000 OR the entity projected turnover >= 75000).
4. **Current Turnover Definition:** an entity has a current turnover if current turnover = monthly amount + past amount (previous 11 months).
5. **Projected Turnover Definition:** an entity projected turnover is a projection if projection = monthly amount + future amount (next 11 months).
6. **Total Business Income (TBI):** TBI = Sales Associates + Disconnected_sales + Input_taxed + Exports + Sales.
7. **GST Turnover Calculation:** GST_Turnover = TBI - GST - Sales_Associates - Disconnected_sales - Input_taxed - Exports.