# Mathematical Expressions in Software Engineering Artifacts
### MathyB dataset
<ul>
<li>To run MEDSEA: A Mathematical Expression Detector Tool for Software Engineering Artifacts, download the dataset from https://zenodo.org/record/5229831#.YSFg644zZPY. </li>
<li>Change the <b>INPUT_PATH</b> in MEFinder.py to the location of the project in your local system and <b>OUTPUT_PATH</b> to the location in your local system where you want to save the output. </li>
 <li><b>remove_status</b> in MEFinder.py manages whether MEDSEA should ignore URLs and collection of black listed words while scanning through the bug reports. Default value of <b>remove_status</b> is True. You can change its value between True and False according to your wish.</li>
 <li> Each column in <b>ME_RULES.csv</b> corresponds to the collection of operators or mathemtical fucntions corresponding to that rule. Columns corresponding to rules 1 to 12 are named so in the file. The last column is the collection of black listed words. If you want to add/remove regex based rules then change them accordingly in the ME_RULES.csv file. Make sure ME_remove_words is the last column in the file. </li>
<li>Then run this command:</li>
</ul>

```python
$ python MEFinder.py -input_path [path of the input project file which should be a .xlsx file] -output_path [path of the output file which should be a .csv file] - preprocessing [True or False]
```
The default settings are:
```python
$ python MEFinder.py -input_path Bug_data_linux.xlsx -output_path LINUX.csv - preprocessing True
```
<ul>
<li> You can test our tool on custom input at the web version of our tool available at the <a href="https://share.streamlit.io/mathyb/mathyb_dataset/main/website/MedSea.py">project site</a></li></ul>

### NNGen
To evaluate NNGen with the modified data (Mathematical Expression removed code differences), download the dataset <b>NNGen_modified_data</b> from https://zenodo.org/record/5229831#.YSFg644zZPY and follow the instructions at https://github.com/Tbabm/nngen to execute the NNGen task.
