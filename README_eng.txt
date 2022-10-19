DATA DESCRIPTION

Buoy data is prepared within the framework of the program International Arctic Buoy Programme (IABP): https://iabp.apl.uw.edu/index.html. 
Database includes data, received by several research institutions and national centers.  
Daily buoy data on Arctic and Antarctic (in full resolution) is available by the following link: https://iabp.apl.uw.edu/Data_Products/Daily_Full_Res_Data/

Attribute description:
     BuoyID Ц buoy identificator
     Year Ц year
     Hour Ц hour
     Min Ц minute
     DOY Ц the day of the year to the decimal minute (1.0 to 365.999) of the reported data
     POS_DOY Ц the day of the year to the decimal minute of the reported positio Lat Ц широта (дес€тичные градусы)
     Lat Ц latitude (decimal degrees)
     Lon Ц longitude (decimal degrees)
     BP Ц Barometric Pressure, if available (otherwise, the value is set to -999)
     Ts Ц Surface Temperature if available (otherwise, the value is set to -999)
     Ta Ц Air Temperature if available (otherwise, the value is set to -999)

Note that "Surface Temperature (Ts)" is measured from the bottom of the buoy hull. 
If the buoy is floating, then the reported temperature is of the sea surface. 
If the buoy is frozen into the ice, or sitting on top of it, then the reported temperature is of the ground or ice. 
The freezing temperature of sea water is about -1.8C, so temperature readings below this indicate ground or ice temperatures.
