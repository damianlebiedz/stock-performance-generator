> [!CAUTION]
> Follow this information to run the program! Prepare your data to avoid generator failure.

About `.csv` files:

- They should be formatted like the files in the `/template` folder to run the generator.
- You can use `template/(TEMPLATE).xlsx` file: paste the data into the appropriate table and export each spreadsheet to a `.csv` file - then move them to the `/data` folder.
- To run this program, you must have `CLOSED POSITIONS.csv` and `OPEN POSITIONS.csv` files in `/data` folder.
- The `Purchase value`/`Sale value` should be in the currency of the account.
- Works only on stocks listed in Yahoo Finance, CFD positions must be removed from history to avoid generator failure.
