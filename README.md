# CSV to NEXUS for SplitsTree

I made this a while ago during my SEA-PHAGES research semester because I needed a way to compare phages by their phams in SplitsTree. I'm sharing it in case anyone else runs into the same problem.

The script takes a CSV with `PhageID` and `PhamID` columns and makes a `.nex` file. Each pham is marked `1` if a phage has it or `0` if it doesn't. If a phage has the same pham more than once, it still counts as just one.

You only need Python 3. From this folder, run:

```sh
python3 csv_to_nex.py example/AU2_phams.csv output.nex
```

Then open `output.nex` in SplitsTree. 

Change the two filenames to use your own CSV and choose where the NEXUS file goes.

The `example` folder has my AU2 phage CSV and the NEXUS file made from it. Tipton is one of the eight phages in that example. The CSV needs rows like this:

```csv
PhageID,PhamID
Tipton,183
Tokki,183
```

The results will depend on the pham data you put in, so double check that your CSV has all the phages and phams you intended to include.