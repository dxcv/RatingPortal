This project is to build a system handling the credit risk analysis of fixed income products.

Designed workflow is based on excel spreadsheet to rate product by consuming its financial report.

Data source is from Wind online API data or the database deployed in intranet.

Project starts from Aug 1, 2017.

---------------------------------------------------------------
- GeneralBond£º A base class
1. get_raw_data:
   get data from database
   read an excel with rawdata attributes(DBTableName, DBFieldName, OutputName) and then get data from databases, self.rawdata is a DataFrame

2. pretreat_data£º
   pretreat raw data
   pretreatdata in order to calc indicators, such as fill nan with 0, drop a colume without valid values etc, self.pretreat_data is a DataFrame

3. calc_indicators£º
   calculate indicators
   self.indicators is a DataFrame

4. indicators2score£º
   convert indicators to standard score
   read an excel with indicators_to_score criterion, and then convert indicators to score according to threshold.
   self.score is a DataFrame

5. weight_score_and_rating£º
   get a total score and do rating
   read an excel with weight of each indicators, and then calculate total score, and then convert total score to rating result.
   self.rate is a DataFrame

6. score2rating
   convert score to rating
   read an excel with total score and corresponding rating, and then convert total score to rating result.

7. external_rating
   get outside rating result from database


---------------------------------------------------------------
- Bond1 etc: A specific bond class needed to do rating, Subclass of GeneralBond
realize or refine methods in GeneralBond
