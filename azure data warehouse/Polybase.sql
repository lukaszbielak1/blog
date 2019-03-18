CREATE SCHEMA EXT;
GO;
	CREATE EXTERNAL DATA SOURCE Rejestr
	WITH
	(
	TYPE = HADOOP,  
       LOCATION = 		'wasbs://[kontener]@[kontomagazynu].blob.core.windows.net/'
	);
GO;
CREATE EXTERNAL FILE FORMAT csv

	WITH 
	(   
    FORMAT_TYPE = DELIMITEDTEXT,
    FORMAT_OPTIONS
    (   
         FIELD_TERMINATOR = ';',
         FIRST_ROW = 2,
		 Encoding = 'UTF8'
    )
);	
GO;

CREATE EXTERNAL TABLE [EXT].[RejestrUmow]
(
[Lp] [int] NOT NULL,
[NumerUmowy] [nvarchar](50) NOT NULL,
[NazwaKontrahenta] [nvarchar](100) NOT NULL,
[DataZawarcia] [datetime2](7) NOT NULL,
[DataZakonczenia] [datetime2](7) NOT NULL,
[Opis] [nvarchar](200) NOT NULL,
[KwotaUmowy] [float] NOT NULL
) 
WITH (
	LOCATION='/',   
   	DATA_SOURCE = Rejestr,  
   	FILE_FORMAT = CSV
	);  

GO;
CREATE TABLE [dbo].[RejestrUmow]
WITH
( 
    DISTRIBUTION = Round_Robin,
    CLUSTERED COLUMNSTORE INDEX
)
AS
SELECT * FROM [ext].[RejestrUmow]

GO;

